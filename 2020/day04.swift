class Day04 {
	enum EyeColor: String {
		case amber = "amb"
		case blue = "blu"
		case brown = "brn"
		case grey = "gry"
		case green = "grn"
		case hazel = "hzl"
		case other = "oth"
	}

	enum Height {
		case inches(Int)
		case centimeters(Int)

		init?(fromString s: String) {
			guard s.hasSuffix("cm") || s.hasSuffix("in") else {
				debug("hgt: invalid unit")
				return nil
			}

			var numberString = s
			numberString.removeLast(2)
			guard let number = Int(numberString) else {
				debug("hgt: invalid number")
				return nil
			}

			if s.hasSuffix("cm") {
				guard number >= 150 && number <= 193 else {
					debug("hgt number invalid for centimeter range")
					return nil
				}
				self = .centimeters(number)
			} else {
				// inches
				guard number >= 59 && number <= 76 else {
					debug("hgt number invalid for inches range")
					return nil
				}
				self = .inches(number)
			}
		}
	}

	struct HairColor: CustomStringConvertible {
		var color: Int

		var hexValue: String { String(format: "#%06x", color) }
		var description: String { hexValue }

		init?(fromString s: String) {
			var hcl = s

			guard hcl.removeFirst() == "#" else { debug("hcl missing #"); return nil }
			guard hcl.count == 6 else { debug("hcl: not six hex digits"); return nil }
			guard let c = Int(hcl, radix: 16) else { debug("hcl: invalid hex"); return nil }
			color = c
		}
	}

	struct RawPassport {
		var passportId: String

		var birthYear: String
		var issueYear: String
		var expiryYear: String

		var height: String

		var hairColor: String
		var eyeColor: String

		var countryId: String? // optional

		init?(fromKeyValuePairs pairs: Dictionary<String, String>) {
			guard let pid = pairs["pid"] else { debug("pid missing"); return nil }
			passportId = pid

			guard let byr = pairs["byr"] else { debug("byr missing"); return nil }
			birthYear = byr

			guard let iyr = pairs["iyr"] else { debug("iyr missing"); return nil }
			issueYear = iyr

			guard let eyr = pairs["eyr"] else { debug("eyr missing"); return nil }
			expiryYear = eyr

			guard let hgt = pairs["hgt"] else { debug("hgt missing"); return nil }
			height = hgt

			guard let hcl = pairs["hcl"] else { debug("hcl missing"); return nil }
			hairColor = hcl

			guard let ecl = pairs["ecl"] else { debug("ecl missing"); return nil }
			eyeColor = ecl

			countryId = pairs["cid"]
		}
	}

	struct Passport {
		var passportId: String // could be zero-filled, hence String

		var birthYear: Int
		var issueYear: Int
		var expiryYear: Int

		var height: Height

		var hairColor: HairColor
		var eyeColor: EyeColor

		var countryId: String? // optional; not validated!

		init?(fromRawPassport rp: RawPassport) {
			// ----- passportId -----
			guard let pidInt = Int(rp.passportId) else { debug("pid: invalid number"); return nil }
			guard String(format: "%09d", pidInt) == rp.passportId else { debug("pid: not nine digits"); return nil }
			passportId = rp.passportId

			// ----- birthYear -----
			guard let byr = Int(rp.birthYear), byr >= 1920 && byr <= 2002 else { debug("byr invalid"); return nil }
			birthYear = byr

			// ----- issueYear -----
			guard let iyr = Int(rp.issueYear), iyr >= 2010 && iyr <= 2020 else { debug("iyr invalid"); return nil }
			issueYear = iyr

			// ----- expiryYear -----
			guard let eyr = Int(rp.expiryYear), eyr >= 2020 && eyr <= 2030 else { debug("eyr invalid"); return nil }
			expiryYear = eyr

			// ----- height -----
			guard let hgt = Height(fromString: rp.height) else { debug("hgt invalid"); return nil }
			height = hgt

			// ----- hairColor -----
			guard let hcl = HairColor(fromString: rp.hairColor) else { debug("hcl invalid"); return nil }
			hairColor = hcl

			// ----- eyeColor -----
			guard let ecl = EyeColor(rawValue: rp.eyeColor) else { debug("ecl invalid"); return nil }
			eyeColor = ecl

			// ----- countryId -----
			countryId = rp.countryId
		}
	}

	static func parseRawPassports(_ inputLines: [String]) -> [RawPassport] {
		var r = [RawPassport]()
		var allPassportData = [[String:String]]()
		var thisPassportData = [String:String]()

		// first, form key/value pairs for all passport records
		for line in inputLines {
			if line.isEmpty {
				allPassportData += [thisPassportData]
				thisPassportData = [String:String]()
				continue
			}

			let pairStrings = line.split(separator: " ").map { String($0) }
			for ps in pairStrings {
				let kv = ps.split(separator: ":").map { String($0) }
				thisPassportData[kv[0]] = kv[1]
			}
		}

		// flush last entry
		allPassportData += [thisPassportData]

		// now create actual RawPassports from the key/value pairs
		for passportData in allPassportData {
			debug("Passport raw data: \(passportData)")
			guard let pp = RawPassport(fromKeyValuePairs: passportData) else {
				continue
			}

			r += [pp]
		}

		return r
	}

	static func part1(_ input: PuzzleInput) -> PuzzleResult {
		let rawPassports = parseRawPassports(input.lines)
		return rawPassports.count
	}

	static func part2(_ input: PuzzleInput) -> PuzzleResult {
		let rawPassports = parseRawPassports(input.lines)
		var passports = [Passport]()

		for rp in rawPassports {
			debug("Passport: \(rp)")
			guard let pp = Passport(fromRawPassport: rp) else {
				continue
			}

			passports += [pp]
		}

		return passports.count
	}
}

