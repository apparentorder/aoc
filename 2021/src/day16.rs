use crate::aoc;

struct Packet {
	version: i32,
	packet_type: PacketType,
}

enum PacketType {
	LiteralValue(i64),
	OperatorPacket(OperatorPacketData),
}

struct OperatorPacketData {
	length_type_id: char,
	operation: Operation,
	packets: Vec<Packet>,
}

enum Operation {
	Sum,
	Product,
	Minimum,
	Maximum,
	GreaterThan,
	LessThan,
	EqualTo,
}

impl Packet {
	fn from_hex(s: &str) -> Packet {
		let mut bits = String::new();

		for hexchar in s.chars() {
			let v = i32::from_str_radix(&hexchar.to_string(), 16).unwrap();
			let vbits = format!("{:04b}", v);
			bits.push_str(&vbits.chars().collect::<String>());
		}

		return Packet::from_bits(&mut bits)
	}

	fn from_bits(s: &mut String) -> Packet {
		//println!("new packet from {}", s);
		let version = i32::from_str_radix(&s[0..=2], 2).unwrap();
		let type_id = i32::from_str_radix(&s[3..=5], 2).unwrap();
		*s = s[6..].to_string();

		let packet_type = PacketType::new(type_id, s);

		return Packet {
			version,
			packet_type,
		}
	}
}

impl Operation {
	fn from_type(type_id: i32) -> Operation {
		match type_id {
			0 => Operation::Sum,
			1 => Operation::Product,
			2 => Operation::Minimum,
			3 => Operation::Maximum,
			5 => Operation::GreaterThan,
			6 => Operation::LessThan,
			7 => Operation::EqualTo,
			_ => panic!(),
		}
	}
}

impl OperatorPacketData {
	fn new(s: &mut String, type_id: i32) -> OperatorPacketData {
		let mut packets = Vec::<Packet>::new();

		let operation = Operation::from_type(type_id);

		let length_type_id = s.chars().nth(0).unwrap();

		let length;
		if length_type_id == '0' {
			length = i32::from_str_radix(&s[1..=15], 2).unwrap();
			//println!("new oper packet, length {} bits = {:?}", length, s);
			*s = s[16..].to_string();
		} else {
			length = i32::from_str_radix(&s[1..=11], 2).unwrap();
			//println!("new oper packet, length {} PACKETS = {:?}", length, s);
			*s = s[12..].to_string();
		}

		if length_type_id == '0' {
			//*s = &s[length..(s.len() - length)].to_string();
			let mut sub_s = String::new();
			sub_s.push_str(&s[0..length as usize]);

			while !sub_s.is_empty() {
				packets.push(Packet::from_bits(&mut sub_s));
			}

			*s = s[length as usize..].to_string();
		} else /* length in packets */ {
			for _ in 0..length {
				packets.push(Packet::from_bits(s));
			}
		}

		return OperatorPacketData {
			length_type_id,
			operation,
			packets,
		}
	}
}

impl PacketType {
	fn new(type_id: i32, s: &mut String) -> PacketType {
		//println!("new packetType from {}", s);
		match type_id {
			4 => return PacketType::LiteralValue(PacketType::literal_value(s)),
			_ => return PacketType::OperatorPacket(OperatorPacketData::new(s, type_id)),
		}
	}

	fn literal_value(s: &mut String) -> i64 {
		//println!("new literal from {}", s);
		let mut bits = String::new();

		loop {
			let keep_reading = s.chars().nth(0).unwrap();
			bits.push_str(&s[1..=4]);
			*s = s[5..].to_string();

			if keep_reading == '0' {
				break
			}
		}

		//println!("literal: {}", i64::from_str_radix(&bits, 2).unwrap());
		return i64::from_str_radix(&bits, 2).unwrap();
	}
}

fn version_sum(packet: &Packet) -> i32 {
	let mut sum = packet.version;

	if let PacketType::OperatorPacket(op) = &packet.packet_type {
		for subpacket in &op.packets {
			sum += version_sum(&subpacket);
		}
	}

	return sum
}

fn run_operation(op: &OperatorPacketData) -> i64 {
	let values = op.packets.iter().map(|p| eval_packet(p)).collect::<Vec<_>>();

	match &op.operation {
		Operation::Sum => values.iter().sum(),
		Operation::Product => values.iter().fold(1, |product, v| product * v),
		Operation::Minimum => *values.iter().min().unwrap(),
		Operation::Maximum => *values.iter().max().unwrap(),
		Operation::GreaterThan => if values[0] > values[1] { 1 } else { 0 },
		Operation::LessThan => if values[0] < values[1] { 1 } else { 0 },
		Operation::EqualTo => if values[0] == values[1] { 1 } else { 0 },
	}
}

fn eval_packet(packet: &Packet) -> i64 {
	match &packet.packet_type {
		PacketType::LiteralValue(v) => *v,
		PacketType::OperatorPacket(op) => run_operation(&op),
	}
}

pub fn part1(input: String) -> String {
	let packet = Packet::from_hex(&input);
	return version_sum(&packet).to_string()
}

pub fn part2(input: String) -> String {
	let packet = Packet::from_hex(&input);
	return eval_packet(&packet).to_string()
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

