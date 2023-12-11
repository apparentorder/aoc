from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any

pipes = {
    "S": [],
    ".": [],
    "|": [Coordinate(0, -1), Coordinate(0, 1)],
    "-": [Coordinate(-1, 0), Coordinate(1, 0)],
    "L": [Coordinate(0, -1), Coordinate(1, 0)],
    "J": [Coordinate(0, -1), Coordinate(-1, 0)],
    "7": [Coordinate(-1, 0), Coordinate(0, 1)],
    "F": [Coordinate(1, 0),  Coordinate(0, 1)],
}

def try_loop_path(grid, start, heading):
    path = [start]
    pos = start + heading
    pos_pipe_char = grid.get(pos)
    
    while pos_pipe_char != "S":
        
        # verify that we could have entered this way, given our heading
        pipe_entry = Coordinate(-heading.x, -heading.y)
        if pipe_entry not in pipes[pos_pipe_char]:
            # cannot continue, loop incomplete
            return None
            
        # determine new heading (which way the pipe is pointing)
        pipe_exit = [dir for dir in pipes[pos_pipe_char] if dir != pipe_entry][0]
        heading = pipe_exit
        path += [pos]
        pos += heading
        pos_pipe_char = grid.get(pos)
        
    return path
    
def find_pipe_path(grid):
    start = [pos for pos in grid.getActiveCells() if grid.get(pos) == "S"][0]
    #print(f"start at {start}")
    
    for neigh in grid.getNeighboursOf(start, includeDiagonal = False):
        heading = neigh - start
        
        path = try_loop_path(grid, start, heading)
        if path: return path
            
    raise Exception("no path")

def x2(grid, loop_path):
    new_grid = Grid()
    
    for pos in grid.getActiveCells():
        new_grid.set(pos * 2, grid.get(pos))
        
    loop_path = [pos * 2 for pos in loop_path]
    loop_path += [loop_path[0]] # add starting position to end
    
    # reconnect the loop path by finding the gap between each step
    for i in reversed(range(1, len(loop_path))):
        neigh_a = set(new_grid.getNeighboursOf(loop_path[i],     includeDefault = True, includeDiagonal = False))
        neigh_b = set(new_grid.getNeighboursOf(loop_path[i - 1], includeDefault = True, includeDiagonal = False))
        missing = list(neigh_a & neigh_b)[0]
        loop_path.insert(i, missing)        
        
    return new_grid, loop_path
    
def inside_count(grid, loop_path):
    # start at the top left corner of the loop, which must be an "F" pipe (or "S")
    # therefore, the diagonally next (south east) position must be inside the loop.
    
    top_left_y = min(pos.y for pos in loop_path)
    top_left_x = min(pos.x for pos in loop_path if pos.y == top_left_y)
    top_left = Coordinate(top_left_x, top_left_y)
    #print(f"loop top left is {top_left} char {grid.get(top_left)}")       
    
    if grid.get(top_left) not in ["F", "S"]:
        raise Exception(f"invalid top left corner at {top_left} char {grid.get(top_left)}")
        
    # having a place to start from inside the loop, scan the area for positions
    # with non-default values (i.e. those not added by the x2 expansion)
    
    pos_seen = set(loop_path)
    pos_queue = set([top_left + Coordinate(1, 1)])
    
    count = 0
    while len(pos_queue) > 0:
        for pos in pos_queue.copy():
            pos_seen.add(pos)
            pos_queue.remove(pos)
            
            if grid.get(pos) not in [" ", False]:
                count += 1
            
            for neigh in grid.getNeighboursOf(pos, includeDiagonal = True, includeDefault = True):
                if neigh not in pos_seen:
                    pos_queue.add(neigh)
                    
    return count
    
class Day(AOCDay):
    inputs = [
        [
            (4, "input10-test1"),
            (8, "input10-test2"),
            (6823, "input10"),
        ],
        [
            (1, "input10-test1"),
            (4, "input10-testp2-1"),
            (8, "input10-testp2-2"),
            (10, "input10-testp2-3"),
            (415, "input10"),
        ]
    ]

    def part1(self) -> Any:
        grid = Grid.from_data(self.getInput(), default = ".")
        return len(find_pipe_path(grid)) // 2

    def part2(self) -> Any:
        grid = Grid.from_data(self.getInput(), default = " ") # n.b. different default
        loop_path = find_pipe_path(grid)
        grid, loop_path = x2(grid, loop_path)
        return inside_count(grid, loop_path)

if __name__ == '__main__':
    day = Day(2023, 10)
    day.run(verbose=True)
