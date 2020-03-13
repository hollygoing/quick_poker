import unittest

class TestPoker(unittest.TestCase):
    def BlackWin_test(self):
        assert play("Black: 4C 4S 2H 2D 4H  White: QS 8S AS 2S 3S") == "Black wins"
        assert play("Black: KD 3D 5S 9C 2H  White: 2C 3H 4S 8C KH") == "Black wins"

    def WhiteWin_test(self):
        assert play("Black: 9C 3D 5S 2H KD  White: 2C 3H 4S 8C AH") == "White wins"
        assert play("Black: 5S 3D 2H 9C KD  White: AD AS AH AC 2C") == "White wins"

    def NoWin_NoFail_test(self):
        assert play("Black: kD 3D 5S 9C 2H  White: 2D 3H 5C 9S KH") == "NoWin_NoFail"
        assert play("Black: 6H 5H 4H 3H 2H  White: 2C 3C 4C 5C 6C") == "NoWin_NoFail"

def parseInput(myinput):
    hands = {}
    hand_length = 6
    splitinput = [x for x in myinput.split(' ') if x.strip() != '']
    while len(splitinput) > 0:
        playerhand = splitinput[0:hand_length]
        player = playerhand.pop(0).replace(":", "")
        hands[player] = playerhand
        splitinput = splitinput[hand_length:]
    return hands

def getValue(card):
    valuemap = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
    "Q": 12, "K": 13, "A": 14,
    }
    return valuemap[card[0]]

def cardsort(cards):
    return sorted(cards, key=lambda x: getValue(x))

def isSeq(vals):
    vals.sort()
    for v in range(len(vals)):
        if v == 0:
            prev = vals[v]
        else:
            if vals[v] != prev + 1:
                return False
    return True

def compareHands(hands):
    rankings = {}
    for player in hands:
        rank = hands[player]["rank"]
        if rank not in rankings:
            rankings[rank] = [player]
        else:
            rankings[rank].append(player)

    results = []
    for key in sorted(rankings.keys(), reverse=True):
        results.append(rankings[key])
    return results

def getHands(name, hand):
    handset = {
    "vals": [], "S": [], "H": [], "D": [], "C": []
    }
    handranks = ["Straight Flush", "Four of a Kind", "Full House", "Flush",
                 "Straight", "Three of a Kind", "Two Pairs", "Pair", "High Card"]
    if type(hand) == str:
        cards = hand.split(' ')
    else:
        cards = hand

    for card in cards:
        value = getValue(card)
        if value not in handset:
            handset[value] = [card]
        else:
            handset[value].append(card)

        handset[card[-1]].append(card)
        handset["vals"].append(value)
        if value == 14:  # ace
            handset["vals"].append(1)

        if len(handset[card[-1]]) == 5:
            handset["Flush"] = cardsort(cards)
        if len(handset["vals"]) == 5 and isSeq(handset["vals"]):
            if "Flush" in handset:
                handset["Straight Flush"] = cardsort(cards)
                break
            else:
                handset["Straight"] = cardsort(cards)
                break

        if "High Card" not in handset:
            handset["High Card"] = [card]
        elif value > getValue(handset["High Card"][-1]):
            handset["High Card"].append(card)
        else:
            handset["High Card"].insert(0, card)

        if len(handset[value]) == 2:
            if "Three of a Kind" in handset:
                handset["Full House"] = cardsort(list(set(handset["Three of a Kind"] + handset[value])))
            elif "Pair" in handset:
                handset["Two Pairs"] = cardsort(list(set(handset["Pair"] + handset[value])))
            else:
                handset["Pair"] = handset[value]

        elif len(handset[value]) == 3:
            if "Two Pairs" in handset:
                handset["Full House"] = cardsort(list(set([card] + handset["Two Pairs"])))
            else:
                handset["Three of a Kind"] = handset[value]

        elif handset[value] == 4:
            handset["Four of a Kind"] = handset[value]
            break;

    for h in handranks:
        if h in handset:
            rank = ((len(handranks) - handranks.index(h)) * (10 ** 11))
            for i in range(1, 2 * len(handset[h]), 2):
                rank += getValue(handset[h][(i - 1) // 2]) * (10 ** i)
            return {
                "rank": rank,
                "title": h,
                "hand": handset[h]
            }

def play(inputs):
    inputs = inputs.split('\n')
    print(inputs)
    for i in inputs:
        hands = parseInput(i)
        results = {}
        for player in hands:
            results[player] = getHands(player, hands[player])

        rankings = compareHands(results)
    if len(rankings[0]) == 1:
        print("%s wins" % rankings[0][0])
        return ("%s wins" % rankings[0][0])
    else:
        print("NoWin_NoFail")
        return ("NoWin_NoFail")

if __name__ == '__main__':
    unittest.main()
