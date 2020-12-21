class Day20: PuzzleClass {
	var allTiles = [Int:Image](minimumCapacity: 150)
	var allBorders = [[Character]:[Int]](minimumCapacity: 150 * 8)

	// the number of Tiles that make up *one* edge of the full image
	// (e.g. for an input of 144 tiles, each edge would be 12 tiles long)
	var imageEdgeTileCount = 0

	struct Image: CustomStringConvertible {
		var id: Int
		var data: [[Character]]

		var rows: Int { data.count }
		var columns: Int { data[0].count }

		var borderTop: [Character] { data.first! }
		var borderBottom: [Character] { data.last! }
		var borderRight: [Character] { self.column(self.columns - 1) }
		var borderLeft: [Character] { self.column(0) }

		var borders: [[Character]] {
			[
				borderTop,
				borderBottom,
				borderLeft,
				borderRight,
				borderTop.reversed(),
				borderBottom.reversed(),
				borderLeft.reversed(),
				borderRight.reversed(),
			]
		}

		func column(_ column: Int) -> [Character] {
			self.data.map { $0[column] }
		}

		mutating func rotateRight() {
			self.data = (0..<self.columns).map { self.column($0).reversed() }
		}

		mutating func flip() {
			self.data.reverse()
		}

		mutating func cutBorders() {
			data.removeFirst()
			data.removeLast()

			for row in 0..<data.count {
				data[row].removeFirst()
				data[row].removeLast()
			}
		}

		var hashCount: Int {
			self.data.flatMap { $0 }.filter { $0 == "#" }.count
		}

		var description: String {
			let s = (data.map { String($0) }).joined(separator: "\n")
			return s
		}

		struct OrientationSequence: Sequence {
			let image: Image

			func makeIterator() -> OrientationIterator {
				return OrientationIterator(image: image)
			}
		}

		struct OrientationIterator: IteratorProtocol {
			var image: Image
			var iterCount = 0

			mutating func next() -> Image? {
				defer { iterCount += 1 }
				guard iterCount > 0 else { return image }
				guard iterCount < 8 else { return nil }

				if iterCount == 4 {
					image.flip()
				}

				image.rotateRight()
				return image
			}
		}
	}

	func findCornerPieceIds() -> Set<Int> {
		// besides finding corner pieces in the process, do a quick sanity check on our input.

		// - all borders must have exactly 1 or 2 corresponding pieces
		let invalidBorders = allBorders.values.filter { ![1,2].contains($0.count) }
		assert(invalidBorders.isEmpty, "some borders don't belong to exactly 1 or 2 pieces: \(invalidBorders)")

		// - exactly (imageEdgeTileCount * 4 - 4) pieces each have at least one unique border (edge pieces)
		let edgePieceIdsWithDuplicates = allBorders.values.filter { $0.count == 1 }.flatMap { $0 }
		let edgePieceIds = Set(edgePieceIdsWithDuplicates)
		assert(
			edgePieceIds.count == imageEdgeTileCount * 4 - 4,
			"expected \(imageEdgeTileCount * 4 - 4) edge pieces but found \(edgePieceIds.count)"
		)

		// - four of those images each have two unique borders (corner pieces)
		// note that for counting corner pieces (two unique borders), we search for edge pieces that have *four*
		// unique borders! this is because allBorders also includes the reversed version of each // border, s
		let cornerPieceIds = edgePieceIds.filter { epId in allBorders.values.filter { $0 == [epId] }.count == 4 }
		assert(cornerPieceIds.count == 4, "found \(cornerPieceIds.count) corner pieces instead of 4")

		debug("edge pieces: \(edgePieceIds)")
		debug("corner pieces: \(cornerPieceIds)")

		return cornerPieceIds
	}

	func assembleImage() -> Image {
		var imageTiles = [[Image]]()

		// start with any corner piece
		// n.b.: the first! of a Dictionary will be *undefined* and therefore
		// pseudo-random, which can have huge difference on the run time (on
		// how often the image/pattern in part 2 needs to be rotated and scanned).
		var topLeft = allTiles[findCornerPieceIds().first!]!

		// rotate it so it's the top-left corner
		for t in Image.OrientationSequence(image: topLeft) {
			let topIsUnique = allBorders[t.borderTop]! == [t.id]
			let leftIsUnique = allBorders[t.borderLeft]! == [t.id]
			guard !topIsUnique || !leftIsUnique else {
				topLeft = t
				break
			}
		}

		var tileRow = [Image]()
		tileRow += [topLeft]

		// now attach the other pieces
		while imageTiles.count < imageEdgeTileCount {
			let isFirstInRow = tileRow.isEmpty
			let tileToMatch = isFirstInRow ? imageTiles.last![0] : tileRow.last!
			let borderToMatch = isFirstInRow ? tileToMatch.borderBottom : tileToMatch.borderRight

			let nextTileIdList = allBorders[borderToMatch]!.filter { $0 != tileToMatch.id }
			assert(nextTileIdList.count == 1, "ambiguous next border after \(imageTiles.flatMap { $0 }.map { $0.id })")
			let nextTileId = nextTileIdList.first!

			for t in Image.OrientationSequence(image: allTiles[nextTileId]!) {
				let otherBorderToMatch = isFirstInRow ? t.borderTop : t.borderLeft
				if borderToMatch == otherBorderToMatch {
					tileRow += [t]
					break
				}
			}

			if tileRow.count == imageEdgeTileCount {
				imageTiles += [tileRow]
				tileRow.removeAll(keepingCapacity: true)
			}
		}

		debug("imageTiles complete! \(imageTiles.flatMap { $0 }.map { $0.id })")

		// now just cut all the borders ...
		for tileRow in 0..<imageTiles.count {
			for tile in 0..<imageTiles[0].count {
				imageTiles[tileRow][tile].cutBorders()
			}
		}

		// ... and glue everything together ...
		var imageData = [[Character]]()
		imageData.reserveCapacity(200)
		for tileRow in imageTiles {
			for row in 0..<tileRow[0].data.count {
				var imageRow = [Character]()
				imageRow.reserveCapacity(200)
				for tile in tileRow {
					imageRow += tile.data[row]
				}
				imageData += [imageRow]
			}
		}

		// ... to create a new Image
		return Image(id: 0, data: imageData)

	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		parse(input)

		imageEdgeTileCount = Int(Float(allTiles.count).squareRoot())
		debug("image size \(imageEdgeTileCount)")

		return findCornerPieceIds().reduce(1, *)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		parse(input)

		imageEdgeTileCount = Int(Float(allTiles.count).squareRoot())
		debug("image size \(imageEdgeTileCount)")

		let image = assembleImage()
		debug("\(image)")

		let nemoPattern = [
			Array("                  # "),
			Array("#    ##    ##    ###"),
			Array(" #  #  #  #  #  #   "),
		]
		let nemo = Image(id: -1, data: nemoPattern)

		for nemoOrientation in Image.OrientationSequence(image: nemo) {
			let nemoCount = findNemo(in: image, usingPattern: nemoOrientation)
			if nemoCount > 0 {
				debug("GOTCHA!")
				return image.hashCount - nemo.hashCount * nemoCount
			}
		}

		err("no monsters here. apparently, that's a bad thing.")
	}

	func findNemo(in image: Image, usingPattern patternImage: Image) -> Int {
		let pattern = patternImage.data
		let patternHashCount = patternImage.hashCount
		var debugImage = image

		var found = 0
		for imageRow in 0..<(image.data.count - pattern.count) {
			for imageColumn in 0..<(image.data[0].count - pattern[0].count) {
				var hashCount = 0
				var debugImageTry = debugImage
				for patternRow in 0..<pattern.count {
					for patternColumn in 0..<pattern[0].count where pattern[patternRow][patternColumn] == "#" {
						if image.data[imageRow + patternRow][imageColumn + patternColumn] == "#" {
							hashCount += 1
							#if DEBUG
							debugImageTry.data[imageRow + patternRow][imageColumn + patternColumn] = "O"
							#endif
						}
					}
				}

				if hashCount == patternHashCount {
					debug("Nemo found! Nemo (0,0) at image (\(imageColumn), \(imageRow))")
					found += 1
					debugImage = debugImageTry
				}
			}
		}

		if found > 0 {
			debug(debugImage)
		}
		return found
	}

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

			let tile = Image(id: id, data: data)
			allTiles[id] = tile
			for border in tile.borders {
				allBorders[border] = (allBorders[border] ?? []) + [id]
			}
		}
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

