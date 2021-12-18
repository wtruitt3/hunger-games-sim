# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 20:24:27 2021

@author: Carlos Villa
"""

import random
import math
 
           
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))
        
        
        
        
        
        
class Room(object):
    """
    A Room represents a rectangular region containing clean or dusty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dust. The tile is considered clean only when the amount
    of dust on this tile is 0.
    """
    def __init__(self, width, height, danger_zone_amounts,num_weapons):
        """
        Initializes a rectangular room with the specified width, height, and
        dust_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dust_amount: an integer >= 0
        """
        self.width = width
        self.height = height
        self.position = {}
        for i in range(self.width):
            for j in range(self.height):
                self.position[(i, j)] = 0
        
        for _ in range(danger_zone_amounts):
            randx = random.randint(0, self.width)
            randy = random.randint(0, self.height)           
            self.position[(randx, randy)] = 1.0
        for _ in range(num_weapons):
            randx = random.randint(0, self.width)
            randy = random.randint(0, self.height)           
            self.position[(randx, randy)] = 2.0

                
    def in_danger(self, w, h):
        """
        Returns the amount of the tile (w, h)

        Assumes that (w, h) represents a valid tile inside the room.

        w: an integer
        h: an integer

        Returns: boolean. True is in danger.
        """
        if float(self.position[(w,h)]) == 1:
            return True
        else:
            return False 

    def clean_tile_at_position(self, pos):
        """
        Mark the tile under the position pos as cleaned by cleaning_volume amount of dust.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        cleaning_volume: a float, the amount of dust to be cleaned in a single time-step.
                  Can be negative which would mean adding dust to the tile.

        Note: The amount of dust on each tile should be NON-NEGATIVE.
              If the cleaning_volume exceeds the amount of dust on the tile, mark it as 0.
        """
        w = math.floor(pos.get_x())
        h = math.floor(pos.get_y())
       
        self.position[(w,h)] = 0

    #def is_tile_cleaned(self, w, h):
        """
        Return True if the tile (w, h) has been cleaned.

        Assumes that (w, h) represents a valid tile inside the room.

        w: an integer
        h: an integer

        Returns: True if the tile (w, h) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dust on this
              tile is 0.
        """
        return self.position[(w,h)] == 0

    #def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        count = 0
        vals = self.position.values()
        for i in vals:
            if i == 0:
                count +=1
        return count
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        return pos.get_x() >= 0 and pos.get_x() < self.width and pos.get_y() >= 0 and pos.get_y() < self.height

    #def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return self.width*self.height

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        w = random.randint(0, self.width -1)
        h = random.randint(0, self.height -1)
        pos = Position(w, h)

        return pos
        
 
class Participant(object):
    def __init__(self, room, name, height, speed, strength, intelligence, creativity):
        """
        name - str - name of participant
        room - room object
        height - int - # of inches. Participant gets .1 points for every inch above 58 inches
        speed, strength, intelligence, creativity - float - attributes must add up to 10
        self.health - float - health is a multiplier of a participants stats
        """
        self.position=self.room.get_random_position()
        self.direction=random.uniform(0.0,360.0)
        self.health= 1.0
        self.name = name
        self.height = (height-58)*.1
        if sum([self.height,speed,strength,intelligence,creativity])<=10:
            self.speed = speed
            self.strength = strength
            self.intelligence=intelligence
            self.creativity = creativity
        else:
            raise AssertionError('Adjust stats to be <= 10')
        
    def get_name(self):
           return self.name
    def get_strength(self):
           return self.strength
    def get_speed(self):
           return self.speed
    def get_intelligence(self):
           return self.intelligence
    def get_height(self):
           return self.height
           
    #update Participant class to mimic robot    
    def get_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position

    def get_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position=position

    def set_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction=direction

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Moves robot to new position and cleans tile according to robot movement
        rules.
        """
        #Gets a new position using get_new_position function
        nextPos = Position.get_new_position(self.position,self.direction,self.speed)
        #checks if the new position is in the room. If it is it moves the robot
        #to the new position and cleans the tile. If not it changes the robot's direction.
        if self.room.is_position_in_room(nextPos):
            self.position=nextPos
            self.room.clean_tile_at_position(self.position)
        else:
            self.direction=random.uniform(0.0,360.0)    
            
def check_teams(pList):
    primeList = pList
    if len(pList)>2:
        if (pList[0].get_intelligence + pList[0].get_creativity) >= 5   and  (pList[1].get_intelligence + pList[1].get_creativity) >= 5 and (pList[2].get_intelligence + pList[2].get_creativity) <  5:
          if random.random()>.3:
              print(f'Alliance formed between {pList[0].get_name} and {pList[1].get_name}')
              pList=[[primeList[0],primeList[1]],primeList[2]]
              
        elif (pList[1].get_intelligence + pList[1].get_creativity) >= 5   and  (pList[2].get_intelligence + pList[2].get_creativity) >= 5 and (pList[0].get_intelligence + pList[0].get_creativity) <  5:
            print(f'Alliance formed between {pList[0].get_name} and {pList[1].get_name}')
            pList=[[primeList[1],primeList[2]],primeList[0]]
            
        elif (pList[0].get_intelligence + pList[0].get_creativity) >= 5   and  (pList[2].get_intelligence + pList[2].get_creativity) >= 5 and (pList[1].get_intelligence + pList[1].get_creativity) <  5:
            print(f'Alliance formed between {pList[0].get_name} and {pList[2].get_name}')
            pList=[[primeList[0],primeList[2]],primeList[1]] 
            
        else:
            print("No Alliance formed")
    return pList

def Encounter(pList):
    """
    pList - List of participant objects
    if Ps are on a team - make them together in a list - ex: pList could be [[p1, p2], p3]
    """
    new_pList = check_teams(pList)            
            
def HungerGames(participants, num_weapons, danger_zones_amount, room_width, room_height):
    """
    participants - list - list of Participant instances
    num_weapons - int - number of weapons
    danger_zones_amount - int - number of danger zone amounts
    room_width - int - width of room
    room_height - int - height of room
    """
    #similar to run_simulation
