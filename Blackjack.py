# Author: Daniel Welch
# Description: Blackjack simulation 
# Date: July 1, 2022
# Last Updated: July 25, 2022

import random
import math
import PySimpleGUI as sg
import pandas as pd

# Getting blackjack table
table = pd.read_excel(r"C:\\Users\\Daniel\\Documents\\GitHub\\ISYE6644-Simulation\\Project\\Program\\Combinations.xlsx")

# Function to draw a card
def get_rand_index(num):
    index = math.floor(random.uniform(0, 1)*num)
    return index

# Function to draw a card
def draw_card():  
    rank = math.ceil(random.uniform(0, 1)*13)
    suit = math.ceil(random.uniform(0, 1)*4)
    return (rank, suit)

# Function to get the sum of a given hand
def get_hand_sum(arr):
    sum = 0
    ace = 0
    for n in arr:
        if n[0] == 1:
            sum = sum + 11
            ace = ace + 1
        elif n[0] > 10:
            sum = sum + 10
        else:
            sum = sum + n[0]
    if ace > 0 and sum > 21:
        sum = sum - 10
    if ace > 1 and sum > 21:
        sum = sum - 10
    return sum

# Function to get the value of the first card in a hand
def get_first_card(arr):
    if arr[0][0] > 10:
        return 10
    else:
        return arr[0][0]

# Function to decide winner and add to stats
def get_winner(arr1, arr2):
    if get_hand_sum(arr1) <= 21 and get_hand_sum(arr2) <= 21:
        if get_hand_sum(arr1) > get_hand_sum(arr2):
            return 'player'
        elif get_hand_sum(arr1) < get_hand_sum(arr2):
            return 'dealer'
        elif get_hand_sum(arr1) == get_hand_sum(arr2):
            return 'tie'
    elif get_hand_sum(arr1) <= 21 and get_hand_sum(arr2) > 21:
        return 'player'
    elif get_hand_sum(arr1) > 21 and get_hand_sum(arr2) <= 21:
        return 'dealer'
    elif get_hand_sum(arr1) > 21 and get_hand_sum(arr2) > 21:
        return 'dealer'

# Function to check for ace
def check_ace(arr):
    for n in arr:
        if n[0] == 1:
            return True
    return False

# Check if hand is hard or soft
def check_hard_soft(arr):
    sum = 0
    for n in arr:
        if n[0] == 1:
            sum = sum + 11
        elif n[0] > 10:
            sum = sum + 10
        else:
            sum = sum + n[0]
    if sum > 21:
        return 'H'
    else:
        return 'S'


# Selection window
sg.theme('Dark Blue 3')
layout = [[sg.Text('Please enter parameters of the blackjack simulation')],
          [sg.Text('Number of decks:', size=(20, 1)), sg.Combo(['Infinite', '8', '4', '2', '1'], size=(15, 1))],
          [sg.Text('Reshuffle frequency:', size=(20, 1)), sg.Combo(['1', '2', '3', '4', '5', '6', '7', '8'], size=(15, 1))],
          [sg.Text('Number of hands:', size=(20, 1)), sg.Input(size=(15, 1))],
          [sg.Submit(), sg.Cancel()]]
window = sg.Window('Blackjack Simulation', layout)

# Getting choices from user selections
event, values = window.read()
window.close()
source_filename = values[0]
number_of_decks = values[0]
iterations = values[2]

# Variables for output statistics
player_wins = 0
dealer_wins = 0
ties = 0

# Card management
discard = []
active_cards = []
if number_of_decks != 'Infinite':
    deck = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), 
            (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2),
            (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3),
            (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4)]
    playing_deck = deck*int(number_of_decks)
    reshuffle = int(values[1])

