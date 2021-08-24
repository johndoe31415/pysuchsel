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

import json
from BaseAction import BaseAction
from SVGDocument import SVGDocument

class ActionFontTest(BaseAction):
	def run(self):
		svg = SVGDocument()
		with open("definitions.json") as f:
			crypto = json.load(f)["crypto"]
		size = 20
		for (y, (name, alphabets)) in enumerate(crypto.items()):
			svg.textregion(-100, size * y, 90, size, name, halign = "right")
			alphabet = "".join(alphabets)
			if self._args.sort:
				alphabet = sorted(set(alphabet))
			for (x, letter) in enumerate(alphabet):
				svg.rect(size * x, size * y, size, size)
				svg.textregion(size * x, size * y + 4, size, size, letter, halign = "center")
		svg.autosize()
		svg.writefile(self._args.outfile)
