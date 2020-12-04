class Day04 {
	//enum PassportField {
		//case byr, iyr, eyr, hgt, hcl, ecl, pid, cid
	//}

	struct Passport: CustomStringConvertible {
		//var data: Dictionary<PassportField, String>
		var data: Dictionary<String, String>

		var isValidPart1: Bool {
			debug("Checking passwort with data \(data)")
			guard data["byr"] != nil else { return false }
			guard data["iyr"] != nil else { return false }
			guard data["eyr"] != nil else { return false }
			guard data["hgt"] != nil else { return false }
			guard data["hcl"] != nil else { return false }
			guard data["ecl"] != nil else { return false }
			guard let pid = data["pid"] else { return false }
			debug("passport pid=\(pid) is valid (part1)")
			return true
		}

		var description: String {
			var d = ""

			guard isValidPart1 else { return "(incomplete record)" }

			d += "[ "
			d += "pid \(data["pid"]!) / "
			d += "byr \(data["byr"]!) / "
			d += "iyr \(data["iyr"]!) / "
			d += "eyr \(data["eyr"]!) / "
			d += "hcl \(data["hcl"]!) / "
			d += "ecl \(data["ecl"]!) / "
			d += "hgt \(data["hgt"]!) / "
			d += "]"

			return d
		}

		var isValidData: String {
			guard isValidPart1 else { return "not isValidPart1" }

			guard let byr = Int(data["byr"]!) else { return "byr: bad int" }
			guard let iyr = Int(data["iyr"]!) else { return "iyr: bad int" }
			guard let eyr = Int(data["eyr"]!) else { return "eyr: bad int" }

			guard byr >= 1920 && byr <= 2002 else { return "byr: bad range" }
			guard iyr >= 2010 && iyr <= 2020 else { return "iyr: bad range" }
			guard eyr >= 2020 && eyr <= 2030 else { return "eyr: bad range" }

			// hgt
			var hgt = data["hgt"]!
			var hgtMin: Int
			var hgtMax: Int
			if hgt.hasSuffix("cm") {
				hgtMin = 150
				hgtMax = 193
			} else if hgt.hasSuffix("in") {
				hgtMin = 59
				hgtMax = 76
			} else {
				// bad suffix!
				return "hgt: missing suffix"
			}

			hgt.removeLast(2)
			var hgtInt = Int(hgt)!
			guard hgtInt >= hgtMin && hgtInt <= hgtMax else { return "hgt: bad range" }

			// hcl
			var hcl = data["hcl"]!
			guard hcl.removeFirst() == "#" else { return "hcl: missing #" }
			guard hcl.count == 6 else { return "hcl: not six hex digits" }
			guard Int(hcl, radix: 16) != nil else { return "hcl: invalid hex" }

			// ecl
			switch data["ecl"] {
			case "amb": break
			case "blu": break
			case "brn": break
			case "gry": break
			case "grn": break
			case "hzl": break
			case "oth": break
			default: return "ecl: unknown color"
			}

			guard let pidInt = Int(data["pid"]!) else { return "pid: invalid number" }
			guard String(format: "%09d", pidInt) == data["pid"]! else { return "pid: not nine digits" }

			return "OK"
		}
	}

	static func parsePassports(_ inputLines: [String]) -> [Passport] {
		var r = [Passport]()
		var pairs = Dictionary<String, String>()

		debug(inputLines)
		for line in inputLines {
			if line == "" {
				debug("end passport")
				r += [Passport(data: pairs)]
				pairs = Dictionary<String, String>()
				continue
			}

			let pairStrings = line.split(separator: " ").map { String($0) }

			for ps in pairStrings {
				let kv = ps.split(separator: ":").map { String($0) }

				pairs[kv[0]] = kv[1]
			}
		}

		r += pairs.count > 0 ? [Passport(data: pairs)] : []

		return r
	}

	static func part1(_ input: PuzzleInput) -> PuzzleResult {
		return parsePassports(input.lines).filter { $0.isValidPart1 }.count
	}

	static func part2(_ input: PuzzleInput) -> PuzzleResult {
		let passports = parsePassports(input.lines)
		passports.forEach { debug("\($0) => \($0.isValidData)") }
		return parsePassports(input.lines).filter { $0.isValidData == "OK" }.count
	}
}

