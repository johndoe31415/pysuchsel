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
from .CryptoPuzzle import CryptoPuzzle
from .Tools import Tools

class ActionCrypto(BaseAction):
	def run(self):
		if len(self._args.alphabet) == 0:
			raise Exception("No alphabet given on command line.")
		plain_lines = Tools.read_file(self._args.infile)
		cp = CryptoPuzzle(plain_lines = plain_lines, alphabet_names = self._args.alphabet, reveal_letters = self._args.reveal, crypto_solution = self._args.solution_word)
		if self._args.verbose >= 1:
			cp.dump()
		cp.write_svg(self._args.outfile)
