from random import randint
from players import *
from pathfinder import *
from enum import *
class InvalidRequestException(Exception):
    pass
class AIStage(Enum):
    HEALTHPACKS = "healthpacks" #looking for healthpacks
    ATTACK = "attack" #attacking squirrels
    HOME = "home" #going home

class AISquirrel(Squirrel):
    def __init__(self, coordinate, board):
        super(Squirrel, self).__init__(coordinate, board)
        self.nuts = 0
        self.pic = pygame.image.load(os.path.join("imgs/squirrelright.png"))
        self.priority = Priority.player
        super().setSpeed((0,0))
        self.tileType = "squirrel"
        self.aiTicks = 0
        self.STONESPEED = 8

    # Turn *off* the ability to set a speed
    def setSpeed(self,speed):
        return

    # Don't do anything!
    def handleEvent(self,ev):
        return

    # Every half second, the squirrel gets 1 more fuel
    def clockTick(self,fps,num):
        self.aiTicks += num
        if (self.aiTicks > 5):
            self.board.state.incrementFuel(3)
            self.aiTicks -= 5

    def getHealthPacks(self):
        self.board.state.decrementFuel(20)
        x = []
        for hpack in self.board.healthpacks:
            x.append((hpack.getX(),hpack.getY()))
        return x

    def getStones(self):
        x = []
        for stone in self.board.stones:
            x.append((stone.getX(), stone.getY()))
        return x

    def getFerrets(self):
        self.board.state.decrementFuel(5)
        x = []
        for ferret in self.board.ferrets:
            if ferret.hp > 0:
                x.append((ferret.getX(),ferret.getY()))
        return x

    def getExit(self):
        self.board.state.decrementFuel(30)
        return (self.board.endTile.getX(),self.board.endTile.getY())

    def abs(self,x):
        if (x < 0): return -x
        return x

    # Uses |x| + |y| fuel
    def move(self,x,y):
        print('at move')
        if (x < -1 or x > 1 or y < -1 or y > 1):
            print("here1")
            raise InvalidRequestException()
        if self.canMoveTo(self.getX() + x, self.getY() + y):
            super().move(x,y)
            self.board.state.decrementFuel(self.abs(x) + self.abs(y))
        else:
            print("here2")
            raise InvalidRequestException()

    # Where x & y are in the range of integers [-1,1]
    def fireStone(self,x,y):
        if (x < -1 or x > 1 or y < -1 or y > 1):
            raise InvalidRequestException()
        
        startingTile = (self.getX()+x,
                        self.getY()+y)

        movementVector = [x,y]

        # Make sure we're not trying to, shoot at something we can't,
        # e.g., a wall.
        if (self.canMoveTo(startingTile[0], startingTile[1])):
            stone = Stone(startingTile,self.board)
            stone.setPosition(startingTile[0], startingTile[1])
            stone.setSpeed((movementVector[0] * self.STONESPEED,
                            movementVector[1] * self.STONESPEED))
            self.board.addTile(stone)
            self.board.registerForClockTick(stone)
            self.board.state.decrementFuel((self.abs(x) + self.abs(y)) * 3)
        else:
            raise InvalidRequestException()

class MyAISquirrel(AISquirrel):
    def __init__(self, coordinate, board):
        super().__init__(coordinate, board)
        self.myTicks = 0
        self.setSpeed((0,0))
        self.myPathfinder = PathFinder(self.board,self)
        self.stage = AIStage("home")
        self.stageInit= True
        self.queuedPath = []
        self.FUELBUFFER = 20
        self.goalTile = (self.getX(),self.getY()) #where we are currently trying to navigate to
    # Get the current fuel
    def getFuel(self):
        return self.board.state.getFuel()

    # You may call this method as often as you like: it does not use
    # any fuel.
    def canMove(self,x,y):
        print((self.getX() + x, self.getY() + y))
        return self.canMoveTo(self.getX() + x, self.getY() + y)

    # Use this method to move in any direction one tile. This will use
    # |x| + |y| fuel (i.e., if you call it with (-1, 1) it will use 2)
    def move(self,x,y):
        super().move(x,y)

    # Where x,y are in the range [-1,1] (integers)
    # Uses (|x| + |y|) * 3 fuel
    def fireStone(self,x,y):
        super().fireStone(x,y)

    # Gets the position of all stones on the board
    # 
    # Uses 0 fuel each time it is called
    def getStones(self):
        return super().getStones()

    # Gets the position of all ferrets (which will change!)
    # 
    # Uses 5 fuel each time it is called
    def getFerrets(self):
        return super().getFerrets()

    # Gets the position of the exit tile (nut)
    # 
    # Uses 30 fuel
    def getHealthPacks(self):
        return super().getHealthPacks()

    # Implement the main logic for your AI here. You may not
    # manipulate the other tiles on the board directly: this will be
    # considered cheating. Similarly, you may not manipulate the fuel
    # directly.
    # 
    # Every half second, you will receive 3 more fuel. This is
    # implemented in the parent class's clockTick (which, again, you
    # may not change).
    def clockTick(self,fps,num):
        super().clockTick(fps,num)
        
        print("Fuel: ",self.getFuel())
        print("Stage: ",self.stage)
        if(self.stage == AIStage("home")):
            if(self.stageInit and self.getFuel() >= 30+self.FUELBUFFER): #we wanna make sure we have enough fuel for the operation
                try:
                    self.goalTile = self.getExit()
                    path = self.myPathfinder.findPath(self.goalTile)
                    path = path[1:]
                    print("found path: ",path)
                    self.queuedPath = self.queuedPath + path
                    self.stageInit = False
                except:
                    print("WARNING pathfinder search failed.")
            if(self.goalTile == (self.getX(),self.getY())):
                print("WE DONE!")
            if(self.getFuel()>= 1 + self.FUELBUFFER):
                if(len(self.queuedPath)>0):
                    d = self.queuedPath.pop(0)
                    print("moving ",d)
                    self.move(d[0],d[1]) #we should move the first item in the list
            #now we should have a path or we are done
        #print("The stones are here!")
        #for stone in self.getStones():
        #    print(stone)

        return
