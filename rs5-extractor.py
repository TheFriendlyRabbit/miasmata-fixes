#!/usr/bin/env python

import zlib
import sys
import os
import rs5archive
import rs5file

undo_file = r'MIASMOD\UNDO'
undo_dir_placeholder = r'MIASMOD\ORIGDIR'
mod_manifests = r'MIASMOD\MODS'
mod_order_file = r'MIASMOD\ORDER'

def file_blacklisted(name):
	'''Files not permitted to be manually added to an archive'''
	if name.upper() in (undo_file, undo_dir_placeholder, mod_order_file):
		return True
	if name.upper().startswith('%s\\' % mod_manifests):
		return True
	return False

def list_files(archive, file_list, list_chunks=False, sha=False):
	import hashlib

	rs5 = rs5archive.Rs5ArchiveDecoder(open(archive, 'rb'))
	if not file_list:
		file_list = rs5
	for filename in file_list:
		filename = filename.replace(os.path.sep, '\\')
		try:
			file = rs5[filename]
		except KeyError:
			print '%s not found in %s~' % (filename, archive)
			continue
		if sha:
			print '%s -' % hashlib.sha1(file.read()).hexdigest(),
		print '%4s %8i %s' % (file.type, file.uncompressed_size, file.filename)
		if list_chunks and file.type not in ('PROF', 'INOD', 'FOGN'):
			try:
				chunks = rs5file.rs5_file_decoder_factory(file.decompress())
			except zlib.error as e:
				print '%4s %8s zlib: %s' % ('', '', str(e))
			else:
				if not hasattr(chunks, 'itervalues'):
					continue
				for chunk in chunks.itervalues():
					print '%4s %8s - %4s %8i' % ('', '', chunk.name, chunk.size)
			print

def extract(archive, dest, file_list, strip, chunks, overwrite, filter):
	rs5 = rs5archive.Rs5ArchiveDecoder(open(archive, 'rb'))
	print 'Extracting files to %s' % dest
	if not file_list:
		file_list = rs5
	for filename in file_list:
		filename = filename.replace(os.path.sep, '\\')
		if filename not in rs5:
			print '%s not found in %s!' % (filename, archive)
			continue
		type = rs5[filename].type
		if filter and type not in filter:
			continue
		try:
			print 'Extracting %s %s...' % (repr(type), filename)
			if chunks:
			    rs5[filename].extract_chunks(dest, overwrite)
			else:
			    rs5[filename].extract(dest, strip, overwrite)
		except OSError as e:
			print>>sys.stderr, 'ERROR EXTRACTING %s: %s, SKIPPING!' % (file.filename, str(e))

def is_chunk_dir(path):
	return os.path.isfile(os.path.join(path, '00-HEADER'))

def add_files(rs5, file_list):
	for filename in file_list:
		if os.path.isdir(filename):
			if is_chunk_dir(filename):
				rs5.add_chunk_dir(filename)
				continue
			for (root, dirs, files) in os.walk(filename):
				for dir in dirs[:]:
					path = os.path.join(root, dir)
					if is_chunk_dir(path):
						rs5.add_chunk_dir(path)
						dirs.remove(dir)
				for file in files:
					path = os.path.join(root, file)
					if file_blacklisted(os.path.relpath(path, filename).replace(os.path.sep, '\\')):
						print 'Skipping %s' % path
						continue
					rs5.add(path)
		else:
			rs5.add(filename)

def create_rs5(archive, file_list, overwrite):
	if not file_list:
		print 'Must specify at least one file!'
		return
	if os.path.exists(archive) and not overwrite:
		print '%s already exists, refusing to continue!' % archive
		return
	rs5 = rs5archive.Rs5ArchiveEncoder(archive)
	add_files(rs5, file_list)
	rs5.save()

def add_rs5_files(archive, file_list):
	rs5 = rs5archive.Rs5ArchiveUpdater(open(archive, 'rb+'))
	add_files(rs5, file_list)
	rs5.save()

