#	pysuchsel - Create Suchsel word puzzles from Python
#	Copyright (C) 2019-2021 Johannes Bauer
#
#	This file is part of pysuchsel.
#
#	pysuchsel is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pysuchsel is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#	Johannes Bauer <JohannesBauer@gmx.de>

class XMLTools():
	@classmethod
	def getDoc(cls, element):
		if element.nodeType == element.DOCUMENT_NODE:
			doc = element
		else:
			doc = element.ownerDocument
		return doc

	@classmethod
	def createElement(cls, parent, name, attrs = None):
		new_element = cls.getDoc(parent).createElement(name)
		if attrs is not None:
			for (key, value) in attrs.items():
				new_element.setAttribute(key, value)
		parent.appendChild(new_element)
		return new_element

	@classmethod
	def createText(cls, parent, text):
		new_element = cls.getDoc(parent).createTextNode(text)
		parent.appendChild(new_element)
		return new_element

	@classmethod
	def getChild(cls, node, *path):
		if len(path) == 0:
			return node
		else:
			for child in node.childNodes:
				if (child.nodeType == child.ELEMENT_NODE) and (child.tagName == path[0]):
					return cls.getChild(child, *path[1:])
			else:
				raise Exception("No such child: %s has no %s" % (node, path[0]))
