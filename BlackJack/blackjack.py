# Simple BlackJack version, by BLDR
import os
import random
import sys

from . import utils


class Game:
    def __init__(self):
        self.playing = False
        self.table_bet = 0  # Minimum bet
        self.dealer = None
        self.number_of_players = 0
        self.players = None
        self.number_of_decks = 0
        self.deck = None
        self.five_card_rule = False  # Special rule
        self.lobby_actions = {'P': 'Play', 'E': 'Exit'}
        self.ingame_actions = {'H': 'Hit', 'S': 'Stand'}

    def init(self):
        os.system('clear')
        self.number_of_players = utils.input_number('Number of players: ')
        self.number_of_decks = utils.input_number('Number of decks: ')
        self.table_bet = utils.input_number('Initial table bet: ')
        self.five_card_rule = utils.input_boolean('Activate five card rule: ')
        self.players = [Player(i) for i in range(1, self.number_of_players + 1)]
        self.deck = Deck(self.number_of_decks)
        self.dealer = Dealer()

    def main(self):
        self.init()
        while True:
            self.display_lobby()
            action = utils.input_action(self.lobby_actions)
            if action == 'Play':
                self.new_game()
                self.play()
                results, balances = self.solve_bets()
                self.display_results_ui(results, balances)
            elif action == 'Exit':
                sys.exit()

    def play(self):
        for player in self.players:
            while player.playing:
                self.display_ingame_ui()
                player.do_move(self.ingame_actions, self.deck)
                player.assess_points()
        while self.dealer.playing:
            self.dealer.do_move(self.deck)
            self.dealer.assess_points()
        self.playing = False

    def new_game(self):
        self.playing = True
        self.deck.new_deck()
        self.dealer.get_ready()
        for player in self.players:
            player.get_ready(table_bet=self.table_bet)
        for i in range(2):
            self.dealer.withdraw_card(self.deck)
            for player in self.players:
                player.withdraw_card(self.deck)

    def solve_bets(self):
        results = self.get_results()
        balances = self.get_balances(results)
        for player in self.players:
            player.update_cash(balances[player.name])
        return results, balances

    def get_results(self):
        dealer = self.dealer
        player_results = {}
        for player in self.players:
            if self.five_card_rule:
                result = 'WIN DOUBLE' if len(player.hand) >= 5 and not player.bust else ''
                if result:
                    player_results[player.name] = result
                    continue
            if player.blackjack:
                result = 'PUSH' if dealer.blackjack else 'WIN DOUBLE'
            elif player.bust:
                result = 'PUSH' if dealer.bust else 'LOSE'
            else:
                result = 'WIN' if player.points_in_hand() > dealer.points_in_hand() or dealer.bust else 'LOSE'
            player_results[player.name] = result
        return player_results

    def get_balances(self, results):
        player_balance = {}
        for player in self.players:
            result = results[player.name]
            if result == 'WIN':
                balance = player.amount_bet
            elif result == 'WIN DOUBLE':
                balance = player.amount_bet * 3 / 2
            elif result == 'LOSE':
                balance = -player.amount_bet
            else:
                balance = 0
            player_balance[player.name] = balance
        return player_balance

    def display_lobby(self):
        os.system('clear')
        string = ''
        string += self.display_headers() + '\n'
        string += self.display_players() + '\n'
        string += 'Table bet is: {}$'.format(self.table_bet) + '\n'
        string += self.display_action_menu(self.lobby_actions)
        print(string)

    def display_ingame_ui(self):
        os.system('clear')
        string = ''
        string += self.display_headers() + '\n'
        string += self.display_hands() + '\n'
        string += self.display_action_menu(self.ingame_actions)
        print(string)

    def display_results_ui(self, results, balances):
        os.system('clear')
        string = ''
        string += self.display_headers() + '\n'
        string += self.display_hands() + '\n'
        string += '-' * 20 + '\nRound Ended\n\n'
        string += 'Dealer: {0}\n'.format(self.dealer.get_status())
        for player in self.players:
            string += '{0}: {1} -> {2}: {3}$\n'.format(player.name, player.get_status(), results[player.name].title(), balances[player.name])
        print(string)
        input('\n\tContinue...')

    @staticmethod
    def display_headers():
        return "- BlackJack 21, by BLDR -"

    def display_hands(self):
        string = ''
        if self.playing:
            string += "\nDealer's hand: {0}\n".format(self.dealer.show_half_hand())
        else:
            string += "\nDealer's hand: {0}\nPoints: {1}\n".format(self.dealer.show_hand(), self.dealer.points_in_hand())
        for player in self.players:
            string += "\n{0}'s hand: {1}\nPoints: {2}\n".format(player.name, player.show_hand(), player.points_in_hand())
        return string

    def display_players(self):
        string = ''
        for player in self.players:
            string += "\n{0}: {1}$\n".format(player.name, player.cash)
        return string

    @staticmethod
    def display_action_menu(actions):
        string = '-' * 20 + '\n'
        for k, v in actions.items():
            string += '{} for {}\n'.format(k, v)
        return string