# Looping through user chosen number of iterations
for n in range(int(iterations)):
    # Setting default values
    ace = False
    doubles = False
    hand = 'H'
    hand1 = 'H'
    hand2 = 'H'
    split = 'No Split'
    action = 'none'

    # Check for reshuffle
    if number_of_decks != 'Infinite':
        if reshuffle <= 0:
            playing_deck = deck*int(number_of_decks)

    # Draw initial hands and card management
    if number_of_decks == 'Infinite':
        player = [draw_card(), draw_card()]
        dealer = [draw_card(), draw_card()]
    else:
        deck_length = len(playing_deck)
        index = get_rand_index(deck_length)
        card1 = playing_deck.pop(index)
        deck_length = len(playing_deck)
        index = get_rand_index(deck_length)
        card2 = playing_deck.pop(index)
        deck_length = len(playing_deck)
        index = get_rand_index(deck_length)
        card3 = playing_deck.pop(index)
        deck_length = len(playing_deck)
        index = get_rand_index(deck_length)
        card4 = playing_deck.pop(index)
        player = [card1, card2]
        dealer = [card3, card4]
        active_cards.append([card1, card2, card3, card4])

    # Getting final dealer sum
    dealer_sum = get_hand_sum(dealer)
    while dealer_sum < 17:
        if number_of_decks == 'Infinite':
            dealer.append(draw_card())
        else:
            deck_length = len(playing_deck)
            index = get_rand_index(deck_length)
            card = playing_deck.pop(index)
            dealer.append(card)
        dealer_sum = get_hand_sum(dealer)

    # Check if player hand is doubles
    if player[0][0] == player[1][0]:
        doubles = True
    
    # If the player has doubles decide whether to split or not
    if doubles == True:
        player_reference = str(player[0][0]) + ', ' + str(player[1][0])
        index = table.index[table['reference'] == player_reference].tolist()
        split = table.at[index[0], get_first_card(dealer)]
        
    # No split
    if split == 'No Split':
        # Loop to hit when needed    
        while action != 'Stand':
            # Check if ace in player hand
            if check_ace(player):
                hand = check_hard_soft(player)

            # Getting player action based off sum and dealer number - references table
            player_sum = get_hand_sum(player)
            player_reference = str(player_sum) + ', ' + hand
            index = table.index[table['reference'] == player_reference].tolist()
            action = table.at[index[0], get_first_card(dealer)]

            # Dealing with hits
            if action == 'Hit':
                if number_of_decks == 'Infinite':
                    player.append(draw_card())
                else:
                    deck_length = len(playing_deck)
                    index = get_rand_index(deck_length)
                    card = playing_deck.pop(index)
                    player.append(card)
                    active_cards.append(card)

        # Adding to stats
        outcome = get_winner(player, dealer)
        if outcome == 'player':
            player_wins = player_wins + 1
        if outcome == 'dealer':
            dealer_wins = dealer_wins + 1
        if outcome == 'tie':
            ties = ties + 1

        # End of round cleaning up
        discard.append(player)
        discard.append(dealer)
        active_cards = []
        if number_of_decks != 'Infinite':
            reshuffle = reshuffle - 1

    # Split  
    else:
        # New card for each hand
        if number_of_decks == 'Infinite':
            player1 = [player[0], draw_card()]
            player2 = [player[1], draw_card()]
        else:
            deck_length = len(playing_deck)
            index = get_rand_index(deck_length)
            card1 = playing_deck.pop(index)    
            deck_length = len(playing_deck)
            index = get_rand_index(deck_length)
            card2 = playing_deck.pop(index)   
            player1 = [player[0], card1]
            player2 = [player[1], card2]
            active_cards.append([card1, card2])        

        # Hand #1
        while action != 'Stand':
            # Check if ace in player1 hand
            if check_ace(player1):
                hand1 = check_hard_soft(player1)
            # Getting player action based off sum and dealer number - references table
            player_sum = get_hand_sum(player1)
            player_reference = str(player_sum) + ', ' + hand1
            index = table.index[table['reference'] == player_reference].tolist()
            action = table.at[index[0], get_first_card(dealer)]

            # Dealing with hits
            if action == 'Hit':
                if number_of_decks == 'Infinite':
                    player1.append(draw_card())
                else:
                    deck_length = len(playing_deck)
                    index = get_rand_index(deck_length)
                    card = playing_deck.pop(index)  
                    player1.append(card)
                    active_cards.append(card)

        # Hand #2
        action = 'none'
        while action != 'Stand':
            # Check if ace in player1 hand
            if check_ace(player2):
                hand2 = check_hard_soft(player2)
            # Getting player action based off sum and dealer number - references table
            player_sum = get_hand_sum(player2)
            player_reference = str(player_sum) + ', ' + hand2
            index = table.index[table['reference'] == player_reference].tolist()
            action = table.at[index[0], get_first_card(dealer)]

            # Dealing with hits
            if action == 'Hit':
                if number_of_decks == 'Infinite':
                    player2.append(draw_card())
                else:
                    deck_length = len(playing_deck)
                    index = get_rand_index(deck_length)
                    card = playing_deck.pop(index)  
                    player2.append(card)
                    active_cards.append(card)

        # Adding to stats - player 1
        outcome = get_winner(player1, dealer)
        if outcome == 'player':
            player_wins = player_wins + 1
        if outcome == 'dealer':
            dealer_wins = dealer_wins + 1
        if outcome == 'tie':
            ties = ties + 1

        # Adding to stats - player2
        outcome = get_winner(player1, dealer)
        if outcome == 'player':
            player_wins = player_wins + 1
        if outcome == 'dealer':
            dealer_wins = dealer_wins + 1
        if outcome == 'tie':
            ties = ties + 1

        # End of round cleaning up
        discard.append(player1)
        discard.append(player2)
        discard.append(dealer)
        active_cards = []
        if number_of_decks != 'Infinite':
            reshuffle = reshuffle - 1

# Strings for output
player_string = 'Player wins: ' + str(player_wins)
dealer_string = 'Dealer wins: ' + str(dealer_wins)
ties_string = 'Ties: ' + str(ties)
total = 'Total:' + str(player_wins + dealer_wins + ties)
player_perc_string = '%.3f'%((player_wins/(player_wins + dealer_wins + ties))*100) + '%'
dealer_perc_string = '%.3f'%((dealer_wins/(player_wins + dealer_wins + ties))*100) + '%'
ties_perc_string = '%.3f'%((ties/(player_wins + dealer_wins + ties))*100) + '%'

# Output stats
sg.theme('Dark Blue 3')
layout = [[sg.Text(player_string, size=(15, 1)), sg.Text(player_perc_string, size=(15, 1))],
          [sg.Text(dealer_string, size=(15, 1)), sg.Text(dealer_perc_string, size=(15, 1))],
          [sg.Text(ties_string, size=(15, 1)) , sg.Text(ties_perc_string, size=(15, 1))],
          [sg.Text(total, size=(15, 1))]]
window = sg.Window('Blackjack Results', layout)
window.read()
window.close()