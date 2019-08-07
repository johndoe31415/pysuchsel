#!/usr/bin/python3
#
#	XMLParser - Simple expat based XML parser.
#	Copyright (C) 2011-2012 Johannes Bauer
#
#	This file is part of pycommon.
#
#	pycommon is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pycommon is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pycommon; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>
#
#	File UUID d93f813c-5df5-489a-8f18-ada965493642

import xml.parsers.expat

class XMLException(Exception):
	def __init__(self, text):
		Exception.__init__(self, text)

class XMLNode():
	"""Represents an XML element node and XML DOM tree representation. Used for
	easily accessing XML/HTML in a "pythonic" manner. Don't expect this
	implementation to understand all XML features."""

	CDATA_NODENAME = "#cdata"
	CDATA_ATTRIBUTE = "text"

	def __init__(self, name, attrs = None, parent = None, linenumber = None):
		"""Creates a node with a specific name. May be initialized with a
		attribute dictionary (or None if no attributes are given) and a parent
		node (or None if root node)."""
		assert(isinstance(name, str))
		assert((linenumber is None) or isinstance(linenumber, int))
		if attrs is None:
			attrs = { }
		else:
			# Create a copy of the attribute dictionary
			attrs = dict(attrs)

		self._name = name
		self._parent = parent
		self._linenumber = linenumber
		self._attrs = attrs
		self._children = [ ]
		self._cdata = ""

	def getname(self):
		"""Returns the name of the current node."""
		return self._name

	def getattrs(self):
		"""Returns the attribute dictionary of the node."""
		return self._attrs

	def getparent(self, index = 0):
		"""Returns the parent node or None if the current node is the root
		node. Can also retrieve grandparents if the given index is greater than
		0."""
		assert(isinstance(index, int))
		assert(index >= 0)
		node = self
		for i in range(index + 1):
			node = node._parent
		return node

	def getlinenumber(self):
		"""Returns the line number on which the starting tag occured in the
		original XML file."""
		return self._linenumber

	def _nodematch(self, nodename, **attrs):
		"""Matches if the current node has the required name (or do not match
		name if nodename is None) and if the required arguments are all present
		and have the desired value. Returns a bool value."""
		match = (nodename is None) or (self.getname() == nodename)
		if match:
			# Name is already a match, do the kwargs match?
			for (reqattrname, reqattrvalue) in attrs.items():
				value = self.get(reqattrname)
				if (value is None) or (value != reqattrvalue):
					# If the attribute does not exist or is unequal to the
					# required prerequisite, this node does not match
					match = False
					break
		return match

	def searchparent(self, nodename, **attrs):
		"""Go up the parent nodes until a node is found which satisfies all
		conditions (parent node name and attributes). Return None if no such
		node exists."""
		node = self.getparent()
		while node:
			if node._nodematch(nodename, **attrs):
				break
			node = node.getparent()
		return node

	def addchild(self, node, **kwargs):
		"""Adds a node to the child list of the current node. May be either of
		type XMLNode (in which case it is taken as-is) or of type str (in which
		case a XMLNode is created on-the-fly with that nodename)."""
		if isinstance(node, str):
			node = XMLNode(node, kwargs)
		assert(isinstance(node, XMLNode))
		self._children.append(node)
		return node
	
	def getallchildren(self):
		"""Return an iterator over all children."""
		return iter(self._children)

	def getchildren(self, nodename, **attrs):
		"""Return an iterator over all children that have the specified
		nodename and satisfy all kwargs conditions for attributes."""
		for child in self._children:
			if child._nodematch(nodename, **attrs):
				yield child

	def getchild(self, nodename, **attrs):
		"""Return the first child that has the specified nodename and satisfies
		all kwargs conditions for attributes. Returns 'None' if no child was
		found."""
		for node in self.getchildren(nodename, **attrs):
			return node
		return None

	def search(self, nodename, **attrs):
		"""Recursively searches for nodes with the required attributes,
		including the current node itself."""
		if self._nodematch(nodename, **attrs):
			yield self

		# Recurse
		for child in self._children:
			for match in child.search(nodename, **attrs):
				yield match

	def searchunique(self, nodename, **attrs):
		"""Recursively searches for nodes with the required attributes,
		including the current node itself. Returns only one single node. If no
		matching nodes are found or more than one node is found that matches
		the criteria an exception is thrown."""
		result = None
		for nextresult in self.search(nodename, **attrs):
			if result is None:
				result = nextresult
			else:
				raise XMLException("More than one node matched criteria for nodename '%s', attributes %s. Node not unique." % (nodename, str(attrs)))
		if result is None:
			raise XMLException("No node matched criteria for nodename '%s', attributes %s." % (nodename, str(attrs)))
		return result

	def treestrip(self, allowedtags, startnode = None):
		"""Recursively strips the tree of all nodes which have a name that is
		not contained in the 'allowedtags' parameter (which should be a set).
		Creates copies of all nodes and returns a new root XMLNode named
		'result'."""
		if startnode is None:
			startnode = XMLNode("result")
		beginnode = startnode

		if self.getname() in allowedtags:
			# Add myself to the tree, copy node
			startnode = startnode.addchild(XMLNode(self.getname(), self.getattrs(), startnode))

		# Recurse
		for child in self._children:
			child.treestrip(allowedtags, startnode)

		return beginnode

	def attrstrip(self, allowedattrs):
		"""Recursively strips the tree of all attributes which are not
		contained in the 'allowedattrs' parameters (which should be a set)."""
		newattrs = { }
		for (key, value) in self._attrs.items():
			if key in allowedattrs:
				newattrs[key] = value
		self._attrs = newattrs

		# Recurse
		for child in self._children:
			child.attrstrip(allowedattrs)

		return self

	def appendcdata(self, cdata):
		"""Appends the given cdata to the current node (i.e. creates a child
		node which contains cdata or appends to the last cdata child node).
		Returns original node."""
		if (len(self._children) > 0) and (self._children[-1].getname() == XMLNode.CDATA_NODENAME):
			# Last child node is already a cdata node, append text
			self._children[-1][XMLNode.CDATA_ATTRIBUTE] += cdata
		else:
			self.addchild(XMLNode(XMLNode.CDATA_NODENAME, { XMLNode.CDATA_ATTRIBUTE: cdata }, self))
		return self

	def getcdata(self, recursive = True, spacers = False, jointostr = True):
		"""Returns the cdata of the current node (or also of preceding or
		succeeding nodes). If spacers are enabled, cdata nodes that are
		separated by some non-cdata node are concatenated with a single
		space."""
		cdata = [ ]
		if self.getname() == XMLNode.CDATA_NODENAME:
			cdata.append(self[XMLNode.CDATA_ATTRIBUTE])
		if spacers:
			cdata.append(None)

		if recursive:
			for child in self._children:
				cdata += child.getcdata(recursive, spacers, False)

		if jointostr:
			# Filter out leading and trailing "None", remove more than one
			# subsequent of "None" and in the end, replace them all with one
			# single space.

			# Filter out trailing None first
			if len(cdata) > 0:
				for i in range(len(cdata) - 1, -1, -1):
					if cdata[i] is not None:
						break
				cdata = cdata[:i + 1]

			# Then go over array, change Nones to single spaces on-the-fly and
			# remove leading and double None occurences
			dostrip = True
			strippedcdata = [ ]
			for i in range(len(cdata)):
				if cdata[i] is not None:
					strippedcdata.append(cdata[i])
					dostrip = False
				else:
					if not dostrip:
						strippedcdata.append(" ")
						dostrip = True
			cdata = strippedcdata

			return "".join(cdata)
		else:
			return cdata

	def getstrippedcdata(self, recursive = True):
		"""Returns the cdata of the current node (or also of preceding or
		succeeding nodes), but strips whitespace left and right before
		returning the string."""
		text = self.getcdata(recursive).lstrip().rstrip()
		return text

	def hasattr(self, attribute):
		"""Returns true if the specified attribute is set in the attribute
		dictionary of the node."""
		return attribute in self._attrs.keys()

	def __getitem__(self, key):
		"""Get a attribute of a node or select the n-th node. Behavior depends
		on the type of key -- if it's a str, attributes will be selected
		(attribute mode). If it's an integer, will return the n-th sibling node
		(selection mode). For attribute mode, throws an exception if the
		attribute does not exist in the attribute dictionary. For selection
		mode, throws an exception if the index is out of bounds."""
		assert(isinstance(key, str) or isinstance(key, int))
		if isinstance(key, str):
			result = self._attrs[key]
		else:
			cnt = 0
			for partialresult in self._parent.getchildren(self.getname()):
				if cnt == key:
					result = partialresult
					break
				cnt += 1
		return result
	
	def get(self, key, defaultvalue = None):
		"""Get a attribute of the node. Returns None if the attribute does not
		exist in the attribute dictionary."""
		return self._attrs.get(key, defaultvalue)

	def __setitem__(self, key, value):
		"""Sets a attribute of the node. Value must be a string."""
		assert(isinstance(value, str))
		self._attrs[key] = value

	def __getattr__(self, attribute):
		"""Returns the first child node with the appropriate name. Shortcut for
		getchild(), but throws an exception if no such child is found."""
		child = self.getchild(attribute)
		if child is None:
			raise XMLException("Node has no child node called '%s'." % (attribute))
		return child

	def __iter__(self):
		"""Returns an iterator over the parents' node children which have the
		same name as the current node. This allows the use of
		iter(rootnode.foochild) to iterate over all 'foochild' nodes that are
		children of the 'rootnode'."""
		if self._parent is None:
			# Iterating over root node will only return the root node iterator
			# (we're guaranteed to have only one root node)
			return iter([ self ])
		return self._parent.getchildren(self.getname())

	def dump(self, indent = 0):
		"""Recursively dumps the whole tree."""
		print((" " * indent) + self._name + " = " + str(self._attrs))
		for child in self._children:
			child.dump(indent + 4)

	def _xmlescape(string):
		"""Escapes a a string so that it can be embedded into an XML file."""
		string = string.replace("&", "&amp;")
		string = string.replace("\"", "&quot;")
		string = string.replace("<", "&lt;")
		return string

	def _dumpattrstring(self, pretty = True, sortkey = None):
		"""Returns attributes as a XML string that can be written into an XML
		file. Attributes are sorted accorting to the given sortkey function (or
		alphabetican order if pretty-printing is used)."""

		keyorder = list(self._attrs.keys())
		if sortkey is not None:
			keyorder.sort(key = sortkey)
		elif pretty is not None:
			keyorder.sort()
		attributes = [ "%s=\"%s\"" % (key, XMLNode._xmlescape(self._attrs[key])) for key in keyorder ]
		return " ".join(attributes)

	def _dumpnode(self, f, pretty = False, indent = 0, sortkey = None):
		"""Recursively dumps a XML node (i.e. the subtree) to a file (i.e. tag
		names and attribute strings) in a pretty manner (i.e. with indenting)
		or raw manner (no indenting, no newlines)."""
		attrstring = self._dumpattrstring(pretty = pretty, sortkey = sortkey)
		if len(attrstring) > 0:
			attrstring = " " + attrstring

		if not pretty:
			(preopen, postopen, preclose, postclose) = ("", "", "", "")
		else:
			if self.getname() == XMLNode.CDATA_NODENAME:
				(preopen, postopen, preclose, postclose) = ("", "", "", "")
			elif (len(self._children) == 1) and (self._children[0].getname() == XMLNode.CDATA_NODENAME):
				(preopen, postopen, preclose, postclose) = (("\t" * indent), "", "", "\n")
			else:
				(preopen, postopen, preclose, postclose) = (("\t" * indent), "\n", ("\t" * indent), "\n")

		if len(self._children) > 0:
			f.write("%s<%s%s>%s" % (preopen, self.getname(), attrstring, postopen))
			for child in self._children:
				child._dumpnode(f, pretty, indent + 1, sortkey)
			f.write("%s</%s>%s" % (preclose, self.getname(), postclose))
		else:
			if self.getname() != XMLNode.CDATA_NODENAME:
				# Regular node with no children
				f.write("%s<%s%s />%s" % (preopen, self.getname(), attrstring, postclose))
			else:
				# Cdata node (with no children by definition)
				f.write("%s%s%s" % (preopen, XMLNode._xmlescape(self[XMLNode.CDATA_ATTRIBUTE]), postclose))

	def write(self, f, pretty = False, sortkey = None):
		"""Writes an XML stream to the given file object without any formatting
		(i.e.  as close to the original source as possible). Attributes are
		output in arbitrary order."""
		f.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
		self._dumpnode(f, pretty, sortkey = sortkey)

	def getxmlstr(self, pretty = False):
		"""Returns the XML string as it would be written to a file by the
		'write' function."""
		class MemWriter():
			def __init__(self): self._data = [ ]
			def write(self, text): self._data.append(text)
			def get(self): return "".join(self._data)
		f = MemWriter()
		self.write(f, pretty)
		return f.get()

	def __str__(self):
		"""Returns a string representation of the current XML node and its
		attributes, but not its children."""
		return "XMLNode<%s, %s>" % (self.getname(), str(self.getattrs()))


