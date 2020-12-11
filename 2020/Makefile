all: aoc2020 aoc2020-debug
debug: aoc2020-debug

aoc2020: *.swift
	swiftc -O -o aoc2020 *.swift

aoc2020-debug: *.swift
	swiftc -Onone -g -DDEBUG -o aoc2020-debug *.swift

clean:
	rm -f aoc2020 aoc2020-debug

