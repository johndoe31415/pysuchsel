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

import random
from SVGDocument import SVGDocument

class Suchsel():
	def __init__(self, width, height, placement):
		self._width = width
		self._height = height
		self._placement = placement
		self._grid = { }

	def _rulerange(self, origin_x, origin_y, rulename):
		(x, y) = (origin_x, origin_y)
		while True:
			yield (x, y)
			if rulename == "lr":
				x += 1
			elif rulename == "tb":
				y += 1
			elif rulename == "dbr":
				x += 1
				y += 1
			elif rulename == "dbl":
				x -= 1
				y += 1
			elif rulename == "dtr":
				x += 1
				y -= 1
			elif rulename == "dtl":
				x -= 1
				y -= 1
			else:
				raise NotImplementedError(rulename)

	def _attempt_place(self, word, must_be_contiguous = False):
		rule = self._placement.event()
		if rule in [ "lr", "rl" ]:
			req_width = len(word)
			req_height = 1
		elif rule in [ "tb", "bt" ]:
			req_width = 1
			req_height = len(word)
		elif rule in [ "dbr", "dtl", "dtr", "dbl" ]:
			req_width = len(word)
			req_height = len(word)
		else:
			raise NotImplementedError(rule)

		if rule in [ "rl", "bt" ]:
			word = "".join(reversed(word))
			if rule == "rl":
				rule = "lr"
			elif rule == "bt":
				rule = "tb"


		max_x = self._width - req_width
		max_y = self._height - req_height
		if (max_x < 0) or (max_y < 0):
			# Word does not fit with this rule, abort.
			return False

		src_x = random.randint(0, max_x)
		src_y = random.randint(0, max_y)

		if rule in [ "dtl", "dbl" ]:
			src_x += len(word) - 1
		if rule in [ "dtr", "dtl" ]:
			src_y += len(word) - 1

		contiguous_letters = 0
		for (want_place, (x, y)) in zip(word, self._rulerange(src_x, src_y, rule)):
			present = self._grid.get((x, y))
			if present == want_place:
				contiguous_letters += 1
			if (present is not None) and (present != want_place):
				# Letter already occupied
				return False

		if must_be_contiguous and (contiguous_letters == 0):
			return False

		# All letters fit!
		for (want_place, (x, y)) in zip(word, self._rulerange(src_x, src_y, rule)):
			self._grid[(x, y)] = want_place
		return True

	def place(self, word, contiguous = False):
		# First try contiguous placement
		if contiguous and (len(self._grid) > 0):
			for i in range(500):
				if self._attempt_place(word, must_be_contiguous = True):
					return
		for i in range(500):
			if self._attempt_place(word):
				return
		print("Warning: Could not place word '%s'." % (word))

	def fill(self, filler):
		for y in range(self._height):
			for x in range(self._width):
				pos = (x, y)
				if pos not in self._grid:
					self._grid[pos] = filler.get()

	def dump(self):
		print("+-" + "-" * (2 * self._width) + "-+")
		for y in range(self._height):
			line = [ ]
			for x in range(self._width):
				letter = self._grid.get((x, y), " ")
				line.append(letter)
			print("| " + (" ".join(line)) + "  |")
		print("+-" + ("-" * (2 * self._width)) + "-+")

	def write_svg(self, output_filename):
		svg = SVGDocument()
		size = 20
		for y in range(self._height):
			for x in range(self._width):
				pos = (x, y)
				letter = self._grid.get(pos)
				if letter is None:
					continue
				svg.rect(size * x, size * y, size, size)
				svg.textregion(size * x, size * y + 4, size, size, letter, halign = "center")

		svg.autosize()
		with open(output_filename, "w") as f:
			svg.write(f)


