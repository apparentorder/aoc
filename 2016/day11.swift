class Day11: PuzzleClass {
	struct Element: CustomStringConvertible, Equatable, Hashable {
		let name: String
		let symbol: String

		var description: String { symbol }
	}

	struct Item: CustomStringConvertible, Equatable, Hashable {
		let element: Element
		let type: ItemType
		var floor: Int

		var description: String { "\(element)\(type)#\(floor)" }
	}

	enum ItemType: CustomStringConvertible, Hashable {
		case Generator
		case Microchip

		var description: String {
			switch self {
				case .Generator: return "G"
				case .Microchip: return "M"
			}
		}
	}

	struct ItemPair: Equatable, Hashable, Comparable, CustomStringConvertible {
		let generatorFloor: Int
		let microchipFloor: Int

		var description: String { "[G\(generatorFloor)-M\(microchipFloor)" }

		static func <(lhs: ItemPair, rhs: ItemPair) -> Bool {
			guard lhs.generatorFloor != rhs.generatorFloor else {
				return (lhs.microchipFloor < rhs.microchipFloor)
			}

			return (lhs.generatorFloor < rhs.generatorFloor)
		}
	}

	struct LabState: Hashable, Equatable, CustomStringConvertible {
		let items: Set<Item>
		let elevatorFloor: Int
		let sortedPairs: [ItemPair]

		func floorItems(_ floor: Int? = nil) -> Set<Item> {
			items.filter { $0.floor == (floor ?? self.elevatorFloor) }
		}

		//
		// check for equivalence, as described on the solutions reddit by u/p_tseng --
		// https://www.reddit.com/r/adventofcode/comments/5hoia9/2016_day_11_solutions/db1v1ws/
		// 
		// we implement this by overriding ==() and the hasher function, so different but
		// equivalent states are treated as being equal (especially in a Set!)
		//

		static func ==(lhs: LabState, rhs: LabState) -> Bool {
			lhs.sortedPairs == rhs.sortedPairs && lhs.elevatorFloor == rhs.elevatorFloor
		}

		func hash(into hasher: inout Hasher) {
			hasher.combine(self.sortedPairs)
			hasher.combine(elevatorFloor)
		}

		init(items: Set<Item>, elevatorFloor: Int) {
			self.items = items
			self.elevatorFloor = elevatorFloor

			var sp = [ItemPair]()
			sp.reserveCapacity(100)

			for generator in self.items.filter({ $0.type == .Generator }) {
				let match = self
					.items
					.filter { $0.element == generator.element && $0.type == .Microchip }
					.first!
				sp += [ItemPair(generatorFloor: generator.floor, microchipFloor: match.floor)]
			}

			self.sortedPairs = sp.sorted()
		}

		var description: String {
			var s = "<<<"
			s += "E\(self.elevatorFloor) "

			for floor in (1...4).reversed() {
				let items = self.floorItems(floor)
				guard !items.isEmpty else { continue }
				s += "F\(floor)=\(items.sorted(by: { $1.element.symbol > $0.element.symbol })) "
			}

			return s.dropLast() + ">>>"
		}
	}

	func shortestPath(from sourceState: LabState, to targetState: LabState) -> [LabState] {
		var paths = [[sourceState]]
		var statesSeen = Set<LabState>()
		statesSeen.reserveCapacity(50_000)

		while true {
			var nextPaths = [[LabState]]()
			nextPaths.reserveCapacity(1_000)

			guard !paths.isEmpty else { err("verlaufen") }
			print("\(paths.first!.count) steps, \(paths.count) paths, seen \(statesSeen.count)")

			for path in paths {
				let state = path.last!

				guard state != targetState else { return path }

				nextPaths += getNextStates(for: state, statesSeen: &statesSeen).map { path + [$0] }
			}

			paths = nextPaths
		}
	}

	func getNextStates(for state: LabState, statesSeen: inout Set<LabState>) -> [LabState] {
				// -- figure out next possible states for each path --
				var nextStates = [LabState]()
				nextStates.reserveCapacity(1_000)

				let floorItems = state.floorItems()

				// minimum one, maximum two items are to be moved
				var itemPermutations = Set<Set<Item>>()
				itemPermutations.reserveCapacity(100)

				for i1 in floorItems {
					for i2 in floorItems {
						itemPermutations.insert(Set([i1, i2]))
					}
				}

				let nextFloors = []
				+ (state.elevatorFloor < 4 ? [state.elevatorFloor + 1] : [])
				+ (state.elevatorFloor > 1 ? [state.elevatorFloor - 1] : [])

				for nextFloor in nextFloors {
					// theoretical optimization: don't move to already-empty floors
					// doesn't make much of a difference (about ~1,000 states saved,
					// but about the same run time), therefore disabled.
					#if false
					if nextFloor == 1 && state.floorItems(1).isEmpty {
						if nextFloor == 2 && state.floorItems(2).isEmpty {
							continue
						}
						continue
					}
					#endif

					tryPerm: for tryPerm in itemPermutations {
						// move tryPerm items to nextFloor
						let tryItems = Set(state.items.map {
							(i: Item) -> Item in
							if !tryPerm.contains(i) {
								return i
							} else {
								var x = i
								x.floor = nextFloor
								return x
							}
						})

						for checkFloor in [state.elevatorFloor, nextFloor] {
							let checkItems = tryItems.filter { $0.floor == checkFloor }
							let generators = checkItems.filter({ $0.type == .Generator })
							guard (
								generators.isEmpty ||
								Set(checkItems.map { $0.element })
								.subtracting(generators.map { $0.element })
								.isEmpty
							) else {
								continue tryPerm
							}
						}

						let n = LabState(items: tryItems, elevatorFloor: nextFloor)

						guard !statesSeen.contains(n) else { continue }
						nextStates.append(n)
						statesSeen.insert(n)
					}
				}

				return nextStates
	}

	func parse(_ lines: [String]) -> Set<Item> {
		// The first floor contains a promethium generator and a promethium-compatible microchip.
		// The second floor contains a cobalt generator, a curium generator, a ruthenium generator, \
		//     and a plutonium generator.
		// The third floor contains a cobalt-compatible microchip, a curium-compatible microchip, \
		//     a ruthenium-compatible microchip, and a plutonium-compatible microchip.
		// The fourth floor contains nothing relevant.

		var items = Set<Item>()

		for var line in lines {
			line.removeAll { [",", "."].contains($0) } // remove junk chars
			var parts = line.components(separatedBy: " ")

			let junkWords = ["The", "nothing", "relevant", "a", "and", "contains", "floor" ]
			parts.removeAll { junkWords.contains($0) }

			let floorString = parts.removeFirst()

			let floor: Int
			switch floorString {
				case "first": floor = 1
				case "second": floor = 2
				case "third": floor = 3
				case "fourth": floor = 4
				default: err("unknown floor \(floorString)")
			}

			debug("floor \(floor) parse: \(parts)")
			while !parts.isEmpty {
				let elementString = parts[0].components(separatedBy: "-").first! // possible "-compatible" suffix
				let typeString = parts[1]
				parts.removeFirst(2)

				debug("floor \(floor) item \(typeString) for \(elementString)")

				let symbols: [String:String] = [
					"hydrogen": "H",
					"cobalt": "Co",
					"lithium": "Li",
					"promethium": "Pm",
					"curium": "Cm",
					"ruthenium": "Ru",
					"plutonium": "Pu",
				]

				guard let symbol = symbols[elementString] else { err("unknown element \(elementString)") }

				items.insert(Item(
					element: Element(name: elementString, symbol: symbol),
					type: (typeString == "generator" ? ItemType.Generator : ItemType.Microchip),
					floor: floor
				))
			}
		}

		debug("parse complete: \(items)")
		return items
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let items = parse(input.lines)
		let initialState = LabState(items: items, elevatorFloor: 1)

		let targetItems = items.map { Item(element: $0.element, type: $0.type, floor: 4) }
		let targetState = LabState(items: Set(targetItems), elevatorFloor: 4)

		debug(initialState)

		let shortest = shortestPath(from: initialState, to: targetState)
		shortest.forEach { debug($0) }
		return shortest.count - 1 // not counting the initial state
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		var items = parse(input.lines)
		items.insert(Item(element: Element(name: "elerium", symbol: "el"), type: .Generator, floor: 1))
		items.insert(Item(element: Element(name: "elerium", symbol: "el"), type: .Microchip, floor: 1))
		items.insert(Item(element: Element(name: "dilithium", symbol: "di"), type: .Generator, floor: 1))
		items.insert(Item(element: Element(name: "dilithium", symbol: "di"), type: .Microchip, floor: 1))

		let initialState = LabState(items: items, elevatorFloor: 1)

		let targetItems = items.map { Item(element: $0.element, type: $0.type, floor: 4) }
		let targetState = LabState(items: Set(targetItems), elevatorFloor: 4)

		debug(initialState)

		let shortest = shortestPath(from: initialState, to: targetState)
		shortest.forEach { debug($0) }
		return shortest.count - 1 // not counting the initial state
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "11-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "11-input-test"), result: 11),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "11-input"),
			tests: []
		),
	]

	required init() {}

}

