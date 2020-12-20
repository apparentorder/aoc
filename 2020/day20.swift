class Day20: PuzzleClass {
	var imageSize = 0
	var image = [[Tile]]()

	struct Tile: CustomStringConvertible {
		var id: Int
		var data: [[Character]]

		var rows: Int { data.count }
		var columns: Int { data[0].count }

		var borderTop: [Character] { data.first! }
		var borderBottom: [Character] { data.last! }
		var borderRight: [Character] { self.column(self.columns - 1) }
		var borderLeft: [Character] { self.column(0) }

		func column(_ column: Int) -> [Character] {
			var r = [Character]()

			for row in 0..<self.rows {
				r += [self.data[row][column]]
			}

			return r
		}

		mutating func rotateRight() {
			var dataNew = [[Character]]()

			for column in 0..<self.columns {
				dataNew += [self.column(column).reversed()]
			}

			self.data = dataNew
		}

		mutating func rotateRight(_ times: Int) {
			for _ in 0..<times { self.rotateRight() }
		}

		mutating func flip() {
			var dataNew = [[Character]]()

			for row in (0..<self.rows).reversed() {
				dataNew += [data[row]]
			}

			self.data = dataNew
		}

		mutating func cutBorders() {
			data.removeFirst()
			data.removeLast()

			for row in 0..<data.count {
				data[row].removeFirst()
				data[row].removeLast()
			}
		}

		var description: String {
			let s = (data.map { String($0) }).joined(separator: "\n")
			return s
		}
	}

	var allTiles = [Int:Tile]()

	func parse(_ input: PuzzleInput) {
		for lg in input.lineGroups {
			var id = 0
			var data = [[Character]]()
			for line in lg {
				if line.hasPrefix("Tile ") {
					var parts = line.components(separatedBy: " ")
					parts[1].removeLast() // ":"
					id = Int(parts[1])!
					continue
				}

				data += [Array(line)]
			}

			allTiles[id] = Tile(id: id, data: data)
		}
	}

	func findImage(imageSoFar: [[Tile]] = []) -> [[Tile]]? {
		let imageIdsSoFar = imageSoFar.flatMap { $0 }.map { $0.id }
		guard imageIdsSoFar.count < allTiles.count else {
			// done!
			return imageSoFar
		}

		debug("with \(imageIdsSoFar) ...")
		for (id, tile) in allTiles where !imageIdsSoFar.contains(id) {
			debug("... trying next \(id)")

			var tilesToTry = [Tile]()
			tilesToTry += [tile]

			for i in 1...3 {
				var t = tile
				t.rotateRight(i)
				tilesToTry += [t]
			}

			var tileFlipped = tile
			tileFlipped.flip()
			tilesToTry += [tileFlipped]

			for i in 1...3 {
				var t = tileFlipped
				t.rotateRight(i)
				tilesToTry += [t]
			}

			for ttt in tilesToTry {
				var nextImageSoFar = imageSoFar

				if ttt.id == 1951 && imageSoFar.isEmpty {
					debug("ttt 1951:\n\(ttt)\n")
				}

				// add new row if necessary
				if nextImageSoFar.isEmpty || nextImageSoFar.last!.count == imageSize {
					nextImageSoFar += [[Tile]()]
				}

				guard tileFits(image: nextImageSoFar, nextTile: ttt) else { continue }

				nextImageSoFar[nextImageSoFar.count - 1] += [ttt]

				if let result = findImage(imageSoFar: nextImageSoFar) {
					return result
				}
			}
		}

		// if we get here, nothing worked out
		return nil
	}

	func tileFits(image: [[Tile]], nextTile: Tile) -> Bool {
		guard !image.isEmpty else { return true } // always fits

		#if DEBUG
		let imageIdsSoFar = image.flatMap { $0 }.map { $0.id }
		if imageIdsSoFar == [1951, 2311] && nextTile.id == 3079 {
			debug("1951:\n\(image[0][0])\n")
			debug("2311:\n\(image[0][0])\n")
			debug("3079:\n\(nextTile)\n")
		}
		#endif

		let nextTileRow = image.count - 1
		let nextTileColumn = image.last!.count

		debug("... ... tileFits? \(nextTile.id) at row=\(nextTileRow) column=\(nextTileColumn)")

		guard nextTileRow == 0    || nextTile.borderTop ==  image[nextTileRow - 1][nextTileColumn].borderBottom else { return false }
		guard nextTileColumn == 0 || nextTile.borderLeft == image[nextTileRow][nextTileColumn - 1].borderRight  else { return false }

		return true
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		parse(input)

		imageSize = Int(Float(allTiles.count).squareRoot())
		debug("image size \(imageSize)")

		guard let image = findImage() else { err("not imaginable") }
		debug("final image: \(image.flatMap { $0 }.map { $0.id })")

		var r = 1
		r *= image[0][0].id
		r *= image[0][imageSize - 1].id
		r *= image[imageSize - 1][0].id
		r *= image[imageSize - 1][imageSize - 1].id

		return r
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		parse(input)

		imageSize = Int(Float(allTiles.count).squareRoot())
		debug("image size \(imageSize)")

		guard var imageTiles = findImage() else { err("not imaginable") }
		debug("final image: \(image.flatMap { $0 }.map { $0.id })")

		for tileRow in 0..<imageTiles.count {
			for tile in 0..<imageTiles[0].count {
				imageTiles[tileRow][tile].cutBorders()
			}
		}

		var imageData = [[Character]]()
		for tileRow in imageTiles {

			for row in 0..<tileRow[0].data.count {
				var imageRow = [Character]()
				for tile in tileRow {
					imageRow += tile.data[row]
				}
				imageData += [imageRow]
			}

		}

		var image = Tile(id: 0, data: imageData)
		debug("\(image)")

		var tryNemo = [image]

		image.rotateRight()
		tryNemo += [image]

		image.rotateRight()
		tryNemo += [image]

		image.rotateRight()
		tryNemo += [image]

		image.flip()
		tryNemo += [image]

		image.rotateRight()
		tryNemo += [image]

		image.rotateRight()
		tryNemo += [image]

		image.rotateRight()
		tryNemo += [image]

		for nemo in tryNemo {
			if let nemoImage = findNemo(nemo) {
				debug("GOTCHA!\n\(nemoImage)")
				return nemoImage.data.flatMap { $0 }.filter { $0 == "#" }.count
			}
		}

		return 0
	}

	func findNemo(_ imageX: Tile) -> Tile? {
		let pattern = [
			Array("                  # "),
			Array("#    ##    ##    ###"),
			Array(" #  #  #  #  #  #   "),
		]

		var image = imageX
		var found = false

		for imageRow in 0..<(image.data.count - pattern.count - 1) {
			for imageColumn in 0..<(image.data[0].count - pattern[0].count - 1) {
				debug("finding nemo starting at row \(imageRow) col \(imageColumn)")
				var tryImage = image
				for patternRow in 0..<pattern.count {
					for patternColumn in 0..<pattern[0].count {
						if pattern[patternRow][patternColumn] == "#" && image.data[imageRow + patternRow][imageColumn + patternColumn] == "#" {
							tryImage.data[imageRow + patternRow][imageColumn + patternColumn] = "O"
						}
					}
				}
				let expectedOCount = pattern.flatMap { $0 }.filter { $0 == "#" }.count
				let oCountBefore = image.data.flatMap { $0 }.filter { $0 == "O" }.count
				let oCountNow = tryImage.data.flatMap { $0 }.filter { $0 == "O" }.count

				if (oCountNow - oCountBefore) == expectedOCount {
					// we have a winner (but keep looking for other nemos)
					image = tryImage
					found = true
					debug("found one!")
				}
			}
		}

		return found ? image : nil
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "20-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "20-input-test"), result: 20899048083289),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "20-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "20-input-test"), result: 273),
			]
		),
	]

	required init() {}
}

