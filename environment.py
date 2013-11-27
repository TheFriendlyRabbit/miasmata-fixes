#!/usr/bin/env python

import sys
import struct
import json

import rs5

data_types = {}
json_decoders = {}
def data_type(c):
	global data_types
	data_types[c.id] = c
	if hasattr(c, 'from_json'):
		json_decoders['__%s__'%c.id] = c
	return c

def parse_type(t, f):
	c = data_types[t]
	if hasattr(c, 'dec_new'):
		return c.dec_new(f)
	r = c()
	r.dec(f)
	return r

def encode_json_types(obj):
	return {'__%s__' % obj.id: obj.to_json()}

def decode_json_types(dct):
	assert(len(dct) == 1)
	(k,v) = dct.items()[0]
	if k in json_decoders:
		r = json_decoders[k]()
		r.from_json(v)
		# print r
		return r
	return (null_str(k), v)

def dump_json(node):
	return json.dumps(node, default=encode_json_types, ensure_ascii=True, indent=4, separators=(',', ':'))

def parse_json(j):
	return json.loads(j, object_hook=decode_json_types, parse_int=env_int, parse_float=env_float)


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
		# TODO: Store these as an ordered dictionary to make the output
		# clearer, while not losing order
		self.children = []
	def dec(self, f):
		while True:
			name = null_str.dec_new(f)
			if name == '':
				break
			t = f.read(1)
			try:
				child = parse_type(t, f)
				self.children.append({name: child})
			except:
				print>>sys.stderr, dump_json(self.children)
				raise
	def to_json(self):
		return self.children
	def from_json(self, c):
		for (name, child) in c:
			if isinstance(child, unicode):
				child = null_str(child)
			self.children.append((null_str(name), child))
	def enc(self):
		ret = ''
		for (name, child) in self.children:
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

def parse_environment():
	f = open('environment', 'r')
	(magic, filename, filesize) = rs5.parse_header(f)
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
	return dump_json(root)

def dump_env(node):
	# TODO: DATA header, RAW header
	r = node.id + node.enc()
	# pad = '\0' * (4 - (len(r) % 4) % 4)
	return r

def json2env(j):
	root = parse_json(j)
	# print dump_json(root)
	return dump_env(root)

def main():
	j = parse_environment()
	# print j

	# print>>sys.stderr, '-'*79
	sys.stdout.write(json2env(j))

	# if len(sys.argv) == 1:
	# 	return parse_environment()
	# return json2env(open(sys.argv[1], 'r'))

if __name__ == '__main__':
	main()
