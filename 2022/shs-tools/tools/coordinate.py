from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import gcd, sqrt, inf, atan2, degrees
from .math import round_half_up
from typing import Union, List, Optional


class DistanceAlgorithm(Enum):
    MANHATTAN = 0
    EUCLIDEAN = 1
    PYTHAGOREAN = 1
    CHEBYSHEV = 2
    CHESSBOARD = 2

@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int
    z: Optional[int] = None

    def getDistanceTo(self, target: Coordinate, algorithm: DistanceAlgorithm = DistanceAlgorithm.EUCLIDEAN,
                      includeDiagonals: bool = False) -> Union[int, float]:
        """
        Get distance to target Coordinate

        :param target:
        :param algorithm: Calculation Algorithm (s. DistanceAlgorithm)
        :param includeDiagonals: in Manhattan Mode specify if diagonal
                                 movements are allowed (counts as 1.4 in 2D, 1.7 in 3D)
        :return: Distance to Target
        """
        if algorithm == DistanceAlgorithm.EUCLIDEAN:
            if self.z is None:
                return sqrt(abs(self.x - target.x) ** 2 + abs(self.y - target.y) ** 2)
            else:
                return sqrt(abs(self.x - target.x) ** 2 + abs(self.y - target.y) ** 2 + abs(self.z - target.z) ** 2)
        elif algorithm == DistanceAlgorithm.CHEBYSHEV:
            if self.z is None:
                return max(abs(target.x - self.x), abs(target.y - self.y))
            else:
                return max(abs(target.x - self.x), abs(target.y - self.y), abs(target.z - self.z))
        elif algorithm == DistanceAlgorithm.MANHATTAN:
            if not includeDiagonals:
                if self.z is None:
                    return abs(self.x - target.x) + abs(self.y - target.y)
                else:
                    return abs(self.x - target.x) + abs(self.y - target.y) + abs(self.z - target.z)
            else:
                dist = [abs(self.x - target.x), abs(self.y - target.y)]
                if self.z is None:
                    o_dist = max(dist) - min(dist)
                    return o_dist + 1.4 * min(dist)
                else:
                    dist.append(abs(self.z - target.z))
                    d_steps = min(dist)
                    dist.remove(min(dist))
                    dist = [x - d_steps for x in dist]
                    o_dist = max(dist) - min(dist)
                    return 1.7 * d_steps + o_dist + 1.4 * min(dist)

    def inBoundaries(self, minX: int, minY: int, maxX: int, maxY: int, minZ: int = -inf, maxZ: int = inf) -> bool:
        if self.z is None:
            return minX <= self.x <= maxX and minY <= self.y <= maxY
        else:
            return minX <= self.x <= maxX and minY <= self.y <= maxY and minZ <= self.z <= maxZ

    def getCircle(self, radius: int = 1, algorithm: DistanceAlgorithm = DistanceAlgorithm.EUCLIDEAN,
                  minX: int = -inf, minY: int = -inf, maxX: int = inf, maxY: int = inf,
                  minZ: int = -inf, maxZ: int = inf) -> list[Coordinate]:
        ret = []
        if self.z is None:  # mode 2D
            for x in range(self.x - radius * 2, self.x + radius * 2 + 1):
                for y in range(self.y - radius * 2, self.y + radius * 2 + 1):
                    target = Coordinate(x, y)
                    if not target.inBoundaries(minX, minY, maxX, maxY):
                        continue
                    dist = round_half_up(self.getDistanceTo(target, algorithm=algorithm, includeDiagonals=False))
                    if dist == radius:
                        ret.append(target)

        else:
            for x in range(self.x - radius * 2, self.x + radius * 2 + 1):
                for y in range(self.y - radius * 2, self.y + radius * 2 + 1):
                    for z in range(self.z - radius * 2, self.z + radius * 2 + 1):
                        target = Coordinate(x, y)
                        if not target.inBoundaries(minX, minY, maxX, maxY, minZ, maxZ):
                            continue
                        dist = round_half_up(self.getDistanceTo(target, algorithm=algorithm, includeDiagonals=False))
                        if dist == radius:
                            ret.append(target)

        return ret

    def getNeighbours(self, includeDiagonal: bool = True, minX: int = -inf, minY: int = -inf,
                      maxX: int = inf, maxY: int = inf, minZ: int = -inf, maxZ: int = inf) -> list[Coordinate]:
        """
        Get a list of neighbouring coordinates.

        :param includeDiagonal: include diagonal neighbours
        :param minX: ignore all neighbours that would have an X value below this
        :param minY: ignore all neighbours that would have an Y value below this
        :param minZ: ignore all neighbours that would have an Z value below this
        :param maxX: ignore all neighbours that would have an X value above this
        :param maxY: ignore all neighbours that would have an Y value above this
        :param maxZ: ignore all neighbours that would have an Z value above this
        :return: list of Coordinate
        """
        if self.z is None:
            if includeDiagonal:
                nb_list = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            else:
                nb_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            return [
                Coordinate(self.x + dx, self.y + dy)
                for dx, dy in nb_list
                if minX <= self.x + dx <= maxX and minY <= self.y + dy <= maxY
            ]
        else:
            if includeDiagonal:
                nb_list = [(x, y, z) for x in [-1, 0, 1] for y in [-1, 0, 1] for z in [-1, 0, 1]]
                nb_list.remove((0, 0, 0))
            else:
                nb_list = [(-1, 0, 0), (0, -1, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]

            return [
                Coordinate(self.x + dx, self.y + dy, self.z + dz)
                for dx, dy, dz in nb_list
                if minX <= self.x + dx <= maxX and minY <= self.y + dy <= maxY and minZ <= self.z + dz <= maxZ
            ]

    def getAngleTo(self, target: Coordinate, normalized: bool = False) -> float:
        """normalized returns an angle going clockwise with 0 starting in the 'north'"""
        if self.z is not None:
            raise NotImplementedError()  # which angle?!?!

        dx = target.x - self.x
        dy = target.y - self.y
        if not normalized:
            return degrees(atan2(dy, dx))
        else:
            angle = degrees(atan2(dx, dy))
            if dx >= 0:
                return 180.0 - angle
            else:
                return 180.0 + abs(angle)

    def getLineTo(self, target: Coordinate) -> List[Coordinate]:
        diff = target - self

        if self.z is None:
            steps = gcd(diff.x, diff.y)
            step_x = diff.x // steps
            step_y = diff.y // steps
            return [self.__class__(self.x + step_x * i, self.y + step_y * i) for i in range(steps + 1)]
        else:
            steps = gcd(diff.x, diff.y, diff.z)
            step_x = diff.x // steps
            step_y = diff.y // steps
            step_z = diff.z // steps
            return [self.__class__(self.x + step_x * i, self.y + step_y * i, self.z + step_z * i) for i in range(steps + 1)]

    def __add__(self, other: Coordinate) -> Coordinate:
        if self.z is None:
            return self.__class__(self.x + other.x, self.y + other.y)
        else:
            return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Coordinate) -> Coordinate:
        if self.z is None:
            return self.__class__(self.x - other.x, self.y - other.y)
        else:
            return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __gt__(self, other):
        if self.z is None:
            return self.x > other.x and self.y > other.y
        else:
            return self.x > other.x and self.y > other.y and self.z > other.z

    def __ge__(self, other):
        if self.z is None:
            return self.x >= other.x and self.y >= other.y
        else:
            return self.x >= other.x and self.y >= other.y and self.z >= other.z

    def __lt__(self, other):
        if self.z is None:
            return self.x < other.x and self.y < other.y
        else:
            return self.x < other.x and self.y < other.y and self.z < other.z

    def __le__(self, other):
        if self.z is None:
            return self.x <= other.x and self.y <= other.y
        else:
            return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __str__(self):
        if self.z is None:
            return "(%d,%d)" % (self.x, self.y)
        else:
            return "(%d,%d,%d)" % (self.x, self.y, self.z)

    def __repr__(self):
        if self.z is None:
            return "%s(x=%d, y=%d)" % (self.__class__.__name__, self.x, self.y)
        else:
            return "%s(x=%d, y=%d, z=%d)" % (self.__class__.__name__, self.x, self.y, self.z)

    @staticmethod
    def generate(from_x: int, to_x: int, from_y: int, to_y: int,
                 from_z: int = None, to_z: int = None) -> List[Coordinate]:
        if from_z is None or to_z is None:
            return [self.__class__(x, y) for x in range(from_x, to_x + 1) for y in range(from_y, to_y + 1)]
        else:
            return [
                self.__class__(x, y, z)
                for x in range(from_x, to_x + 1)
                for y in range(from_y, to_y + 1)
                for z in range(from_z, to_z + 1)
            ]


