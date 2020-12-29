all: aoc2016 aoc2016-debug
debug: aoc2016-debug

SWIFTC= swiftc -whole-module-optimization -num-threads 8 -print-educational-notes

aoc2016: *.swift
	$(SWIFTC) -O -o aoc2016 *.swift

aoc2016-debug: *.swift
	$(SWIFTC) -Onone -g -DDEBUG -o aoc2016-debug *.swift

clean:
	rm -f aoc2016 aoc2016-debug

