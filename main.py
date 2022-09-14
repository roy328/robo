# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random

import pack
import hand_helpers as Hands
import Logging
import Bots.Register as Register

class Table:
    def __init__(self, deck):
        self.deck = deck
        self.burned = []
        self.flop1 = None
        self.flop2 = None
        self.flop3 = None
        self.turn = None
        self.river = None

    def _turn(self):
        print("\nTURN:", end="\t")
        self.burned = self.deck.pop(0)
        self.turn = self.deck.pop(0)
        self.flop1.print_with_color()
        self.flop2.print_with_color()
        self.flop3.print_with_color()
        self.turn.print_with_color()
        print("******")

    def flop(self):
        print("\nFLOP:", end="\t")
        self.burned = self.deck.pop(0)
        self.flop1 = self.deck.pop(0)
        self.flop2 = self.deck.pop(0)
        self.flop3 = self.deck.pop(0)
        self.flop1.print_with_color()
        self.flop2.print_with_color()
        self.flop3.print_with_color()
        print("******")

    def _river(self):
        print("\nRIVER:", end="\t")
        self.burned = self.deck.pop(0)
        self.river = self.deck.pop(0)
        self.flop1.print_with_color()
        self.flop2.print_with_color()
        self.flop3.print_with_color()
        self.turn.print_with_color()
        self.river.print_with_color()
        print("******")

    def show(self):
        show_string = ""
        if (self.flop1):
            show_string += self.flop1.log_string() + ','
        if (self.flop2):
            show_string += self.flop2.log_string() + ','
        if (self.flop3):
            show_string += self.flop3.log_string() + ','
        if (self.turn):
            show_string += self.turn.log_string() + ','
        if (self.river):
            show_string += self.river.log_string() + ','
        return show_string


names = ['Adam', 'Ben', 'Caleb', 'Dan', 'Eli', 'Frank', 'Gad', 'Huz', 'Isiah', 'John']

def deal(players, table):
    deck = pack.getDeck()
    print(deck.pop(0))
    hands = []
    for i in range(0, 2):
        for player in players:
            player.add_card(deck.pop(0))

    for hand in hands:
        hand.show(table)

def flop(table, hands):
    table.flop()
    for hand in hands:
        hand.show(table)

def turn(table, hands):
    table._turn()
    for hand in hands:
        hand.show(table)

def river(table, hands):
    table._river()
    for hand in hands:
        hand.show(table)

def end(players):
    Table(pack.getDeck())
    for player in players:
        player.new_hand()

#def betting():
    # later

class Actions:
    fold = 0
    call = 1
    bet = 2
    check = 3
    allin = 4


def fold_player(player, players, bets):
    if player:
        player.fold()
    if player in players:
        players.remove(player)
    if player.name in bets.keys():
        bets.__delitem__(player.name)


def betting(players, table, pot):
    current_bet = 0
    bet = 0
    bets = {} # player, bet
    for player in players:
        bets[player.name] = 0
    Betting_done = False
    actions = {}
    while not Betting_done:
        for player in players:
            if player.folded:
                fold_player(player, players, bets)
                continue
            if current_bet > 0 and bets[player.name] == current_bet:
                continue
            bet = player.outer_act(current_bet, bets[player.name], table, actions, pot)
            if bet is None:
                fold_player(player, players, bets)
                continue
            pot += bet
            bets[player.name] += bet
            if bets[player.name] < current_bet:
                fold_player(player, players, bets)
                continue
            elif bets[player.name] >= current_bet * 2:
                current_bet = bets[player.name]
        Betting_done = True
        for bet in bets.values():
            if bet < current_bet:
                Betting_done = False
                break
    print("pot: " + str(pot))
    return pot

def play(num_starting_players):
    all_players = []
    for player in range(0, num_starting_players):
        i = random.randint(0, len(Register.register())-1)
        all_players.append(Register.register()[i](names[player], 1000))

    for round in range(0, 1000):
        table = Table(pack.getDeck())
        players = []
        for person in all_players:
            if not person.busted:
                person.new_hand()
                players.append(person)
        deal(players, table)
        hands = []
        pot = 0
        for player in players:
            hands.append(player.hand)
        pot = betting(players, table, pot)
        flop(table, hands)
        pot = betting(players, table, pot)
        turn(table, hands)
        pot = betting(players, table, pot)
        river(table, hands)
        pot = betting(players, table, pot)

        best_hand_value = 0
        winners = []
        for hand in hands:
            if hand.get_value(table) > best_hand_value:
                winners = []
                winners.append(hand.name)
                best_hand_value = hand.get_value(table)
            elif hand.get_value(table) == best_hand_value:
                winners.append(hand.name)

        num_split = len(winners)
        for player in players:
            if player.name in winners:
                player.chips += (pot/num_split)

        Logging.Log_chips(players, table)
        for person in all_players:
            person.status(table)
        end(players)
        ended = False
        for player in players:
            if player.chips < 0:
                ended = True
        if ended:
            break

def print_hi(name):
    play(5)
    # Use a breakpoint in the code line below to debug your script.
    print("LETS GO")  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