def repack_rs5(old_archive, new_archive):
	old_rs5 = rs5archive.Rs5ArchiveDecoder(open(old_archive, 'rb'))
	new_rs5 = rs5archive.Rs5ArchiveEncoder(new_archive)
	for old_file in old_rs5.itervalues():
		if file_blacklisted(old_file.filename):
			print 'Discarding %s' % old_file.filename
			continue
		print 'Repacking %s...' % old_file.filename
		new_entry = rs5archive.Rs5CompressedFileRepacker(new_rs5.fp, old_file)
		new_rs5[new_entry.filename] = new_entry
	new_rs5.save()

def validate_undo(rs5):
	print 'STUB: validate_undo()'
	# TODO: Make sure the values in the undo file look sane - that there is
	# a central directory archive where it points and that there is no file
	# listed in that directory past the truncation point.
	return True

class UndoMeta(dict):
	import json

	def revert_rs5(self, rs5):
		# TODO: Validate undo
		rs5.d_off = self['directory_offset']
		rs5.ent_len = self['entry_size']
		rs5.write_header()
		rs5.fp.flush()
		rs5.fp.truncate(self['filesize'])

	class Placeholder(rs5archive.Rs5CompressedFile):
		def __init__(self, undo_file):
			self.undo_file = undo_file

		@property
		def data_off(self):
			return self.undo_file['directory_offset']
		@property
		def compressed_size(self):
			return self.undo_file['directory_size']
		@property
		def uncompressed_size(self):
			return self.undo_file['directory_size']
		@property
		def modtime(self):
			import time
			return time.time()
		@property
		def filename(self):
			return undo_dir_placeholder
		type = 'META'
		u1 = 0x30080000000
		u2 = 1
	@property
	def placeholder(self):
		return self.Placeholder(self)

class UndoMetaEncoder(UndoMeta, rs5file.Rs5FileEncoder):
	def __init__(self, rs5):
		self['filesize'] = os.fstat(rs5.fp.fileno()).st_size
		self['directory_offset'] = rs5.d_off
		self['entry_size'] = rs5.ent_len
		self['directory_size'] = rs5.d_orig_len
		rs5file.Rs5FileEncoder.__init__(self, 'META', undo_file, self.json.dumps(self), 0)

class UndoMetaDecoder(UndoMeta, rs5file.Rs5FileDecoder):
	def __init__(self, rs5):
		rs5file.Rs5FileDecoder.__init__(self, rs5[undo_file].decompress())
		self.update(self.json.loads(self.data))

def do_add_undo(rs5, overwrite=False):
	if undo_file in rs5 and not overwrite:
		print 'Previously added undo metadata found'
		if validate_undo(rs5):
			return 1
		print 'Undo metadata appears to be invalid, updating'
	undo = UndoMetaEncoder(rs5)
	try:
		rs5.add_from_buf(undo.encode())
		rs5[undo_dir_placeholder] = undo.placeholder
		rs5.save()
	except Exception as e:
		print>>sys.stderr, 'ERROR: %s occured while adding undo metadata: %s' % (e.__class__.__name__, str(e))
		print>>sys.stderr, 'REVERTING CHANGES...'
		undo.revert_rs5(rs5)
		print>>sys.stderr, '\nFILE RESTORED'
		raise

def add_undo(archive, overwrite):
	rs5 = rs5archive.Rs5ArchiveUpdater(open(archive, 'rb+'))
	try:
		return do_add_undo(rs5, overwrite)
	except Exception as e:
		return 1

def revert(archive):
	rs5 = rs5archive.Rs5ArchiveUpdater(open(archive, 'rb+'))
	if undo_file not in rs5:
		print '%s does not contain undo metadata!' % archive
		return 1
	if not validate_undo(rs5):
		print 'Undo metadata appears to be invalid, aborting!'
		return 1
	undo = UndoMetaDecoder(rs5)
	undo.revert_rs5(rs5)

