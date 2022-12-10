class AsciiLetterProperties:
	_letter_properties = {
		"B": ["bottom_left", "bottom_partial", "center_partial", "left_full", "left_partial", "right_partial", "top_left", "top_partial"],
		"J": ["bottom_partial", "right_partial", "top_partial", "top_right"],
		"H": ["bottom_left", "bottom_partial", "bottom_right", "center_partial", "left_full", "left_partial", "right_full", "right_partial", "top_left", "top_partial", "top_right"],
		"R": ["bottom_left", "bottom_partial", "bottom_right", "center_partial", "left_full", "left_partial", "right_partial", "top_left", "top_partial"],
		"F": ["bottom_left", "center_partial", "left_full", "left_partial", "top_full", "top_left", "top_partial", "top_right"],
		"U": ["bottom_partial", "left_partial", "right_partial", "top_left", "top_partial", "top_right"],
	}

	def from_list(properties):
		c = {}
		for key in properties:
			c[key] = True

		return AsciiLetterProperties(c)

	def __init__(self, some_keys):
		self.properties = {
			"top_full": False,
			"top_partial": False,
			"bottom_full": False,
			"bottom_partial": False,
			"left_full": False,
			"left_partial": False,
			"right_full": False,
			"right_partial": False,

			"center_partial": False,

			"top_left": False,
			"top_right": False,
			"bottom_left": False,
			"bottom_right": False,
		}

		for key, value in some_keys.items():
			self.properties[key] = value

	def letter(self):
		candidate_letters = []

		for letter, lp_keys in self._letter_properties.items():
			lp = AsciiLetterProperties.from_list(lp_keys)
			if lp.properties == self.properties:
				candidate_letters += [letter]

		if len(candidate_letters) != 1:
			raise Exception("match failed, candidates: %s" % (candidate_letters))

		return candidate_letters[0]

	def __str__(self):
		keys_true = []
		for key in sorted(self.properties):
			if self.properties[key]:
				keys_true += ["\"" + key + "\""]

		return ", ".join(keys_true)

class AsciiOcr:
	def __init__(self, grid, letter_width, spacing):
		self.grid = grid
		self.letter_width = letter_width
		self.spacing = spacing

		self._letter_grids = self._get_letter_grids()

	def __str__(self):
		s = ""
		for letter_grid in self._letter_grids:
			lp = AsciiLetterProperties(self._get_letter_properties(letter_grid))
			s += lp.letter()
			#s = "\n".join("".join(line) for line in letter_grid)
			#print(s)
			#print(lp)
			#print(lp.letter())
			#print()

		return s

	def _get_letter_properties(self, grid):
		c = {}

		count_top = grid[0].count("#")
		count_left = [line[0] for line in grid].count("#")
		count_right = [line[len(line) - 1] for line in grid].count("#")
		count_bottom = grid[len(grid) - 1].count("#")

		if count_top == self.letter_width:
			c["top_full"] = True
			c["top_partial"] = True
		if self.letter_width//2 <= count_top < self.letter_width:
			c["top_partial"] = True

		if count_bottom == self.letter_width:
			c["bottom_full"] = True
			c["bottom_partial"] = True
		if self.letter_width//2 <= count_bottom < self.letter_width:
			c["bottom_partial"] = True

		if count_left == len(grid):
			c["left_full"] = True
			c["left_partial"] = True
		if len(grid)//2 <= count_left < len(grid):
			c["left_partial"] = True

		if count_right == len(grid):
			c["right_full"] = True
			c["right_partial"] = True
		if len(grid)//2 <= count_right < len(grid):
			c["right_partial"] = True

		center_dots = sum(line[1:len(line)-1].count("#") for line in grid[1:len(grid)-1])
		c["center_partial"] = center_dots >= 2

		c["top_left"] = grid[0][0] == "#"
		c["top_right"] = grid[0][len(grid[0]) - 1] == "#"
		c["bottom_left"] = grid[len(grid)-1][0] == "#"
		c["bottom_right"] = grid[len(grid)-1][len(grid[0])-1] == "#"

		return c

	def _get_letter_grids(self):
		r = []

		count = len(self.grid[0]) // (self.letter_width + self.spacing)
		for letter_number in range(count):
			letter = []
			for line in self.grid:
				start = letter_number * (self.letter_width + self.spacing)
				end = letter_number * (self.letter_width + self.spacing) + (self.letter_width)

				letter += [list(line[start:end])]

			r += [letter]

		return r

