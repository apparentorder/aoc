struct SCRef: CustomStringConvertible {
	let refValue: Int
	let isRegister: Bool

	var value: Int {
		get {
			self.isRegister ? register[refValue - 32768] : refValue
		}

		set {
			guard self.isRegister else {
				fatalError("attempt to write to non-register \(refValue)")
			}

			register[refValue - 32768] = newValue
		}
	}

	init(_ refValue: Int) {
		switch refValue {
		case 0...32767:
			self.isRegister = false
		case 32768..<32776:
			self.isRegister = true
		default:
			fatalError("SCRef(): invalid refValue \(refValue)")
		}
		self.refValue = refValue
	}

	var description: String {
		let r = self.isRegister ? "REGISTER" : ""
		return "SCRef(refValue=\(self.refValue) \(r)value=\(self.value))"
	}
}

