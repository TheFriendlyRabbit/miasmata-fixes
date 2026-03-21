#!/usr/bin/env python

import argparse
import binascii
import collections
import itertools
import json
import struct
import sys

from lib import rs5file

data_types = collections.OrderedDict()
json_decoders = {}


def data_type(c):
    global data_types
    data_types[c.id] = c
    if hasattr(c, 'from_json'):
        json_decoders[c.id] = c
    return c


def parse_type(t, f):
    c = data_types[t.decode("utf-8")]
    if hasattr(c, 'dec_new'):
        return c.dec_new(f)
    r = c()
    r.dec(f)
    return r


def encode_json_types(obj):
    return obj.to_json()


def decode_json_types(dct):
    ret = collections.OrderedDict()
    for (k, v) in dct:
        assert k[1] == ':'
        if k[0] in json_decoders:
            r = json_decoders[k[0]]()
            r.from_json(v)
            ret[NullStr(k)] = r
        else:
            ret[NullStr(k)] = v
    return ret


def dump_json(node, outputfd):
    return json.dump(node, outputfd, default=encode_json_types,
                     ensure_ascii=False, indent=4, separators=(',', ': '))


def dumps_json(node):
    return json.dumps(node, default=encode_json_types, ensure_ascii=False,
                      indent=4, separators=(',', ': '))


def dumps_json_node(node):
    return json.dumps((node.id, node), default=encode_json_types,
                      ensure_ascii=False, separators=(',', ': '))


def parse_json(j):
    j = json.load(j,
                  object_pairs_hook=decode_json_types,
                  parse_int=DataInt, parse_float=DataFloat)
    root = data_tree()
    root.from_json(j)
    return root


def parse_json_node(j):
    (type, node) = json.loads(j,
                              object_pairs_hook=decode_json_types,
                              parse_int=DataInt,
                              parse_float=DataFloat)
    if type in json_decoders:
        r = json_decoders[type]()
        r.from_json(node)
        return r
    return data_types[type](node)


@data_type
class data_null(object):
    id = '.'
    desc = 'NULL'

    def dec(self, f):
        pass

    def to_json(self):
        return None

    def from_json(self, j):
        pass

    def enc(self):
        return b''

    def __eq__(self, other):
        return isinstance(other, data_null)

    def __ne__(self, other):
        return not isinstance(other, data_null)

    def __str__(self):
        return '<NULL>'


@data_type
class NullStr(str):
    id = 's'
    desc = 'String'

    @classmethod
    def dec_new(cls, f=''):
        r = ''
        while True:
            c = f.read(1)
            if c == b'\0':
                return str.__new__(cls, r)
            r += c.decode('cp1252')

    def enc(self):
        return bytes(self.encode('cp1252') + b'\0')

    def search(self, s):
        return self.lower().find(s) != -1


