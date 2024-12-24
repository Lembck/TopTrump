import random

cardInfo = [["Old Faithful", 55, 14, 65, 7432, 118, 2],
            ["Mount Fuji", 3776, 13, 69, 8671, 25, 2],
            ["Perito Moreno Glacier", 60, 9, 82, 13230, -5, 3],
            ["The Dead Sea", 418, 13, 91, 3666, 25, 1],
            ["Ngorongoro Crater", 610, 14, 19, 5804, 30, 2],
            ["Mount Erebus", 3794, 4, 95, 17059, -49, 3],
            ["Great Rift Valley", 1470, 14, 12, 5887, 25, 4],
            ["Grand Canyon", 1600, 15, 80, 8296, 30, 4],
            ["Giant's Causeway", 12, 19, 17, 592, 15, 2],
            ["Planet Earth", 11033, 20, 30, None, 14, 5],
            ["Northern Lights", 15000, 17, 0, 150, None, 4],
            ["Guilin Caves", 220, 9, 16, 9101, 30, 2],
            ["Mount Vesuvius", 1281, 18, 95, 1630, 30, 1],
            ["Giant Sequoia", 84, 15, 2, 8570, 30, 2],
            ["Great Barrier Reef", 60, 10, 10, 15292, 28, 4],
            ["Gobi Desert", 2700, 9, 84, 7279, 30, 3],
            ["The Matterhorn", 4478, 17, 85, 840, -5, 2],
            ["Iguassu Falls", 82, 11, 50, 10064, 25, 4],
            ["Mont Blanc", 4808, 18, 85, 808, 0, 2],
            ["Mount Everest", 8840, 7, 95, 7424, -10, 4],
            ["Uluru", 346, 10, 70, 14993, 35, 4],
            ["Amazonia", 60, 10, 10, 8100, 30, 4],
            ["Death Valley", 86, 15, 97, 8500, 40, 3],
            ["The Moon", 5500, 1, 100, 384402, -18, 5],
            ["The Nile", 1400, 13, 8, 3515, 35, 3],
            ["Niagara Falls", 50, 18, 69, 5804, 20, 4],
            ["Sahara Desert", 3445, 14, 84, 3800, 35, 3],
            ["Kilauea", 1247, 9, 65, 11783, 30, 3],
            ["Lake Baikal", 1637, 8, 55, 6613, -30, 2],
            ["Bungle Bungles", 578, 9, 60, 14150, 35, 2]]

def findBestStat(card, otherCards):
    ranks = []

    stat_names = ["size", "accessibility", "hostility", "distance", "temperature", "wonder"]

    for stat_index in range(6):
        stat_values = [getattr(c, stat_names[stat_index]) for c in otherCards]
        stat_values_sorted = sorted(stat_values, key=lambda x: (x is None, x), reverse=True)
        card_stat = getattr(card, stat_names[stat_index])

        if card_stat is None:
            rank = len(stat_values_sorted)
        else:
            rank = next((i for i, val in enumerate(stat_values_sorted) if val is not None and val < card_stat), len(stat_values_sorted))
        
        ranks.append(len(stat_values_sorted) - rank)
        
    best_stat_index = ranks.index(max(ranks))
    return stat_names[best_stat_index]


class Card:
    def __init__(self, name, size, accessibility, hostility, distance, temperature, wonder):
        self.name = name
        self.size = size  
        self.accessibility = accessibility
        self.hostility = hostility
        self.distance = distance
        self.temperature = temperature
        self.wonder = wonder

    def __str__(self):
        return (f"{self.name} (Size: {self.size}, Accessibility: {self.accessibility}, "
                f"Hostility: {self.hostility}, Distance: {self.distance}, "
                f"Temperature: {self.temperature}, Wonder: {self.wonder})\n")

    def __repr__(self):
        return (f"{self.name} (Size: {self.size}, Accessibility: {self.accessibility}, "
                f"Hostility: {self.hostility}, Distance: {self.distance}, "
                f"Temperature: {self.temperature}, Wonder: {self.wonder})\n")

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

class Player:
    def __init__(self, name, hand, allCards):
        self.name = name
        self.hand = hand
        self.allCards = allCards
        self.cardsKnownInHand = []
        self.cardsKnownInOpponentsHands = []

    def handIsEmpty(self):
        return len(self.hand) == 0

    def chooseStatToPlay(self):
        if (self.handIsEmpty()):
            return 0
        if (self.hand[0] not in self.cardsKnownInHand):
            self.cardsKnownInHand.append(self.hand[0])

        otherCards = set(self.allCards) - set(self.cardsKnownInHand)
        stat = findBestStat(self.hand[0], otherCards)
        return stat
        
    def __str__(self):
        return f"{self.name} {self.hand}"
    
    def __repr__(self):
        return f"{self.name} {self.hand}"

class Game:
    def __init__(self, player_names, allCards):
        self.players = [Player(name, [], allCards[:]) for name in player_names]
        self.playerUp = 0
        self.dealCards()
        self.startGame()

    def printGameState(self):
        print(", ".join(list(map(lambda p: p.name + " " + str(len(p.hand)), self.players))))

    def startGame(self):
        while True:
            userInput = input("")
            if (userInput == "q"):
                print("Quiting!")
                break
            self.playRound()
            self.printGameState()
            if all(player.handIsEmpty() for player in self.players):
                print("Game over! All players have empty hands.")
                break

    def playRound(self):
        any_hand_empty = any(player.handIsEmpty() for player in self.players)

        def checkWhoWon(stat):
            values = list(map(lambda p: getattr(p.hand[0], stat), self.players))
            winningValue = max([v for v in values if v is not None])
            return values.index(winningValue)
        
        def moveCardsToWinner(winner):
            cardsWon = []
            for player in self.players:
                cardsWon.append(player.hand.pop(0))
            self.players[winner].hand.extend(cardsWon)
            return cardsWon
        
        if (not any_hand_empty):
            stat = self.players[self.playerUp].chooseStatToPlay()
            winner = checkWhoWon(stat)
            cardsWon = moveCardsToWinner(winner)
            print(self.players[winner].name, "won", ", ".join(list(map(lambda c: getattr(c, "name"), cardsWon))))
            
            self.nextPlayerUp()
        
    def nextPlayerUp(self):
        self.playerUp = (self.playerUp + 1) % len(self.players)

    def dealCards(self):
        cardsUndealt = list(range(30))
        nextPlayerToDeal = 0
        
        def updateNextPlayerToDeal():
            nonlocal nextPlayerToDeal
            nextPlayerToDeal = (nextPlayerToDeal + 1) % len(self.players)
        
        for i in range(30):
            c = random.choice(cardsUndealt)
            cardToDeal = Card(cardInfo[c][0], cardInfo[c][1], cardInfo[c][2], cardInfo[c][3], cardInfo[c][4], cardInfo[c][5], cardInfo[c][6])
            self.players[nextPlayerToDeal].hand.append(cardToDeal)
            cardsUndealt.remove(c)
            updateNextPlayerToDeal()
        

allCards = list(map(lambda c: Card(c[0], c[1], c[2], c[3], c[4], c[5], c[6]), cardInfo))
game = Game(["Charlotte", "Olive", "Michael", "Andrew"], allCards)

#winDistribution = {0: 0, 1: 0, 2: 0, 3: 0}
#for i in range(100000):
#    game = Game(["Charlotte", "Olive", "Michael", "Andrew"], allCards)
#    winDistribution[game.playRound()] += 1
#print(winDistribution)

