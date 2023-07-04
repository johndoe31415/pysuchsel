#!/usr/bin/env python3
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

import sys
import pysuchsel
from .MultiCommand import MultiCommand
from .ActionSuchselCrossword import ActionSuchselCrossword
from .ActionSolutionWord import ActionSolutionWord
from .ActionCrypto import ActionCrypto
from .ActionFontTest import ActionFontTest

def main():
	mc = MultiCommand(trailing_text = "version: pysuchsel v%s" % (pysuchsel.VERSION))

	def genparser(parser):
		parser.add_argument("-f", "--fill-rule", choices = [ "en", "de" ], default = "en", help = "Distribute empty spaces with this alphabet and natural language frequency distribution. I.e., every letter occurs with the same probability or is the frequency that is also commonly found in the natural language used. Can be one of %(choices)s, defaults to %(default)s.")
		parser.add_argument("--uniform-distribution", action = "store_true", help = "Instead of choosing natural language distribution, distribute space letters uniformly. Each letter will appear with the same probability.")
		parser.add_argument("-x", "--width", metavar = "width", type = int, default = 15, help = "Choose this width for the suchsel. Defaults to %(default)d spaces.")
		parser.add_argument("-y", "--height", metavar = "height", type = int, default = 20, help = "Choose this height for the suchsel. Defaults to %(default)d spaces.")
		parser.add_argument("-p", "--placement", choices = [ "lr", "tb", "rl", "bt", "dbr", "dtr", "dbl", "dtl" ], action = "append", default = [ ], help = "Defines the placement rule of words within the suchsel. Can be specified multiple times and accepts %(choices)s as option. By default tb and lr is used (top -> bottom and left -> right). Choices beginning with 'd' mean diagonal (diagonal to bottom right/bottom left/top right/top left).")
		parser.add_argument("-c", "--contiguous", action = "store_true", help = "Try to create a contiguous Suchsel, i.e., where some letters overlap.")
		parser.add_argument("--place-attempts", metavar = "cnt", type = int, default = 500, help = "Placing words is non-deterministic. This increases the amounts of attempts for placing a word before giving up. Longer might yield better results, but also takes longer.")
		parser.add_argument("-a", "--creation-attempts", metavar = "cnt", type = int, default = 1, help = "Sometimes, not all words can be placed. This gives the number of attempts that creation of the Suchsel/cross word puzzle is re-attempted before giving up.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be specified multiple times.")
		parser.add_argument("infile", metavar = "infile", help = "Input filename that contains all words separated by newlines.")
		parser.add_argument("outfile", metavar = "outfile", help = "Output SVG file to create.")
	mc.register("suchsel", "Create a Suchsel word puzzle", genparser, action = ActionSuchselCrossword)
	mc.register("crossword", "Create a crossword puzzle", genparser, action = ActionSuchselCrossword)

	def genparser(parser):
		parser.add_argument("--place-attempts", metavar = "cnt", type = int, default = 500, help = "Placing words is non-deterministic. This increases the amounts of attempts for placing a word before giving up. Longer might yield better results, but also takes longer.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be specified multiple times.")
		parser.add_argument("infile", metavar = "infile", help = "Input filename that contains all words separated by newlines.")
		parser.add_argument("outfile", metavar = "outfile", help = "Output SVG file to create.")
		parser.add_argument("solword", metavar = "word", help = "Solution word to search.")
	mc.register("solword", "Create a solution word puzzle", genparser, action = ActionSolutionWord)

	def genparser(parser):
		parser.add_argument("-a", "--alphabet", choices = [ "alpha", "math", "graph", "zodiac", "chess", "runes" ], action = "append", default = [ ], required = True, help = "Name of the ciphertext alphabet(s) to use. Can be specified multiple times, can be any of %(choices)s. Must be given at least once.")
		parser.add_argument("-r", "--reveal", metavar = "letters", default = "ERNSTL", help = "Letters to initially reveal. Defaults to %(default)s.")
		parser.add_argument("-w", "--solution-word", metavar = "word", help = "When puzzle should contain a final solution word, this parameter sets it.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be specified multiple times.")
		parser.add_argument("infile", metavar = "infile", help = "Input filename that contains all lines separated by newlines.")
		parser.add_argument("outfile", metavar = "outfile", help = "Output SVG file to create.")
	mc.register("crypto", "Create crypto word puzzle", genparser, action = ActionCrypto)

	def genparser(parser):
		parser.add_argument("-s", "--sort", action = "store_true", help = "Sort the alphabets before printing")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be specified multiple times.")
		parser.add_argument("outfile", metavar = "outfile", help = "Output SVG file to create.")
	mc.register("fonttest", "Test the fonts for crypto word puzzles", genparser, action = ActionFontTest)

	return mc.run(sys.argv[1:])

if __name__  == "__main__":
	main()
