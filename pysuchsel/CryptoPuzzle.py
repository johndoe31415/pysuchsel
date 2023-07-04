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
import json
import pkgutil
from pysvgedit import SVGDocument, SVGGroup, SVGRect, Vector2D, Convenience as svgc
from .Exceptions import PuzzleNotSolvableException

class CryptoPuzzle():
	def __init__(self, plain_lines, alphabet_names, reveal_letters, crypto_solution = None):
		self._plain_lines = plain_lines
		self._crypto_solution = crypto_solution
		self._reveal_letters = set(reveal_letters)
		crypto_alphabet_names = json.loads(pkgutil.get_data("pysuchsel", "definitions.json"))["crypto"]

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


	def write_svg(self, output_filename):
		svg = SVGDocument.new()
		cipher_layer = svg.add(SVGGroup.new(is_layer = True))
		cipher_layer.label = "Ciphertext"

		initial_layer = svg.add(SVGGroup.new(is_layer = True))
		initial_layer.label = "Initially given"

		inference_layer = svg.add(SVGGroup.new(is_layer = True))
		inference_layer.label = "Initially inferrable"
		inference_layer.style.hide()

		solution_layer = svg.add(SVGGroup.new(is_layer = True))
		solution_layer.label = "Solution"
		solution_layer.style.hide()

		if self._crypto_solution is not None:
			final_ciphertext = svg.add(SVGGroup.new(is_layer = True))
			final_ciphertext.label = "Final ciphertext"

			final_plaintext = svg.add(SVGGroup.new(is_layer = True))
			final_plaintext.label = "Final solution"
			final_plaintext.style.hide()


		size = 20
		yoffset = 4
		line_height = 2 * size + 10

		revealed_letters = set()
		for (y, line) in enumerate(self._plain_lines):
			for (x, plain_letter) in enumerate(line):
				if plain_letter == " ":
					continue
				cipher_letter = self._key[plain_letter]
				cipher_layer.add(SVGRect.new(pos = Vector2D(size * x, line_height * y), extents = Vector2D(size, size)))
				cipher_layer.add(SVGRect.new(pos = Vector2D(size * x, line_height * y + size), extents = Vector2D(size, size)))
				svgc.text(cipher_layer, pos = Vector2D(size * x, line_height * y + yoffset), extents = Vector2D(size, size - yoffset), text = cipher_letter, halign = "center")
				svgc.text(solution_layer, pos = Vector2D(size * x, line_height * y + size + yoffset), extents = Vector2D(size, size - yoffset), text = plain_letter, halign = "center", attribute = "bold")
				if plain_letter in self._reveal_letters:
					svgc.text(inference_layer, pos = Vector2D(size * x, line_height * y + size + yoffset), extents = Vector2D(size, size - yoffset), text = plain_letter, halign = "center")
					if plain_letter not in revealed_letters:
						svgc.text(initial_layer, pos = Vector2D(size * x, line_height * y + size + yoffset), extents = Vector2D(size, size - yoffset), text = plain_letter, halign = "center")
						revealed_letters.add(plain_letter)

		y += 1
		half_height = size // 2
		if self._crypto_solution is not None:
			for (x, plain_letter) in enumerate(self._crypto_solution):
				cipher_letter = self._key[plain_letter]
				rect = final_ciphertext.add(SVGRect.new(pos = Vector2D(size * x, line_height * y + half_height), extents = Vector2D(size, size)))
				rect.style["fill"] = "#f1c40f"

				final_ciphertext.add(SVGRect.new(pos = Vector2D(size * x, line_height * y + size + half_height), extents = Vector2D(size, size)))
				svgc.text(final_ciphertext, pos = Vector2D(size * x, line_height * y + half_height + yoffset), extents = Vector2D(size, size - yoffset), text = cipher_letter, halign = "center")

				svgc.text(final_plaintext, pos = Vector2D(size * x, line_height * y + size + half_height + yoffset), extents = Vector2D(size, size - yoffset), text = plain_letter, halign = "center", attribute = "bold")

		svgc.autosize(svg)
		svg.writefile(output_filename)

if __name__ == "__main__":
	cp = CryptoPuzzle([ "THIS IS A", "SUPER SECRET", "MESSAGE" ], [ "alpha" ], "ERNSTL", crypto_solution = "TATA")
	cp.dump()
	cp.write_svg("x.svg")
