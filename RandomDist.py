#!/usr/bin/python3
#
#	RandomDist - Generate random values of given distribution
#	Copyright (C) 2011-2013 Johannes Bauer
#	
#	This file is part of pycommon.
#
#	pycommon is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pycommon is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pycommon; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>
#
#	File UUID 7e9a90a5-a1a1-4e49-a67c-5d935126abfe

import random

class RandomDist():
	def __init__(self, distribution):
		self._sum = 0
		self._values = [ ]
		for (key, value) in distribution.items():
			if value > 0:
				self._sum += value
				self._values.append((key, self._sum))

	def coinflip(self):
		return random.randint(0, 1) == 0

	def event(self):
		randval = random.random() * self._sum
		for (key, value) in self._values:
			if randval < value:
				return key

if __name__ == "__main__":
	rdist = RandomDist({
		"10_1":	10,
		"10_2":	10,
		"20":	20,
		"60":	60,
	})
	
	total = 300000
	events = { }
	for i in range(total):
		x = rdist.event()
		events[x] = events.get(x, 0) + 1
	for (event, cnt) in events.items():
		print("%-8s %7.4f%%" % (event, cnt / total * 100))


