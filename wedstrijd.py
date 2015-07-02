#!/bin/python3

###############################
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
        
    #maak een slang dood, en geef terug of dit gelukt is, of dat hij al dood was
    def Die(self):
        
        if not self.dead:

            #verander alle delen van de slang in '.'
            for blockNr in range(0, len(self.blocks)):
                positie = self.blocks[blockNr]
                self.playField.playerPositions[positie[1]][positie[0]] = '.'
            
            #geef aan waar je staart de vorige beurt zat
            self.blocks.append(self.tailLastMove)
            
            #zet de positie van de vorige beurt om in obstakels
            for blockNr in range(1, len(self.blocks)):
                positie = self.blocks[blockNr]
                self.playField.level[positie[1]][positie[0]] = '#'
                
            self.dead = True
            #geef terug dat er iemand dood is gegaan
            return True

        return False    
        
    #Zoek de dichtsbijzijnde speler op een gegeven positie, en geef terug wat die afstand is, 
    #hoe groot de grootste speler is in verhouding tot jezelf, en hoe groot spelers zijn in het huidige gebied 
    def findClosest(self, pos):
        AndereSpelers = [speler for speler in self.playField.spelers if not speler.nr == self.nr]
        eigengebiedNr = self.playField.gebieden[pos[1]][pos[0]]
        
        biggestDistance = self.playField.level_hoogte**2 + self.playField.level_breedte**2
        closestPlayerDist = biggestDistance
        
        grootteAndereInGebied = 0
        size = 1
        
            
        #controleer spelers op grootte en afstand    
        for speler in AndereSpelers:
            zijnPos = speler.blocks[0]
            gebiedNr = self.playField.gebieden[zijnPos[1]][zijnPos[0]]
            if not speler.dead and eigengebiedNr.isnumeric() and gebiedNr == eigengebiedNr:
                grootteAndereInGebied += len(speler.blocks)
                afstandTotSpeler = (zijnPos[0]-pos[0])**2 + (zijnPos[1]-pos[1])**2
                if afstandTotSpeler < closestPlayerDist:
                    closestPlayerDist = afstandTotSpeler
            size = max(size, len(speler.blocks[0]))
        #zet ze om in ratio's, die ideaal zijn voor scoring
        closestRatio = 1.5 - closestPlayerDist/biggestDistance
        sizeRatio = len(self.blocks)/size
        
        return [closestRatio, grootteAndereInGebied, sizeRatio]

    # scan info plaats pos met voedsel en geef een puntenhoeveelheid terug
    def pointsForEating(self, pos, closestInfo):
        
        aantalAndereSpelers = len(self.playField.spelers)-1
        aantalAndereLevendeSpelers = self.playField.livingSpelers -1
        ratio = aantalAndereLevendeSpelers/aantalAndereSpelers
        
        
        
        eigengebiedNr = self.playField.gebieden[pos[1]][pos[0]]
        
        
        tijdRatio = 1-(self.playField.steps/500)
        sizeRatio = closestInfo[2]
        
        formule = 2*sizeRatio**3*ratio*tijdRatio
        #controle of het een gang is
        if eigengebiedNr.isnumeric():
            mapGrootte = self.playField.level_hoogte*self.playField.level_breedte
            gebiedGrootte = self.playField.GebiedInfo[int(eigengebiedNr)][0]
            
            andereRatio = (closestInfo[1]/gebiedGrootte) + 0.5
            gebiedRatio = 1-(gebiedGrootte/mapGrootte)
            
            formule *= andereRatio**2*gebiedRatio**2
            formule *= self.pointsForEmpty(pos, closestInfo)
        else:
            formule *= self.pointsForHallway(pos, closestInfo)
            
        return formule
            
    #puntentelling voor plaatsen waar een gang is    
    def pointsForHallway(self, pos, closestInfo):
        
        
        #haal de informatie van de huidige gang op
        gateIndex = int(self.playField.gebieden[pos[1]][pos[0]][1:])
        GateUitgangen = self.playField.gateInfo[gateIndex]
        
        
        
        formule = 0
        #als er maar 1 gebied als uitgang is, zie dit als een doodlopende gang
        if len(GateUitgangen) == 1:
            return self.pointsForDeadEnd()*0.95
        
        
        
        eigenPos = self.blocks[0]
        
        eigengebiedNr = self.playField.gebieden[eigenPos[1]][eigenPos[0]]
        gebiedGrootte = 1
        #controle of huidige positie van de slang in een gang of gebied is
        if eigengebiedNr.isnumeric():
            gebiedGrootte = self.playField.GebiedInfo[int(eigengebiedNr)][0]
            
        
        gebiedTeller = {}
        #tellen hoeveel slangen er in een gebied zijn
        for speler in self.playField.spelers:
            zijnPos = speler.blocks[0]
            gbdNr = self.playField.gebieden[zijnPos[1]][zijnPos[0]]
            
            if not gbdNr in gebiedTeller:
                gebiedTeller[gbdNr] = 0
            gebiedTeller[gbdNr] += 1
        
        #bekijk alleen de gebieden waarin je je niet begeeft
        notThis = [x for x in GateUitgangen.keys() if not str(x) == eigengebiedNr]
        
        for gbdNr in notThis:
            #haal informatie op van een van de gebieden waar deze gang een uitgang op heeft
            info = self.playField.GebiedInfo[gbdNr]
            gbdGrootte = info[0]
            gbdUitgangen = info[1]
            
            #kijk hoeveel spelers zich hierin begeven
            if not gbdNr in gebiedTeller:
                Splrs = 0
            else:
                Splrs = gebiedTeller[gbdNr]
            #bepaal een score aan de hand van de scoreformule
            formulePart = 1/(gbdGrootte)* (gbdUitgangen/(Splrs+1))
            formule += formulePart
        
        
        eigenLengte = len(self.blocks)    
        
        formule *= (eigenLengte + gebiedGrootte)/(len(notThis)+1)
        formule *= self.pointsForEmpty(pos, closestInfo)
        
        #bepaal absoluut de afstand naar de dichtbijzijnde speler, zodat je weet of het wel veilig is om een gang in te gaan
        AndereSpelers = [speler for speler in self.playField.spelers if not speler.nr == self.nr]
        biggestDistance = self.playField.level_hoogte**2 + self.playField.level_breedte**2
        closestPlayerDist = biggestDistance
        for speler in AndereSpelers:
            zijnPos = speler.blocks[0]
            gbdNr = self.playField.gebieden[zijnPos[1]][zijnPos[0]]
            if not speler.dead and gbdNr in notThis:
                afstandTotSpeler = (zijnPos[0]-pos[0])**2 + (zijnPos[1]-pos[1])**2
                if afstandTotSpeler < closestPlayerDist:
                    closestPlayerDist = afstandTotSpeler
        
        formule +=  75*(1.5 - closestPlayerDist/biggestDistance)**3
       
        print("gatePoints for gate:", gateIndex, "=", formule*(1/6)) 
        
        return formule*(1/6)
        
    #puntentelling voor lege plaatsen
    def pointsForEmpty(self, pos, closestInfo):
        
        formule = 100 * closestInfo[0]**3
        #print("pointsforEmpty:", formule)
        return formule
    
    #punten voor een staartdeel
    def pointsForTail(self, tail):
        
        ownLength = len(self.blocks)
        
        spelerNr = int(tail[:-1])
        
        #het is je eigen staart
        if spelerNr == self.nr:
            return (self.pointsForDeadEnd()*0.8)
        else:
            otherLength = len(self.playField.spelers[spelerNr].blocks)
            #het is een slang die kleiner is dan jij, die beweegt eerst, dus deze zet is geen zekere dood
            if otherLength < ownLength:
                return (self.pointsForDeadEnd()*0.7)
            #de slang is even lang, dus het is een gok of het zekere dood is
            elif otherLength == ownLength:
                return (self.pointsForDeadEnd()*0.9)
            #de slang is langer als jij
            else:
                return (self.pointsForDeadEnd()*1.5)
    
    #punten voor een vakje met "D", zekere dood na 1 stap
    def pointsForDeadEnd(self):
        return 5000
    
    #punten voor een andere snake
    def pointsForFoundSnake(self, snake):
        if 't' in snake:
            return self.pointsForTail(snake)
        
        if 'h' in snake:
            return (self.pointsForDeadEnd()*3)
        
        return self.pointsForDeadEnd()*2
        
    #bekijk wat er op de huidige positie zit om de punten te berekenen
    def costForPosition(self, pos):
        
        item = self.playField.level[pos[1]][pos[0]]
        
        closest = self.findClosest(pos)
        
        if item == "#":
            return -1
        elif item == "D":
            return self.pointsForDeadEnd()
        else:
            playerItem = self.playField.playerPositions[pos[1]][pos[0]]
            if playerItem == '.':
                eten = self.playField.voedsel[pos[1]][pos[0]]
                if eten:
                    return self.pointsForEating(pos, closest)
                if "G" in item:
                    return self.pointsForHallway(pos, closest)
                #leeg punt
                return self.pointsForEmpty(pos, closest)
            else:
                return self.pointsForFoundSnake(playerItem)
                
    #vindt een pad van 5 stappen, maakt gebruik van een Dijkstra Algoritme
    def FindPath(self):
        
        paths = []
        bodyQueue = collections.deque()
        for x in reversed(range(len(self.blocks))):
            bodyQueue.append(self.blocks[x])
        heapq.heappush(paths, (0, bodyQueue, [], 0))
        
        calculated = {}
        
        while not len(paths) == 0:
            
            currentPath = heapq.heappop(paths)
            current = currentPath[1][-1]
            #pak het pad met de laagste score
            pathLength = len(currentPath[2])
            #als hij lang genoeg is, ben je klaar
            if pathLength > 4:
                break
            
            #kijk naar alle kanten die je op kan vanaf het hoofd van dit pad
            for nextDir in range(len(self.moves)):
                newPosition = self.CalculateNewPosition(nextDir, current)
                if newPosition not in currentPath[1]:
                    #bereken de prijs van deze positie, als die niet al berekend is voor een vorig pad
                    if not newPosition in calculated:
                        calculateCost = int(self.costForPosition(newPosition))
                        calculated[newPosition] = calculateCost
                    else:
                        calculateCost = calculated[newPosition]
                    
                    #als de kosten meer zijn dan 0, dan kan je er heen dus voeg een pad toe met dit stukje eraan vast
                    if calculateCost >= 0:
                        #bekijk of je zou eten als je hier komt
                        eetHier = 0
                        if self.playField.voedsel[newPosition[1]][newPosition[0]]:
                            eetHier = 1
                        gegeten = currentPath[3] + eetHier
                        newCost = (currentPath[0]+ calculateCost)
                        
                        #geeft aan waar je theoretische lichaam zou zitten met dit pad
                        newBodyList = copy.copy(currentPath[1])
                        newBodyList.append(newPosition)
                        if len(newBodyList) > len(self.blocks) + gegeten:
                            newBodyList.popleft()
                        directionList = currentPath[2][:]
                        directionList.append(nextDir)
                        
                        #voeg het nieuwe pad toe aan de priorityQueue
                        newTuple = (newCost, newBodyList, directionList, gegeten)
                        heapq.heappush(paths, newTuple)
                
        
        return currentPath[2]
        
    #bepaal de beste kan die je op kan gaan
    def Move(self):
        
        #bereken elke stap een nieuw pad
        T1 = time.perf_counter()
        path = self.FindPath()
        T2 = time.perf_counter()
        
        print("move")
        richting = self.moves[path[0]]
        print(richting)
        
        
    #bereken waar je terecht komt als je deze kant op gaat
    def CalculateNewPosition(self, directionNR, positie = None):
        if positie == None:
            positie = self.blocks[0]
        #Verander de huidige positie
        positie = (positie[0] + self.dx[directionNR], positie[1] + self.dy[directionNR])
        
        return self.playField.checkXY(positie)
    #beweeg een kant op   
    def MoveDir(self, direction):
        directionNR = self.moves.index(direction)
        
        positie = self.CalculateNewPosition(directionNR)
        
        #als een speler zich op het voedsel begeeft, eet het voedsel op
        if self.playField.voedsel[positie[1]][positie[0]]:
            
            #correct the tail
            if len(self.blocks) > 1:
                bodyPos = self.blocks[-1]
                self.playField.playerPositions[bodyPos[1]][bodyPos[0]] = self.nr 
            
            # voeg een extra slangenstuk toe aan het eind van het lichaam, 
            # er is alleen tijdelijk 2x hetzelfde stuk omdat alles zometeen 1 vooruit wordt geschoven, 
            # dus de positie van dit block maakt eigenlijk niet echt uit
            self.blocks.append(self.blocks[-1]) 
            self.playField.voedsel[positie[1]][positie[0]] == False
            
        else:
            #if you haven't eaten, remove last position from playerPositions
            pos = self.blocks[-1]
            self.playField.playerPositions[pos[1]][pos[0]] = '.'
            
            
        #draw the body
        if len(self.blocks) > 2:
            bodyPos = self.blocks[0]
            self.playField.playerPositions[bodyPos[1]][bodyPos[0]] = str(self.nr)
        
        
        self.tailLastMove = self.blocks[-1]
        
        #beweeg alle blockjes 1 vooruit
        for i in reversed(range(1, len(self.blocks))):
            self.blocks[i] = self.blocks[i-1]
        #het voorste blokje is de nieuwe positie
        self.blocks[0] = positie
        #draw the head
        self.playField.playerPositions[positie[1]][positie[0]] =  'h' + str(self.nr)
        
        
        #draw the tail
        if len(self.blocks) > 1:
            tailPos = self.blocks[-1]
            self.playField.playerPositions[tailPos[1]][tailPos[0]] = str(self.nr) + 't'