class XMLParser():
	"""Parses an XML document using expat and returns a DOM representation with
	a XMLNode root node."""
	def __init__(self):
		self._rootnode = None
		self._curnode = None

		self._parser = xml.parsers.expat.ParserCreate()			
		self._parser.StartElementHandler = self._startElementHandler
		self._parser.EndElementHandler = self._endElementHandler
		self._parser.CharacterDataHandler = self._cDataHandler

	def _startElementHandler(self, nodename, nodeattrs):
		newNode = XMLNode(nodename, nodeattrs, self._curnode, self._parser.CurrentLineNumber)
		if self._curnode is None:
			# If rootnode, just set newnode to curnode
			self._rootnode = newNode
		else:
			# Else add to children
			self._curnode.addchild(newNode)
		self._curnode = newNode

	def _endElementHandler(self, nodename):
		if nodename != self._curnode.getname():
			raise XMLException("Invalid XML, expected </%s>, but encountered </%s>." % (self._curnode.getname(), nodename))
		self._curnode = self._curnode.getparent()

	def _cDataHandler(self, cdata):
		self._curnode.appendcdata(cdata)
	
	def parsehandle(self, filehdl):
		"""Parse the given file handle, which has to be opened in binary mode
		(e.g. sys.stdin.buffer) and return the root node."""
		self._parser.ParseFile(filehdl)
		return self._rootnode

	def parsefile(self, filename):
		"""Parse the given XML file and return the root node."""
		return self.parsehandle(open(filename, "rb"))
	
	def parse(self, xmltext):
		"""Parse the given XML text and return the root node."""
		self._parser.Parse(xmltext)
		return self._rootnode

	def getrootnode(self):
		"""Returns the root node of the parsed XML tree."""
		return self._rootnode


