#!/bin/python
import random



###############################mag dit??
import time
import heapq
import collections
import copy
###############################

class Snake:
    moves = ['u', 'r','d', 'l']
    # u=up, d=down, l=left, r=right
    # dx en dy geven aan in welke richting 'u', 'r', 'd' en 'l' zijn:
    dx = [ 0, 1, 0,-1]
    dy = [-1, 0, 1, 0]
    
    #maak een slang aan
    def __init__(self, beginPositie, playerNr, playField):
        self.nr = playerNr
        self.playField = playField
        self.blocks = [(beginPositie[0], beginPositie[1])]
        self.playField.level[beginPositie[1]][beginPositie[0]] = '.'
        self.playField.playerPositions[beginPositie[1]][beginPositie[0]] = 'h' + str(self.nr)
        self.dead = False
        self.tailLastMove = beginPositie
    
    #maak een slang dood
    def Die(self):
        
        if not self.dead:
            
            #verander alles waar je nu staat in leeg
            for blockNr in range(0, len(self.blocks)):
                positie = self.blocks[blockNr]
                playField.playerPositions[positie[1]][positie[0]] = '.'
            
            #geef aan waar je staart de vorige beurt zat, want je vorige zet zorgde ervoor dat je dood ging, dus deze zet moet ongedaan worden
            self.blocks.append(self.tailLastMove)
            
            #zet de die je was de vorige beurt allemaal om in obstakels
            for blockNr in range(1, len(self.blocks)):
                positie = self.blocks[blockNr]
                playField.level[positie[1]][positie[0]] = '#'
                
            self.dead = True
            #geef terug dat er iemand dood is gegaan
            return True
        #hij wist al dat hij dood was
        return False    
        
    def costForPosition(self, pos):
        
        item = playField.level[pos[1]][pos[0]]
        
        
        if item == "#":
            return -1
        elif item == "D":
            return 9
        else:
            playerItem = playField.playerPositions[pos[1]][pos[0]]
            if 't' in playerItem:
                return 8
            if playerItem == '.':
                
                eten = playField.voedsel[pos[1]][pos[0]]
                if eten:
                    return 3
                if item == "G":
                    return 2
                #gang en leeg = 1 punt
                return 1
                
            else:
                return 100
            
            
        
    def FindPath(self):
        
        start = self.blocks[0]
        print("start: ", start)
        
        paths = []
        bodyQueue = collections.deque()
        for x in reversed(range(len(self.blocks))):
            bodyQueue.append(self.blocks[x])
        heapq.heappush(paths, (0, bodyQueue, []))
        
        
        while not len(paths) == 0:
            #print(paths.qsize())
            
            currentPath = heapq.heappop(paths)
            current = currentPath[1][-1]#.get()
            #print("current:", currentPath, " - ", current, " len = ", len(currentPath[2]))
            
            if len(currentPath[2]) > 4:
                break
            
            '''
            if current == goal:
                break
            '''
            for nextDir in range(len(self.moves)):
                newPosition = self.CalculateNewPosition(nextDir, current)
                if newPosition not in currentPath[1]:
                    calculateCost = self.costForPosition(newPosition)
                    if calculateCost >= 0:
                        newCost = currentPath[0] + calculateCost
                        newBodyList = copy.copy(currentPath[1])
                        newBodyList.append(newPosition)
                        if len(newBodyList) > len(self.blocks):
                            newBodyList.popleft()
                        directionList = currentPath[2][:]
                        directionList.append(nextDir)
                        #newPath = {"pos":newPosList, "dir":directionList}
                        newTuple = (newCost, newBodyList, directionList)
                        #print("new Path:", newTuple)
                        heapq.heappush(paths, newTuple)
                
                
                '''
                if newPosition not in costSoFar or newCost < costSoFar[newPosition]:
                    costSoFar[newPosition] = newCost
                    heapq.heappush(paths, (newCost, newPosition))
                    #paths.put(newCost, newPosition)
                    cameFrom[newPosition] = current
                    dirWent[newPosition] = nextDir
                    pathLength[newPosition] = pathLength[current] + 1
                    print("dir: ", nextDir, "current: ", current, " = ", newPosition, " - ", newCost)
                '''
                
                
        
        '''
        path = []
        while not current == start:
            path.append(dirWent[current])
            current = cameFrom[current]
        '''
        return currentPath[2]
        
    #bepaal de beste kan die je op kan gaan
    def Move(self):
        #'''
        path = self.FindPath()
        print(path)
        
        print("move")
        
        richting = self.moves[path[0]]
        print(richting)
        #'''
        
        '''
        
        dangerousMoves = []
        possibleMoves = []
        #kijk voor alle mogelijke kanten die je op kan bewegen, of dit niet je dood veroorzaakt
        for directionNR in range(len(self.moves)):
            newPosition = self.CalculateNewPosition(directionNR)
            
            #print('probeer directie', self.moves[directionNR], ':',newPosition)
        
            
            fieldItem = playField.level[newPosition[1]][newPosition[0]]
            #er is an obstakel in de weg
            if fieldItem == '#':
                continue
            
            if fieldItem == 'D':
                #als je langer bent als 1, dan is het zekere dood volgende beurt, maar beter als zekere dood nu
                #als er voedsel zit, is het zekere dood volgende beurt, anders is het veilig zolang je maar 1 lang bent
                if len(self.blocks) > 1 or playField.voedsel[newPosition[1]][newPosition[0]]:
                    dangerousMoves.append(directionNR)
                    continue
            #print("no obstakel found", playField.level[newPosition[1]], playField.level[newPosition[1]][newPosition[0]])
            
            #er zit een speler in de weg
            playerItem = playField.playerPositions[newPosition[1]][newPosition[0]]
            if  playerItem != '.':
                #het is een staart, dus als je niks anders kan, is dit nog een optie
                if "t" in playerItem:
                    dangerousMoves.append(directionNR)
                continue
            #print("no other players found", playField.playerPositions[newPosition[1]], playField.playerPositions[newPosition[1]][newPosition[0]])
            
            #niks in de weg, dus voeg toe
            possibleMoves.append(directionNR)
        print(possibleMoves)  
        
        #als je nergens heen kan, doe dan maar gewoon omhoog
        
        print('move') #Geef door dat we gaan bewegen
        #Als ergens een staart is, dan kunnen we beter die kant op gaan als we nergens anders heen kunnen ;),niet?
        if len(possibleMoves) == 0:
            if len(dangerousMoves) == 0:
                print('u') #Geef de richting door
            else:
                i = random.randrange(len(dangerousMoves))
                newMove = dangerousMoves[i]
                richting = self.moves[newMove]
                print(richting)
        else:
            #anders gebruik onze "strategy"
            
            #Kies een random richting uit de mogelijke richtingen
            i = random.randrange(len(possibleMoves))
            
            newMove = possibleMoves[i]
                
            richting = self.moves[newMove]  
            #self.MoveDir(i)  
            print(richting)                 #Geef de richting door
         #'''
        
        
    #bereken waar je terecht komt als je deze kant op gaat
    def CalculateNewPosition(self, directionNR, positie = None):
        if positie == None:
            positie = self.blocks[0]
        #Verander de huidige positie
        positie = (positie[0] + self.dx[directionNR], positie[1] + self.dy[directionNR])
        
        return playField.checkXY(positie)
    #beweeg een kant op   
    def MoveDir(self, direction):
        directionNR = self.moves.index(direction)
        
        positie = self.CalculateNewPosition(directionNR)
        
        
        #als een speler zich op het voedsel begeeft, eet het voedsel op
        if playField.voedsel[positie[1]][positie[0]]:
            
            #correct the tail
            if len(self.blocks) > 1:
                bodyPos = self.blocks[-1]
                playField.playerPositions[bodyPos[1]][bodyPos[0]] = self.nr #Moet niet str(self.nr) zijn?
            
            #voeg een extra slangenstuk toe aan het eind van het lichaam, er is alleen tijdelijk 2x hetzelfde stuk omdat alles zometeen 1 vooruit wordt geschoven, dus de positie van dit block maakt eigenlijk niet echt uit
            self.blocks.append(self.blocks[-1]) # Krijg je niet twee keer de coördinaten van self.blocks[-1]?
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
        
        
        self.tailLastMove = self.blocks[-1]
        
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
    
    
    #maak een playingField aan
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
            
        self.updateLevel()
        
    #bekijk welke positie een bepaalde vector is, in verband met het periodieke veld
    def checkXY(self, positie):
        #Let op periodieke randvoorwaarden!
        positie = ((positie[0] + self.level_breedte)% self.level_breedte, (positie[1] + self.level_hoogte) % self.level_hoogte)
        
        return positie
    
    #het level is veranderd, dus update onze informatie
    def updateLevel(self):
        #voor als we iets willen doen met nieuwe obstakels?
        #self.level = []
        
        self.gates = []
        
        
        T1 = time.perf_counter()
        #kijk waar alle gates en doodlopende eindes zijn
        for y in range(self.level_hoogte):
            for x in range(self.level_breedte):
                
                if self.level[y][x] == '#':
                    continue
                
                
                #bereken alle kanten die je op kan van de huidige positie
                newXY = self.checkXY((x, y-1))
                up = self.level[newXY[1]][newXY[0]]
                newXY = self.checkXY((x, y+1))
                down = self.level[newXY[1]][newXY[0]]
                newXY = self.checkXY((x-1, y))
                left = self.level[newXY[1]][newXY[0]]
                newXY = self.checkXY((x + 1, y))
                right = self.level[newXY[1]][newXY[0]]
                
                
                item = '.'
                
                #kijk of er een hekje zit
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
                        newPoint = (0, 0) # check een schuin hekje
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
                    #bereken de schuine kanten van de huidige positie
                    newXY = self.checkXY((x+1, y-1))
                    upRight = self.level[newXY[1]][newXY[0]]
                    newXY = self.checkXY((x+1, y+1))
                    downRight = self.level[newXY[1]][newXY[0]]
                    newXY = self.checkXY((x-1, y-1))
                    upLeft = self.level[newXY[1]][newXY[0]]
                    newXY = self.checkXY((x - 1, y+1))
                    downLeft = self.level[newXY[1]][newXY[0]]
                    
                    closures = 0
                    direct = (0, 0)
                    
                    directionList = [up, down, left, right, upRight, downRight, upLeft, downLeft]
                    
                    toAdd = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, -1), (1, 1), (-1, -1),(-1, 1)] 
                    for nr in range(len(directionList)):
                        path = directionList[nr]
                        if path == "#":
                            closures += 1
                            if closures == 1:
                                direct = (direct[0] + toAdd[nr][0], direct[1] + toAdd[nr][1])
                            if closures == 2:
                                direct = (direct[0] - toAdd[nr][0], direct[1] - toAdd[nr][1])
                                            
                    if closures > 1:
                        #print("closures found of with added direction", direct, "added that is", direct[0] + direct[1])
                        if abs(direct[0] + direct[1]) > 2:
                            item = 'G'
                    else:
                        continue
                
                if item == 'G':
                    self.gates.append((x, y))
                
                self.level[y][x] = item
        T2 = time.perf_counter()  
        
        print("calculated gates for a field with size (", self.level_breedte, ",", self.level_hoogte, ") in", T2-T1, "seconds")
        #printArray(self.level)  
        '''
        
        #copieer het level zodat je het op kan delen in gebieden met behulp van floodfill
        self.gebieden = []
        for y in range(self.level_hoogte):
            self.gebieden.append([])
            for x in range(self.level_breedte):
                self.gebieden[y].append(self.level[y][x])
        
        
        
        T3 = time.perf_counter()
        #creëer gebieden bij iedere gate
        self.GebiedInfo = []
        self.gateInfo = []
        toMerge = []
        huidigGebiedAantal = 0
        for gateNr in range(len(self.gates)):
            gate = self.gates[gateNr]
            x = gate[0]
            y = gate[1]
            up = self.checkXY((x, y-1))
            down = self.checkXY((x, y+1))
            left = self.checkXY((x-1, y))
            right = self.checkXY((x + 1, y))
            
            self.gateInfo.append({})
            
            
            for direction in [up, down, left, right]:
                
                found = self.gebieden[direction[1]][direction[0]]
                
                if  found == '.':
                    geverftGrootte = self.floodFill(direction, huidigGebiedAantal)
                    #print("gebied", huidigGebiedAantal, "heeft", geverft, "gebieden geverft")
                    
                    self.GebiedInfo.append([geverftGrootte, 0])
                    self.gateInfo[gateNr][huidigGebiedAantal] = 1
                    
                    huidigGebiedAantal += 1
                elif str(found).isnumeric(): #isinstance( found, int ):
                    if int(found) in self.gateInfo[gateNr]:
                        self.gateInfo[gateNr][int(found)] += 1
                    else:
                        self.gateInfo[gateNr][int(found)] = 1
                    #if int(found) not in self.gates[gateNr]:
                    #self.gateInfo[gateNr].append(int(found))
                elif found == "G":
                    othergateNr = self.gates.index(direction)
                    toMerge.append([gateNr, othergateNr])
            
            #print("gate nr: ", gateNr, ":", self.gates[gateNr] ,"-", self.gateInfo[gateNr])
              
                
        T4 = time.perf_counter()
        
          
        #print(toMerge);
        ##join gates here somewhere:
            
        ###
        
        T5 = time.perf_counter()
        #bereken hoeveel gates uitgangen zijn voor elk gebied.
        for gateNr in range(len(self.gateInfo)):
            gebieden = list(self.gateInfo[gateNr].keys())
            if len(gebieden) > 1:
                for gebiedNr in gebieden:
                    self.GebiedInfo[gebiedNr][1] += 1
        
        T6 = time.perf_counter()
        
        
        #for huidigGebied in range(len(self.GebiedInfo)):
        #   print("gebied nr:", huidigGebied, " -", self.GebiedInfo[huidigGebied])
        
        
        
        
        print("finding gate Exits took: ", T6-T5, "seconds")
        print("finding areas took: ", T4-T3, "seconds")
        print("calculated new Level in ", T6 - T1, "seconds")
        
        printArray(self.gebieden)
        '''
        
        
    #floodfill, voor het bepalen van gebieden
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
    
    #er is een beurt geweest, dus zet alle zetten van de andere spelers in ons geheugen. En kijk waar het voedsel zit
    def Update(self, pBewegingen):
        
        someOneDied = False
        
        #String met bewegingen van alle spelers
        for i in range(len(pBewegingen)):
            #Nu is speler_bewegingen[i] de richting waarin speler i beweegd
            direction = pBewegingen[i]
            if direction == 'x':
                #als er een x is, is er misschien iemand doodgegaan, controlleer dat nu
                someOneDied = someOneDied or self.spelers[i].Die()
            else:
                #beweeg anders de speler gewoon
                self.spelers[i].MoveDir(direction)
        
        #als er snakes dood zijn gegaan deze beurt, update het level
        if someOneDied:
            self.updateLevel()
        
        
        #print waar de slangen zich nu begeven
        printArray(playField.playerPositions)

        aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
        
        if aantal_voedsel == 0:
            input() #lege newLine
        #self.voedsel_posities = []
        for i in range(aantal_voedsel):
            voedsel_positie = [int(s) for s in input().split()]
            # Sla de voedsel positie op in het level
            self.voedsel[voedsel_positie[1]][voedsel_positie[0]] = True
 
 
#een manier om netjes een lijst van lijsten te printen  
def printArray(array):
    print()
    for line in array:
        print("\t\t".join(line))


#print("starting")
#creëer een playingField
playField = PlayingField()
#bepaal welke slang wij zijn aan de hand van input
Player = playField.spelers[int(input())]


#elke beurt
while True:
    
    #bepaal waar we heen willen bewegen
    Player.Move()
    
    #Lees nieuwe informatie
    line = input()                  
    
    if line == "quit":              #We krijgen dit door als het spel is afgelopen
        print("bye")                #Geef door dat we dit begrepen hebben
        break
 
    #update het veld met deze input
    playField.Update(line)     