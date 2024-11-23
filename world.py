from __future__ import annotations
from typing import Tuple, List, Set


class World:
    def __init__(self, W: int, H: int):
        self.W = W
        self.H = H
        self.sand: Set[Sand] = set()
        self.grid = [[None for y in H] for x in W]
        self.updated: Set[Sand] = set()
        self.onqueue: Set[Sand] = set()
        self.next_update: Set[Sand] = set()
    
    def add_sand(self, sand: Sand):
        """Adds a brand new sand object to the world.

        Args:
            sand (Sand): A new sand object
        """
        self.sand.add(sand)
        self.grid[sand.x][sand.y] = sand
    
    def remove_sand(self, sand: Sand):
        """Removes a sand object from the world. 
        Should only be called from the sand object itself.

        Args:
            sand (Sand): Sand object to remove
        """
        self.sand.remove(sand)
        self.grid[sand.x][sand.y] = None
    
    def move_sand(self, sand: Sand, x: int, y: int):
        """Moves a sand object from its original position to a new one.

        Args:
            sand (Sand): Sand object to be moved
            x (int): New x position
            y (int): New y position
        """
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

    def move(self, x: int, y: int):
        """Moves a sand object to a new position.

        Args:
            x (int): New x position for the sand
            y (int): New y position for the sand
        """
        self.world.move_sand(self, x, y)
    
    def destroy(self):
        """Removes a sand object from its world."""
        self.world.remove_sand(self)
    