class ModCentralDirectoryEncoder(rs5archive.Rs5CentralDirectoryEncoder, rs5file.Rs5FileEncoder):
	def __init__(self, name, ent_len):
		self.ent_len = ent_len
		self.flags = 0
		rs5archive.Rs5CentralDirectoryEncoder.__init__(self)
		self.filename = '%s\%s.manifest' % (mod_manifests, name)

	def encode(self):
		from StringIO import StringIO
		self.fp = StringIO()
		self.write_directory()
		rs5file.Rs5FileEncoder.__init__(self, 'META', self.filename, self.fp.getvalue(), 0)
		return rs5file.Rs5FileEncoder.encode(self)

class UndoMetaCentralDirectory(rs5archive.Rs5CentralDirectoryDecoder):
	def __init__(self, rs5):
		undo = UndoMetaDecoder(rs5)
		self.fp = rs5.fp
		self.d_off = undo['directory_offset']
		self.ent_len = undo['entry_size']
		rs5archive.Rs5CentralDirectoryDecoder.__init__(self)

class ModCentralDirectoryDecoder(rs5archive.Rs5CentralDirectoryDecoder):
	def __init__(self, rs5, manifest):
		from StringIO import StringIO
		decoder = rs5file.Rs5FileDecoder(manifest.decompress())
		self.fp = StringIO(decoder.data)
		self.d_off = 0
		self.ent_len = rs5.ent_len
		rs5archive.Rs5CentralDirectoryDecoder.__init__(self)

class ModOrder(list):
	import json

class ModOrderEncoder(ModOrder, rs5file.Rs5FileEncoder):
	def __init__(self, rs5, order):
		list.__init__(self, order)
		rs5file.Rs5FileEncoder.__init__(self, 'META', mod_order_file, self.json.dumps(self), 0)

class ModOrderDecoder(ModOrder, rs5file.Rs5FileDecoder):
	def __init__(self, rs5):
		rs5file.Rs5FileDecoder.__init__(self, rs5[mod_order_file].decompress())
		list.__init__(self, self.json.loads(self.data))

def rs5_mods(rs5):
	mods = filter(lambda x: x.startswith('%s\\' % mod_manifests), rs5)
	if mod_order_file in rs5:
		order = ModOrderDecoder(rs5)
		for mod in order:
			manifest = '%s\\%s.manifest' % (mod_manifests, mod)
			if manifest in rs5:
				# print 'Processing %s (ordered)' % mod
				yield mods.pop(mods.index(manifest))
			else:
				print 'WARNING: %s listed in %s not found in archive!' % (mod, mod_order_file)
	for mod in mods:
		# print 'Processing %s (UNORDERED)' % mod
		yield mod

# Too slow when dealing with a large number of files, could still be useful for
# another list command though...
# def iter_all_file_versions(rs5):
# 	'''
# 	Iterates over every file in the archive, including multiple versions of
# 	the same file where a mod has overridden them.
# 	'''
# 	done = set()
# 	def process(file):
# 		done.add((file.filename, file.data_off))
# 		return file
#
# 	yield process(rs5[undo_file])
# 	for file in UndoMetaCentralDirectory(rs5).itervalues():
# 		yield process(file)
# 	for mod in rs5_mods(rs5):
# 		yield process(rs5[mod])
# 		for file in ModCentralDirectoryDecoder(rs5, rs5[mod]).itervalues():
# 			yield process(file)
#
# 	for (filename, off) in set([(x.filename, x.data_off) for x in rs5.values()]).difference(done):
# 		yield rs5[filename]

def iter_mod_file_versions(rs5, undo_pos):
	'''
	Iterates over every file in the archive that has been added via a mod
	or manually since undo information was added, including multiple
	versions of the same file where multiple mods have touched the same file.
	'''
	done = set()
	def process(file):
		assert(file.data_off >= undo_pos)
		done.add((file.filename, file.data_off))
		return file

	for mod in rs5_mods(rs5):
		yield process(rs5[mod])
		for file in ModCentralDirectoryDecoder(rs5, rs5[mod]).itervalues():
			yield process(file)

	remaining = set([(x.filename, x.data_off) for x in rs5.values()]).difference(done)
	remaining = filter(lambda (filename, off): off >= undo_pos, remaining)
	for (filename, off) in remaining:
		yield rs5[filename]

