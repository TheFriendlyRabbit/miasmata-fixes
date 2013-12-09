#!/usr/bin/env python

# Based loosely on git://github.com/klightspeed/RS5-Extractor

# I wanted something a bit lower level that didn't convert the contained files
# so I could examine the format for myself. Don't expect this to be feature
# complete for a while

import struct
import zlib
import sys
import os
import collections
import rs5file

# http://msdn.microsoft.com/en-us/library/system.datetime.fromfiletimeutc.aspx:
# A Windows file time is a 64-bit value that represents the number of
# 100-nanosecond intervals that have elapsed since 12:00 midnight,
# January 1, 1601 A.D. (C.E.) Coordinated Universal Time (UTC).
import calendar
win_epoch = calendar.timegm((1601, 1, 1, 0, 0, 0))
def from_win_time(win_time):
	return win_time / 10000000 + win_epoch
def to_win_time(unix_time):
	return (unix_time - win_epoch) * 10000000

def mkdir_recursive(path):
	if path == '':
		return
	(head, tail) = os.path.split(path)
	mkdir_recursive(head)
	if not os.path.exists(path):
		os.mkdir(path)
	elif not os.path.isdir(path):
		raise OSError(17, '%s exists but is not a directory' % path)

class NotAFile(Exception): pass

class Rs5CompressedFile(object):
	def gen_dir_ent(self):
		return struct.pack('<QIQ4sQQ',
				self.data_off, self.compressed_size, self.u1,
				self.type, self.uncompressed_size << 1 | self.u2,
				to_win_time(self.modtime)) + self.filename + '\0'

class Rs5CompressedFileDecoder(Rs5CompressedFile):
	def __init__(self, f, data):
		self.fp = f
		(self.data_off, self.compressed_size, self.u1, self.type, self.uncompressed_size,
				modtime) \
			= struct.unpack('<QIQ4sQQ', data[:40])

		self.u2 = self.uncompressed_size & 0x1
		if not self.u2:
			raise NotAFile()
		self.uncompressed_size >>= 1

		filename_len = data[40:].find('\0')
		self.filename = data[40:40 + filename_len]
		self.modtime = from_win_time(modtime)

	def _read(self):
		self.fp.seek(self.data_off)
		return self.fp.read(self.compressed_size)

	def decompress(self):
		return zlib.decompress(self._read())

	def extract(self, base_path, strip, overwrite):
		dest = os.path.join(base_path, self.filename.replace('\\', os.path.sep))
		if os.path.isfile(dest) and not overwrite: # and size != 0
			print>>sys.stderr, 'Skipping %s - file exists.' % dest
			return
		(dir, file) = os.path.split(dest)
		mkdir_recursive(dir)
		f = open(dest, 'wb')
		try:
			data = self.decompress()
			if strip:
				contents = rs5file.Rs5FileDecoder(data)
				assert(contents.magic == self.type)
				assert(contents.filename == self.filename)
				assert(len(contents.data) == filesize)
				f.write(contents.data)
			else:
				f.write(data)
		except zlib.error, e:
			print>>sys.stderr, 'ERROR EXTRACTING %s: %s. Skipping decompression!' % (dest, str(e))
			f.write(self._read())
		f.close()
		os.utime(dest, (self.modtime, self.modtime))

class Rs5CompressedFileEncoder(Rs5CompressedFile):
	def __init__(self, fp, filename):
		self.modtime = os.stat(filename).st_mtime
		uncompressed = open(filename, 'rb').read()
		self.uncompressed_size = len(uncompressed)
		contents = rs5file.Rs5FileDecoder(uncompressed)
		(self.type, self.filename) = (contents.magic, contents.filename)
		compressed = zlib.compress(uncompressed)
		self.compressed_size = len(compressed)
		self.u1 = 0x30080000000
		self.u2 = 1

		self.data_off = fp.tell()
		fp.write(compressed)

class Rs5CompressedFileRepacker(Rs5CompressedFile):
	def __init__(self, newfp, oldfile):
		self.compressed_size = oldfile.compressed_size
		self.u1 = oldfile.u1
		self.type = oldfile.type
		self.uncompressed_size = oldfile.uncompressed_size
		self.u2 = oldfile.u2
		self.modtime = oldfile.modtime
		self.filename = oldfile.filename

		self.data_off = newfp.tell()
		newfp.write(oldfile._read())



class Rs5ArchiveDecoder(collections.OrderedDict):
	def __init__(self, f):
		magic = f.read(8)
		if magic != 'CFILEHDR':
			print 'Invalid file header'
			return 1

		(d_off, ent_len, u1) = struct.unpack('<QII', f.read(16))

		f.seek(d_off)
		data = f.read(ent_len)
		(d_off1, d_len, flags) = struct.unpack('<QII', data[:16])
		assert(d_off == d_off1)

		collections.OrderedDict.__init__(self)

		for f_off in range(d_off + ent_len, d_off + d_len, ent_len):
			try:
				entry = Rs5CompressedFileDecoder(f, f.read(ent_len))
				self[entry.filename] = entry
			except NotAFile:
				# XXX: Figure out what these are.
				# I think they are just deleted files
				continue

class Rs5ArchiveEncoder(collections.OrderedDict):
	header_len = 24
	ent_len = 168
	u1 = 0
	flags = 0x80000000

	def __init__(self, filename):
		collections.OrderedDict.__init__(self)
		self.fp = open(filename, 'wb')
		self.fp.seek(self.header_len)

	def add(self, filename):
		print "Adding %s..." % filename
		entry = Rs5CompressedFileEncoder(self.fp, filename)
		self[entry.filename] = entry

	def _write_directory(self):
		print "Writing central directory..."
		self.d_off = self.fp.tell()

		dir_hdr = struct.pack('<QII', self.d_off, self.ent_len * (1 + len(self)), self.flags)
		pad = '\0' * (self.ent_len - len(dir_hdr)) # XXX: Not sure if any data here is important
		self.fp.write(dir_hdr + pad)

		for file in self.itervalues():
			ent = file.gen_dir_ent()
			pad = '\0' * (self.ent_len - len(ent)) # XXX: Not sure if any data here is important
			self.fp.write(ent + pad)

	def _write_header(self):
		print "Writing RS5 header..."
		self.fp.seek(0)
		self.fp.write(struct.pack('<8sQII', 'CFILEHDR', self.d_off, self.ent_len, self.u1))

	def save(self):
		self._write_directory()
		self._write_header()
		self.fp.flush()
		print "Done."

class Rs5ArchiveUpdater(Rs5ArchiveEncoder, Rs5ArchiveDecoder):
	def __init__(self, fp):
		self.fp = fp
		return Rs5ArchiveDecoder.__init__(self, fp)

	def add(self, filename):
		self.fp.seek(0, 2)
		return Rs5ArchiveEncoder.add(self, filename)

	def save(self):
		self.fp.seek(0, 2)
		return Rs5ArchiveEncoder.save(self)