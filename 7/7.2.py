import argparse
from pathlib import Path


def get_hand_and_bids():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    hands_and_bids = []

    with Path(args.path).open() as f:
        for line in f:
            hand, bid = line.split(' ')
            hands_and_bids.append([hand.strip(), int(bid)])
    return hands_and_bids


def get_combo_coefficient(hand):
    number_of_a_kind = dict((k, 0) for k in "J23456789TJQKA")
    for card in hand:
        number_of_a_kind[card] += 1

    if 5 in number_of_a_kind.values():
        return 7
    if 4 in number_of_a_kind.values():
        if number_of_a_kind["J"] == 1 or number_of_a_kind["J"] == 4:
            return 7
        else:
            return 6
    if 3 in number_of_a_kind.values() and number_of_a_kind["J"] != 3:
        if number_of_a_kind["J"] == 2:
            return 7
        if number_of_a_kind["J"] == 1:
            return 6
        if 2 in number_of_a_kind.values():
            return 5
        else:
            return 4

    pairs_count = 0
    for value in number_of_a_kind.values():
        if value == 2:
            pairs_count += 1

    if number_of_a_kind["J"] == 3:
        if pairs_count == 1:
            return 7
        else:
            return 6

    if pairs_count == 2:
        if number_of_a_kind["J"] == 2:
            return 6
        if number_of_a_kind["J"] == 1:
            return 5
        else:
            return 3

    if pairs_count == 1:
        if number_of_a_kind["J"] == 2:
            return 4
        if number_of_a_kind["J"] == 1:
            return 4
        else:
            return 2
    if number_of_a_kind["J"] == 1:
        return 2
    return 1


def card_to_score(card):
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    if card in values[:8]:
        return "0" + card
    if card == "T":
        return "10"
    if card == "J":
        return "01"
    if card == "Q":
        return "12"
    if card == "K":
        return "13"
    if card == "A":
        return "14"


def hand_to_score(hand):
    coef = get_combo_coefficient(hand)
    hand_score = str(coef)
    for card in hand:
        hand_score += card_to_score(card)
    return int(hand_score)


def main():
    hands_and_bids = get_hand_and_bids()
    for hand in hands_and_bids:
        hand[0] = hand_to_score(hand[0])
    hands_and_bids = sorted(hands_and_bids, key=lambda x: x[0])
    winnings = 0
    for i in range(0, len(hands_and_bids)):
        winnings += (i + 1) * hands_and_bids[i][1]
    print(winnings)


if __name__ == "__main__":
    main()