class HexCoordinate(Coordinate):
    """
    https://www.redblobgames.com/grids/hexagons/#coordinates-cube
    Treat as 3d Coordinate
    +y   -x   +z
      y  x  z
        yxz
      z  x  y
    -z   +x   -y
    """
    neighbour_vectors = {
        'ne': Coordinate(-1, 0, 1),
        'nw': Coordinate(-1, 1, 0),
        'e': Coordinate(0, -1, 1),
        'w': Coordinate(0, 1, -1),
        'sw': Coordinate(1, 0, -1),
        'se': Coordinate(1, -1, 0),
    }

    def __init__(self, x: int, y: int, z: int):
        assert (x + y + z) == 0
        super().__init__(x, y, z)

    def get_length(self) -> int:
        return (abs(self.x) + abs(self.y) + abs(self.z)) // 2

    def getDistanceTo(self, target: Coordinate, algorithm: DistanceAlgorithm = DistanceAlgorithm.EUCLIDEAN,
                      includeDiagonals: bool = True) -> Union[int, float]:
        # includeDiagonals makes no sense in a hex grid, it's just here for signature reasons
        if algorithm == DistanceAlgorithm.MANHATTAN:
            return (self - target).get_length()

    def getNeighbours(self, includeDiagonal: bool = True, minX: int = -inf, minY: int = -inf,
                      maxX: int = inf, maxY: int = inf, minZ: int = -inf, maxZ: int = inf) -> list[Coordinate]:
        # includeDiagonals makes no sense in a hex grid, it's just here for signature reasons
        return [
            self + x for x in self.neighbour_vectors.values()
            if minX <= (self + x).x <= maxX and minY <= (self + x).y <= maxY and minZ <= (self + x).z <= maxZ
        ]

