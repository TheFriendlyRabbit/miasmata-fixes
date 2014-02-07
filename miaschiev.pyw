#!/usr/bin/env python

import sys, os
import threading
import traceback

# # --- PyQt4 ---
# from PyQt4 import QtCore, QtGui, uic
# QtCore.Slot = QtCore.pyqtSlot

# --- PySide ---
import PySide
from PySide import QtCore, QtGui
sys.modules['PyQt4'] = PySide # ImageQt is hardcoded to use PyQt4

import Image, ImageDraw, ImageQt
from miaschiev_ui import Ui_Miaschiev

import miasutil
import data
import markers
import exposure_map

class Miaschiev(QtGui.QWidget):
	def __init__(self, parent=None):
		super(Miaschiev, self).__init__(parent)

		self.ui = Ui_Miaschiev()
		self.ui.setupUi(self) # doesn't work with a dynamically loaded UI

	def process_paths(self):
		try:
			install_path = miasutil.find_miasmata_install()
			self.ui.install_path.setText(install_path)
		except: pass
		try:
			save_path = miasutil.find_miasmata_save()
			self.ui.save_path.setText(save_path)
		except: pass
		try:	self.process_install_path(install_path)
		except: pass
		try:	self.process_save_path(save_path)
		except: pass

	def __del__(self):
		del self.ui

	def progress(self, msg):
		if not hasattr(self, 'busy') or not self.busy:
			QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
		self.busy = True
		self.ui.progress.setText(msg)
		self.ui.progress.repaint()
		self.repaint()

	def done(self, msg='Done'):
		QtGui.QApplication.restoreOverrideCursor()
		self.busy = False
		self.ui.progress.setText(msg)

	def process_install_path(self, path):
		import rs5archive, rs5file, imag, environment
		# def _async():
		main_path = os.path.join(path, 'main.rs5')
		self.progress('Loading main.rs5...')
		try:
			self.rs5main = rs5archive.Rs5ArchiveDecoder(open(main_path, 'rb'))
			self.progress('main.rs5 Loaded')
		except Exception as e:
			traceback.print_exc()
			self.done('%s loading main.rs5: %s' % (e.__class__.__name__, str(e)))
			return

		self.progress('Extracting Map_FilledIn...')
		filledin = rs5file.Rs5ChunkedFileDecoder(self.rs5main['TEX\\Map_FilledIn'].decompress())
		self.progress('Decoding Map_FilledIn...')
		self.filledin = imag.open_rs5file_imag(filledin, (1024, 1024), 'RGB')

		self.progress('Extracting Map_OverlayInfo...')
		overlayinfo = rs5file.Rs5ChunkedFileDecoder(self.rs5main['TEX\\Map_OverlayInfo'].decompress())
		self.progress('Decoding Map_OverlayInfo...')
		self.overlayinfo = imag.open_rs5file_imag(overlayinfo, (1024, 1024), 'RGB')

		self.progress('Extracting markers...')
		self.markers = rs5file.Rs5ChunkedFileDecoder(self.rs5main['markers'].decompress())

		# TODO: Try all rs5 files alphabetically to find the first one
		# that contains a valid environment file
		self.progress('Loading environment.rs5...')
		try:
			self.environment = environment.parse_from_archive(os.path.join(path, 'environment.rs5'))
		except Exception as e:
			traceback.print_exc()
			self.done('%s loading environment.rs5: %s' % (e.__class__.__name__, str(e)))
			return

		self.done()

		# Python's GIL still causes UI thread to starve. Can I use
		# multiprocessing for this?
		# t = threading.Thread(target=_async)
		# t.daemon = True
		# t.run()

	def enable_save_slots(self, slots):
		self.ui.save0.setEnabled('save0' in slots)
		self.ui.save1.setEnabled('save1' in slots)
		self.ui.save2.setEnabled('save2' in slots)

	def process_save_path(self, path):
		self.progress('Loading saves...')
		try:
			self.saves = data.parse_data(open(path, 'rb'))
			self.done('Saves Loaded')
		except Exception as e:
			traceback.print_exc()
			self.done('%s loading saves.dat: %s' % (e.__class__.__name__, str(e)))
			return
		enable_slots = filter(lambda x: self.saves[x]['text_description'] != None,
				['save0', 'save1', 'save2'])
		# self.enable_save_slots(self.saves.children.keys())
		self.enable_save_slots(enable_slots)

	def show_image(self, image):
		self.progress('Rendering...')
		image1 = ImageQt.ImageQt(image)
		# Using an ImageQt crashes python on Windows, make a
		# (non-shallow) copy of the image to turn it into a real
		# QImage so it won't crash:
		image2 = image1.copy()
		pixmap = QtGui.QPixmap.fromImage(image2)
		label = QtGui.QLabel('', self.ui.scrollArea)
		label.setPixmap(pixmap)
		self.ui.scrollArea.setWidget(label)
		self.done()

	def main_rs5_loaded(self):
		return hasattr(self, 'filledin') and hasattr(self, 'overlayinfo')

	def coord(self, (x, y)):
		# Game coords are rotated 90 degrees clockwise and in the range
		# 8192.0 x 8192.0. Rotate coord 90 degrees counter-clockwise
		# (transpose then mirror y), then divide by 8.
		return map(int, (y / 8, (8192 - x) / 8))

	def gen_map(self, save):
		if not self.main_rs5_loaded():
			self.process_install_path(self.ui.install_path.text())
		if not self.main_rs5_loaded():
			self.done('Fill in your Miasmata install location!')
			return

		self.progress('Extracting exposure_map...')
		exp = save['player']['MAP']['exposure_map'].raw
		self.progress('Generating map...')
		(self.map, self.outline_mask, self.filledin_mask, self.overlayinfo_mask, self.exposure_extra) = \
				exposure_map.gen_map(exp, self.filledin, self.overlayinfo)

		self.show_image(self.map)

	def darken_map(self, amount):
		self.progress('Darkening...')
		return Image.eval(self.map, lambda x: x / amount)

	def show_coast(self):
		image = self.darken_map(4)
		exposure_map.overlay_smap(image, self.shoreline, self.outline_mask, self.filledin_mask)
		self.show_image(image)
	@QtCore.Slot()
	def on_show_coast_clicked(self):
		self.show_coast()

	def coast_progress(self):
		import rs5file, smap

		self.progress('Extracting player_map_achievements...') # XXX: Also in environment.rs5
		self.shoreline = rs5file.Rs5ChunkedFileDecoder(self.rs5main['player_map_achievements'].decompress())

		revealed = 0
		filledin_pix = self.filledin_mask.load()

		for (total, (x, y)) in enumerate(smap.smap_iter(self.shoreline, self.map.size[0]), 1):
			if filledin_pix[x, y]:
				revealed += 1

		self.ui.coast.setText('%i%% (%i/%i)' % (revealed * 100 / total, revealed, total))
		self.ui.lbl_coast.setEnabled(True)
		self.ui.show_coast.setEnabled(True)

		self.done()

	def urn_iter(self, save):
		# XXX TODO: Read urns from markers file and match these up -
		# Seems that sometimes camp fires do get counted?
		urns = save['state']['urns']
		for urn in urns.itervalues():
			pos = list(urn['pos'])
			yield (urn['touched'], self.coord(pos[:2]))

	def count_touched_urns(self, save):
		urns_lit = filter(lambda (t, pos): t, self.urn_iter(save))
		self.ui.urns.setText(str(len(urns_lit)))
		self.ui.lbl_urns.setEnabled(True)
		self.ui.show_urns.setEnabled(True)

	def enumerate_head_statues(self):
		head_types = []
		marker_types = self.environment['marker_types']
		for marker_type in marker_types.itervalues():
			if not isinstance(marker_type, data.data_tree):
				continue
			if 'is_head' in marker_type and marker_type['is_head'] == 1:
				name = marker_type.name
				if name.startswith('modelsets\\'):
					name = name[10:]
				head_types.append(name)

		for (idx, name, u1, x, y, z, u2) in markers.parse_markers(self.markers):
			if name in head_types:
				yield self.coord((x, y))

	def count_discovered_heads(self):
		if not hasattr(self, 'environment'):
			self.ui.heads.setText('Environment not loaded')
			return
		if not hasattr(self, 'markers'):
			self.ui.heads.setText('Markers not loaded')
			return

		pix = self.filledin_mask.load()
		found = total = 0
		for (x, y) in self.enumerate_head_statues():
			if pix[x, y]:
				found += 1
			total += 1
		self.ui.heads.setText('%i / %i' % (found, total))

		if total == found:
			self.ui.reset_head.setEnabled(True)
		self.ui.lbl_heads.setEnabled(True)
		self.ui.show_heads.setEnabled(True)

	def show_head_progress(self):
		if not hasattr(self, 'map'):
			self.gen_map(self.save)

		image = self.darken_map(2)
		draw = ImageDraw.Draw(image)

		self.progress('Plotting Head Statues...')
		pix = self.filledin_mask.load()
		for (x, y) in self.enumerate_head_statues():
			c = (255, 0, 0)
			if pix[x, y]:
				c = (0, 255, 0)
			draw.rectangle((x-5, y-5, x+5, y+5), outline=c)
		self.show_image(image)
	@QtCore.Slot()
	def on_show_heads_clicked(self):
		self.show_head_progress()

	def show_urn_progress(self):
		if not hasattr(self, 'map'):
			self.gen_map(self.save)

		image = self.darken_map(2)
		draw = ImageDraw.Draw(image)

		self.progress('Plotting Urns...')
		for (t, (x, y)) in self.urn_iter(self.save):
			c = (255, 0, 0)
			if t:
				c = (0, 255, 0)
			draw.rectangle((x-5, y-5, x+5, y+5), outline=c)
		self.show_image(image)
	@QtCore.Slot()
	def on_show_urns_clicked(self):
		self.show_urn_progress()

	def count_notes(self, save):
		notes = save['player']['journal']['notes']
		if notes == None:
			notes = {}
		removed = save['inst_tree']['removed_types']
		self.ui.notes.setText(str(len(notes)))
		self.ui.lbl_notes.setEnabled(True)
		if 'modelsets\\NoteZZ' in removed and 'NoteZZ' not in notes:
			self.ui.reset_notezz.setEnabled(True)

	def count_plants(self, save):
		plants = save['player']['journal']['plants']
		if plants == None:
			plants = []
		else:
			plants = plants.keys()
		plants = filter(lambda x: x.lower().startswith('plant'), plants)
		self.ui.plants.setText(str(len(plants)))
		self.ui.lbl_plants.setEnabled(True)

	def backup_saves_dat(self, save_path):
		import time
		try:
			timestamp_str = time.strftime('%Y%m%d%H%M%S')
			backup = '%s~%s' % (save_path, timestamp_str)
			os.rename(save_path, backup)
		except Exception as e:
			traceback.print_exc()
			self.done('%s backing up saves.dat: %s' % (e.__class__.__name__, str(e)))
			raise
		return backup

	@QtCore.Slot()
	def on_reset_notezz_clicked(self):
		save_path = self.ui.save_path.text()
		self.progress('Writing %s...' % save_path)

		try:
			backup = self.backup_saves_dat(save_path)
		except:
			return

		self.save['inst_tree']['removed_types'].remove('modelsets\\NoteZZ')

		open(save_path, 'wb').write(data.encode(self.saves))

		self.ui.reset_notezz.setEnabled(False)
		self.process_save_path(save_path)
		self.process_save(self.save.name)
		self.done('Backup written to %s' % backup)

	@QtCore.Slot()
	def on_reset_head_clicked(self):
		# TODO:
		# I may still need to match the head statues up with the
		# landmarks listed in saves.dat to reset one. Needs testing.

		# TODO: Reset ONE statue, not all of them.
		self.progress('Resetting head statues...')
		draw = ImageDraw.Draw(self.filledin_mask)
		for (x, y) in self.enumerate_head_statues():
			draw.rectangle((x-5, y-5, x+5, y+5), fill=0)

		self.progress('Encoding exposure_map...')
		new_exposure_map = data.data_raw(exposure_map.make_exposure_map(
				self.outline_mask, self.filledin_mask,
				self.overlayinfo_mask, self.exposure_extra))

		save_path = self.ui.save_path.text()
		self.progress('Writing %s...' % save_path)

		try:
			backup = self.backup_saves_dat(save_path)
		except:
			return

		self.save['player']['MAP']['exposure_map'] = new_exposure_map

		open(save_path, 'wb').write(data.encode(self.saves))

		self.ui.reset_head.setEnabled(False)
		self.process_save_path(save_path)
		self.process_save(self.save.name)
		self.show_head_progress()
		self.done('Backup written to %s' % backup)

	def clear_progress(self):
		self.ui.lbl_coast.setEnabled(False)
		self.ui.show_coast.setEnabled(False)
		self.ui.coast.setText('')
		self.ui.lbl_urns.setEnabled(False)
		self.ui.show_urns.setEnabled(False)
		self.ui.urns.setText('')
		self.ui.lbl_heads.setEnabled(False)
		self.ui.show_heads.setEnabled(False)
		self.ui.reset_head.setEnabled(False)
		self.ui.heads.setText('')
		self.ui.lbl_notes.setEnabled(False)
		self.ui.reset_notezz.setEnabled(False)
		self.ui.notes.setText('')
		self.ui.lbl_plants.setEnabled(False)
		self.ui.plants.setText('')

	def process_save(self, save):
		# Ensure we are up to date:
		self.clear_progress()
		save_path = self.ui.save_path.text()
		self.process_save_path(save_path)

		try:
			self.save = self.saves[save]
			self.count_touched_urns(self.save)
			self.count_notes(self.save)
			self.count_plants(self.save)

			self.gen_map(self.save)
			self.count_discovered_heads()
			self.coast_progress()
		except Exception as e:
			traceback.print_exc()
			self.done('%s processing %s: %s' % (e.__class__.__name__, save, str(e)))

	@QtCore.Slot()
	def on_save0_clicked(self): self.process_save('save0')
	@QtCore.Slot()
	def on_save1_clicked(self): self.process_save('save1')
	@QtCore.Slot()
	def on_save2_clicked(self): self.process_save('save2')

	@QtCore.Slot()
	def on_install_browse_clicked(self):
		install_path = self.ui.install_path.text()
		dialog = QtGui.QFileDialog(self,
				caption="Select Miasmata Install Location...",
				directory=install_path)
		dialog.setFileMode(QtGui.QFileDialog.Directory)
		if not dialog.exec_():
			return
		install_path = dialog.selectedFiles()[0]
		self.process_install_path(install_path)
		self.ui.install_path.setText(install_path)

	@QtCore.Slot()
	def on_install_path_returnPressed(self):
		install_path = self.ui.install_path.text()
		self.process_install_path(install_path)

	@QtCore.Slot()
	def on_save_browse_clicked(self):
		save_path = self.ui.save_path.text()
		save_path = QtGui.QFileDialog.getOpenFileName(self,
				"Select Miasmata Saved Game...",
				save_path, 'Miasmata save files (*.dat)')[0]
		if not save_path:
			return
		self.ui.save_path.setText(save_path)
		self.process_save_path(save_path)

	@QtCore.Slot()
	def on_save_path_returnPressed(self):
		save_path = self.ui.save_path.text()
		self.process_save_path(save_path)

if __name__ == '__main__':
	import multiprocessing
	multiprocessing.freeze_support()
	if hasattr(multiprocessing, 'set_executable'): # Windows
		script_dir = os.path.dirname(os.path.join(os.curdir, sys.argv[0]))
		interpreter = os.path.join(script_dir, 'py.exe')
		if os.path.isfile(interpreter):

			# HACK TO WORK AROUND CRASH ON CONSOLE OUTPUT WITH BBFREEZE GUI_ONLY
			sys.stdout = sys.stderr = open('miaschiev.log', 'w')

			print 'Setting multiprocessing exe to %s' % interpreter
			multiprocessing.set_executable(interpreter)
		else:
			print 'WARNING: Did not set multiprocessing exe!'
			print 'Running this as a frozen exe may be unbearably slow!'

	app = QtGui.QApplication(sys.argv)
	dialog = Miaschiev()

	dialog.show()
	dialog.process_paths()
	app.exec_()
	# If using PyQt4, this prevents "python.exe has stopped working..." on
	# close (Seems unnecessary with PySide):
	del dialog

# vi:noexpandtab:sw=8:ts=8
