use crate::aoc;

type BeaconList = Vec<Coord>;
type ScannerList = Vec<BeaconList>;
type BeaconDistanceList = Vec<i32>;
type BeaconPairList<'a> = Vec<(&'a Coord, &'a Coord)>;

#[derive(Debug, PartialEq, Clone, Eq, Hash, Copy)]
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

	fn all_rotations(&self) -> BeaconList {
		let mut beacons = BeaconList::with_capacity(48);

		for &x in &[ self.x, -self.x ] {
			for &y in &[ self.y, -self.y] {
				for &z in &[self.z, -self.z] {
					beacons.push(Coord { x:x, y:y, z:z });
					beacons.push(Coord { x:x, y:z, z:y });
					beacons.push(Coord { x:y, y:x, z:z });
					beacons.push(Coord { x:y, y:z, z:x });
					beacons.push(Coord { x:z, y:x, z:y });
					beacons.push(Coord { x:z, y:y, z:x });
				}
			}
		}

		return beacons
	}
}

fn beacon_distances(beacon_list: &BeaconList, from_beacon: &Coord) -> BeaconDistanceList {
	beacon_list
		.iter()
		.map(|beacon| beacon.distance(from_beacon))
		.filter(|&d| d != 0)
		.collect()
}

fn fixed_beacons(scanner: &BeaconList, reference_pairs: &BeaconPairList) -> (BeaconList, Coord) {
	let reference_rotations = reference_pairs
		.iter()
		.map(|(_reference, unrotated)| unrotated.all_rotations())
		.collect::<Vec<_>>();

	let try_first_reference = reference_pairs[0].0;

	// go through all possible rotations, find one that works for *all* distance-matched beacons
	'rotation: for n_rotation in 0..reference_rotations[0].len() {
		let try_first_rotated = reference_rotations[0][n_rotation];

		let try_scanner_position = Coord {
			x: try_first_reference.x + try_first_rotated.x,
			y: try_first_reference.y + try_first_rotated.y,
			z: try_first_reference.z + try_first_rotated.z,
		};

		for i in 0..reference_pairs.len() {
			let rotated = reference_rotations[i][n_rotation];

			let this_try = Coord {
				x: reference_pairs[i].0.x + rotated.x,
				y: reference_pairs[i].0.y + rotated.y,
				z: reference_pairs[i].0.z + rotated.z,
			};

			if this_try != try_scanner_position {
				continue 'rotation
			}
		}

		// expectation was met for all reference pairs
		// now convert all beacons: rotate into place,
		// then map from the scanner's view to scanner0's view
		let beacons = scanner
			.iter()
			.map(|beacon| {
				let rotated_beacon = beacon.all_rotations()[n_rotation];
				return Coord {
					x: try_scanner_position.x - rotated_beacon.x,
					y: try_scanner_position.y - rotated_beacon.y,
					z: try_scanner_position.z - rotated_beacon.z
				}
			})
			.collect();

		return (beacons, try_scanner_position)
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
						continue
					}
				}

				if beacon_pairs.len() >= 2 {
					// two pairs seem to be sufficient
					break
				}
			}

			if !beacon_pairs.is_empty() {
				let (beacons, scanner_pos) = fixed_beacons(other_scanner, &beacon_pairs);
				//println!("SCANNER: {:?}", expect);
				scanner_positions.push(scanner_pos);

				for b in beacons {
					if !scanner0.contains(&b) {
						scanner0.push(b);
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
		("79", "file:19-input-test"),
	],
	tests_part2: &[
	],
};

