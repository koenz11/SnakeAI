#!/bin/python
import random

class Snake:
    moves = ['u', 'r','d', 'l']
    # u=up, d=down, l=left, r=right
    # dx en dy geven aan in welke richting 'u', 'r', 'd' en 'l' zijn:
    dx = [ 0, 1, 0,-1]
    dy = [-1, 0, 1, 0]
    
    
    def __init__(self, beginPositie, playerNr, playField):
        self.nr = playerNr
        self.playField = playField
        self.blocks = [(beginPositie[0], beginPositie[1])]
        self.playField.level[beginPositie[1]][beginPositie[0]] = '.'
        self.playField.playerPositions[beginPositie[1]][beginPositie[0]] = 'h' + str(self.nr)
        self.dead = False
        
    def Die(self):
        
        if not self.dead:
            for positie in self.blocks:
                playField.level[positie[1]][positie[0]] = '#'
                playField.playerPositions[positie[1]][positie[0]] = '.'
                
            self.dead = True
            #playField.updateLevel()
        

    def Move(self):
        
        possibleMoves = []
        for directionNR in range(len(self.moves)):
            newPosition = self.CalculateNewPosition(directionNR)
            
            print('probeer directie', self.moves[directionNR], ':',newPosition)
            
            #there is an obstacle in the way
            if playField.level[newPosition[1]][newPosition[0]] == '#':
                continue
            print("no obstakel found", playField.level[newPosition[1]], playField.level[newPosition[1]][newPosition[0]])
            
            '''
            if playField.obstakel[newPosition[1]][newPosition[0]]:
                continue
            '''
            
            playerItem = playField.playerPositions[newPosition[1]][newPosition[0]]
            if  playerItem != '.':
                continue
            
            print("no other players found", playField.playerPositions[newPosition[1]], playField.playerPositions[newPosition[1]][newPosition[0]])
            '''
            for speler in playField.spelers:
                for block in speler.blocks:
                    print('player found at', block)
                    if block[0] == newPosition[0] and block[1] == newPosition[1]:
                        continue
                    
                    #if block[0] == newPosition[0] and block[1] == newPosition[1]:
                    #    continue
            '''
            
            possibleMoves.append(directionNR)
        print(possibleMoves)  
        
        
        if len(possibleMoves) == 0:
            print('move')
            print('u')
        else:
            #Kies een random richting
            i = random.randrange(len(possibleMoves))
            
            newMove = possibleMoves[i]
                
            richting = self.moves[newMove]  
            #self.MoveDir(i)
            
            print('move')                   #Geef door dat we gaan bewegen
            print(richting)                 #Geef de richting door
    
    def CalculateNewPosition(self, directionNR):
        positie = self.blocks[0]
        #Verander de huidige positie
        positie = (positie[0] + self.dx[directionNR], positie[1] + self.dy[directionNR])
        
        return playField.checkXY(positie)
    
        
    def MoveDir(self, direction):
        directionNR = self.moves.index(direction)
        
        positie = self.CalculateNewPosition(directionNR)
        
        
        #als een speler zich op het voedsel begeeft, eet het voedsel op
        if playField.voedsel[positie[1]][positie[0]]:
            
            #correct the tail
            if len(self.blocks) > 1:
                bodyPos = self.blocks[-1]
                playField.playerPositions[bodyPos[1]][bodyPos[0]] = self.nr
            
            self.blocks.append(self.blocks[-1])
            #print("ate food")
            playField.voedsel[positie[1]][positie[0]] == False
            
        else:
            #if you haven't eaten, remove last position from playerPositions
            pos = self.blocks[-1]
            playField.playerPositions[pos[1]][pos[0]] = '.'
            
            
        #draw the body
        if len(self.blocks) > 2:
            bodyPos = self.blocks[0]
            playField.playerPositions[bodyPos[1]][bodyPos[0]] = str(self.nr)
        
        
        #beweeg alle blockjes 1 vooruit
        for i in reversed(range(1, len(self.blocks))):
            self.blocks[i] = self.blocks[i-1]
        #het voorste blokje is de nieuwe positie
        self.blocks[0] = positie
        #draw the head
        playField.playerPositions[positie[1]][positie[0]] =  'h' + str(self.nr)
        
        #draw the tail
        if len(self.blocks) > 1:
            tailPos = self.blocks[-1]
            playField.playerPositions[tailPos[1]][tailPos[0]] = str(self.nr) + 't'