if __name__ == "__main__":
	def testcase1():
		xmltest = """<?xml version="1.0" encoding="UTF-8"?>
				<xmldefinition>
					<someitem foo="1.0" bar="1.2" id="blubb" />
					<someitem foo="1.9" bar="1.4" id="määh" />
					<thirditem>
						<someitem blubb="9" id="blubb" />
				</thirditem>
			</xmldefinition>
		"""
		tree = XMLParser().parse(xmltest)
		assert(tree.getname() == "xmldefinition")
		assert(tree.someitem["foo"] == "1.0")
		assert(tree.someitem["bar"] == "1.2")
		assert(tree.someitem["id"] == "blubb")

		expect = {
			0: {
				"foo":	"1.0",
				"bar":	"1.2",
				"id":	"blubb",
			},
			1: {
				"foo":	"1.9",
				"bar":	"1.4",
				"id":	"määh",
			},
		}
		cnt = 0
		for item in tree.someitem:
			for (key, value) in expect[cnt].items():
				assert(item[key] == value)
			cnt += 1

		assert(tree.getchild("foo") is None)
		assert(tree.getchild("someitem") is tree.someitem)

		specialchild = tree.getchild("someitem", bar = "1.4")
		assert(specialchild["bar"] == "1.4")

		assert(len(list(tree.search("someitem", id = "blubb"))) == 2)

	def testcase2():
		xmltest = """<?xml version="1.0" encoding="UTF-8"?>
			<xmldefinition>here is some cdata
				and here too<someitem foo="1.0" bar="1.2" id="blubb" />and here also
				<someitem foo="1.9" bar="1.4" id="määh">
					this is some <interrupt />interrupted cdata!
				</someitem>
			</xmldefinition>
		"""
		tree = XMLParser().parse(xmltest)

		someitems = list(tree.search("someitem"))
		assert(len(someitems) == 2)
		someitem = someitems[1]
		assert(someitem.getstrippedcdata() == "this is some interrupted cdata!")

	def testcase3():
		xmltest = """<?xml version="1.0" encoding="UTF-8"?>
			<xmldefinition>
				<someitem foo="1.0" bar="1.2" id="index0" />
				<someitem foo="1.9" bar="1.4" id="index1" />
				<someitem foo="1.9" bar="1.4" id="index2">
					<otheritem foo="5.5" bar="344" id="subindex0" />
					<otheritem foo="4.1" bar="244" id="subindex1" />
					<otheritem foo="3.3" bar="154" id="subindex2" />
					<otheritem foo="2.8" bar="542" id="subindex3" />
				</someitem>
				<someitem foo="1.9" bar="1.4" id="index3" />
			</xmldefinition>
		"""

		tree = XMLParser().parse(xmltest)
		assert(tree.someitem[0] is tree.someitem)
		assert(tree.someitem[0]["id"] == "index0")
		assert(tree.someitem[1]["id"] == "index1")
		assert(tree.someitem[2]["id"] == "index2")
		assert(tree.someitem[3]["id"] == "index3")

		assert(tree.someitem[2] is tree.searchunique("someitem", id = "index2"))
		assert(tree.someitem[2].otheritem[0]["id"] == "subindex0")
		assert(tree.someitem[2].otheritem[1]["id"] == "subindex1")
		assert(tree.someitem[2].otheritem[2]["id"] == "subindex2")
		assert(tree.someitem[2].otheritem[3]["id"] == "subindex3")

	def testcase4():
		xmltest = """<?xml version="1.0" encoding="UTF-8"?>
			<xmldefinition>here is some cdata<anode /><xnode /><bnode>and here also</bnode>this is some<cnode />interrupted cdata</xmldefinition>
		"""
		tree = XMLParser().parse(xmltest)
		print(tree.getcdata(spacers = True))


	testcase1()
	testcase2()
	testcase3()
	testcase4()

#	import os
#	for (directory, subdirs, files) in os.walk("xmltest/"):
#		for filename in files:
#			fullfilename = directory + "/" + filename
#			if "invalid" in fullfilename:
#				continue
#			if "not-sa" in fullfilename:
#				continue
#			if not fullfilename.endswith(".xml"):
#				continue
#			print(fullfilename)
#			t = XMLParser().parsefile(fullfilename)
#			t.dump()
