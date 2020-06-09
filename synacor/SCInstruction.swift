struct SCI: CustomStringConvertible, Equatable {
	static func == (lhs: SCI, rhs: SCI) -> Bool {
		lhs.address == rhs.address
	}

	static let Addresses = [
		1458: "TextOutputPrint",
		1518: "TextOutput",
		1517: "TextOutputRet",
		1527: "TextOutputRet2",
		5445: "Teleport",
		5472: "TeleportRet",
		5483: "TeleportStartCheck",
		5489: "TeleportCheckR7Call",
		5498: "TeleportAfterCheck",
		5558: "TeleportDoneRet",
		5605: "TeleportDestinationDefault",
		6027: "TeleportCheckR7",
		0: ""
	]
	let address: Int

	init(_ address: Int) {
		self.address = address
	}

	init(byName name: String) {
		//address = SCI.Addresses.first(where: { $1 == name })
		address = SCI.Addresses.first { $1 == name }!.key
	}

	var description: String {
		SCI.Addresses[address] == nil ? "\(address)" : "\(address)=\(SCI.Addresses[address]!)"
	}
}

