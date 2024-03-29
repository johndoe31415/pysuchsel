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

class Tools():
	@classmethod
	def read_file(cls, filename, shuffle = False):
		words = [ ]
		with open(filename) as f:
			for line in f:
				line = line.strip(" \t\r\n")
				if line.startswith("#") or line == "":
					continue
				words.append(line.upper())
		if shuffle:
			random.shuffle(words)
		return words