# Too slow when dealing with a large number of files
# def iter_all_used_sections(rs5):
# 	yield (0, 24, '__header__') # Header
# 	yield (rs5.d_off, rs5.d_off + rs5.d_orig_len, '__directory__') # Central Directory
# 	for file in iter_all_file_versions(rs5):
# 		yield (file.data_off, file.data_off + file.compressed_size, file.filename)

def iter_used_sections(rs5):
	undo = rs5[undo_file]
	undo_pos = undo.data_off + undo.compressed_size

	yield (0, undo_pos, '__original__')
	if rs5.d_off >= undo_pos:
		yield (rs5.d_off, rs5.d_off + rs5.d_orig_len, '__directory__') # Central Directory
	for file in iter_mod_file_versions(rs5, undo_pos):
		yield (file.data_off, file.data_off + file.compressed_size, file.filename)

def find_eof(rs5):
	'''
	Finds the end of the rs5 archive, ensuring that it is past the undo
	metadata, central directory and any installed mods. The archive should
	be safe to truncate at this point.
	'''
	return max([x[1] for x in iter_used_sections(rs5)])

# A bit slow for what I wanted, but may still be useful for printing out the
# used regions
# def find_hole(rs5, size):
# 	'''
# 	Finds a hole in the rs5 archive large enough to fit some data.
# 	Guaranteed not to return a position before the end of the undo
# 	metadata.
# 	'''
# 	undo = rs5[undo_file]
# 	undo_pos = undo.data_off + undo.compressed_size
# 	regions = sorted(iter_all_used_sections(rs5))
# 	for (i, (start, fin, name)) in enumerate(regions):
# 		space = 0
# 		if i:
# 			space = start - regions[i-1][1]
# 		print '%.8x:%.8x %+8i %s' % (start, fin, space, name)
# 		if fin < undo_pos:
# 			continue
# 		if i == len(regions) - 1 or regions[i+1][0] - fin >= size:
# 			return fin
# 	raise Exception()

def find_largest_hole(rs5):
	undo = rs5[undo_file]
	undo_pos = undo.data_off + undo.compressed_size
	regions = sorted(iter_used_sections(rs5))
	hole = (0, None)
	for (i, (start, fin, name)) in enumerate(regions[:-1]):
		assert (fin >= undo_pos)
		space = regions[i+1][0] - fin
		if space > hole[0]:
			hole = (space, fin)
	return hole

class Rs5ModArchiveUpdater(rs5archive.Rs5ArchiveUpdater):
	def __init__(self, fp):
		rs5archive.Rs5ArchiveUpdater.__init__(self, fp)
		self.clear_largest_hole()

	def clear_largest_hole(self):
		self.largest_hole_size = self.largest_hole_pos = None

	def update_largest_hole(self):
		print 'Searching for holes...'
		self.largest_hole_size, self.largest_hole_pos = find_largest_hole(self)
		if self.largest_hole_pos is not None:
			print 'Largest hole is %i bytes at 0x%x' % (self.largest_hole_size, self.largest_hole_pos)
		else:
			print 'No holes found'

	def seek_find_hole(self, size):
		if undo_file not in self:
			return self.seek_eof()
		if self.largest_hole_size is None:
			self.update_largest_hole()
		if self.largest_hole_size < size:
			return self.seek_eof()
		self.fp.seek(self.largest_hole_pos)
		self.clear_largest_hole()

def apply_mod_order(rs5):
	'''
	Rebuild the central directory from the original and any contained mod
	manifests to ensure that files touched by multiple mods use the correct
	one.
	'''
	directory = UndoMetaCentralDirectory(rs5)
	for mod in rs5_mods(rs5):
		directory.update(ModCentralDirectoryDecoder(rs5, rs5[mod]))

	rs5.update(directory)

def order_mods(archive, mod_list):
	rs5 = Rs5ModArchiveUpdater(open(archive, 'rb+'))
	do_add_undo(rs5)
	file = ModOrderEncoder(rs5, mod_list)
	rs5.add_from_buf(file.encode())
	apply_mod_order(rs5)
	rs5.save()
	rs5.fp.truncate(find_eof(rs5))

class ModNotFound(Exception): pass

