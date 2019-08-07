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

import json
import string
from RandomDist import RandomDist

class Alphabet():
	_ALPHABETS = {
		"az":		string.ascii_uppercase,
		"az-de":	string.ascii_uppercase + "ÄÖÜß",
	}

	def __init__(self, fill_rule, fill_dist):
		self._alphabet = self._ALPHABETS[fill_rule]
		if fill_dist == "uniform":
			self._dist = RandomDist({ letter: 1 for letter in self._alphabet })
		else:
			with open("distributions.json") as f:
				distributions = json.load(f)
			distribution = distributions[fill_dist]
			self._dist = RandomDist({ letter: round(10000 * distribution[letter]) for letter in self._alphabet })

	def get(self):
		return self._dist.event()

if __name__ == "__main__":
	alpha = Alphabet("az-de", "natlang-de")
	for i in range(20):
		print(alpha.get())