@data_type
class data_tree(object):
    id = 'T'
    desc = 'Tree Node'

    def __init__(self, *args):
        self.children = collections.OrderedDict(args)
        for (name, child) in self.children.items():
            child.parent = self
            child.name = name
        self.parent = None
        self.name = None
        self.last_search = ('None', True)

    def dec(self, f):
        while True:
            name = NullStr.dec_new(f)
            if name == '':
                break
            t = f.read(1)
            try:
                child = parse_type(t, f)
                self[name] = child
            except:
                dump_json(self.children, sys.stderr)
                raise

    def to_json(self):
        r = collections.OrderedDict()
        for (name, child) in self.items():
            r[f'{child.id}:{name}'] = child
        return r

    def from_json(self, c):
        for (name, child) in c.items():
            if isinstance(child, str):
                child = NullStr(child)
            self[NullStr(name[2:])] = child

    def enc(self):
        ret = b''
        for (name, child) in self.items():
            try:
                ret += name.enc() + \
                       child.id.encode("utf-8") + \
                       child.enc()
            except:
                print(name, type(name), type(child.id))
                raise
        return ret + b'\0'

    def expand_tree(self):
        ret = [self]
        for child in self.values():
            if isinstance(child, data_tree):
                ret.extend(child.expand_tree())
            else:
                ret.append(child)
        return ret

    def copy(self):
        j = dumps_json_node(self)
        ret = parse_json_node(j)
        ret.name = self.name
        assert self == ret
        return ret

    def __eq__(self, other):
        if not isinstance(other, data_tree):
            return False
        my_children = set(self.children)
        other_children = set(other.children)
        if my_children != other_children:
            return False
        for child in self:
            if self[child] != other[child]:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def diff(self, other, root=None, other_root=None):
        def expand_node(node):
            if isinstance(node, data_tree):
                return node.expand_tree()
            return [node]

        my_children = set(self.children)
        other_children = set(other.children)

        added = [(parent_list(other[child], root=other_root), other[child]) \
                 for child in other_children.difference(my_children)]
        removed = [(parent_list(self[child], root=root), self[child]) \
                   for child in my_children.difference(other_children)]

        changed = []
        for child in my_children.intersection(other_children):
            my_child = self[child]
            other_child = other[child]
            if type(my_child) != type(other_child):
                changed.append(
                    (parent_list(other_child, root=other_root), my_child,
                     other_child))
            elif isinstance(my_child, data_tree):
                (a, r, c) = my_child.diff(other_child, root=root,
                                          other_root=other_root)
                added.extend(a)
                removed.extend(r)
                changed.extend(c)
            elif my_child != other_child:
                changed.append(
                    (parent_list(other_child, root=other_root), my_child,
                     other_child))
        return (added, removed, changed)

    def _search(self, s):
        for (name, child) in self.items():
            if name.lower().find(s) != -1:
                return True
            if hasattr(child, 'search'):
                ret = child.search(s)
                if ret:
                    return True
        return False

    def search(self, s):
        if s != self.last_search[0]:
            self.last_search = (s, self._search(s))
        return self.last_search[1]

    def check_parent_invariant(self):
        for (name, child) in self.items():
            if not hasattr(child, 'parent'):
                print(
                    'WARNING: Detected Broken Invariant: %s[%s].parent is '
                    'missing' % (
                        format_parent(self), name),
                    file=sys.stderr)
            elif child.parent is not self:
                print(
                    'WARNING: Detected Broken Invariant: %s[%s].parent is not '
                    'self' % (
                        format_parent(self), name),
                    file=sys.stderr)
            if isinstance(child, data_tree):
                child.check_parent_invariant()

    def clear_dirty_flags(self):
        ret = []
        if hasattr(self, 'dirty') and self.dirty:
            ret.append(parent_index_list(self))
            del self.dirty
        for (name, child) in self.items():
            if hasattr(child, 'dirty') and child.dirty:
                ret.append(parent_index_list(child))
                del child.dirty
            if isinstance(child, data_tree):
                ret.extend(child.clear_dirty_flags())
        return ret

    def __getitem__(self, item):
        return self.children[item]

    def __iter__(self):
        return iter(self.children)

    def keys(self):
        return list(self.children.keys())

    def values(self):
        return list(self.children.values())

    def items(self):
        return list(self.children.items())

    def iterkeys(self):
        return iter(self.children.keys())

    def itervalues(self):
        return iter(self.children.values())

    def iteritems(self):
        return iter(self.children.items())

    def __len__(self):
        return len(self.children)

    def __setitem__(self, item, val):
        val.name = item
        val.parent = self
        self.children[item] = val

    def __delitem__(self, item):
        del self.children[item]


def _parent_list(node, skip=0, root=None):
    if node.parent and node is not root:
        ret = _parent_list(node.parent, skip, root=root)
        if isinstance(ret, int):
            if ret < 0:
                return ret + 1
            return [node.name]
        return ret + [node.name]
    return -skip


