use crate::aoc;
use std::collections::{HashMap, HashSet};

type BeaconList = Vec<Coord>;
type ScannerList = Vec<BeaconList>;
type BeaconDistanceList = Vec<i32>;
type BeaconPairList<'a> = Vec<(&'a Coord, &'a Coord)>;

#[derive(Debug, PartialEq, Clone, Eq, Hash)]
struct Coord {
	x: i32,
	y: i32,
	z: i32,
}

impl Coord {
	fn distance(&self, target: &Coord) -> i32 {
		(target.x - self.x).abs()
		+ (target.y - self.y).abs()
		+ (target.z - self.z).abs()
	}

	fn rotations(&self) -> Vec<Coord> {
		let mut r = Vec::<Coord>::new();

		let possible_values = [ self.x, -self.x, self.y, -self.y, self.z, -self.z ].to_vec();

		for px in &possible_values {
			for py in &possible_values {
				for pz in &possible_values {
					r.push(Coord { x: px.clone(), y: py.clone(), z: pz.clone() });
				}
			}
		}

		return r
	}
}

fn beacon_distances(beacon_list: &BeaconList, from_beacon: &Coord) -> BeaconDistanceList {
	let mut distances = BeaconDistanceList::new();

	for other_beacon in beacon_list {
		let d = other_beacon.distance(from_beacon);
		if d != 0 {
			distances.push(d);
		}
	}

	return distances
}

fn fixed_beacons(scanner: &BeaconList, reference_pairs: &BeaconPairList) -> (BeaconList, Coord) {
	'rotation: for i in 0..scanner[0].rotations().len() {
		let try_scanners = scanner.iter().map(|s| s.rotations()[i].clone()).collect::<Vec<_>>();
		let try_reference_pairs = reference_pairs.iter().map(|(p0, p1)| (p0, p1.rotations()[i].clone())).collect::<Vec<_>>();
		//println!("{:?} <-> {:?}", try_reference_pairs[0].0, try_reference_pairs[1].1);

		let expect = Coord {
			x: try_reference_pairs[2].0.x - try_reference_pairs[2].1.x,
			y: try_reference_pairs[2].0.y - try_reference_pairs[2].1.y,
			z: try_reference_pairs[2].0.z - try_reference_pairs[2].1.z,
		};
		//println!("   expect {:?}", expect);

		for pair in try_reference_pairs {
			let this_try = Coord {
				x: pair.0.x - pair.1.x,
				y: pair.0.y - pair.1.y,
				z: pair.0.z - pair.1.z,
			};

			if this_try != expect {
				continue 'rotation
			}
		}

		// expectation was met for all reference pairs
		println!("SCANNER: {:?}", expect);
		let really_fixed_beacons = try_scanners.iter().map(|b| Coord {
			x: expect.x + b.x,
			y: expect.y + b.y,
			z: expect.z + b.z
		}).collect();
		return (really_fixed_beacons, expect)
	}
	panic!();
}

fn beacons(scanner_list: &ScannerList) -> (i32, i32) {
	let mut remaining_scanners = scanner_list.clone();
	let mut scanner0 = remaining_scanners.remove(0);
	let mut scanner_positions = BeaconList::new();

	while !remaining_scanners.is_empty() {
		let mut any_matches = false;

		for (other_scanner_index, other_scanner) in remaining_scanners.clone().iter().enumerate() {
			let mut beacon_pairs = BeaconPairList::new();

			for beacon in &scanner0 {
				for other_beacon in other_scanner {
					let mut distances = beacon_distances(&scanner0, &beacon);
					let mut other_distances = beacon_distances(&other_scanner, other_beacon);

					distances.retain(|d| other_distances.contains(d));
					other_distances.retain(|od| distances.contains(od));

					distances.sort();
					other_distances.sort();

					if distances == other_distances && distances.len() >= 11 {
						//println!("match: scanner0={:?} scanner{}={:?}", beacon, other_scanner_index, other_beacon);
						beacon_pairs.push((&beacon, other_beacon));
					}
				}
			}

			if !beacon_pairs.is_empty() {
				let (beacons, scanner_pos) = fixed_beacons(other_scanner, &beacon_pairs);
				scanner_positions.push(scanner_pos);

				for b in beacons {
					if !scanner0.contains(&b) {
						scanner0.push(b.clone());
						//println!("adding s0: {:?}", b);
					}
				}

				remaining_scanners.remove(other_scanner_index);
				any_matches = true;
				break
			}
		}

		assert!(any_matches);
	}

	let mut largest_mhd = 0;
	for s1 in &scanner_positions {
		for s2 in &scanner_positions {
			largest_mhd = largest_mhd.max(s1.distance(&s2));
		}
	}

	return (scanner0.len() as i32, largest_mhd)
}

fn parse(input: &str) -> ScannerList {
	let mut r = ScannerList::new();

	for scanner in input.split("\n\n") {
		let mut scanner_beacons = BeaconList::new();

		for line in scanner.lines() {
			if line.starts_with("--- scanner") {
				continue
			}

			let parts = line.split(',').map(|p| p.parse().unwrap()).collect::<Vec<_>>();
			scanner_beacons.push(Coord { x: parts[0], y: parts[1], z: parts[2] });
		}

		r.push(scanner_beacons);
	}

	return r
}

pub fn part1(input: String) -> String {
	let scanners = parse(&input);
	let (beacon_count, _) = beacons(&scanners);
	return beacon_count.to_string()
}

pub fn part2(input: String) -> String {
	let scanners = parse(&input);
	let (_, mhd) = beacons(&scanners);
	return mhd.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 19,
	input: "file:19-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		//("_", "file:19-input-test-2d"),
		("79", "file:19-input-test"),
	],
	tests_part2: &[
	],
};

