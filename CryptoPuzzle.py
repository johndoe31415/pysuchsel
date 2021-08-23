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
from Exceptions import PuzzleNotSolvableException

class CryptoPuzzle():
	def __init__(self, plain_lines, alphabet_names, reveal_letters, crypto_solution = None):
		self._plain_lines = plain_lines
		self._crypto_solution = crypto_solution
		self._reveal_letters = set(reveal_letters)
		with open("definitions.json") as f:
			crypto_alphabet_names = json.load(f)["crypto"]

		crypto_chars = set()
		for alphabet in alphabet_names:
			crypto_chars |= set("".join(crypto_alphabet_names[alphabet]))
		crypto_chars = list(crypto_chars)
		random.shuffle(crypto_chars)

		plain_chars = set("".join(word for word in self._plain_lines))
		if " " in plain_chars:
			plain_chars.remove(" ")
		if len(plain_chars) > len(crypto_chars):
			raise PuzzleNotSolvableException("Alphabet too small, cannot generate puzzle.")
		self._key = { plain_char: crypto_char for (plain_char, crypto_char) in zip(plain_chars, crypto_chars) }

		if self._crypto_solution is not None:
			uncovered_chars = set(crypto_solution) - plain_chars
			if len(uncovered_chars) > 0:
				raise PuzzleNotSolvableException("Cannot produce solution word: %s missing" % (", ".join(sorted(uncovered_chars))))

	def dump(self):
		for line in self._plain_lines:
			show = [ ]
			for letter in line:
				if (letter == " ") or (letter in self._reveal_letters):
					show.append(letter)
				else:
					show.append("_")
			print("".join(show))


	def write_svg(self, output_filename, solution = False):
		svg = SVGDocument()
		size = 20
		line_height = 2 * size + 10

		revealed_letters = set()
		for (y, line) in enumerate(self._plain_lines):
			for (x, plain_letter) in enumerate(line):
				if plain_letter == " ":
					continue
				cipher_letter = self._key[plain_letter]
				svg.rect(size * x, line_height * y, size, size)
				svg.rect(size * x, line_height * y + size, size, size)
				svg.textregion(size * x, line_height * y + 4, size, size, cipher_letter, halign = "center")
				if solution:
					svg.textregion(size * x, line_height * y + size + 4, size, size, plain_letter, halign = "center", font_weight = "bold")
				elif (plain_letter in self._reveal_letters) and (plain_letter not in revealed_letters):
					svg.textregion(size * x, line_height * y + size + 4, size, size, plain_letter, halign = "center")
					revealed_letters.add(plain_letter)

		y += 1
		half_height = size // 2
		if self._crypto_solution is not None:
			for (x, plain_letter) in enumerate(self._crypto_solution):
				cipher_letter = self._key[plain_letter]
				svg.rect(size * x, line_height * y + half_height, size, size, fillcolor = "f1c40f")
				svg.rect(size * x, line_height * y + size + half_height, size, size)
				svg.textregion(size * x, line_height * y + half_height + 4, size, size, cipher_letter, halign = "center")
				if solution:
					svg.textregion(size * x, line_height * y + size + half_height + 4, size, size, plain_letter, halign = "center", font_weight = "bold")


		svg.autosize()
		svg.writefile(output_filename)


if __name__ == "__main__":
	cp = CryptoPuzzle([ "THIS IS A", "SUPER SECRET", "MESSAGE" ], [ "alpha" ], "ERNSTL", crypto_solution = "TATA")
	cp.dump()
	cp.write_svg("x.svg")