def parent_list(node, skip=0, root=None):
    ret = _parent_list(node, skip, root)
    if isinstance(ret, int):
        return ['<root>']
    return ret


def format_parent(node, skip=0):
    return '.'.join(parent_list(node, skip))


def parent_index_list(node):
    ret = []

    while node.parent:
        (child, node) = (node, node.parent)
        ret.append(list(node.keys()).index(child.name))

    return reversed(ret)


@data_type
class DataInt(int):
    id = 'i'
    desc = 'Integer'

    def __new__(cls, i=0):
        i = int(i)
        if i < -2 ** 31 or i >= 2 ** 31:
            raise ValueError(f'Integer value {i} out of range')
        return int.__new__(cls, i)

    @classmethod
    def dec_new(cls, f=0):
        return int.__new__(cls, struct.unpack('<i', f.read(4))[0])

    def enc(self):
        return struct.pack('<i', self)


@data_type
class DataFloat(float):
    id = 'f'
    desc = 'Floating Point Number'

    def __new__(cls, f=0.0):
        # Force rounding to a 4-byte float - important for equality
        # tests & tree diffs where one tree was decoded from an
        # environment file and the other was manufactured in Python:
        return float.__new__(cls,
                             struct.unpack('<f', struct.pack('<f', float(f)))[
                                 0])

    @classmethod
    def dec_new(cls, f=0.0):
        return float.__new__(cls, struct.unpack('<f', f.read(4))[0])

    def enc(self):
        return struct.pack('<f', self)


class DataList(object):
    def __init__(self):
        self.list = []

    def dec(self, f):
        l = DataInt.dec_new(f)
        for i in range(l):
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
            if isinstance(i, str):
                i = NullStr(i)
            self.list.append(i)

    def __iter__(self):
        return iter(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, item, val):
        self.list[item] = val

    def __delitem__(self, item):
        del self.list[item]

    def insert(self, index, object):
        return self.list.insert(index, object)

    def remove(self, item):
        self.list.remove(item)

    @property
    def len(self):
        # Because __len__ casts to a regular int
        return DataInt(len(self.list))

    def __len__(self):
        return len(self.list)

    def summary(self):
        if len(self.list) > 5:
            return ', '.join(list(map(str, self.list[:5])) + ['...'])
        return ', '.join(map(str, self.list))

    def __str__(self):
        return ', '.join(map(str, self.list))

    def __eq__(self, other):
        if not type(self) == type(other):
            return False
        return self.list == other.list

    def __ne__(self, other):
        return not self == other


@data_type
class DataIntList(DataList):
    id = 'I'
    desc = 'List of Integers'
    type = DataInt
    parse = DataInt.dec_new


@data_type
class DataStrList(DataList):
    id = 'S'
    desc = 'List of Strings'
    type = NullStr
    parse = NullStr.dec_new

    def search(self, s):
        return any(map(lambda x: x.find(s) != -1, self))


@data_type
class DataFloatList(DataList):
    id = 'F'
    desc = 'List of Floats'
    type = DataFloat
    parse = DataFloat.dec_new


@data_type
class DataMixedList(DataList):
    id = 'M'
    desc = 'Mixed type List'

    @staticmethod
    def parse(f):
        t = f.read(1)
        return parse_type(t, f)

    def enc(self):
        r = self.len.enc()
        for i in self.list:
            r += i.id.encode("utf-8") + i.enc()
        return r

    def search(self, s):
        for v in self:
            if hasattr(v, 'search'):
                ret = v.search(s)
                if ret:
                    return True
        return False


