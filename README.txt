This project was to create the game of blackjack. However, you can't play it at all. The program is a simulation, so the user enters in a couple 
parameters they want to change about the game and then the program will run a number of hands that you select. Once the program is done running
it will give output statistics about the player's win percentage.


This file includes a couple different files. Listed below are the descriptions and instructions:

'build' : This folder includes all the complilation information that was used when the Blackjack.exe was created. Not important for user.

'Blackjack.exe' : This file is the Blackjack simulation program. It might take a second to open and unfortunately only works
		  on Windows. However, once it boots up it should be good to go. Enter the number of decks you want, how often
		  the dealer should reshuffle the deck, and the number of hands you would like to simulate. Press 'Submit' and
		  after a bit a results window will appear. It might take a while for the program to complete if you simulate a 
		  large number of hands. There are a couple of errors that may appear if you exit the program without entering values.

'Blackjack.py' : This file is the source code for the Blackjack.exe file above. In case the Blackjack.exe file doesn't work, this
		 file can be loaded up and run to access the program. The only thing that will need changing is the path to the 
		 attached Excel file.

Combination.xlsx : This is a reference file for the Blackjack.py file. It has all the information about what is the correct action
		   based off the player hand and dealer face up card.