class PlayingField:
    
    
    #maak een playingField aan
    def __init__(self):
        ###Initialisatie
        # We lezen het doolhof en beginposities in
        
        self.level_hoogte = int(input())         #Lees hoe groot het level is
        self.level_breedte = int(input())
        self.steps = 1
        
        self.level = []                          #Lees het level regel voor regel
        
        for y in range(self.level_hoogte):
            line = list(input())
            self.level.append(line)
        
        #creeer het playerPositie veld
        self.playerPositions = []
        for y in range(self.level_hoogte):
            self.playerPositions.append([])
            for x in range(self.level_breedte):
                self.playerPositions[y].append('.')
        
        
        self.aantal_spelers = int(input())       #Lees het aantal spelers en hun posities
        self.livingSpelers = self.aantal_spelers
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
                        #als de afstand tussen de hekjes meer is als 2, dan is er een gate
                        if abs(direct[0] + direct[1]) > 2:
                            item = 'G'
                    else:
                        continue
                
                if item == 'G':
                    self.gates.append((x, y))
                
                self.level[y][x] = item
        T2 = time.perf_counter()  
        
        
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
        
        
        groups = []
        groupPointers = {}
        amountOfGroups = 0
        
        huidigGebiedAantal = 0
        for gateNr in range(len(self.gates)):
            gate = self.gates[gateNr]
            x = gate[0]
            y = gate[1]
            #geef de gate een nummer
            self.gebieden[y][x] = "G" + str(gateNr)
            
            up = self.checkXY((x, y-1))
            down = self.checkXY((x, y+1))
            left = self.checkXY((x-1, y))
            right = self.checkXY((x + 1, y))
            
            self.gateInfo.append({})
            
            #bekijk of deze gate zich in een groep bevindt
            thisGroup = -1
            if gateNr in groupPointers:
                thisGroup = groupPointers[gateNr]
            
            #onderzoek alle richtingen voor nieuwe gebieden en gateGroepen
            for direction in [up, down, left, right]:
                
                found = self.gebieden[direction[1]][direction[0]]
                #niks gevonden, dus maak een nieuw gebied
                if  found == '.':
                    geverftGrootte = self.floodFill(direction, huidigGebiedAantal)
                    #voeg info over dit gebied toe aan self.GebiedInfo
                    self.GebiedInfo.append([geverftGrootte, 0])
                    #deze gate heeft dus in ieder geval 1 uitgang in dit nieuwe gebied
                    self.gateInfo[gateNr][huidigGebiedAantal] = 1
                    
                    huidigGebiedAantal += 1
                #als een nummer gevonden is, dan is het al een gebied, voeg dan alleen de uitgang naar het gevonden gebied toe aan gateInfo 
                elif str(found).isnumeric():
                    if int(found) in self.gateInfo[gateNr]:
                        self.gateInfo[gateNr][int(found)] += 1
                    else:
                        self.gateInfo[gateNr][int(found)] = 1
                #als we een gate gevonden hebben, bekijken we welke groep deze zich bevind
                elif found == "G":
                    othergateNr = self.gates.index(direction)
                    
                    #zoek zijn groep op
                    otherGroup = -1
                    if othergateNr in groupPointers:
                        otherGroup = groupPointers[othergateNr]
                        
                        
                    #er zijn 3 verschillende mogelijkheden
                    # 1. geen van beide zit in een groep -> maak een nieuwe groep aan
                    # 2. een van beide zit al in een groep -> voeg het gebied zonder groep toe aan de groep
                    # 3. beide zitten al in een groep -> voeg de groepen samen tot 1 groep
                    if thisGroup == -1:
                        if otherGroup == -1:
                            groups.append([gateNr, othergateNr])
                            thisGroup = amountOfGroups
                            otherGroup = amountOfGroups
                            amountOfGroups += 1
                        else:
                            groups[otherGroup].append(gateNr)
                            thisGroup = otherGroup
                    else:
                        if otherGroup == -1:
                            groups[thisGroup].append(othergateNr)
                            otherGroup = thisGroup
                        else:
                            for x in groups[otherGroup]:
                                if x not in groups[thisGroup]:
                                    groups[thisGroup].append(x)
                                groupPointers[x] = thisGroup
                            groups[otherGroup] = []
                            otherGroup = thisGroup
                    
                    #zet de groepnummers voor de gates goed
                    groupPointers[gateNr] = thisGroup
                    groupPointers[othergateNr] = otherGroup
        
        T4 = time.perf_counter()
        
        
        
        ##join gatesInfo of the groep
        oldGateLength = len(self.gates)
            
        added = 0
        for group in groups:
            if len(groups) > 0:
                
                newGateInfo = 
                #creeer de nieuwe gateInfo voor de groep
                beenAdded = []
                for gateNr in group:
                    #voorkom dat gates dubbel worden toegevoegd, elke groep zou all uniek moeten zijn, maar voor de zekerheid
                    if gateNr in beenAdded:
                        continue
                    else:
                        beenAdded.append(gateNr)
                    
                    gatePos = self.gates[gateNr]
                    #geef het groepsnummer aan de gate
                    self.gebieden[gatePos[1]][gatePos[0]] = "G" + str(oldGateLength + added)
                    
                    
                    #voeg alle gateInfo samen tot 1 gateInfo
                    for exit in self.gateInfo[gateNr].keys():
                        exitAmount = self.gateInfo[gateNr][exit]
                        if exit not in newGateInfo:
                            newGateInfo[exit] = exitAmount
                        else:
                            newGateInfo[exit] += exitAmount
                    
                self.gateInfo.append(newGateInfo)
                added += 1
                
        
        T5 = time.perf_counter()
        #bereken hoeveel gates uitgangen zijn voor elk gebied.
        for gateNr in range(oldGateLength):
            gebieden = list(self.gateInfo[gateNr].keys())
            if len(gebieden) > 1:
                for gebiedNr in gebieden:
                    self.GebiedInfo[gebiedNr][1] += 1
        
        T6 = time.perf_counter()
        
        
    #floodfill, voor het bepalen van gebieden, geeft de grootte van het gevonden gebied terug
    def floodFill(self, positie, nr):
        
        x = positie[0]
        y = positie[1]
        
        geverft = 1
        self.gebieden[y][x] = str(nr)
        
        up = self.checkXY((x, y-1))
        down = self.checkXY((x, y+1))
        left = self.checkXY((x-1, y))
        right = self.checkXY((x + 1, y))
        #floodfill alle andere gebieden om je heen die niet leeg zijn
        for direction in [up, down, left, right]:
            if self.gebieden[direction[1]][direction[0]] == '.':
                geverft += self.floodFill(direction, nr)
        return geverft
    
    #er is een beurt geweest, dus zet alle zetten van de andere spelers in ons geheugen. En kijk waar het voedsel zit
    def Update(self, pBewegingen):
        self.steps += 1
        snakesDied = 0
        
        #sorteer de spelers op puntenaantal (lengte) zodat de beurten in de goede volgorde gebeuren
        tempQ = []
        for i in range(len(self.spelers)):
            p = self.spelers[i]
            heapq.heappush(tempQ, (len(p.blocks), p.nr))
        
        #beweeg alle spelers
        while not len(tempQ) == 0:
            i = heapq.heappop(tempQ)[1]
            #Nu is speler_bewegingen[i] de richting waarin speler i beweegd
            direction = pBewegingen[i]
            if direction == 'x':
                #als er een x is, is er misschien iemand doodgegaan, controlleer dat nu
                if self.spelers[i].Die():
                    snakesDied += 1
            else:
                #beweeg anders de speler gewoon
                self.spelers[i].MoveDir(direction)
                
        #als er snakes dood zijn gegaan deze beurt, update het level
        if snakesDied > 0:
            self.livingSpelers -= snakesDied
            self.updateLevel()

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
        print("\t".join(line))
# een manier om netjes een lijst van lijstjes met bools te printen
def printBoolArray(array):
    print()
    for line in array:
        toPrint = ""
        for row in line:
            if row:
                toPrint += "x\t"
            else:
                toPrint += ".\t"


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