class Deck:
    def __init__(self, decks):
        self.number_of_decks = decks
        self.deck = []
        self.suits_symbols = [u'\u2660', u'\u2665', u'\u2666', u'\u2663']
        self.special_chars = ['A', 'J', 'Q', 'K']

    def new_deck(self):
        for i in range(self.number_of_decks):
            deck = self.create_deck()
            self.deck.extend(deck)
        self.shuffle_deck(self.deck)

    def create_deck(self):
        deck = []
        for suit in self.suits_symbols:
            for n in range(2, 11):
                deck.append(str(n) + suit)
            for c in self.special_chars:
                deck.append(str(c) + suit)
        return deck

    @staticmethod
    def shuffle_deck(deck):
        random.shuffle(deck)

    def take_card(self):
        if self.deck:
            return self.deck.pop()
        else:
            raise Exception('Deck is empty!')


class Participant:
    def __init__(self):
        self.hand = []
        self.playing = False
        self.stand = False
        self.bust = False
        self.blackjack = False

    def get_ready(self):
        self.hand = []
        self.playing = True
        self.stand = False
        self.bust = False
        self.blackjack = False

    def has_stand(self):
        self.stand = True
        self.playing = False

    def has_bust(self):
        self.bust = True
        self.playing = False

    def has_blackjack(self):
        self.blackjack = True
        self.playing = False

    def get_status(self):
        if self.bust:
            return 'BUST'
        elif self.blackjack:
            return 'BLACKJACK'
        elif self.stand:
            return 'STAND'

    def show_hand(self):
        return ' '.join(self.hand)

    def points_in_hand(self):
        points = 0
        ace = 0
        for card in self.hand:
            value = card[:-1]
            if value.isdigit():
                points += int(value)
            elif value in ['J', 'Q', 'K']:
                points += 10
            elif value == 'A':
                ace += 1
                points += 11
        for i in range(ace):
            if points > 21:
                points -= 10
        return points

    def assess_points(self):
        points = self.points_in_hand()
        if points > 21:
            self.has_bust()
        elif points == 21:
            self.has_blackjack()

    def withdraw_card(self, deck):
        self.hand.append(deck.take_card())
        self.assess_points()


class Player(Participant):
    def __init__(self, number):
        super().__init__()
        self.name = self.set_name(number)
        self.cash = self.set_cash()
        self.amount_bet = 0

    def get_ready(self, **kwargs):
        super().get_ready()
        print(kwargs)
        self.amount_bet = kwargs['table_bet']

    @staticmethod
    def set_name(number):
        while True:
            name = input('Player\'s {} name: '.format(number))
            if len(name) > 0:
                return name

    def set_cash(self):
        return utils.input_number('{}\'s initial cash: '.format(self.name), float_=True)

    def update_cash(self, amount):
        self.cash += amount

    def do_move(self, actions, deck):
        action = utils.input_action(actions, self.name)
        if action == 'Hit':
            self.withdraw_card(deck)
        elif action == 'Stand':
            self.has_stand()


class Dealer(Participant):
    """
    AI
    always stand hard 17 and over, never stand a soft 17, double soft hands A,2 and A,3 vs 5-6, A,4 and A,5 vs 4-6, and A,6 and A,7 vs 3-6.
    """

    def show_half_hand(self):
        return ' '.join(self.hand[:len(self.hand) - 1] + ['#'])

    def do_move(self, deck):
        points = self.points_in_hand()
        if points < 17:
            self.withdraw_card(deck)
        else:
            self.has_stand()


if __name__ == '__main__':
    t = Game()
    t.main()
