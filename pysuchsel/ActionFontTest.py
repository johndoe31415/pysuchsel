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

import json
import pkgutil
from pysvgedit import SVGDocument, SVGRect, Vector2D, Convenience as svgc
from .BaseAction import BaseAction

class ActionFontTest(BaseAction):
	def run(self):
		svg = SVGDocument.new()
		crypto = json.loads(pkgutil.get_data("pysuchsel", "definitions.json"))["crypto"]
		size = 20
		for (y, (name, alphabets)) in enumerate(crypto.items()):
			svgc.text(svg, text = name, x = -100, y = size * y, width = 90, height = size, halign = "right")
			alphabet = "".join(alphabets)
			if self._args.sort:
				alphabet = sorted(set(alphabet))

			yshift = 4
			for (x, letter) in enumerate(alphabet):
				svg.add(SVGRect.new(pos = Vector2D(size * x, size * y), extents = Vector2D(size, size)))
				svgc.text(svg, text = letter, x = size * x, y = size * y + yshift, width = size, height = size - yshift, halign = "center")
		svgc.autosize(svg)
		svg.writefile(self._args.outfile)
