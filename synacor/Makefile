all: sc

clean:
	rm -f sc

run: sc
	./sc

sc: *.swift
	swiftc -O -o sc *.swift

