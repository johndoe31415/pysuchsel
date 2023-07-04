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

from .BaseAction import BaseAction
from .SolutionWordPuzzle import SolutionWordPuzzle, PuzzleNotSolvableException
from .Tools import Tools

class ActionSolutionWord(BaseAction):
	def run(self):
		word_list = Tools.read_file(self._args.infile)
		swp = SolutionWordPuzzle(word_list = word_list, solution_word = self._args.solword)
		solution = None
		for i in range(self._args.place_attempts):
			try:
				solution = swp.find_solution()
			except PuzzleNotSolvableException:
				continue
		if solution is None:
			print("Could not find a solution for this word puzzle, giving up.")
			return 1

		if self._args.verbose >= 1:
			indent = max(index for (word, index) in solution)
			print("   " + (" " * indent) + "#")
			for (word_no, (word, letter_index)) in enumerate(solution, 1):
				word_indent = " " * (indent - letter_index)
				print("%2d %s%s" % (word_no, word_indent, word))
		swp.write_svg(self._args.outfile)
		return 0