def do_rm_mod(rs5, mod):
	manifest_name = '%s\\%s.manifest' % (mod_manifests, mod)
	try:
		manifest = rs5[manifest_name]
	except:
		print 'ERROR: %s not found in archive!' % manifest_name
		raise ModNotFound()
	for (filename, mod_f) in ModCentralDirectoryDecoder(rs5, manifest).iteritems():
		cur_f = rs5[filename]
		if cur_f.data_off == mod_f.data_off:
			print 'Removing %s...' % filename
			del rs5[filename]
		else:
			print 'Skipping %s - offsets do not match' % filename
	print 'Removing %s...' % manifest_name
	del rs5[manifest_name]
	print 'Rebuilding directory from mod order...'
	apply_mod_order(rs5)
	rs5.save()
	rs5.fp.truncate(find_eof(rs5))

def rm_mod(archive, mods):
	rs5 = Rs5ModArchiveUpdater(open(archive, 'rb+'))
	do_add_undo(rs5)
	for mod in mods:
		try:
			do_rm_mod(rs5, mod)
		except ModNotFound:
			return 1

def add_mod(dest_archive, source_archives):
	rs5 = Rs5ModArchiveUpdater(open(dest_archive, 'rb+'))
	do_add_undo(rs5)
	for source_archive in source_archives:
		source_rs5 = rs5archive.Rs5ArchiveDecoder(open(source_archive, 'rb'))
		mod_name = os.path.splitext(os.path.basename(source_archive))[0]
		mod_entries = ModCentralDirectoryEncoder(mod_name, rs5.ent_len)
		for source_file in source_rs5.itervalues():
			if file_blacklisted(source_file.filename):
				print 'Skipping %s' % source_file.filename
				continue
			print 'Adding %s->%s...' % (source_archive, source_file.filename)
			entry = rs5archive.Rs5CompressedFileRepacker(rs5.fp, source_file, seek_cb=rs5.seek_find_hole)
			rs5[entry.filename] = entry
			mod_entries[entry.filename] = entry
		rs5.add_from_buf(mod_entries.encode())
	apply_mod_order(rs5)
	rs5.save()
	rs5.fp.truncate(find_eof(rs5))

def analyse(filename):
	rs5 = rs5archive.Rs5ArchiveDecoder(open(filename, 'rb'))
	interesting = ('cterr_texturelist',)
	for file in rs5.itervalues():
		if not file.filename:
			# XXX: What are these?
			# print 'SKIPPING FILE OF TYPE %s WITHOUT FILENAME' % repr(file.type)
			continue
		try:
			d = file.decompress()
			size = len(d)
		except zlib.error as e:
			# XXX: What are these?
			print 'ERROR EXTRACTING %s: %s' % (file.filename, str(e))
			print '%s %x %8i %x    |   %-25s  |  compressed_size: %i' \
				% (file.type, file.u1, file.uncompressed_size, file.u2, file.filename, file.compressed_size)
			if file.filename in interesting:
				continue
			raise
			# continue
		contents = rs5file.rs5_file_decoder_factory(d)
		# if file.filename in interesting:
		if True:
			print '0x%.8x - 0x%.8x  |  %s %x %8i %x %x  |   %-25s  |  compressed_size: %i\t|  size: %8i' \
				% (file.data_off, file.data_off + file.compressed_size-1, file.type, file.u1, file.uncompressed_size, file.u2, contents.u2, file.filename, file.compressed_size, contents.filesize+contents.data_off)

		assert(file.u2 == 1)
		assert(file.uncompressed_size == size)
		assert(file.type == contents.magic)
		assert(file.filename == contents.filename)

		# ALIGNMENT CONSTRAINT FOUND - FILE IS PADDED TO 8 BYTES BEFORE COMPRESSION
		assert(file.uncompressed_size % 8 == 0)

		# PADDING CONSTRAINT - FILE HEADER IS PADDED TO A MULTIPLE OF 8 BYTES
		assert(contents.data_off % 8 == 0)

		# NO PADDING CONSTRAINTS FOUND ON CONTAINED FILES IN THE GENERAL CASE
		# assert(contents.filesize % 2 == 0)
		# assert(contents.filesize % 4 == 0)
		# assert(contents.filesize % 8 == 0)
		#assert((contents.data_off + contents.filesize) % 2 == 0)
		#assert((contents.data_off + contents.filesize) % 4 == 0)
		#assert((contents.data_off + contents.filesize) % 8 == 0)
		#assert((contents.data_off + contents.filesize) % 16 == 0)

