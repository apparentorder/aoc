from __future__ import annotations
from .coordinate import Coordinate, DistanceAlgorithm, Shape
from .types import Numeric
from enum import Enum
from heapq import heappop, heappush
from math import inf
from typing import Any, Dict, List, Union

OFF = False
ON = True


class GridTransformation(Enum):
    # Rotations always take the axis to rotate around as if it were the z-axis and then rotate clockwise
    # Counter-Rotations likewise, just anti-clockwise
    # 3D-only OPs have a number > 10
    ROTATE_Z = 3
    ROTATE_X = 11
    ROTATE_Y = 12
    COUNTER_ROTATE_X = 14
    COUNTER_ROTATE_Y = 15
    COUNTER_ROTATE_Z = 7
    FLIP_X = 4
    FLIP_Y = 5
    FLIP_Z = 13

    # Handy aliases
    FLIP_HORIZONTALLY = 5
    FLIP_VERTICALLY = 4
    ROTATE_RIGHT = 3
    ROTATE_LEFT = 7


class Grid:
    def __init__(self, default=False):
        self.__default = default
        self.__grid = {}
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None
        self.minZ = None
        self.maxZ = None
        self.mode3D = False

    def __trackBoundaries(self, pos: Coordinate):
        if self.minX is None:
            self.minX, self.maxX, self.minY, self.maxY = pos.x, pos.x, pos.y, pos.y
        else:
            self.minX = pos.x if pos.x < self.minX else self.minX
            self.minY = pos.y if pos.y < self.minY else self.minY
            self.maxX = pos.x if pos.x > self.maxX else self.maxX
            self.maxY = pos.y if pos.y > self.maxY else self.maxY

        if self.mode3D:
            if self.minZ is None:
                self.minZ = self.maxZ = pos.z
            else:
                self.minZ = pos.z if pos.z < self.minZ else self.minZ
                self.maxZ = pos.z if pos.z > self.maxZ else self.maxZ

    def getBoundaries(self) -> (int, int, int, int, int, int):
        if self.mode3D:
            return self.minX, self.minY, self.maxX, self.maxY, self.minZ, self.maxZ
        else:
            return self.minX, self.minY, self.maxX, self.maxY, -inf, inf

    def rangeX(self, pad: int = 0, reverse=False):
        if reverse:
            return range(self.maxX + pad, self.minX - pad - 1, -1)
        else:
            return range(self.minX - pad, self.maxX + pad + 1)

    def rangeY(self, pad: int = 0, reverse=False):
        if reverse:
            return range(self.maxY + pad, self.minY - pad - 1, -1)
        else:
            return range(self.minY - pad, self.maxY + pad + 1)

    def rangeZ(self, pad: int = 0, reverse=False):
        if not self.mode3D:
            raise ValueError("rangeZ not available in 2D space")
        if reverse:
            return range(self.maxZ + pad, self.minZ - pad - 1, -1)
        else:
            return range(self.minZ - pad, self.maxZ + pad + 1)

    def toggle(self, pos: Coordinate):
        if pos in self.__grid:
            del self.__grid[pos]
        else:
            self.__trackBoundaries(pos)
            self.__grid[pos] = not self.__default

    def toggleGrid(self):
        for x in self.rangeX():
            for y in self.rangeY():
                if not self.mode3D:
                    self.toggle(Coordinate(x, y))
                else:
                    for z in self.rangeZ():
                        self.toggle(Coordinate(x, y, z))

    def set(self, pos: Coordinate, value: Any = True) -> Any:
        if pos.z is not None:
            self.mode3D = True

        if (value == self.__default) and pos in self.__grid:
            del self.__grid[pos]
        elif value != self.__default:
            self.__trackBoundaries(pos)
            self.__grid[pos] = value

        return value

    def add(self, pos: Coordinate, value: Numeric = 1) -> Numeric:
        return self.set(pos, self.get(pos) + value)

    def sub(self, pos: Coordinate, value: Numeric = 1) -> Numeric:
        return self.set(pos, self.get(pos) - value)

    def mul(self, pos: Coordinate, value: Numeric = 1) -> Numeric:
        return self.set(pos, self.get(pos) * value)

    def div(self, pos: Coordinate, value: Numeric = 1) -> Numeric:
        return self.set(pos, self.get(pos) / value)

    def add_shape(self, shape: Shape, value: Numeric = 1) -> None:
        for x in range(shape.top_left.x, shape.bottom_right.x + 1):
            for y in range(shape.top_left.y, shape.bottom_right.y + 1):
                if not shape.mode_3d:
                    pos = Coordinate(x, y)
                    self.set(pos, self.get(pos) + value)
                else:
                    for z in range(shape.top_left.z, shape.bottom_right.z + 1):
                        pos = Coordinate(x, y, z)
                        self.set(pos, self.get(pos) + value)

    def get(self, pos: Coordinate) -> Any:
        return self.__grid.get(pos, self.__default)

    def getOnCount(self) -> int:
        return len(self.__grid)

    def isSet(self, pos: Coordinate) -> bool:
        return pos in self.__grid

    def getCorners(self) -> List[Coordinate]:
        if not self.mode3D:
            return [
                Coordinate(self.minX, self.minY),
                Coordinate(self.minX, self.maxY),
                Coordinate(self.maxX, self.minY),
                Coordinate(self.maxX, self.maxY),
            ]
        else:
            return [
                Coordinate(self.minX, self.minY, self.minZ),
                Coordinate(self.minX, self.minY, self.maxZ),
                Coordinate(self.minX, self.maxY, self.minZ),
                Coordinate(self.minX, self.maxY, self.maxZ),
                Coordinate(self.maxX, self.minY, self.minZ),
                Coordinate(self.maxX, self.minY, self.maxZ),
                Coordinate(self.maxX, self.maxY, self.minZ),
                Coordinate(self.maxX, self.maxY, self.maxZ),
            ]

    def isCorner(self, pos: Coordinate) -> bool:
        return pos in self.getCorners()

    def isWithinBoundaries(self, pos: Coordinate) -> bool:
        if self.mode3D:
            return self.minX <= pos.x <= self.maxX and self.minY <= pos.y <= self.maxY \
                   and self.minZ <= pos.z <= self.maxZ
        else:
            return self.minX <= pos.x <= self.maxX and self.minY <= pos.y <= self.maxY

    def getActiveCells(self, x: int = None, y: int = None) -> List[Coordinate]:
        if x:
            return [c for c in self.__grid.keys() if c.x == x]
        elif y:
            return [c for c in self.__grid.keys() if c.y == y]
        else:
            return list(self.__grid.keys())

    def getActiveRegion(self, start: Coordinate, includeDiagonal: bool = False, ignore: List[Coordinate] = None) \
        -> List[Coordinate]:
        if not self.get(start):
            return []
        if ignore is None:
            ignore = []
        ignore.append(start)
        for c in self.getNeighboursOf(start, includeDiagonal=includeDiagonal):
            if c not in ignore:
                ignore = self.getActiveRegion(c, includeDiagonal, ignore)

        return ignore

    def values(self):
        return self.__grid.values()

    def getSum(self, includeNegative: bool = True) -> Numeric:
        if not self.mode3D:
            return sum(
                self.get(Coordinate(x, y))
                for x in self.rangeX()
                for y in self.rangeY()
                if includeNegative or self.get(Coordinate(x, y)) >= 0
            )
        else:
            return sum(
                self.get(Coordinate(x, y, z))
                for x in self.rangeX()
                for y in self.rangeY()
                for z in self.rangeZ()
                if includeNegative or self.get(Coordinate(x, y)) >= 0
            )

    def getNeighboursOf(self, pos: Coordinate, includeDefault: bool = False, includeDiagonal: bool = True) \
            -> List[Coordinate]:
        neighbours = pos.getNeighbours(
            includeDiagonal=includeDiagonal,
            minX=self.minX, minY=self.minY, minZ=self.minZ,
            maxX=self.maxX, maxY=self.maxY, maxZ=self.maxZ
        )
        if includeDefault:
            return neighbours
        else:
            return [x for x in neighbours if x in self.__grid]

    def getNeighbourSum(self, pos: Coordinate, includeNegative: bool = True, includeDiagonal: bool = True) -> Numeric:
        neighbour_sum = 0
        for neighbour in self.getNeighboursOf(pos, includeDefault=includeDiagonal):
            if includeNegative or self.get(neighbour) > 0:
                neighbour_sum += self.get(neighbour)

        return neighbour_sum

    def flip(self, c1: Coordinate, c2: Coordinate):
        buf = self.get(c1)
        self.set(c1, self.get(c2))
        self.set(c2, buf)

    def transform(self, mode: GridTransformation):
        if mode.value > 10 and not self.mode3D:
            raise ValueError("Operation not possible in 2D space", mode)

        coords = self.__grid
        self.__grid, self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ = {}, 0, 0, 0, 0, 0, 0
        if mode == GridTransformation.ROTATE_X:
            for c, v in coords.items():
                self.set(Coordinate(c.x, -c.z, c.y), v)
        elif mode == GridTransformation.ROTATE_Y:
            for c, v in coords.items():
                self.set(Coordinate(-c.z, c.y, c.x), v)
        elif mode == GridTransformation.ROTATE_Z:
            for c, v in coords.items():
                self.set(Coordinate(c.y, -c.x, c.z), v)
        elif mode == GridTransformation.COUNTER_ROTATE_X:
            for c, v in coords.items():
                self.set(Coordinate(c.x, c.z, -c.y), v)
        elif mode == GridTransformation.COUNTER_ROTATE_Y:
            for c, v in coords.items():
                self.set(Coordinate(c.z, c.y, -c.x), v)
        elif mode == GridTransformation.COUNTER_ROTATE_Z:
            for c, v in coords.items():
                self.set(Coordinate(-c.y, c.x, c.z), v)
        elif mode == GridTransformation.FLIP_X:
            for c, v in coords.items():
                self.set(Coordinate(-c.x, c.y, c.z), v)
        elif mode == GridTransformation.FLIP_Y:
            for c, v in coords.items():
                self.set(Coordinate(c.x, -c.y, c.z), v)
        elif mode == GridTransformation.FLIP_Z:
            for c, v in coords.items():
                self.set(Coordinate(c.x, c.y, -c.z), v)
        else:
            raise NotImplementedError(mode)

    def getPath(self, pos_from: Coordinate, pos_to: Coordinate, includeDiagonal: bool, walls: List[Any] = None,
                weighted: bool = False) -> Union[None, List[Coordinate]]:
        f_costs = []
        if walls is None:
            walls = [self.__default]

        openNodes: Dict[Coordinate, tuple] = {}
        closedNodes: Dict[Coordinate, tuple] = {}

        openNodes[pos_from] = (0, pos_from.getDistanceTo(pos_to), None)
        heappush(f_costs, (0, pos_from))

        while f_costs:
            _, currentCoord = heappop(f_costs)
            if currentCoord not in openNodes:
                continue
            currentNode = openNodes[currentCoord]

            closedNodes[currentCoord] = currentNode
            del openNodes[currentCoord]
            if currentCoord == pos_to:
                break

            for neighbour in self.getNeighboursOf(currentCoord, includeDefault=True, includeDiagonal=includeDiagonal):
                if self.get(neighbour) in walls or neighbour in closedNodes:
                    continue

                if weighted:
                    neighbourDist = self.get(neighbour)
                elif not includeDiagonal:
                    neighbourDist = 1
                else:
                    neighbourDist = currentCoord.getDistanceTo(neighbour, DistanceAlgorithm.MANHATTAN, includeDiagonal)

                targetDist = neighbour.getDistanceTo(pos_to)
                f_cost = targetDist + neighbourDist + currentNode[1]

                if neighbour not in openNodes or f_cost < openNodes[neighbour][0]:
                    openNodes[neighbour] = (f_cost, currentNode[1] + neighbourDist, currentCoord)
                    heappush(f_costs, (f_cost, neighbour))

        if pos_to not in closedNodes:
            return None
        else:
            currentNode = closedNodes[pos_to]
            pathCoords = [pos_to]
            while currentNode[2]:
                pathCoords.append(currentNode[2])
                currentNode = closedNodes[currentNode[2]]

            return pathCoords

    def print(self, spacer: str = "", true_char: str = None, false_char: str = " "):
        for y in range(self.minY, self.maxY + 1):
            for x in range(self.minX, self.maxX + 1):
                if true_char:
                    print(true_char if self.get(Coordinate(x, y)) else false_char, end="")
                else:
                    print(self.get(Coordinate(x, y)), end="")
                print(spacer, end="")

            print()

    def __str__(self):
        s = ""
        for y in range(self.minY, self.maxY + 1):
            for x in range(self.minX, self.maxX + 1):
                s += self.get(Coordinate(x, y))

            s += "\n"

        return s

