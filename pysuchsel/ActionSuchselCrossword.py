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
from .RandomDist import RandomDist
from .Suchsel import Suchsel
from .Tools import Tools
from .Alphabet import Alphabet

class ActionSuchselCrossword(BaseAction):
	def _get_placement_rule(self):
		if len(self._args.placement) == 0:
			plcrule = RandomDist({
				"lr":	1,
				"tb":	1,
			})
		else:
			plcrule = RandomDist({ name: 1 for name in self._args.placement })
		return plcrule

	def _attempt_placement(self, plcrule):
		self._unplaced_words = [ ]
		self._placed_words = { }
		next_id = 1
		self._suchsel = Suchsel(self._args.width, self._args.height, plcrule, attempts = self._args.place_attempts, is_crossword = (self._cmd == "crossword"))
		for word in self._words:
			if self._cmd == "suchsel":
				placed = self._suchsel.place(word, contiguous = self._args.contiguous)
			elif self._cmd == "crossword":
				placed = self._suchsel.place_crossword(word, crossword_marker = next_id)
				if placed:
					self._placed_words[next_id] = word
					next_id += 1
			else:
				raise NotImplementedError(self._args.mode)
			if not placed:
				self._unplaced_words.append(word)
		return len(self._unplaced_words) == 0

	def run(self):
		self._words = Tools.read_file(self._args.infile, shuffle = True)
		plcrule = self._get_placement_rule()

		for creation_attempt in range(self._args.creation_attempts):
			if self._attempt_placement(plcrule):
				break

		for unplaced_word in self._unplaced_words:
			print("Warning: could not place word \"%s\"." % (unplaced_word))

		if self._args.verbose >= 1:
			self._suchsel.dump()

		if self._cmd == "suchsel":
			filler = Alphabet(self._args.fill_rule, uniform_distribution = self._args.uniform_distribution)
			self._suchsel.fill(filler)
			if self._args.verbose >= 2:
				self._suchsel.dump()

		self._suchsel.write_svg(self._args.outfile)

		if self._cmd == "crossword":
			for (word_id, word) in sorted(self._placed_words.items()):
				print("%2d: %s" % (word_id, word))
