# Optimal-Game-Choice
Players A-D are playing a game where they choose a real number in the range 0-1 inclusive.
A chooses first, then B etc. 

What is the optimal move for A?

Very simple approach:
A and B are grid searchers.
D is a greedy (going for the max possible area)
C is where most of the logic happens 
(i.e. C judges the state of the board and how D will react before choosing).

D often ends up with multiple possible choices, A and B take this into account by checking
the minimum area they can guarentee regardless of D's choice.


########################
# To do/ clean ups
CChoose is the logic C uses to make a decision
at the moment it does the high and low bounds of the scale separately which is unneccessary
and can be condensced into just one block. 
(at the moment left like this to match the by hand maths)

DChoose returns a list of possible choices, where each choice is either the midpoint of the 
range or immediately above or below in the edge cases. Strictly speaking, D wouldn't have to
choose a mid point in non edge cases. It would be nice to have A B and C take into account
this potential randomness (even through an associated 'bravery' function i.e. B takes more 
risk than A how does that effect the game)

Double for loop grid search seems like over kill

Extend to 5 players?
