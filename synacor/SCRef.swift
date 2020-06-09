struct SCRef: CustomStringConvertible {
	let refValue: Int
	let register: Int?
	let isRegister: Bool

	var value: Int {
		get {
			self.isRegister ? sc.register[self.register!] : refValue
		}

		set {
			guard self.isRegister else {
				fatalError("attempt to write to non-register \(refValue)")
			}

			sc.register[self.register!] = newValue
		}
	}

	init(_ refValue: Int) {
		switch refValue {
		case 0...32767:
			self.isRegister = false
			self.register = nil
		case 32768..<32776:
			self.isRegister = true
			self.register = refValue - 32768
		default:
			fatalError("SCRef(): invalid refValue \(refValue)")
		}
		self.refValue = refValue
	}

	var location: String {
		self.isRegister ? "R\(self.register!)" : "@\(self.refValue)"
	}

	var description: String {
		if self.isRegister {
			return "[\(self.location)]\(sc.register[self.register!])"
		} else {
			return "\(self.refValue)"
		}
	}
}

