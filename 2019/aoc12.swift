#!/usr/bin/env swift

//import Foundation

class Coordinates: CustomStringConvertible {
	public var x = 0
	public var y = 0
	public var z = 0

	init(_ x: Int, _ y: Int, _ z: Int) {
		self.x = x
		self.y = y
		self.z = z
	}

	init(copy source: Coordinates) {
		self.x = source.x
		self.y = source.y
		self.z = source.z
	}

	public var description: String {
		return "(\(self.x),\(self.y),\(self.z))"
	}

	public var energy: Int {
		return abs(self.x) + abs(self.y) + abs(self.z)
	}
}

class Moon: CustomStringConvertible {
	public let id: String
	public var position: Coordinates
	public var velocity: Coordinates

	public let original_position: Coordinates

	public var energyPotential: Int {
		return position.energy
	}

	public var energyKinetic: Int {
		return velocity.energy
	}

	public var energyTotal: Int {
		return self.energyPotential * self.energyKinetic
	}

	init(_ id: String, position: Coordinates, velocity: Coordinates) {
		self.id = id
		self.position = position
		self.velocity = velocity
		self.original_position = Coordinates(copy: self.position)
	}

	init(_ id: String, _ position: Coordinates) {
		self.id = id
		self.position = position
		self.velocity = Coordinates(0, 0, 0)
		self.original_position = Coordinates(copy: self.position)
	}

	public var description: String {
		return "position=\(self.position) velocity=\(self.velocity) " +
			"energy=\(self.energyPotential)/\(self.energyKinetic)/" +
			"\(self.energyTotal) id=\(self.id)"
	}

	public func move() {
		self.position.x += self.velocity.x
		self.position.y += self.velocity.y
		self.position.z += self.velocity.z
	}

	public func adjustVelocity(relativeTo: Moon) {
		if self === relativeTo {
			return
		}

		switch compareAxis(self.position.x, relativeTo.position.x, debug: true) {
			case .partnerIsAhead:  self.velocity.x += 1
			case .partnerIsBehind: self.velocity.x -= 1
			case .partnerIsSame: break
		}

		switch compareAxis(self.position.y, relativeTo.position.y) {
			case .partnerIsAhead:  self.velocity.y += 1
			case .partnerIsBehind: self.velocity.y -= 1
			case .partnerIsSame: break
		}

		switch compareAxis(self.position.z, relativeTo.position.z) {
			case .partnerIsAhead:  self.velocity.z += 1
			case .partnerIsBehind: self.velocity.z -= 1
			case .partnerIsSame: break
		}
	}

	// ---------

	enum GravityPull {
		case partnerIsAhead
		case partnerIsBehind
		case partnerIsSame
	}

	private func compareAxis(_ me: Int, _ partner: Int, debug: Bool = false) -> GravityPull {
		if partner > me { return .partnerIsAhead }
		if partner < me { return .partnerIsBehind }
		return .partnerIsSame
	}
}

// ex. 1:
// <x=-1, y=0, z=2>
// <x=2, y=-10, z=-7>
// <x=4, y=-8, z=8>
// <x=3, y=5, z=-1>

let moons_ex1 = [
	Moon("io",       Coordinates(-1, 0, 2)),
	Moon("europa",   Coordinates(2, -10, -7)),
	Moon("ganymede", Coordinates(4, -8, 8)),
	Moon("callisto", Coordinates(3, 5, -1)),
]

let moons_ex2 = [
	Moon("io",       Coordinates(-8, -10, 0)),
	Moon("europa",   Coordinates(5, 5, 10)),
	Moon("ganymede", Coordinates(2, -7, 3)),
	Moon("callisto", Coordinates(9, -8, -3)),
]

let moons_actual = [
	Moon("io",       Coordinates(0, 4, 0)),
	Moon("europa",   Coordinates(-10, -6, -14)),
	Moon("ganymede", Coordinates(9, -16, -3)),
	Moon("callisto", Coordinates(6, -1, 2)),
]

//let moons = moons_actual
let moons = moons_actual

var initial_x_values = [Int]()
var initial_y_values = [Int]()
var initial_z_values = [Int]()

print("initial:")
for m in moons {
	print(m)

	initial_x_values += [m.position.x]
	initial_y_values += [m.position.y]
	initial_z_values += [m.position.z]
}
print()

var step = 0
var x = [Int]()
var y = [Int]()
var z = [Int]()
var cycle_x = 0
var cycle_y = 0
var cycle_z = 0
var dump = false
var dump_all = false

while true {
//for _ in 1 ... 10 {
	step += 1
	x = []
	y = []
	z = []
	dump = false

	for m in moons {
		for partner in moons {
			m.adjustVelocity(relativeTo: partner)
		}
	}

	for m in moons {
		m.move()

		x += [m.position.x]
		y += [m.position.y]
		z += [m.position.z]
	}

	if x == initial_x_values && (cycle_x == 0) {
		print("\(step)+1 - first X axis cycle complete")
		cycle_x = step + 1
		dump = true
	}

	if y == initial_y_values && (cycle_y == 0) {
		print("\(step)+1 - first Y axis cycle complete")
		cycle_y = step + 1
		dump = true
	}

	if z == initial_z_values && (cycle_z == 0) {
		print("\(step)+1 - first Z axis cycle complete")
		cycle_z = step + 1
		dump = true
	}

	if dump || dump_all {
		print("after step \(step):")
		for m in moons { print(m) }
		print()
	}

	if (cycle_x != 0) && (cycle_y != 0) && (cycle_z != 0) {
		print("complete! finding mininum steps to repeat ...")

		// find the smallest number that is divisible by
		// all axis' required steps to cycle.

		var incr = [cycle_x, cycle_y, cycle_z].max()!
		var attempt = incr
		var loops = 0
		var have_two = false
		while true {
			var matches = 0
			matches += (attempt % cycle_x == 0) ? 1 : 0
			matches += (attempt % cycle_y == 0) ? 1 : 0
			matches += (attempt % cycle_z == 0) ? 1 : 0

			if matches == 2 && !have_two {
				// first time we have two numbers
				// that fit, so we can increase the
				// steps \o/
				incr = attempt
				have_two = true
			}

			if matches == 3 {
				break
			}

			attempt += incr
			loops += 1
		}

		print("cycle repeats after merely \(attempt) steps")
		print("(needed \(loops) loops to figure that out)")
		break
	}
}

var energySystem = 0
for m in moons {
	energySystem += m.energyTotal
}

print("total energy in system after \(step) steps: \(energySystem)")

