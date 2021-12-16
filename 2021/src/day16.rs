use crate::aoc;

struct Packet {
	version: i32,
	packet_data: PacketData,
}

enum PacketData {
	LiteralValue(i64),
	OperatorPacket(OperatorPacketData),
}

struct OperatorPacketData {
	type_id: i32,
	packets: Vec<Packet>,
}

enum OperatorPacketLength {
	LengthInBits(usize),
	NumberOfPackets(usize),
}

impl Packet {
	//
	// everything here is built around a `String` of individual bits, e.g. "0111001".
	//
	// since packets have unknown length, we pass around a `cursor` pointer (&mut usize),
	// to indicate where we currently are within that `String`. this cursor is incremented
	// as each part of the bits string is read
	//

	fn from_hex(s: &str) -> Packet {
		let mut bits = String::new();

		for i in 0..s.len() {
			let v = i32::from_str_radix(&s[i..=i], 16).unwrap();
			bits.push_str(&format!("{:04b}", v));
		}

		return Packet::from_bits(&bits, /* cursor */ &mut 0)
	}

	fn from_bits(bits: &str, cursor: &mut usize) -> Packet {
		//println!("new packet from {}", bits);
		let version = i32::from_str_radix(&bits[*cursor..=*cursor+2], 2).unwrap();
		let type_id = i32::from_str_radix(&bits[*cursor+3..=*cursor+5], 2).unwrap();
		*cursor += 6;

		let packet_data = PacketData::from_bits(bits, cursor, type_id);

		return Packet {
			version,
			packet_data,
		}
	}

	fn sum_of_versions(&self) -> i32 {
		let mut sum = self.version;

		if let PacketData::OperatorPacket(op) = &self.packet_data {
			for sub_packet in &op.packets {
				sum += sub_packet.sum_of_versions();
			}
		}

		return sum
	}

	fn evaluate(&self) -> i64 {
		match &self.packet_data {
			PacketData::LiteralValue(v) => *v,
			PacketData::OperatorPacket(op) => op.evaluate(),
		}
	}
}

impl PacketData {
	fn from_bits(bits: &str, cursor: &mut usize, type_id: i32) -> PacketData {
		//println!("new packetData from {}", bits);
		match type_id {
			4 => return PacketData::LiteralValue(PacketData::literal_value(bits, cursor)),
			_ => return PacketData::OperatorPacket(OperatorPacketData::from_bits(bits, cursor, type_id)),
		}
	}

	fn literal_value(bits: &str, cursor: &mut usize) -> i64 {
		//println!("new literal from {} cursor {}", bits, *cursor);
		let mut literal_bits = String::new();

		let mut keep_reading = "1";
		while keep_reading == "1" {
			keep_reading = &bits[*cursor..=*cursor];
			literal_bits.push_str(&bits[*cursor+1..=*cursor+4]);
			*cursor += 5;
		}

		//println!("literal: {}", i64::from_str_radix(&literal_bits, 2).unwrap());
		return i64::from_str_radix(&literal_bits, 2).unwrap();
	}
}

impl OperatorPacketData {
	fn from_bits(bits: &str, cursor: &mut usize, type_id: i32) -> OperatorPacketData {
		let mut packets = Vec::<Packet>::new();

		//println!("new oper packet, bits = {:?}", bits);
		match OperatorPacketLength::from_bits(bits, cursor) {
			OperatorPacketLength::LengthInBits(length) => {
				let cursor_at_start = *cursor;
				while *cursor - cursor_at_start < length {
					packets.push(Packet::from_bits(bits, cursor));
				}
			},
			OperatorPacketLength::NumberOfPackets(length) => {
				for _ in 0..length {
					packets.push(Packet::from_bits(bits, cursor));
				}
			}
		}

		return OperatorPacketData {
			type_id,
			packets,
		}
	}

	fn evaluate(&self) -> i64 {
		let values = self.packets.iter().map(|p| p.evaluate()).collect::<Vec<_>>();

		match &self.type_id {
			0 => values.iter().sum(),
			1 => values.iter().fold(1, |product, v| product * v),
			2 => *values.iter().min().unwrap(),
			3 => *values.iter().max().unwrap(),
			5 => if values[0] > values[1] { 1 } else { 0 },
			6 => if values[0] < values[1] { 1 } else { 0 },
			7 => if values[0] == values[1] { 1 } else { 0 },
			_ => panic!(),
		}
	}
}

impl OperatorPacketLength {
	fn from_bits(bits: &str, cursor: &mut usize) -> OperatorPacketLength {
		match &bits[*cursor..=*cursor] {
			"0" => {
				let length = usize::from_str_radix(&bits[*cursor+1..=*cursor+15], 2).unwrap();
				*cursor += 16;
				return OperatorPacketLength::LengthInBits(length)
			},
			"1" => {
				let length = usize::from_str_radix(&bits[*cursor+1..=*cursor+11], 2).unwrap();
				*cursor += 12;
				return OperatorPacketLength::NumberOfPackets(length)
			},
			_ => panic!(),
		}
	}
}

pub fn part1(input: String) -> String {
	let packet = Packet::from_hex(&input);
	return packet.sum_of_versions().to_string()
}

pub fn part2(input: String) -> String {
	let packet = Packet::from_hex(&input);
	return packet.evaluate().to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 16,
	input: "file:16-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("6", "D2FE28"),
		("9", "38006F45291200"),
		("14", "EE00D40C823060"),
		("16", "8A004A801A8002F478"),
		("12", "620080001611562C8802118E34"),
		("23", "C0015000016115A2E0802F182340"),
		("31", "A0016C880162017C3686B18A3D4780"),
	],
	tests_part2: &[
		("3", "C200B40A82"),
		("54", "04005AC33890"),
		("7", "880086C3E88112"),
		("9", "CE00C43D881120"),
		("1", "D8005AC2A8F0"),
		("0", "F600BC2D8F"),
		("0", "9C005AC2F8F0"),
		("1", "9C0141080250320F1802104A08"),
	],
};