@data_type
class DataRaw():
    id = 'R'
    desc = 'Raw Binary Data'

    def __init__(self, raw=''):
        self.raw = raw

    def dec(self, f):
        l = DataInt.dec_new(f)
        self.raw = f.read(l)

    def enc(self):
        return DataInt(len(self.raw)).enc() + self.raw

    def to_json(self):
        return self.raw.hex()

    def from_json(self, l):
        self.raw = binascii.a2b_hex(l)

    def summary(self):
        r = self.raw[:32]
        ret = ' '.join(['%.2x' % x for x in r])
        if r == self.raw:
            return ret
        return ret + '...'

    def __str__(self):
        return ' '.join(['%.2x' % x for x in self.raw])

    def __eq__(self, other):
        if not isinstance(other, DataRaw):
            return False
        return self.raw == other.raw

    def __ne__(self, other):
        return not self == other


def diff_data(tree1, tree2):
    (added, removed, changed) = tree1.diff(tree2, root=tree1, other_root=tree2)
    return {'added': added, 'removed': removed, 'changed': changed}


def diff_data_files(xxx_todo_changeme, output, pretty=False):
    (f1, f2) = xxx_todo_changeme
    data1 = parse_data(f1)
    data2 = parse_data(f2)
    diff = diff_data(data1, data2)
    if pretty:
        pretty_print_diff(diff)
    else:
        json_encode_diff(diff, output)


def null_diff():
    return {'added': [], 'removed': [], 'changed': []}


def is_new_style_diff_removed(removed):
    return len(removed) and len(removed[0]) == 2 and isinstance(removed[0][0],
                                                                list)


def apply_diff(root, diff):
    def find_parent_node(plist):
        node = root
        for name in plist[:-1]:
            node = node[name]
            if not isinstance(node, data_tree):
                raise TypeError(f'{name} is not a tree node')
        return node

    def iter_added_changed(added, changed):
        yield from added
        try:
            for (plist, removed, added) in changed:
                yield (plist, added)
        except ValueError:
            for (plist, c) in changed:
                yield (plist, c)

    for (plist, node) in diff['removed']:
        try:
            parent = find_parent_node(plist)
            del parent[plist[-1]]
        except (KeyError, ValueError):
            # raise # XXX: For testing
            continue

    for (plist, node) in sorted(
            iter_added_changed(diff['added'], diff['changed'])):
        assert type(node) in list(data_types.values())
        try:
            parent = find_parent_node(plist)
        except (KeyError, ValueError):
            # raise # XXX: For testing
            continue
        name = NullStr(plist[-1])
        parent[name] = node


def json_encode_diff(diff, outputfd, version=None):
    tmp = diff.copy()
    tmp['added'] = [(plist, dumps_json_node(node)) for (plist, node) in
                    diff['added']]
    tmp['removed'] = [(plist, dumps_json_node(node)) for (plist, node) in
                      diff['removed']]
    tmp['changed'] = [(plist, dumps_json_node(node1), dumps_json_node(node2)) \
                      for (plist, node1, node2) in diff['changed']]
    if version is not None:
        tmp['version'] = version

    t = json.dumps(tmp, indent=4, ensure_ascii=False)
    outputfd.write(t.encode('utf-8'))


def json_decode_diff(inputfd):
    diff = json.load(inputfd)
    diff['added'] = [(plist, parse_json_node(j)) for (plist, j) in
                     diff['added']]

    if is_new_style_diff_removed(diff['removed']):
        diff['removed'] = [(plist, parse_json_node(j)) for (plist, j) in
                           diff['removed']]
    else:
        diff['removed'] = itertools.zip_longest(diff['removed'], [],
                                                fillvalue=None)

    try:
        diff['changed'] = [(plist, parse_json_node(j1), parse_json_node(j2)) \
                           for (plist, j1, j2) in diff['changed']]
    except ValueError:
        diff['changed'] = [(plist, parse_json_node(j), parse_json_node(j)) \
                           for (plist, j) in diff['changed']]
    return diff


