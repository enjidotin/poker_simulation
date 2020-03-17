import random
from evaluator import *
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

face = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
suit = ('C', 'S', 'D', 'H')
activePlayers = []
deck = []
players = ['P1', 'P2', 'P3', 'P4', 'P5']
pot = 0


class card():
    def _init_(self):
        pass

    def printCard(self):
        print(self.face, self.suit)

    def getcard(self):
        return str(self.face) + str(self.suit) + " "

    def makecard(self, f, s):
        self.face = f
        self.suit = s


class player():
    pile = 100000
    name = 'Player'
    card1 = card()
    card2 = card()
    card3 = card()

    def _init_(self):
        pass

    def setPlayerDetails(self, name, buyin=10000):
        self.pile = buyin
        self.name = name

    def printPlayer(self):
        print(self.name, self.pile)

    def pack(self):
        if(evaluateCards(self.card1, self.card2, self.card3)[0] >=5 or random.randint(1, 1000) == 42):
            return False
        elif((evaluateCards(self.card1, self.card2, self.card3)[0] <= 2 and random.randint(1, 6) > 2) or (evaluateCards(self.card1, self.card2, self.card3)[0] > 3 and random.randint(1, 10) == 2)):
            return True
        else:
            return False
    def pack2(self):
        self.confidence = evaluateCards(self.card1, self.card2, self.card3)[0] ** 3 + evaluateCards(self.card1, self.card2, self.card3)[1]
        return self.confidence
strength = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    "A": 14
}


def colourSequence(a, b, c):
    color = 0
    if(a.suit == b.suit and b.suit == c.suit):
        color = 1
    seq = sequence(a.face, b.face, c.face)
    if(seq and color):
        return 1
    else:
        return 0


def sequence(a, b, c):
    l = [strength[a], strength[b], strength[c]]
    l.sort()
    sequence = 0
    if(l[0]+1 == l[1]and l[1]+1 == l[2]):
        sequence = 1
    elif(l[0]+1 == 3 and l[1]+1 == 4 and l[2]+1 == 15):
        sequence = 1
    return sequence


def getplayerhandname(player):
    return evaluateCards(player.card1, player.card2, player.card3)[2]


def makeDeck():
    for i in suit:
        for j in face:
            newcard = card()
            newcard.makecard(j, i)
            deck.append(newcard)


def dealCards():
    for i in players:
        card1 = random.choice(deck)
        deck.remove(card1)
        card2 = random.choice(deck)
        deck.remove(card2)
        card3 = random.choice(deck)
        deck.remove(card3)
        newplayer = player()
        newplayer.card1 = card1
        newplayer.card2 = card2
        newplayer.card3 = card3
        newplayer.setPlayerDetails(i)
        activePlayers.append(newplayer)
        # print("player cards:: ")
        # newplayer.card1.printCard()
        # newplayer.card2.printCard()
        # newplayer.card3.printCard()
        # print("new deck::")
        # for i in deck:
        #     i.printCard()


def showPlayers():
    for i in activePlayers:
        i.printPlayer()
        i.card1.printCard()
        i.card2.printCard()
        i.card3.printCard()
        print(evaluateCards(i.card1, i.card2, i.card3))


def getplayercards(player):
    c1 = player.card1.getcard()
    c2 = player.card2.getcard()
    c3 = player.card3.getcard()
    return c1+c2+c3


if __name__ == "__main__":
    for __ in range(1):
        df = []
        for _ in range(10000):
            minbet = 20
            pot = 0
            activePlayers = []
            deck = []
            makeDeck()
            dealCards()
            cnt = 1
            p = []
            for i in activePlayers:
                p.append(getplayercards(i))

            bestplayer = activePlayers[0]
            for i in activePlayers:
                if(evaluateCards(i.card1, i.card2, i.card3)[0] > evaluateCards(bestplayer.card1, bestplayer.card2, bestplayer.card3)[0]):
                    bestplayer = i
            bestplayername = bestplayer.name
            bestplayerhand = str(bestplayer.card1.getcard(
            ))+str(bestplayer.card2.getcard())+str(bestplayer.card3.getcard())
            while(len(activePlayers) > 1):
                for i in activePlayers:
                    if((i.pack() == True and len(activePlayers) > 1) or i.pile <= minbet):
                        print(i.name, "PACK")
                        activePlayers.remove(i)
                for i in activePlayers:
                    i.pile -= minbet
                    pot += minbet
                activePlayers = list(np.roll(activePlayers, -1))
                print("PLAYERS LEFT AFTER ROUND :: ", cnt)
                cnt += 1
                showPlayers()
                minbet = minbet*2
                print("___")
            winner = activePlayers[0]
            winner.pile += pot
            pot = 0
            winnerhand = str(winner.card1.getcard()) + \
                str(winner.card3.getcard())+str(winner.card2.getcard())
            print(" ----WINNER!!!!---- ")
            showPlayers()
            df.append({'p1': p[0], 'p2': p[1], 'p3': p[2], 'p4': p[3], 'p5': p[4], 'winner': winner.name,
                    'winner hand': winnerhand, 'winner hand name': getplayerhandname(winner), 'best player': bestplayername, 'best player hand': bestplayerhand, 'best player hand name': getplayerhandname(bestplayer), "winning amount": winner.pile, "no of games played": cnt,"confidence of best player":bestplayer.pack2(),"confidence of winner":winner.pack2()})
        df2 = pd.DataFrame(df)
        print(df2)
        df2.to_csv('results/csvs/smarter2.csv', mode='a', index=False)