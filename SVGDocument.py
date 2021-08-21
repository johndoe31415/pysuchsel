#	pysuchsel - Create Suchsel word puzzles from Python
#	Copyright (C) 2019-2019 Johannes Bauer
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

import io

from XMLParser import XMLNode

class SVGDocument():
	def __init__(self, **kwargs):
		self._counters = { }
		self._xml = XMLNode("svg", {
			"xmlns":			"http://www.w3.org/2000/svg",
			"xmlns:svg":		"http://www.w3.org/2000/svg",
			"xmlns:rdf":		"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
			"xmlns:cc":			"http://creativecommons.org/ns#",
			"xmlns:dc":			"http://purl.org/dc/elements/1.1/",
			"id":				self._getnewid("svg"),
			"version":			"1.1",
			"width":			str(kwargs.get("width", 100)),
			"height":			str(kwargs.get("height", 100)),
		})
		self._ctr = 0
		self._dimensions = {
			"minx":		0,
			"maxx":		0,
			"miny":		0,
			"maxy":		0,
		}

	def setwidth(self, width):
		self._xml["width"] = str(width)

	def setheight(self, height):
		self._xml["height"] = str(height)

	def getwidth(self):
		return float(self._xml["width"])

	def getheight(self):
		return float(self._xml["height"])

	def _getnewid(self, start):
		idname = start + str(self._counters.get(start, 0))
		self._counters[start] = self._counters.get(start, 0) + 1
		return idname

	def _updatedim(self, x, y, width, height):
		self._dimensions["minx"] = min(self._dimensions["minx"], x)
		self._dimensions["maxx"] = max(self._dimensions["maxx"], x + width)
		self._dimensions["miny"] = min(self._dimensions["miny"], y)
		self._dimensions["maxy"] = max(self._dimensions["maxy"], y + height)

	def rect(self, x, y, width, height, **kwargs):
		self._updatedim(x, y, width, height)
		style = {
			"fill":				"#" + kwargs.get("fillcolor", "000000"),
			"fill-opacity":		str(kwargs.get("fillopacity", "0" if "fillcolor" not in kwargs else "1")),
			"stroke":			"#" + kwargs.get("strokecolor", "000000"),
			"stroke-width":		str(kwargs.get("strokewidth", "1")),
		}
		stylestr = SVGDocument._encodestyle(style)
		attrs = {
			"id": 		self._getnewid("rect"),
			"x":		str(x),
			"y":		str(y),
			"width":	str(width),
			"height":	str(height),
			"style":	stylestr,
		}
		node = kwargs.get("parent", self._xml).addchild(XMLNode("rect", attrs))
		return node

	def _encodestyle(styledict):
		return ";".join([ x + ":" + y for (x, y) in styledict.items() ])

	def _encodefontstyle(fontkwargs):
		styledict = {
			"font-family":		fontkwargs.get("font", "Nimbus Sans L"),
			"font-size":		str(fontkwargs.get("fontsize", 12)) + "px",
			"font-style":		"normal",
			"font-variant":		"normal",
			"font-weight":		fontkwargs.get("font_weight", "normal"),
			"font-stretch":		"normal",
			"fill":				"#" + fontkwargs.get("color", "000000"),
		}
		return SVGDocument._encodestyle(styledict)

	def text(self, x, y, text, **kwargs):
		attrs = {
			"id": 		self._getnewid("text"),
			"x":		str(x),
			"y":		str(y),
			"style":	SVGDocument._encodefontstyle(kwargs),
		}
		node = kwargs.get("parent", self._xml).addchild(XMLNode("text", attrs))
		tspan = node.addchild(XMLNode("tspan"))
		tspan.appendcdata(text)
		return node

	def textregion(self, x, y, width, height, text, **kwargs):
		attrs = {
			"id": 		self._getnewid("flowRoot"),
			"x":		str(x),
			"y":		str(y),
			"style":	SVGDocument._encodefontstyle(kwargs),
		}
		if "halign" in kwargs:
			attrs.update({
				"text-anchor":	"middle",
				"text-align":	kwargs["halign"],
			})
		node = kwargs.get("parent", self._xml).addchild(XMLNode("flowRoot", attrs))

		region = node.addchild(XMLNode("flowRegion", { "id": self._getnewid("flowRegion") }))
		self.rect(x, y, width, height, parent = region)

		para = node.addchild(XMLNode("flowPara", { "id": self._getnewid("flowPara") }))
		para.appendcdata(text)

		return node

	def autosize(self):
		self._xml["width"] = str(self._dimensions["maxx"] - self._dimensions["minx"])
		self._xml["height"] = str(self._dimensions["maxy"] - self._dimensions["miny"])

	def write(self, f):
		self._xml.write(f)

	def getxmltext(self):
		f = io.StringIO()
		self.write(f)
		return f.getvalue()

if __name__ == "__main__":
	svg = SVGDocument()
	svg.rect(0, 0, 10, 15)
	svg.autosize()
	svg.write(open("x.svg", "w"))