def pretty_fmt_diff(diff, file1=None, file2=None):
    def iter_changed(changed):
        try:
            for (p, r, a) in changed:
                yield ((p, r), '-')
                yield ((p, a), '+')
        except ValueError:
            for (p, c) in changed:
                yield ((p, c), '>')

    removed = itertools.zip_longest(diff['removed'], [], fillvalue='-')
    added = itertools.zip_longest(diff['added'], [], fillvalue='+')
    changed = iter_changed(diff['changed'])
    combined = sorted(itertools.chain(added, removed, changed),
                      key=lambda p_n_pre: (p_n_pre[0][0], 127 - ord(p_n_pre[1]),
                                           p_n_pre[0][1]))

    ret = []
    if file1 is not None:
        ret.append(f'--- {file1}')
    if file2 is not None:
        ret.append(f'+++ {file2}')
    if file1 is not None or file2 is not None:
        ret.append('')

    for ((plist, node), prefix) in combined:
        if node is not None:
            ret.append(
                f'{prefix} {'->'.join(plist)}: {dumps_json(node)}')
        else:
            ret.append(f'{prefix} {'->'.join(plist)}')
    return '\n'.join(ret)


def pretty_print_diff(diff):
    print(pretty_fmt_diff(diff))


def parse_data(f):
    try:
        t = f.read(1)
        return parse_type(t, f)
    except:
        print(f'Address: 0x{f.tell()}')
        raise


def data2json(f, outputfd):
    return dump_json(parse_data(f), outputfd)


def parse_chunk(chunk):
    assert chunk.name == b'DATA'
    return parse_data(chunk.get_fp())


def chunk2json(chunk, outputfd):
    assert chunk.name == 'DATA'
    return data2json(chunk.get_fp(), outputfd)


def encode(root):
    return root.id.encode("utf-8") + root.enc()


def json2data(j):
    root = parse_json(j)
    return encode(root)


def write_data(j, outputfd):
    outputfd.write(json2data(j))


def make_chunk(data):
    return rs5file.Rs5ChunkEncoder('DATA', data)


def parse_args():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--decode-file', metavar='FILE',
                       type=argparse.FileType('rb'),
                       help='Decode a previously extracted database')
    group.add_argument('-e', '--encode-file', metavar='FILE',
                       type=argparse.FileType('rb'),
                       help='Encode a JSON formatted database')

    group.add_argument('--diff-pretty', nargs=2, metavar='FILE',
                       type=argparse.FileType('rb'),
                       help='Display the differences between two environment '
                            'files in a human readable format')
    group.add_argument('--diff-json', nargs=2, metavar='FILE',
                       type=argparse.FileType('rb'),
                       help='Write the differences between two environment '
                            'files suitable for use with --apply-diff')

    parser.add_argument('-o', '--output',
                        type=argparse.FileType('wb'), default=sys.stdout,
                        help='Store the result in OUTPUT')

    return parser.parse_args()


class MiasmataDataTypeMeta(type):
    def __instancecheck__(self, instance):
        return instance.__class__ in list(data_types.values())

    def __subclasscheck__(self, cls):
        return cls in list(data_types.values())


class MiasmataDataType():
    __metaclass__ = MiasmataDataTypeMeta


class MiasmataDataCoercibleMeta(type):
    coercible = NullStr, DataInt, DataFloat

    def __instancecheck__(self, instance):
        return instance.__class__ in self.coercible

    def __subclasscheck__(self, cls):
        return cls in self.coercible


class MiasmataDataCoercible():
    __metaclass__ = MiasmataDataCoercibleMeta


def main():
    args = parse_args()

    if args.decode_file:
        return data2json(args.decode_file, args.output)

    if args.encode_file:
        return write_data(args.encode_file, args.output)

    if args.diff_pretty:
        return diff_data_files(args.diff_pretty, args.output, pretty=True)
    if args.diff_json:
        return diff_data_files(args.diff_pretty, args.output, pretty=True)


if __name__ == '__main__':
    main()

# vi:noexpandtab:sw=8:ts=8
