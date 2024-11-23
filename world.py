from __future__ import annotations
from typing import Tuple, List, Set


class World:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.sand: Set[Sand] = set()
        self.grid = [[None for y in H] for x in W]
        self.updated: Set[Sand] = set()
        self.onqueue: Set[Sand] = set()
        self.next_update: Set[Sand] = set()
    
    def add_sand(self, sand: Sand):
        self.sand.add(sand)
        self.grid[sand.x][sand.y] = sand
    
    def remove_sand(self, sand: Sand):
        self.sand.remove(sand)
        self.grid[sand.x][sand.y] = None
    
    def move_sand(self, sand: Sand, x: int, y: int):
        self.grid[sand.x][sand.y] = None
        sand.x = x
        sand.y = y
        self.grid[x][y] = sand
        

class Sand:
    def __init__(self, world: World, x: int, y: int, color: Tuple[int, int, int]):
        self.world = world
        self.x: int = x
        self.y: int = y
        self.color: Tuple[int, int, int] = color
        world.add_sand(self)

    def move(self, x, y):
        self.world.move_sand(self, x, y)
    
    def destroy(self):
        self.world.remove_sand(self)
    
