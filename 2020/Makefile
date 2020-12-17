all: aoc2020 aoc2020-debug
debug: aoc2020-debug

SWIFTC= swiftc -whole-module-optimization -num-threads 8 -print-educational-notes

aoc2020: *.swift
	$(SWIFTC) -O -o aoc2020 *.swift

aoc2020-debug: *.swift
	$(SWIFTC) -Onone -g -DDEBUG -o aoc2020-debug *.swift

clean:
	rm -f aoc2020 aoc2020-debug