def parse_args():
	import argparse
	parser = argparse.ArgumentParser()

	group = parser.add_mutually_exclusive_group(required=True)
	parser.add_argument('files', nargs='*', metavar='FILE')
	group.add_argument('-l', '--list', action='store_true',
			help='List all files in the rs5 archive')
	group.add_argument('-L', '--list-chunks', action='store_true',
			help='List all files and contained chunks in the rs5 archive')
	group.add_argument('--sha1', action='store_true',
			help='Calculate the sha1sum of the zlib compressed version of all files within the archive')
	group.add_argument('-x', '--extract', action='store_true',
			help='Extract files from the archive')
	group.add_argument('-c', '--create', action='store_true',
			help='Create a new RS5 file')
	group.add_argument('-a', '--add', action='store_true',
			help='Add/update FILEs in ARCHIVE')
	group.add_argument('--add-mod', action='store_true',
			help='Merge mods specified by FILEs into ARCHIVE with undo metadata')
	group.add_argument('--rm-mod', '--remove-mod', action='store_true',
			help='Remove a mod previously added with --add-mod')
	group.add_argument('--order', '--mod-order', '--set-mod-order', action='store_true',
			help='Change the order of mods added with --add-mod within the archive')
	group.add_argument('--repack', metavar='NEW_ARCHIVE', # TODO: Discard UNDO metadata
			help='Decode ARCHIVE and pack into NEW_ARCHIVE, for testing')

	group.add_argument('--add-undo', action='store_true',
			help='Add undo metadata to an rs5 archive (WARNING: Not all actions can be undone)')
	group.add_argument('--revert', action='store_true',
			help='Use undo metadata in an rs5 archive to restore it to a previous state')

	parser.add_argument('-f', '--file', metavar='ARCHIVE', required=True,
			help='Specify the rs5 ARCHIVE to work on')
	parser.add_argument('-C', '--directory', metavar='DIR',
			help='Change to directory DIR before extacting')

	group1 = parser.add_mutually_exclusive_group()
	group1.add_argument('--strip', action='store_true',
			help='Strip the local file headers during extraction')
	group1.add_argument('--chunks', action='store_true',
			help='Split files up into their component chunks while extracting')
	parser.add_argument('--filter', action='append',
			help='Only extract files of this type')

	parser.add_argument('--overwrite', action='store_true',
			help='Overwrite files without asking')

	group.add_argument('--analyse', action='store_true')

	return parser.parse_args()

def main():
	args = parse_args()

	if args.list:
		return list_files(args.file, args.files)

	if args.list_chunks:
		return list_files(args.file, args.files, list_chunks=True)

	if args.sha1:
		return list_files(args.file, args.files, sha=True)

	if args.extract:
		directory = args.directory
		if directory is None:
			directory = os.path.splitext(os.path.basename(args.file))[0]
			if directory == args.file:
				print 'Unable to determine target directory'
				return
		return extract(args.file, directory, args.files, args.strip, args.chunks, args.overwrite, args.filter)

	if args.create:
		return create_rs5(args.file, args.files, args.overwrite)

	if args.add:
		return add_rs5_files(args.file, args.files)

	if args.repack is not None:
		return repack_rs5(args.file, args.repack)

	if args.analyse:
		return analyse(args.file)

	if args.add_undo:
		return add_undo(args.file, args.overwrite)

	if args.revert:
		return revert(args.file)

	if args.add_mod:
		return add_mod(args.file, args.files)

	if args.rm_mod:
		return rm_mod(args.file, args.files)

	if args.order:
		return order_mods(args.file, args.files)

if __name__ == '__main__':
	sys.exit(main())

# vi:noexpandtab:sw=8:ts=8
