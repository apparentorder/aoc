#!/bin/sh

calcfuel() {
	echo $(( $1 / 3 - 2 ))
}

calcfuel2() {
	mass="$1"

	fuel=$(( $mass / 3 - 2 ))
	totalfuel=0

	while test "$fuel" -gt 0; do
		mass="$fuel"
		#echo "$totalfuel + $fuel" >&2
		totalfuel=$(( $totalfuel + $fuel ))
		fuel=$(( $mass / 3 - 2 ))
	done

	echo "$totalfuel"
}

if false; then
	calcfuel2 14
	calcfuel2 1969
	calcfuel2 100756
	exit 0
fi

totalfuel=0
while read mass; do
	fuel=`calcfuel2 "$mass"`
	totalfuel=$(( $totalfuel + $fuel ))
	echo "$mass -> $fuel [$totalfuel]"
done < aoc1in

