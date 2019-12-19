#!/usr/bin/env swift -O

import Foundation

let inputExample1 = "80871224585914546619083218645595"
let inputExample2 = "19617804207202209144916044189917"
let inputExample3 = "69317163492948606335995924319873"

let inputExample1Part2 = "03036732577212944063491565474664"
let inputExample2Part2 = "02935109699940807407585447034323"
let inputExample3Part2 = "03081770884921959731165446850517"

let inputActual   = "59715091976660977847686180472178988274868874248912891927881770506416128667679122958792624406231072013221126623881489317912309763385182133601840446469164152094801911846572235367585363091944153574934709408511688568362508877043643569519630950836699246046286262479407806494008328068607275931633094949344281398150800187971317684501113191184838118850287189830872128812188237680673513745269645219228183633986701871488467284716433953663498444829748364402022393727938781357664034739772457855166471802886565257858813291667525635001823584650420815316132943869499800374997777130755842319153463895364409226260937941771665247483191282218355610246363741092810592458"

let debugEnabled = false

func debug(_ s: String = "", terminator: String = "\n") {
	if debugEnabled {
		print(s, terminator: terminator)
	}
}

func toIntArray(_ s: String) -> [Int] {
	var out = [Int]()

	for c in s {
		out += [Int(String(c))!]
	}

	return out
}

func fftMutate2(_ inputSignal: [Int], offset: Int = 0) -> [Int] {
	// we prepend a 0, as a counter-measure for the
	// missing first element of the mutation pattern.
	// we can safely do this, because the very first
	// digit will always be 0 (because the pattern starts
	// with 0, so it's always x*0)
	let input = [0] + inputSignal
	var out = [Int](repeating: 0, count: input.count)

	let optimize = true

	var outdigit = 0

	for outputpos in (offset + 1) ..< input.count {
		outdigit = 0

		if optimize && outputpos > input.count/2 {
			// express mode: for positions beyond half of the
			// length, we know that everything before here is *0
			// and everything after here is *1, so we can go
			// backwards and fill up

			var Xoutputpos = input.count - 1
			var X = 0
			while Xoutputpos > input.count/2 {
				X += input[Xoutputpos]
				out[Xoutputpos] = abs(X) % 10
				Xoutputpos -= 1
			}

			// aaaaaand we're done.
			break
		}

		// outpos[0] =  0  1  0 -1  0  1  0 -1  0
		// outpos[1] =  0  0  1  1  0  0 -1 -1  0
		// outpos[2] =  0  0  0  1  1  1  0  0  0
		// outpos[3] =  0  0  0  0  1  1  1  1  0 
		// 'member: that's WITH the prepended input digit
		//
		// we can skip the first <outputpos> digits because
		// they will always be x*0
		//

		var inputpos = outputpos
		while inputpos < input.count {
			switch (inputpos*4 / (outputpos * 4)) % 4 {
			case 0, 2: // *0
				// if we arrive here, then it must be the first 0
				// of this block and so we can skip the block
				//debug("\(input[inputpos])*0   ", terminator: "")
				break
			case 1: // *1
				//debug("\(input[inputpos])*1   ", terminator: "")
				outdigit += input[inputpos]
			case 3: // -1
				//debug("\(input[inputpos])*-1   ", terminator: "")
				outdigit -= input[inputpos]
			default:
				// *1 ?!?!?
				//debug("\(input[inputpos])*???   ", terminator: "")
				print("hä?")
				exit(1)
			}
			inputpos += 1
		}

		outdigit = abs(outdigit) % 10
		//debug("= \(outdigit)")
		out[outputpos] = outdigit
	}

	// remove the extra digit we prepended
	out.remove(at: 0)

	return out
}

//let inputSignal = toIntArray(inputExample3Part2)
let inputSignal = toIntArray(inputActual)
let part2 = true
var signal = inputSignal
var offset = 0
var offsetRange = 0 ..< 8

if part2 {
	var s = ""
	for d in signal[0..<7] {
		s = "\(s)\(d)"
	}
	offset = Int(s)!
	offsetRange = offset ..< offset + 8
	print("offset: \(offsetRange)")

	for _ in 1 ..< 10000 {
		signal += inputSignal
	}

	print("signal len:       \(inputSignal.count)")
	print("total signal len: \(signal.count)")
}

let start = Date()
for phase in 1 ... 100 {
	signal = fftMutate2(signal, offset: offset)
	print("after phase \(phase) => \(signal[offsetRange])")
}
let end = Date()

print("inputSignal*10000 fft100 => \(signal[offsetRange])")
print("time: \(end.timeIntervalSince(start))")

