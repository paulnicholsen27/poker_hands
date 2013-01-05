
import itertools
from collections import defaultdict

def deck_maker():
	"Builds a set of black cards and red cards"
	black_suits = ['S', 'C']
	red_suits = ['H', 'D']
	ranks = '23456789TJQKA'
	black_cards = [rank+suit for rank in ranks for suit in black_suits]
	red_cards = [rank+suit for rank in ranks for suit in red_suits]
	return black_cards, red_cards
	
def best_wild_hand(hand):
	"Try all values for jokers in all 5-card selections."
	black_cards, red_cards = deck_maker()
	black_joker = red_joker = False
	no_joker_hands = [card for card in hand if card.find('?') == -1]
	print "Hands without jokers: ", no_joker_hands
	jokers = [card for card in hand if card.find('?') != -1]
	print "joker:", jokers
	for joker in jokers:
		if joker.find('B') != -1:
			black_joker = True         
		if joker.find('R') != -1:
			red_joker = True
	if black_joker == red_joker == False:
		return best_hand(hand)
	elif black_joker == True: 
		if red_joker == True:
			final_hands = [no_joker_hands + [black_card] + [red_card] for black_card in black_cards if black_joker == True and black_card not in no_joker_hands for red_card in red_cards if red_joker == True and red_card not in no_joker_hands]
		else: #only black joker
			final_hands = [no_joker_hands + [black_card] for black_card in black_cards if black_joker == True and black_card not in no_joker_hands]
	else: #only red joker
		final_hands = [no_joker_hands + [red_card] for red_card in red_cards if red_joker == True and red_card not in no_joker_hands]
	final_ranks = []
	for hand in final_hands:
		final_ranks.append(best_hand(hand))
	print "final ranks: ", final_ranks
	return max(final_ranks, key = lambda x: hand_rank(x))
	
def best_hand(hand):
	"From a 7-card hand, return the best 5 card hand."
	possible_hands = itertools.combinations(hand, 5)
	ranks = defaultdict(int)
	for hand in possible_hands:
		ranks[hand] = hand_rank(hand)
	best_rank = max(ranks, key = lambda x: ranks[x])
	return best_rank

def test_best_wild_hand():
	assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
			== ['7C', '8C', '9C', 'JC', 'TC'])
	assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
			== ['7C', 'TC', 'TD', 'TH', 'TS'])
	assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
			== ['7C', '7D', '7H', '7S', 'JD'])
	return 'test_best_wild_hand passes'

# ------------------
# Provided Functions
# 
# You may want to use some of the functions which
# you have already defined in the unit to write 
# your best_hand function.

def hand_rank(hand):
	"Return a value indicating the ranking of a hand."
	ranks = card_ranks(hand) 
	if straight(ranks) and flush(hand):
		return (8, max(ranks))
	elif kind(4, ranks):
		return (7, kind(4, ranks), kind(1, ranks))
	elif kind(3, ranks) and kind(2, ranks):
		return (6, kind(3, ranks), kind(2, ranks))
	elif flush(hand):
		return (5, ranks)
	elif straight(ranks):
		return (4, max(ranks))
	elif kind(3, ranks):
		return (3, kind(3, ranks), ranks)
	elif two_pair(ranks):
		return (2, two_pair(ranks), ranks)
	elif kind(2, ranks):
		return (1, kind(2, ranks), ranks)
	else:
		return (0, ranks)
	
def card_ranks(hand):
	"Return a list of the ranks, sorted with higher first."
	print "from card_ranks: ", hand
	ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
	ranks.sort(reverse = True)
	return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
	"Return True if all the cards have the same suit."
	suits = [s for r,s in hand]
	return len(set(suits)) == 1

def straight(ranks):
	"""Return True if the ordered 
	ranks form a 5-card straight."""
	return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
	"""Return the first rank that this hand has 
	exactly n-of-a-kind of. Return None if there 
	is no n-of-a-kind in the hand."""
	for r in ranks:
		if ranks.count(r) == n: return r
	return None

def two_pair(ranks):
	"""If there are two pair here, return the two 
	ranks of the two pairs, else None."""
	pair = kind(2, ranks)
	lowpair = kind(2, list(reversed(ranks)))
	if pair and lowpair != pair:
		return (pair, lowpair)
	else:
		return None 

#print test_best_wild_hand()




print best_wild_hand('?B 2S JC JH ?R 4S 9C'.split())


