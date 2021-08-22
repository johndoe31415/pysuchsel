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

import random
import collections
from SVGDocument import SVGDocument

class PuzzleNotSolvableException(Exception): pass

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

	def write_svg(self, output_filename, solution = False):
		svg = SVGDocument()
		size = 20
		for (y, (word, letter_index)) in enumerate(self._solution):

			x_begin = -letter_index - 1
			svg.rect(size * x_begin, size * y, size, size, fillcolor = "3498db")
			svg.textregion(size * x_begin, size * y + 4, size, size, str(y + 1), halign = "center")

			for (x_raw, letter) in enumerate(word):
				x = x_raw - letter_index

				if x == 0:
					svg.rect(size * x, size * y, size, size, fillcolor = "f1c40f")
				else:
					svg.rect(size * x, size * y, size, size)

				if solution:
					svg.textregion(size * x, size * y + 4, size, size, letter, halign = "center", font_weight = "bold" if (x == 0) else "normal")

		svg.autosize()
		with open(output_filename, "w") as f:
			svg.write(f)


if __name__ == "__main__":
	swp = SolutionWordPuzzle([ "PADDELFISCH", "ITZIBITZI", "NUDELSALAT", "SOMMER", "SONNE", "HEITERKEIT" ], "MILK")
	print(swp.find_solution())
