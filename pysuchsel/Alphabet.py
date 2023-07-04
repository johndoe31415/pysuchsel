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
from .RandomDist import RandomDist

class Alphabet():
	def __init__(self, language, uniform_distribution = False):
		distributions = json.loads(pkgutil.get_data("pysuchsel", "definitions.json"))["distributions"]
		distribution = distributions[language]

		if uniform_distribution:
			self._dist = RandomDist({ letter: 1 for letter in distribution.keys() })
		else:
			self._dist = RandomDist({ letter: round(10000 * probability) for (letter, probability) in distribution.items() })

	def get(self):
		return self._dist.event()
