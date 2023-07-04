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
from .Exceptions import PuzzleNotSolvableException

class SolutionWordPuzzle():
	def __init__(self, word_list, solution_word):
		self._word_list = [ word.upper() for word in word_list ]
		self._solution_word = solution_word.upper()
		self._plausibilize()
		self._solution = None

	def _plausibilize(self):
		available_letters = set("".join(word for word in self._word_list))
		necessary_letters = set(self._solution_word)
		unavailable_letters = necessary_letters - available_letters
		if len(unavailable_letters) > 0:
			raise PuzzleNotSolvableException("Puzzle not solvable: letter(s) %s not contained." % (", ".join(sorted(unavailable_letters))))

	def find_solution(self):
		remaining_words = list(self._word_list)
		random.shuffle(remaining_words)
		solution_words = [ ]
		for letter in self._solution_word:
			for (index, candidate) in enumerate(remaining_words):
				if letter in candidate:
					break
			else:
				raise PuzzleNotSolvableException("Could not find word for letter '%s'." % (letter))
			remaining_words.pop(index)
			solution_words.append(candidate)

		solution = [ ]
		for (solution_word, solution_letter) in zip(solution_words, self._solution_word):
			occurrence_indices = set()
			for (index, letter) in enumerate(solution_word):
				if letter == solution_letter:
					occurrence_indices.add(index)
			chosen_index = random.choice(list(occurrence_indices))
			solution.append((solution_word, chosen_index))
		self._solution = solution
		return solution

	def write_svg(self, output_filename):
		svg = SVGDocument.new()
		grid_layer = svg.add(SVGGroup.new(is_layer = True))
		grid_layer.label = "Grid"
		solution_layer = svg.add(SVGGroup.new(is_layer = True))
		solution_layer.label = "Solution"

		size = 20
		yoffset = 4
		for (y, (word, letter_index)) in enumerate(self._solution):

			x_begin = -letter_index - 1
			rect = grid_layer.add(SVGRect.new(pos = size * Vector2D(x_begin, y), extents = Vector2D(size, size)))
			rect.style["fill"] = "#3498db"
			svgc.text(grid_layer, pos = Vector2D(size * x_begin, size * y + yoffset), extents = Vector2D(size, size - yoffset), text = str(y + 1), halign = "center")

			for (x_raw, letter) in enumerate(word):
				x = x_raw - letter_index

				if x == 0:
					rect = grid_layer.add(SVGRect.new(pos = size * Vector2D(x, y), extents = Vector2D(size, size)))
					rect.style["fill"] = "#f1c40f"
				else:
					grid_layer.add(SVGRect.new(pos = size * Vector2D(x, y), extents = Vector2D(size, size)))

				svgc.text(solution_layer, pos = Vector2D(size * x, size * y + yoffset), extents = Vector2D(size, size - yoffset), text = letter, halign = "center", attribute = "bold" if (x == 0) else "none")

		svgc.autosize(svg)
		svg.writefile(output_filename)


if __name__ == "__main__":
	swp = SolutionWordPuzzle([ "PADDELFISCH", "ITZIBITZI", "NUDELSALAT", "SOMMER", "SONNE", "HEITERKEIT" ], "MILK")
	print(swp.find_solution())
