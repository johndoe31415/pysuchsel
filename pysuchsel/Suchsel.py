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

import random
from pysvgedit import SVGDocument, SVGGroup, SVGRect, Vector2D, Convenience as svgc

class VoidPlaceholder():
	def __eq__(self, other):
		return other.__class__ == self.__class__

	def __neq__(self, other):
		return not (self == other)

	def __str__(self):
		return "."

class ArrowMarker():
	def __init__(self, marking, direction):
		self._marking = marking
		self._direction = direction

	@property
	def marking(self):
		return self._marking

	def __str__(self):
		return {
			"left":		"<",
			"right":	">",
			"down":		"v",
		}.get(self._direction, "?")

class Suchsel():
	def __init__(self, width, height, placement, attempts, is_crossword = False):
		self._width = width
		self._height = height
		self._placement = placement
		self._attempts = attempts
		self._is_crossword = is_crossword
		self._grid = { }
		self._fillers_at = set()

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

	def _adjacent_fields(self, x, y, rulename):
		if rulename in [ "tb", "bt" ]:
			yield (x - 1, y)
			yield (x + 1, y)
		elif rulename in [ "lr", "rl" ]:
			yield (x, y - 1)
			yield (x, y + 1)
		else:
			raise NotImplementedError(rulename)

	def _find_rule(self, word, crossword_marker = None):
		rule = self._placement.event()
		if crossword_marker is not None:
			direction = {
				"lr":	"right",
				"rl":	"left",
				"tb":	"down",
				"bt":	"up",
				"dbr":	"down-right",
				"dbl":	"down-left",
				"dtr":	"up-right",
				"dtl":	"up-left",
			}[rule]
			arrow_marker = ArrowMarker(marking = crossword_marker, direction = direction)
			word = [ arrow_marker ] + list(word) + [ VoidPlaceholder() ]

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
			word = list(reversed(word))
			if rule == "rl":
				rule = "lr"
			elif rule == "bt":
				rule = "tb"
		return (word, rule, req_width, req_height)

	def _attempt_place(self, word, must_be_contiguous = False, crossword_marker = None):
		(word, rule, req_width, req_height) = self._find_rule(word, crossword_marker = crossword_marker)

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
			if (present == want_place) and isinstance(present, str):
				# We count overlapping letters, but not overlapping
				# VoidPlacerholders
				contiguous_letters += 1
			if (present is not None) and (present != want_place):
				# Letter already occupied with different letter than we would
				# like there
				return False

			if (present is None) and (crossword_marker is not None):
				# Field is empty, check adjacent fields for emptyness if this
				# is a crossword
				for (adjx, adjy) in self._adjacent_fields(x, y, rule):
					adjacent_content = self._grid.get((adjx, adjy))
					if (adjacent_content is not None) and not isinstance(adjacent_content, VoidPlaceholder):
						# There's a letter or arrowfield in there, that's
						# forbidden
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
			for i in range(self._attempts):
				if self._attempt_place(word, must_be_contiguous = True):
					return True
		for i in range(self._attempts):
			if self._attempt_place(word):
				return True
		return False

	def place_crossword(self, word, crossword_marker):
		contiguous = (len(self._grid) > 0)
		for i in range(self._attempts):
			if self._attempt_place(word, must_be_contiguous = contiguous, crossword_marker = crossword_marker):
				return True
		return False

	def fill(self, filler):
		for y in range(self._height):
			for x in range(self._width):
				pos = (x, y)
				if pos not in self._grid:
					self._grid[pos] = filler.get()
					self._fillers_at.add(pos)

	def dump(self):
		print("+-" + "-" * (2 * self._width) + "-+")
		for y in range(self._height):
			line = [ ]
			for x in range(self._width):
				letter = self._grid.get((x, y), " ")
				line.append(str(letter))
			print("| " + (" ".join(line)) + "  |")
		print("+-" + ("-" * (2 * self._width)) + "-+")

	def write_svg(self, output_filename):
		svg = SVGDocument.new()

		grid_layer = svg.add(SVGGroup.new(is_layer = True))
		grid_layer.label = "Grid"
		if self._is_crossword:
			solution_layer = svg.add(SVGGroup.new(is_layer = True))
			solution_layer.label = "Solution"
		else:
			filler_layer = svg.add(SVGGroup.new(is_layer = True))
			filler_layer.label = "Filler letters"
			solution_layer = svg.add(SVGGroup.new(is_layer = True))
			solution_layer.label = "Solution normal"
			solution_highlight_layer = svg.add(SVGGroup.new(is_layer = True))
			solution_highlight_layer.label = "Solution highlighted"

		size = 20
		yoffset = 4
		for y in range(self._height):
			for x in range(self._width):
				pos = (x, y)
				letter = self._grid.get(pos)
				is_filler = pos in self._fillers_at
				if isinstance(letter, str):
					grid_layer.add(SVGRect.new(pos = size * Vector2D(x, y), extents = Vector2D(size, size)))

					if is_filler:
						# Random filler letter
						svgc.text(filler_layer, pos = Vector2D(size * x, size * y + yoffset), extents = Vector2D(size, size - yoffset), text = letter, halign = "center")

					if not is_filler:
						# Solution letter
						svgc.text(solution_layer, pos = Vector2D(size * x, size * y + yoffset), extents = Vector2D(size, size - yoffset), text = letter, halign = "center")

						if not self._is_crossword:
							# Additionally, put in bold and highlight in the solution highlight layer
							rect = solution_highlight_layer.add(SVGRect.new(pos = size * Vector2D(x, y), extents = Vector2D(size, size)))
							rect.style["fill"] = "#f1c40f"
							svgc.text(solution_highlight_layer, pos = Vector2D(size * x, size * y + yoffset), extents = Vector2D(size, size - yoffset), text = letter, halign = "center", attribute = "bold")
				elif isinstance(letter, ArrowMarker):
					rect = grid_layer.add(SVGRect.new(pos = size * Vector2D(x, y), extents = Vector2D(size, size)))
					rect.style["stroke"] = "#3498db"
					svgc.text(grid_layer, pos = Vector2D(size * x, size * y + yoffset), extents = Vector2D(size, size - yoffset), text = str(letter.marking), halign = "center")

		svgc.autosize(svg)
		svg.writefile(output_filename)
