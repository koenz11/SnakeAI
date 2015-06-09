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
        
    def Move(self):
        
        possibleMoves = []
        for directionNR in range(len(self.moves)):
            newPosition = self.CalculateNewPosition(directionNR)
            
            print('probeer directie', self.moves[directionNR], ':',newPosition)
            
            if playField.obstakel[newPosition[1]][newPosition[0]]:
                continue
            
            print("no obstakel found")
            
            for speler in playField.spelers:
                for block in speler.blocks:
                    print('player found at', block)
                    if block[0] == newPosition[0] and block[1] == newPosition[1]:
                        continue
                    
                    #if block[0] == newPosition[0] and block[1] == newPosition[1]:
                    #    continue
            print("no other players found")
            
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
        positie = (positie[0] + self.dx[directionNR], positie[1] + self.dy[directionNR])
        
        '''
        #reken nieuwe positie uit
        positie[0] += self.dx[directionNR]             #Verander de huidige positie
        positie[1] += self.dy[directionNR]
        
        #Let op periodieke randvoorwaarden!
        positie[0] = (positie[0] + self.playField.level_breedte)% self.playField.level_breedte
        positie[1] = (positie[1] + self.playField.level_hoogte) % self.playField.level_hoogte
        '''
        positie = ((positie[0] + self.playField.level_breedte)% self.playField.level_breedte, (positie[1] + self.playField.level_hoogte) % self.playField.level_hoogte)
        
        return positie
    
        
    def MoveDir(self, direction):
        directionNR = self.moves.index(direction)
        
        positie = self.CalculateNewPosition(directionNR)
        
        #als een speler zich op het voedsel begeeft, eet het voedsel op
        if playField.voedsel_posities[positie[1]][positie[0]]: 
            self.blocks.append(self.blocks[-1])
            playField.voedsel_posities[positie[1]][positie[0]] = False
            print("ate food")
       
        ''' 
        for foodPositie in playField.voedsel_posities:
            if foodPositie == positie: 
                playField.voedsel_posities.remove(foodPositie)
                self.blocks.append(self.blocks[-1])
        '''
        #beweeg alle blockjes 1 vooruit
        for i in range(1, len(self.blocks)):
            self.blocks[i] = self.blocks[i-1]
        #het voorste blokje is de nieuwe positie
        self.blocks[0] = positie

class PlayingField:
    
    def __init__(self):
        ###Initialisatie
        # We lezen het doolhof en beginposities in
        
        self.level_hoogte = int(input())         #Lees hoe groot het level is
        self.level_breedte = int(input())
        
        self.level = []                          #Lees het level regel voor regel
        self.obstakel = []
        for y in range(self.level_hoogte):
            self.obstakel.append([])
            line = list(input())
            for x in range(len(line)):
                if line[x] == '#':
                    self.obstakel[y].append(True)
                else:
                    self.obstakel[y].append(False)
                    
            self.level.append(line)
    
        
        self.aantal_spelers = int(input())       #Lees het aantal spelers en hun posities
        self.spelers = []
        for i in range(self.aantal_spelers):
            begin_positie = [int(s) for s in input().split()]   #Maak lijst met x en y
            newSpeler = Snake(begin_positie, i, self)
            self.spelers.append(newSpeler) #voeg nieuwe speler toe
            
        self.voedsel_posities = []
        for y in range(self.level_hoogte):
            self.voedsel_posities.append([])
            for x in range(self.level_breedte):
                self.voedsel_posities[y].append(False)
            
        
        
    
    def Update(self, pBewegingen):
        #String met bewegingen van alle spelers
        for i in range(len(pBewegingen)):
            #Nu is speler_bewegingen[i] de richting waarin speler i beweegd
            direction = pBewegingen[i]
            self.spelers[i].MoveDir(direction)
                    
        

        aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
        #self.voedsel_posities = []
        for i in range(aantal_voedsel):
            voedsel_positie = [int(s) for s in input().split()]
            # Sla de voedsel positie op in een lijst en in het level
            self.voedsel_posities[voedsel_positie[1]][voedsel_positie[0]] = True
            
            #self.voedsel_posities.append(voedsel_positie)
            self.level[voedsel_positie[1]][voedsel_positie[0]] = "x"
    
    


playField = PlayingField()

Player = playField.spelers[int(input())]


while True:
    
    Player.Move()
    
    line = input()                  #Lees nieuwe informatie
    
    if line == "quit":              #We krijgen dit door als het spel is afgelopen
        print("bye")                #Geef door dat we dit begrepen hebben
        break

    playField.Update(line)      
