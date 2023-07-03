#	pysuchsel - Create Suchsel word puzzles from Python
#	Copyright (C) 2019-2023 Johannes Bauer
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

import xml.dom.minidom
from .XMLTools import XMLTools

class SVGDocument():
	def __init__(self, **kwargs):
		self._counters = { }
		self._root = xml.dom.minidom.Document()
		self._svg = XMLTools.createElement(self._root, "svg", {
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
		self._dimensions = { }

	@property
	def width(self):
		return float(self._svg.getAttribute("width"))

	@width.setter
	def width(self, value):
		self._svg.setAttribute("width", str(value))

	@property
	def height(self):
		return float(self._svg.getAttribute("height"))

	@height.setter
	def height(self, value):
		self._svg.setAttribute("height", str(value))

	def _check_kwargs(self, kwargs, allowed_kwargs):
		excess_args = set(kwargs) - allowed_kwargs
		if len(excess_args) > 0:
			raise ValueError("Unknown kwarg supplied: %s" % (", ".join(sorted(excess_args))))

	def _getnewid(self, start):
		idname = start + str(self._counters.get(start, 0))
		self._counters[start] = self._counters.get(start, 0) + 1
		return idname

	def _updatedim(self, x, y, width, height):
		if "minx" in self._dimensions:
			self._dimensions["minx"] = min(self._dimensions["minx"], x)
		else:
			self._dimensions["minx"] = x
		if "maxx" in self._dimensions:
			self._dimensions["maxx"] = max(self._dimensions["maxx"], x + width)
		else:
			self._dimensions["maxx"] = x + width
		if "miny" in self._dimensions:
			self._dimensions["miny"] = min(self._dimensions["miny"], y)
		else:
			self._dimensions["miny"] = y
		if "maxy" in self._dimensions:
			self._dimensions["maxy"] = max(self._dimensions["maxy"], y + height)
		else:
			self._dimensions["maxy"] = y + height

	def rect(self, x, y, width, height, **kwargs):
		self._check_kwargs(kwargs, set([ "fill", "fillopacity", "fillcolor", "strokecolor", "stokewidth", "parent" ]))
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
		node = XMLTools.createElement(kwargs.get("parent", self._svg), "rect", attrs)
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
		self._check_kwargs(kwargs, set([ "font", "fontsize", "font_weight", "color", "parent" ]))
		attrs = {
			"id": 		self._getnewid("text"),
			"x":		str(x),
			"y":		str(y),
			"style":	SVGDocument._encodefontstyle(kwargs),
		}
		node = XMLTools.createElement(kwargs.get("parent", self._svg), "text", attrs)
		tspan = XMLTools.createElement(node, "tspan")
		XMLTools.createText(tspan, text)
		return node

	def textregion(self, x, y, width, height, text, **kwargs):
		self._check_kwargs(kwargs, set([ "font", "fontsize", "font_weight", "color", "parent", "halign" ]))
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
		flowRoot = XMLTools.createElement(kwargs.get("parent", self._svg), "flowRoot", attrs)
		flowRegion = XMLTools.createElement(flowRoot, "flowRegion", { "id": self._getnewid("flowRegion") })
		self.rect(x, y, width, height, parent = flowRegion)

		flowPara = XMLTools.createElement(flowRoot, "flowPara", { "id": self._getnewid("flowPara") })
		XMLTools.createText(flowPara, text)
		return flowRoot

	def autosize(self):
		def _translate(element):
			element.setAttribute("x", str(float(element.getAttribute("x")) - self._dimensions["minx"]))
			element.setAttribute("y", str(float(element.getAttribute("y")) - self._dimensions["miny"]))

		for element in self._svg.childNodes:
			if (element.nodeType == element.ELEMENT_NODE) and (element.tagName in [ "rect", "text", "flowRoot" ]):
				_translate(element)
				if element.tagName == "flowRoot":
					_translate(XMLTools.getChild(element, "flowRegion", "rect"))
		self.width = self._dimensions["maxx"] - self._dimensions["minx"]
		self.height = self._dimensions["maxy"] - self._dimensions["miny"]
		self._dimensions = {
			"minx":		0,
			"miny":		0,
			"maxx":		self.width,
			"maxy":		self.height,
		}

	def writefile(self, filename):
		with open(filename, "w") as f:
			f.write(self._root.toprettyxml())

if __name__ == "__main__":
	svg = SVGDocument()
	svg.rect(0, 0, 10, 15)
	svg.rect(-100, -100, 10, 15)
	svg.rect(50, 100, 10, 15)
	svg.text(0, 0, "0, 0")
	svg.textregion(20, 20, 50, 50, "foo bar")
	svg.autosize()
	svg.writefile("x.svg")