HexCoordinateR = HexCoordinate
class HexCoordinateF(HexCoordinate):
    """
    https://www.redblobgames.com/grids/hexagons/#coordinates-cube
    Treat as 3d Coordinate
    +y        -x
       y     x
    -z z yxz z +z
       x     y
    +x        -y
    """
    neighbour_vectors = {
        'ne': Coordinate(-1, 0, 1),
        'nw': Coordinate(0, 1, -1),
        'n': Coordinate(-1, 1, 0),
        's': Coordinate(1, -1, 0),
        'sw': Coordinate(1, 0, -1),
        'se': Coordinate(0, -1, 1),
    }

    def __init__(self, x: int, y: int, z: int):
        super().__init__(x, y, z)


class Shape:
    def __init__(self, top_left: Coordinate, bottom_right: Coordinate):
        """
        in 2D mode: top_left is the upper left corner and bottom_right the lower right
                    (top_left.x <= bottom_right.x and top_left.y <= bottom_right.y)
        in 3D mode: same logic applied, just for 3D Coordinates
                    top_left is the upper left rear corner and bottom_right the lower right front
                    (top_left.x <= bottom_right.x and top_left.y <= bottom_right.y and top_left.z <= bottom_right.z)
        """
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.mode_3d = top_left.z is not None and bottom_right.z is not None

    def __len__(self):
        if not self.mode_3d:
            return (self.bottom_right.x - self.top_left.x + 1) * (self.bottom_right.y - self.top_left.y + 1)
        else:
            return (
                (self.bottom_right.x - self.top_left.x + 1)
                * (self.bottom_right.y - self.top_left.y + 1)
                * (self.bottom_right.z - self.top_left.z + 1)
            )

    def intersection(self, other: Shape) -> Union[Shape, None]:
        """
        returns a Shape of the intersecting part, or None if the Shapes don't intersect
        """
        if self.mode_3d != other.mode_3d:
            raise ValueError("Cannot calculate intersection between 2d and 3d shape")

        if not self.mode_3d:
            intersect_top_left = Coordinate(
                self.top_left.x if self.top_left.x > other.top_left.x else other.top_left.x,
                self.top_left.y if self.top_left.y > other.top_left.y else other.top_left.y,
            )
            intersect_bottom_right = Coordinate(
                self.bottom_right.x if self.bottom_right.x < other.bottom_right.x else other.bottom_right.x,
                self.bottom_right.y if self.bottom_right.y < other.bottom_right.y else other.bottom_right.y,
            )
        else:
            intersect_top_left = Coordinate(
                self.top_left.x if self.top_left.x > other.top_left.x else other.top_left.x,
                self.top_left.y if self.top_left.y > other.top_left.y else other.top_left.y,
                self.top_left.z if self.top_left.z > other.top_left.z else other.top_left.z,
            )
            intersect_bottom_right = Coordinate(
                self.bottom_right.x if self.bottom_right.x < other.bottom_right.x else other.bottom_right.x,
                self.bottom_right.y if self.bottom_right.y < other.bottom_right.y else other.bottom_right.y,
                self.bottom_right.z if self.bottom_right.z < other.bottom_right.z else other.bottom_right.z,
            )

        if intersect_top_left <= intersect_bottom_right:
            return self.__class__(intersect_top_left, intersect_bottom_right)

    def __and__(self, other):
        return self.intersection(other)

    def __rand__(self, other):
        return self.intersection(other)

    def __str__(self):
        return "%s(%s -> %s)" % (self.__class__.__name__, self.top_left, self.bottom_right)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.top_left, self.bottom_right)


class Square(Shape):
    def __init__(self, top_left, bottom_right):
        super().__init__(top_left, bottom_right)
        self.mode_3d = False


class Cube(Shape):
    def __init__(self, top_left, bottom_right):
        if top_left.z is None or bottom_right.z is None:
            raise ValueError("Both Coordinates need to be 3D")
        super().__init__(top_left, bottom_right)
