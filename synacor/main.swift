import Foundation

var enable_debug = 0
var suppress_debug = false
var indent = 0

let challenge_input = try! Data(contentsOf: URL(fileURLWithPath: "challenge.bin"))

var memory = [Int](repeating: 0, count: 1<<15)
var register = [Int](repeating: 0, count: 8)
var stack = [Int]()
var inputBuffer = ""

var ip = 0 // instruction pointer
var ic = 0 // instruction counter

// copy challenge to "int" memory
for i in 0..<challenge_input.count/2 {
	let low = Int(challenge_input[i*2])
	let high = Int(challenge_input[i*2 + 1])
	memory[i] = (high << 8) | low
}

ip = 0

if true && ip == 0 {
	// disable teleport verification (change the call into setting r1 to the expected value)
	let tca = SCI(byName: "TeleportStartCheck").address
	memory[tca + 0] = 1 // set r0 to 6
	memory[tca + 1] = 32768
	memory[tca + 2] = 6
	// tca+3...5: set r1 (leave it)
	memory[tca + 6] = 21 // nop away the check routine call
	memory[tca + 7] = 21
}

while true {
	let instruction = memory[ip]
	var a = SCRef(memory[ip + 1])
	let b = SCRef(memory[ip + 2])
	let c = SCRef(memory[ip + 3])

	ic += 1

	d2("ip=\(ip) instruction=\(instruction) a=\(a) b=\(b) c=\(c)")
	if false && ic % 906_850 == 0 {
		print("Enough!")
		print("------------------------------------------------------------------------")
		print("ic: \(ic)")
		print("registers: \(register)")
		print("stack: (\(stack.count)) \(stack[0..<min(stack.count, 100)])")
		print("------------------------------------------------------------------------")
		exit(0)
	}

	//if ip == SCI(byName: "Teleport").address { enable_debug = 1 }
	if ip == SCI(byName: "TextOutputRet").address { suppress_debug = false }
	if ip == SCI(byName: "TextOutputRet2").address { suppress_debug = false }
	//if ip == SCI(byName: "TeleportDoneRet").address { register[7] = 0 }

	switch instruction {
	case 0: // halt
		print("Halt!")
		exit(0)
	case 1: // set
		a.value = b.value
		d1("ip=\(ip) set \(a.location) = \(b)")
		ip += 2
	case 2: // push
		d1("ip=\(ip) push \(a)")
		stack.append(a.value)
		ip += 1
	case 3: // pop
		a.value = stack.popLast()!
		d1("ip=\(ip) pop \(a)")
		ip += 1
	case 4: // eq
		d1("ip=\(ip) eq, \(a.location) = \(b) == \(c)")
		a.value = (b.value == c.value) ? 1 : 0
		ip += 3
	case 5: // gt
		d1("ip=\(ip) gt, \(a.location) = \(b) > \(c)")
		a.value = (b.value > c.value) ? 1 : 0
		ip += 3
	case 6: // jump
		d1("ip=\(ip) jump to \(SCI(a.value))")
		ip = a.value
		continue
	case 7: // jump-if-true
		d1("ip=\(ip) jump to \(SCI(b.value)) if \(a)")
		if a.value != 0 { 
			ip = b.value
			continue
		}
		ip += 2
	case 8: // jump-if-false
		d1("ip=\(ip) jump to \(SCI(b.value)) if NOT \(a)")
		if a.value == 0 { 
			ip = b.value
			continue
		}
		ip += 2
	case 9: // add
		d1("ip=\(ip) add \(a.location) = \(b) + \(c)")
		a.value = (b.value + c.value) % 32768
		ip += 3
	case 10: // mult
		d1("ip=\(ip) mult \(a.location) = \(b) * \(c)")
		a.value = (b.value * c.value) % 32768
		ip += 3
	case 11: // mod
		d1("ip=\(ip) mod \(a.location) = \(b) % \(c)")
		a.value = (b.value % c.value)
		ip += 3
	case 12: // bitand
		d1("ip=\(ip) and, \(a.location) = \(b) & \(c)")
		a.value = (b.value & c.value)
		ip += 3
	case 13: // bitor
		d1("ip=\(ip) or, \(a.location) = \(b) | \(c)")
		a.value = (b.value | c.value)
		ip += 3
	case 14: // bitnot
		d1("ip=\(ip) not, \(a.location) = ~\(b)")
		a.value = ~b.value & 0x7fff
		ip += 2
	case 15: // rmem
		a.value = memory[b.value]
		d1("ip=\(ip) rmem, \(a.location) = @\(b) (\(a.value))")
		ip += 2
	case 16: // wmem
		memory[a.value] = b.value
		d1("ip=\(ip) wmem, address \(a.location) = \(b)")
		ip += 2
	case 17: // call
		let dest = SCI(a.value)
		d1("ip=\(ip) call \(dest)")
		if dest == SCI(byName: "TextOutput") { suppress_debug = true }
		if dest == SCI(byName: "TextOutputPrint") { suppress_debug = true }
		indent += 2
		stack.append(ip + 2)
		ip = a.value
		continue
	case 18: // ret
		if let newIp = stack.popLast() {
			d1("ip=\(ip) ret -> \(SCI(newIp))")
			indent -= 2
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
		d2("buffer: \(inputBuffer)")
		a.value = Int(readCommandChar().asciiValue!)
		ip += 1
	case 21: // nop
		d1("ip=\(ip) nop")
		break
	default:
		fatalError("Unknown instruction \(instruction) at ip=\(ip)")
	}

	ip += 1
}

func readCommandChar() -> Character {
	while inputBuffer.isEmpty {
		inputBuffer = readCommand()
	}

	return inputBuffer.removeFirst()
}

func readCommand() -> String {
	var line: String

	if !SCScript.isEmpty {
		line = SCScript.removeFirst()
	} else {
		print("[orbweight=\(memory[3952])] [orbsteps=\(memory[3953])] " +
			"[orbtime=\(memory[3954])] input> ", terminator: "")
		line = readLine()!
	}

	switch line {
	case "dump":
		print("registers: \(register)")
		print("stack: \(stack)")
		print("addr3954: \(memory[3954])")
	case "debug": enable_debug = (enable_debug == 1) ? 0 : 1
	case "t0":
		register[0] = 29400
		register[1] = 1531
		register[2] = 860 + 6795
	case "text": ip = SCI(byName: "TextOutput").address - 2
	case "set7": register[7] = 25734
	default: return line + "\n"
	}

	return ""
}

func d1(_ message: String) { debugPrint(message, level: 1) }
func d2(_ message: String) { debugPrint(message, level: 2) }
func debugPrint(_ message: String, level: Int) {
	if enable_debug >= level && !suppress_debug {
		print(String(repeating: " ", count: min(indent, 100)) + message)
	}
}

