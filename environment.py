#!/usr/bin/env python

import sys
import struct
import json
import collections

import rs5

data_types = {}
json_decoders = {}
def data_type(c):
	global data_types
	data_types[c.id] = c
	if hasattr(c, 'from_json'):
		json_decoders[c.id] = c
	return c

def parse_type(t, f):
	c = data_types[t]
	if hasattr(c, 'dec_new'):
		return c.dec_new(f)
	r = c()
	r.dec(f)
	return r

def encode_json_types(obj):
	return obj.to_json()

def decode_json_types(dct):
	ret = collections.OrderedDict()
	for (k,v) in dct:
		assert(k[1] == ':')
		if k[0] in json_decoders:
			r = json_decoders[k[0]]()
			r.from_json(v)
			ret[null_str(k)] = r
		else:
			ret[null_str(k)] = v
	# print ret
	return ret

def dump_json(node, outputfd):
	return json.dump(node, outputfd, default=encode_json_types, ensure_ascii=True, indent=4, separators=(',', ': '))

def parse_json(j):
	j = json.load(j, object_pairs_hook=decode_json_types, parse_int=env_int, parse_float=env_float)
	root = env_tree()
	root.from_json(j)
	return root

@data_type
class env_null(object):
	id = '.'
	def dec(self, f):
		pass
	def to_json(self):
		return None
	def from_json(self, j):
		pass
	def enc(self):
		return ''

@data_type
class null_str(str):
	id = 's'
	@classmethod
	def dec_new(cls, f):
		r = ''
		while True:
			c = f.read(1)
			if c == '\0':
				# print>>sys.stderr, 'string: '+r
				return str.__new__(cls, r)
			r += c
	def enc(self):
		return self + '\0'

@data_type
class env_tree(object):
	id = 'T'
	def __init__(self):
		self.children = collections.OrderedDict()
	def dec(self, f):
		while True:
			name = null_str.dec_new(f)
			if name == '':
				break
			t = f.read(1)
			try:
				child = parse_type(t, f)
				self.children[name] = child
			except:
				dump_json(self.children, sys.stderr)
				raise
	def to_json(self):
		r = collections.OrderedDict()
		for (name, child) in self.children.iteritems():
			r['%s:%s' % (child.id, name)] = child
		return r
	def from_json(self, c):
		for (name, child) in c.iteritems():
			if isinstance(child, unicode):
				child = null_str(child)
			self.children[null_str(name[2:])] = child
	def enc(self):
		ret = ''
		for (name, child) in self.children.iteritems():
			ret += name.enc() + child.id + child.enc()
		return ret + '\0'


@data_type
class env_int(int):
	id = 'i'
	@classmethod
	def dec_new(cls, f):
		return int.__new__(cls, struct.unpack('<i', f.read(4))[0])
	def enc(self):
		return struct.pack('<i', self)

@data_type
class env_float(float):
	id = 'f'
	@classmethod
	def dec_new(cls, f):
		return float.__new__(cls, struct.unpack('<f', f.read(4))[0])
	def enc(self):
		return struct.pack('<f', self)

class env_list(object):
	def __init__(self):
		self.list = []
	def dec(self, f):
		self.len = env_int.dec_new(f)
		for i in range(self.len):
			e = self.parse(f)
			self.list.append(e)
	def enc(self):
		r = self.len.enc()
		for i in self.list:
			r += i.enc()
		return r
	def to_json(self):
		return self.list

	def from_json(self, l):
		for i in l:
			if isinstance(i, unicode):
				i = null_str(i)
			self.list.append(i)
		self.len = env_int(len(l))

@data_type
class env_int_list(env_list):
	id = 'I'
	parse = env_int.dec_new

@data_type
class env_str_list(env_list):
	id = 'S'
	parse = null_str.dec_new

@data_type
class env_float_list(env_list):
	id = 'F'
	parse = env_float.dec_new

@data_type
class env_mixed_list(env_list):
	id = 'M'
	@staticmethod
	def parse(f):
		t = f.read(1)
		return parse_type(t, f)
	def enc(self):
		r = self.len.enc()
		for i in self.list:
			r += i.id + i.enc()
		return r

@data_type
class env_remove_list(env_list):
	id = 'R'
	@staticmethod
	def parse(f):
		assert(f.read(1) == '\0')
	def enc(self):
		return self.len.enc() + '\0'*self.len

def parse_environment(f, outputfd):
	(magic, filename, filesize, u2) = rs5.parse_rs5file_header(f)
	assert(magic == 'RAW.')
	assert(filename == 'environment')
	assert(u2 == 1)

	assert(f.read(4) == 'DATA')
	(u1, size, u3) = struct.unpack('<4sI4s', f.read(4*3))
	assert(u1 == '\0\0\1\0')
	# print filesize
	# print size
	assert(u3 == '\0\0\0\0')

	try:
		t = f.read(1)
		root = parse_type(t, f)
	except:
		print 'Address: 0x%x' % f.tell()
		raise
	return dump_json(root, outputfd)

def json2env(j, outputfd):
	root = parse_json(j)
	# print dump_json(root, sys.stdout)
	d = root.id + root.enc()
	dh = struct.pack('<4s4sI4s', 'DATA', '\0\0\1\0', len(d), '\0\0\0\0')
	pad = rs5.padding(len(dh) + len(d), 8) # DATA files are padded before RAW. header is applied
	outputfd.write(rs5.enc_file('RAW.', 'environment', dh + d + pad, 1))

def parse_args():
	import argparse
	parser = argparse.ArgumentParser()

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-d', '--decode-file', metavar='FILE',
			help='Decode a previously extracted environment file')
	group.add_argument('-e', '--encode-file', metavar='FILE',
			help='Encode a JSON formatted environment file')

	parser.add_argument('-o', '--output',
			type=argparse.FileType('wb'), default=sys.stdout,
			help='Store the result in OUTPUT')

	return parser.parse_args()

def main():
	args = parse_args()

	if args.decode_file:
		return parse_environment(open(args.decode_file, 'rb'), args.output)

	if args.encode_file:
		return json2env(open(args.encode_file, 'rb'), args.output)

if __name__ == '__main__':
	main()