class PlayingField:
    
    def checkXY(self, positie):
        #Let op periodieke randvoorwaarden!
        positie = ((positie[0] + self.level_breedte)% self.level_breedte, (positie[1] + self.level_hoogte) % self.level_hoogte)
        
        return positie
    
    
    def __init__(self):
        ###Initialisatie
        # We lezen het doolhof en beginposities in
        
        self.level_hoogte = int(input())         #Lees hoe groot het level is
        self.level_breedte = int(input())
        
        self.level = []                          #Lees het level regel voor regel
        
        #self.obstakel = []
        for y in range(self.level_hoogte):
            #self.obstakel.append([])
            line = list(input())
            self.level.append(line)
        
        self.playerPositions = []
        for y in range(self.level_hoogte):
            self.playerPositions.append([])
            for x in range(self.level_breedte):
                self.playerPositions[y].append('.')
        
        
        
        self.aantal_spelers = int(input())       #Lees het aantal spelers en hun posities
        self.spelers = []
        for i in range(self.aantal_spelers):
            begin_positie = [int(s) for s in input().split()]   #Maak lijst met x en y
            newSpeler = Snake(begin_positie, i, self)
            self.spelers.append(newSpeler) #voeg nieuwe speler toe
             
        self.voedsel = []
        for y in range(self.level_hoogte):
            self.voedsel.append([])
            for x in range(self.level_breedte):
                self.voedsel[y].append(False)
            
        #self.updateLevel()
    
    def updateLevel(self):
        #voor als we iets willen doen met nieuwe obstakels?
        #self.level = []
        
        gates = []
        
        for y in range(self.level_hoogte):
            for x in range(self.level_breedte):
                
                if self.level[y][x] == '#':
                    continue
                
                newXY = self.checkXY((x, y-1))
                up = self.level[newXY[1]][newXY[0]]
                newXY = self.checkXY((x, y+1))
                down = self.level[newXY[1]][newXY[0]]
                newXY = self.checkXY((x-1, y))
                left = self.level[newXY[1]][newXY[0]]
                newXY = self.checkXY((x + 1, y))
                right = self.level[newXY[1]][newXY[0]]
                
                
                item = '.'
                
                closures = 0
                for path in [up, down, left, right]:
                    if path == '#':
                        closures += 1
                if closures > 2:
                    item = 'D'
                elif closures == 2:
                    if left == '#' and right == left:
                        item = 'G'
                    elif up == '#' and up == down:
                        item = 'G'
                    else:
                        newPoint = (0, 0)
                        if left == '#':
                            newPoint = (1, newPoint[1])
                        if right == '#':
                            newPoint = (-1, newPoint[1])
                        if up == '#':
                            newPoint = (newPoint[0], 1)
                        if down == '#':
                            newPoint = (newPoint[0], -1)
                        
                        newPoint = self.checkXY((newPoint[0] + x, newPoint[1] + y))
                        
                        if self.level[newPoint[1]][newPoint[0]] == '#':
                            item = 'G'
                else:
                    continue
                
                if item == 'G':
                    gates.append((x, y))
                
                self.level[y][x] = item
                
        printArray(self.level)  
        
        self.gebieden = []
        for y in range(self.level_hoogte):
            self.gebieden.append([])
            for x in range(self.level_breedte):
                self.gebieden[y].append(self.level[y][x])
        
        
        huidigGebied = 0
        for gate in gates:
            x = gate[0]
            y = gate[1]
            up = self.checkXY((x, y-1))
            down = self.checkXY((x, y+1))
            left = self.checkXY((x-1, y))
            right = self.checkXY((x + 1, y))
            
            for direction in [up, down, left, right]:
                if self.gebieden[direction[1]][direction[0]] == '.':
                    geverft = self.floodFill(direction, huidigGebied)
                    print("gebied", huidigGebied, "heeft", geverft, "gebieden geverft")
            huidigGebied += 1
        printArray(self.gebieden)
        
        
    def floodFill(self, positie, nr):
        
        x = positie[0]
        y = positie[1]
        
        geverft = 1
        self.gebieden[y][x] = str(nr)
        
        up = self.checkXY((x, y-1))
        down = self.checkXY((x, y+1))
        left = self.checkXY((x-1, y))
        right = self.checkXY((x + 1, y))
        
        for direction in [up, down, left, right]:
            if self.gebieden[direction[1]][direction[0]] == '.':
                geverft += self.floodFill(direction, nr)
        return geverft
        
        
    
    def Update(self, pBewegingen):
        #String met bewegingen van alle spelers
        for i in range(len(pBewegingen)):
            #Nu is speler_bewegingen[i] de richting waarin speler i beweegd
            direction = pBewegingen[i]
            if direction == 'x':
                self.spelers[i].Die()
            else:
                self.spelers[i].MoveDir(direction)
                    
        

        aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
        
        if aantal_voedsel == 0:
            leeg = input()
        #self.voedsel_posities = []
        for i in range(aantal_voedsel):
            voedsel_positie = [int(s) for s in input().split()]
            # Sla de voedsel positie op in het level
            self.voedsel[voedsel_positie[1]][voedsel_positie[0]] = True
    
def printArray(array):
    for line in array:
        print("\t\t".join(line))



playField = PlayingField()

Player = playField.spelers[int(input())]


while True:
    
    Player.Move()
    
    line = input()                  #Lees nieuwe informatie
    
    if line == "quit":              #We krijgen dit door als het spel is afgelopen
        print("bye")                #Geef door dat we dit begrepen hebben
        break
 
    print()
    playField.Update(line)     
    printArray(playField.playerPositions)