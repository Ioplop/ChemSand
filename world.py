from __future__ import annotations
from typing import Tuple, List, Set
from random import random


class World:
    def __init__(self, W: int, H: int):
        self.W = W
        self.H = H
        self.sand: Set[Sand] = set()
        self.grid = [[None for y in H] for x in W]
        self.updated: Set[Sand] = set() # Sand that was already updated in this step
        self.updating: Set[Sand] = set() # Sand that is going to be updated in this step
        self.update_queue: List[Sand] = [] # Queue of sand to be updated
        self.next_update: Set[Sand] = set() # Sand that will update on the next step
    
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
    
    def get_sand(self, x: int, y: int) -> Sand:
        """Find the sand object at a specific position and returns it.
        Loops around vertical edges.
        Doesn't loop on horizontal edges. Returns "OUTSIDE" instead.

        Args:
            x (int): X position of the sand.
            y (int): Y position of the sand.

        Returns:
            Sand: Whatever is found.
        """
        while x < 0:
            x += self.W
        while x >= self.W:
            x -= self.W
        while y < 0:
            return "OUTSIDE"
        while y >= self.H:
            return "OUTSIDE"
        return self.grid[x][y]
    
    def enqueue_update(self, sand: Sand):
        if sand in self.updated:
            self.next_update.add(sand)
        elif not (sand in self.updating):
            self.update_queue.append(sand)
    
    def update(self):
        while len(self.update_queue):
            sand = self.update_queue[-1]
            if sand.simulate():
                self.updated.add(sand)
            self.updating.remove(sand)
            self.update_queue.pop()
            
            
        

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
    
    def simulate(self) -> bool:
        """Executes a simulation step for a sand object. Returns a set of all the affected sand surrounding it.

        Returns:
            bool: True if the sand moved.
        """
        below = self.world.get_sand(self.x, self.y-1)
        fell = False
        if below == "OUTSIDE":
            return False
        if not below:
            self.move(self.x, self.y-1)
            fell = True
        else:
            l = self.world.get_sand(self.x-1, self.y-1)
            r = self.world.get_sand(self.x+1, self.y-1)
            xdown = 0
            if not (l or r):
                xdown = -1 if random < 0.5 else 1
            elif not l:
                xdown = -1
            elif not r:
                xdown = 1
            if xdown:
                fell = True
                self.move(xdown, self.y-1)
        if fell:
            self.world.enqueue_update(self)
            self.world.enqueue_update(self.world.get_sand(self.x-1, self.y+1))
            self.world.enqueue_update(self.world.get_sand(self.x, self.y+1))
            self.world.enqueue_update(self.world.get_sand(self.x+1, self.y+1))
        return fell