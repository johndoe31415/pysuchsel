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
import json
from SVGDocument import SVGDocument

class CryptoPuzzle():
	def __init__(self, crypto_words, alphabets, revealed_letters, crypto_solution = None):
		self._crypto_words = crypto_words
		self._crypto_solution = crypto_solution
		self._revealed_letters = set(revealed_letters)
		with open("definitions.json") as f:
			crypto_alphabets = json.load(f)["crypto"]

		crypto_chars = set()
		for alphabet in alphabets:
			crypto_chars |= set("".join(crypto_alphabets[alphabet]))
		crypto_chars = list(crypto_chars)
		random.shuffle(crypto_chars)

		plain_chars = set("".join(word for word in self._crypto_words))
		if " " in plain_chars:
			plain_chars.remove(" ")
		self._key = { plain_char: crypto_char for (plain_char, crypto_char) in zip(plain_chars, crypto_chars) }

		if self._crypto_solution is not None:
			uncovered_chars = set(crypto_solution) - plain_chars
			if len(uncovered_chars) > 0:
				raise Exception("Cannot produce solution word: %s missing" % (", ".join(sorted(uncovered_chars))))

	def dump(self):
		for line in self._crypto_words:
			show = [ ]
			for letter in line:
				if (letter == " ") or (letter in self._revealed_letters):
					show.append(letter)
				else:
					show.append("_")
			print("".join(show))


	def write_svg(self, output_filename, solution = False):
		svg = SVGDocument()
		size = 20
		line_height = 2 * size + 10

		revealed_letters = set()
		for (y, line) in enumerate(self._crypto_words):
			for (x, plain_letter) in enumerate(line):
				if plain_letter == " ":
					continue
				cipher_letter = self._key[plain_letter]
				svg.rect(size * x, line_height * y, size, size)
				svg.rect(size * x, line_height * y + size, size, size)
				svg.textregion(size * x, line_height * y + 4, size, size, cipher_letter, halign = "center")
				if solution:
					svg.textregion(size * x, line_height * y + size + 4, size, size, plain_letter, halign = "center", font_weight = "bold")
				elif (plain_letter in self._revealed_letters) and (plain_letter not in revealed_letters):
					svg.textregion(size * x, line_height * y + size + 4, size, size, plain_letter, halign = "center")
					revealed_letters.add(plain_letter)

		svg.autosize()
		svg.writefile(output_filename)


if __name__ == "__main__":
	cp = CryptoPuzzle([ "THIS IS A", "SUPER SECRET", "MESSAGE" ], [ "alpha" ], "ERNSTL", crypto_solution = "TATA")
	cp.dump()
	cp.write_svg("x.svg")
