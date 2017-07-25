import random

playing = False
chip_pool = 100
bet = 1
restart_phrase = " d - to deal , or q - to quit"
suits = ('H', 'D', 'C', 'S')
ranking = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
card_val = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
result = ""


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.suit + self.rank

    def grab_suit(self):
        return self.suit

    def grab_rank(self):
        return self.rank

    def draw(self):
        print(self.suit + self.rank)


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        # aces can be 1 or 11
        self.ace = False

    def __str__(self):
        hand_comp = ""

        for card in self.cards:
            card_name = card.__str__()
            hand_comp += " " + card_name

        return 'The hand has {}'.format(hand_comp)

    def card_add(self, card):

        self.cards.append(card)

        if card.rank == 'A':
            self.ace = True
        self.value += card_val[card.rank]

    def calc_val(self):

        if self.ace is True and self.value < 12:
            return self.value + 10
        else:
            return self.value

    def draw(self, hidden):

        if hidden is True and playing is True:
            starting_card = 1
        else:
            starting_card = 0

        for x in range(starting_card, len(self.cards)):
            self.cards[x].draw()


class Deck:

    def __init__(self):

        self.deck = []
        for suit in suits:
            for rank in ranking:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

    def __str__(self):
        deck_comp = ""
        for card in self.cards:
            deck_comp += " " + deck_comp.__str__()

        return " The deck has " + deck_comp


def make_bet():

    global bet
    bet = 0

    print(" Enter the Amount of Chips in integers")

    while bet == 0:
        bet_comp = input()
        bet_comp = int(bet_comp)

        if bet_comp >=1 and bet_comp <= chip_pool:
            bet = bet_comp
        else:
            print("Invalid Bet, Only") + str(chip_pool) + "remaining"


def deal_cards():

    global result, playing, deck, player_hand, dealer_hand, chip_pool, bet

    deck = Deck()
    deck.shuffle()
    make_bet()

    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.card_add(deck.deal())
    player_hand.card_add(deck.deal())

    dealer_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())

    result = "Hit or Stand, Press h or S"

    if playing is True:
        print("Fold ")
        chip_pool -= bet

    playing = True
    game_step()


def hit():

    global playing, chip_pool, player_hand, dealer_hand, result, bet

    if playing:
        if player_hand.calc_val() <= 21:
            player_hand.card_add(deck.deal())

        print("Player Hand is {}".format(player_hand))

        if player_hand.calc_val() > 21:
            result = "Busted" + restart_phrase
            chip_pool -= bet
            playing = False
        else:
            result = "sorry, cant hit" + restart_phrase

        game_step()


def stand():

    global playing, chip_pool, deck, player_hand, dealer_hand, result, bet

    if playing is False:
        if player_hand.calc_val() > 0:
            result = "Sorry, you cant stand"
    else:
        # soft 17
        while dealer_hand.calc_val() < 17:
            dealer_hand.card_add(deck.deal())
            playing = False

        # dealer Busts
        if dealer_hand.calc_val() > 21:
            result = "dealer bursts! " + restart_phrase
            playing = False

        # player better than dealer
        elif dealer_hand.calc_val() < player_hand.calc_val():
            result = "You beat the dealer, you win" + restart_phrase
            playing = False

        # push
        elif dealer_hand.calc_val() < player_hand.calc_val():
            result = "Its a Tie" + restart_phrase
            playing = False

    game_step()


def game_step():

    print("")
    print("Player Hand is:", player_hand.draw(hidden=False))
    print("player hand total is: " + str(player_hand.calc_val()))
    print("Dealer Hand is:", dealer_hand.draw(hidden=True))

    if playing is False:
        print("For  a total of " + str(dealer_hand.calc_val()))
        print("chip total: " + str(chip_pool))
    else:
        print("with another card hidden upside down")

    print(result)
    player_input()


def game_exit():

    print("Thanks for playing")
    exit()


def player_input():

    play_in = input().lower()
    if play_in == 'h':
        hit()
    elif play_in == 's':
        stand()
    elif play_in == 'd':
        deal_cards()
    elif play_in == 'q':
        game_exit()
    else:
        print(" Please enter the choice as h,s,d or q")
        player_input()


def intro():
    print(" Welcome to BlackJack!")

deck = Deck()
deck.shuffle()
player_hand = Hand()
dealer_hand = Hand()
intro()
deal_cards()
