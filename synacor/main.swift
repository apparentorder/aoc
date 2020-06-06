import Foundation

//import SCRef

let enable_debug = 0

let challenge_input = try! Data(contentsOf: URL(fileURLWithPath: "challenge.bin"))

var memory = [Int](repeating: 0, count: 1<<15)
var register = [Int](repeating: 0, count: 8)
var stack = [Int]()
var inputBuffer = ""

var ip = 0 // instruction pointer

while ip < challenge_input.count {
	let low = Int(challenge_input[ip])
	let high = Int(challenge_input[ip + 1])

	let n = (high << 8) | low

	memory[ip/2] = n
	ip += 2
}

ip = 0

while true {
	let instruction = memory[ip]
	var a = SCRef(memory[ip + 1])
	let b = SCRef(memory[ip + 2])
	let c = SCRef(memory[ip + 3])

	d2("ip=\(ip) instruction=\(instruction) a=\(a) b=\(b) c=\(c)")

	switch instruction {
	case 0: // halt
		print("Halt!")
		exit(0)
	case 1: // set
		d1("ip=\(ip) set a=\(a) to b=\(b)")
		a.value = b.value
		ip += 2
	case 2: // push
		d1("ip=\(ip) push a=\(a)")
		stack.append(a.value)
		ip += 1
	case 3: // pop
		d1("ip=\(ip) pop a=\(a)")
		a.value = stack.popLast()!
		ip += 1
	case 4: // eq
		d1("ip=\(ip) eq, a=\(a) b=\(b) c=\(c)")
		a.value = (b.value == c.value) ? 1 : 0
		ip += 3
	case 5: // gt
		d1("ip=\(ip) gt, a=\(a) b=\(b) c=\(c)")
		a.value = (b.value > c.value) ? 1 : 0
		ip += 3
	case 6: // jump
		d1("ip=\(ip) jump to \(a)")
		ip = Int(a.value)
		continue
	case 7: // jump-if-true
		d1("ip=\(ip) jump to \(b) if \(a)")
		if a.value != 0 { 
			ip = Int(b.value)
			continue
		}
		ip += 2
	case 8: // jump-if-false
		d1("ip=\(ip) jump to \(b) if NOT \(a)")
		if a.value == 0 { 
			ip = Int(b.value)
			continue
		}
		ip += 2
	case 9: // add
		d1("ip=\(ip) add a=\(a) b=\(b) c=\(c)")
		a.value = (b.value + c.value) % 32768
		ip += 3
	case 10: // mult
		d1("ip=\(ip) mult a=\(a) b=\(b) c=\(c)")
		a.value = (b.value * c.value) % 32768
		ip += 3
	case 11: // mod
		d1("ip=\(ip) mod a=\(a) b=\(b) c=\(c)")
		a.value = (b.value % c.value)
		ip += 3
	case 12: // bitand
		d1("ip=\(ip) and, a=\(a) b=\(b) c=\(c)")
		a.value = (b.value & c.value)
		ip += 3
	case 13: // bitor
		d1("ip=\(ip) or, a=\(a) b=\(b) c=\(c)")
		a.value = (b.value | c.value)
		ip += 3
	case 14: // bitnot
		d1("ip=\(ip) not, a=\(a) b=\(b)")
		a.value = ~b.value & 0x7fff
		ip += 2
	case 15: // rmem
		d1("ip=\(ip) rmem, a=\(a) b=\(b)")
		a.value = memory[b.value]
		ip += 2
	case 16: // wmem
		d1("ip=\(ip) wmem, a=\(a) b=\(b)")
		memory[a.value] = b.value
		ip += 2
	case 17: // call
		d1("ip=\(ip) call, a=\(a)")
		stack.append(ip + 2)
		ip = a.value
		continue
	case 18: // ret
		d1("ip=\(ip) ret")
		if let newIp = stack.popLast() {
			ip = newIp
			continue
		}
		print("empty pop in ret, halt.")
		exit(0)
	case 19: // write ascii
		let char = Character(UnicodeScalar(a.value)!)
		print(char, terminator: "")
		ip += 1
	case 20: // read ascii (promise: at least until \n)
		d1("buffer: \(inputBuffer)")
		while inputBuffer.isEmpty {
			print("input> ", terminator: "")
			inputBuffer = readLine(strippingNewline: false)!
		}
		a.value = Int(inputBuffer.removeFirst().asciiValue!)
		ip += 1
	case 21: // nop
		break
	default:
		fatalError("Unknown instruction \(instruction) at ip=\(ip)")
	}

	ip += 1
}

func d1(_ message: String) {
	if enable_debug >= 1 { print(message) }
}

func d2(_ message: String) {
	if enable_debug >= 2 { print(message) }
}

