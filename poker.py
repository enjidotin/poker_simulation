import random

face = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
suit = ('C', 'S', 'D', 'H')


class card():
    def __init__(self):
        pass

    def printCard(self):
        print(self.face, self.suit)

    def makecard(self, f, s):
        self.face = f
        self.suit = s


class player():
    pile = 100000
    name = 'Player'

    def __init__(self):
        pass

    def setPlayerDetails(self, name, buyin=10000):
        self.pile = buyin
        self.name = name
        self.card1 = card()
        self.card2 = card()

    def printPlayerCards(self):
        print(self.card1.face, self.card1.suit)
        print(self.card2.face, self.card2.suit)

    def printPlayer(self):
        print(self.name, self.pile)


class table():
    pot = 0
    acivePlayers = []

    def __init__(self):
        pass


deck = []
for i in suit:
    for j in face:
        newcard = card()
        newcard.makecard(j, i)
        deck.append(newcard)

table = table()
players = ['Naman', 'CrimeMasterGOGO', 'Bulla',
           'Modiji', 'Doodhwala', 'Homer Simpson']
# for i in players:
#     newPlayer = player()
#     newPlayer.setPlayerDetails(i)
#     newPlayer.printPlayer()
#     newPlayer.printPlayerCards()
#     table.acivePlayers.append(newPlayer)
