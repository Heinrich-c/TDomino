'''
This file provides all necesary functions for TDomino on local play.

DATA DESIGN
    Domino TILES are touples.
    #####
    A player´s HAND is a list of touples. 
        Functions for accesing it should have player input as argument.
        Player input should be saved as global variables, and have player input
        functions handled separated.
    #####
    The drawing STOCK is a list of touples.
        Functions for accesing it should have randomness as arguments.
    #####
    The LINE of play is a list of touples.
        Functions for accesing it should work with l.pop(:touple) and l.insert(:touple).
'''
from random import choice
# Initializers
STOCK = [] 
HAND_1 = []
HAND_2 = []
LINE = []

# FUNCTION genStock :
def genStock():
    '''Procedure for populating the STOCK list.'''
    for i in range(0,7):
        j = i
        for j in range(j,7):
            STOCK.append((i,j)) # Appends TILE equal to tuple(i,j)


# FUNCTION drawToHand : 
def drawToHand(index:int , hand:list):
    '''Given a STOCK index and a hand, pops a tile from STOCK to hand.'''
    hand.append(STOCK.pop(index))

# FUNCTION genHand : 
def genHand(hand:list):
    '''Procedure for popping 7 random TILES from STOCK to a given hand.'''
    for i in range(0,7):
        j = choice(range(0,7)) # Random index
        drawToHand(j,hand)

# Left or right position in the LINE is represented as a string that equals to either "L" for "Left"
# or "R" for "Right"
        
# FUNCTION playToLine :
def playToLine(pos:str , tile_ind:int , hand:list): 
    ''' Given a LINE position, a tile index and a hand, pops the tile from the hand to the LINE.'''
    if pos == "L":
        LINE.insert(0,hand.pop(tile_ind))
    else:
        LINE.append(hand.pop(tile_ind))

# FUNCTION checkLine :
def checkLine(pos:str , tile:tuple)->list:
    ''' Given a LINE position and a tile, checks if the tile can be placed.
    Returns a boolean list, one value for if the tile can be placed, another for if it needs
    to be flipped'''
    if pos == "L":
        LINE_tile = LINE[0]
        if tile[1] == LINE_tile[0]:
            return [True,False]
        elif tile[0] == LINE_tile[0]:   # If flipped 
            return [True,True]
        else:   
            return [False,False]    # Not valid
    else:   # Same with "R"
        LINE_tile = LINE[-1]
        if tile[0] == LINE_tile[1]:
            return [True,False]
        elif tile[1] == LINE_tile[1]:
            return [True,True]
        else:
            return [False,False]

# FUNCTION flipTile :
def flipTile(tile_ind:int , hand:list):
    ''' Procedure for flipping a given tile by index in a given hand.'''
    aux_tile = hand[tile_ind]
    hand[tile_ind] = aux_tile[::-1]

#### RENDERING
    
DOMINO_CHART = ["   ",".  ",":  ",":. ",":: ","::.",":::"]

# FUNCTION renderTile:
def renderTile(tile:tuple)->str:
    ''' Given a tile, returns it in a printable string. '''
    tile_str = ''.join(["||" , DOMINO_CHART[tile[0]] , "|" , DOMINO_CHART[tile[1]] , "||"])
    return tile_str


# FUNCTION printLine:
def print_TileList(tilelist:list):
    ''' Procedure for printing given tile list'''
    for e in tilelist:
        print(renderTile(e)," ",end=' ')
    print("") # Optional, prints the next line

# FUNCTION printTurn:
def printTurn(turn):
    ''' Procedure for checking TURN flag and printing the
    corresponding turn'''
    if turn > 0:
        print("1ST PLAYER TURN")
    else:
        print("2ND PLAYER TURN")

# FUNCTION printOptions:
def printOptions():
    ''' Procedure for printing the player´s options'''
    print("1) Add Tile to Left \t 2) Add Tile to Right \t 3) Draw Tile ")

# FUNCTION optionHandler:
def optionHandler()->int:
    ''' Procedure for receiving player's option'''
    opt = -1 # Initializer
    while opt < 1 or opt > 3 :
        opt = int(input())
    return opt

# FUNCTION selectorHandler: 
def selectorHandler(hand:list)->int:
    ''' Procedure for receiving player´s selection'''
    selector = len(hand) + 1 # Initializer
    while selector >= len(hand):
        selector = int(input("Enter tile index: "))
    return selector
# FUNCTION passHandler:
def passHandler()->str:
    ''' Procedure for receiving player's yes or no option to pass their turn'''
    opt = ' '
    while opt !='Y' or opt !='N':
        opt = input("Do you want to pass your turn? [Y/N]: ")
    return opt

# Main loop
def main():
    WIN = False 
    TURN = 1
    first_turn = True
    drawing_turn = False
    genStock()
    genHand(HAND_1)
    genHand(HAND_2)
    while not WIN: 
        #### FIRST TURN ONLY SECTION
        if first_turn == True: 
            printTurn(TURN)# Print "1ST PLAYER TURN"
            print_TileList(HAND_1)
            printOptions()
            # Store inputs
            opt = optionHandler()
            tile_selector = selectorHandler(HAND_1)
            # Input result handling
            if opt < 3: 
                playToLine("L",tile_selector,HAND_1)
                first_turn = False # Ends first turn
                TURN = -1
            else:
                if STOCK != []:
                    drawToHand(choice(range(0,len(STOCK)-1)),HAND_1)
                    # Repeats the first turn loop
                else: 
                    print("Stock is empty. You can´t draw anymore tiles.")
                    # Repeats the first turn loop
        #### REMAINING TURNS
        else:
            printTurn(TURN) # Call function to decide and print who´s turn is
            if TURN > 0:
                current_hand = HAND_1
            else:
                current_hand = HAND_2
            print_TileList(LINE)
            print("\n")
            print_TileList(current_hand)    # Print player´s hand
            valid = False   # Flag for valid move
            while not valid :
                printOptions()  # Print Options
                opt = optionHandler()
                tile_selector = selectorHandler(current_hand)
                ## Input result handling
                if opt < 3: # Playing move1
                    if opt == 1:
                        pos = "L"
                    else: 
                        pos = "R"
                    check = checkLine(pos,current_hand[tile_selector])
                    if check[0]: # Valid move
                        if check[1]: # Flipping needed
                            flipTile(tile_selector,current_hand)
                        playToLine(pos,tile_selector,current_hand)
                        valid = True
                    else: # Unvalid move
                        print("This move is not valid.")
                        # Repeats loop until it gets a valid move
                else: 
                    if STOCK !=[]:
                        drawToHand(choice(range(0,len(STOCK)-1)),current_hand)
                        print("Drawed.")
                        drawing_turn = True
                        valid = True
                    else:
                        print("Stock is empty. You can´t draw anymore tiles.")
                        if passHandler() == 'N':
                            drawing_turn = True
                            valid = True
                            # Else, drawing_turn keeps False
                ## End input result handling
            if not drawing_turn:
                TURN = TURN * -1
            if HAND_1 == []:
                print("GAME ENDED, WINNER : PLAYER 1")
                Win == True
            elif HAND_2 == []:
                print("GAME ENDED, WINNER : PLAYER 2")
                Win == True



                        



                    
                # If options are to play:
                    # Call checkLine, if it´s valid, end loop
                    # (by changing valid? flag to True)
                    # Else print "Not valid" and repeat
                # If option is to draw from stock
                        # check if stock isn´t empty
                            # call drawToHand on random
                            # print "DRAWED"
                            # set drawing_turn flag to True
                            # repeat loop
                        # if stock is empty
                            # print "THE STOCK IS EMPTY"
                            # set drawing_turn flag to True
                # For finalization, check drawing_turn
                # If false, 
                    # set Turn flag by *-1, passing the game
                    # to the next player
                    # else don´t do an else statement and continue
                    # with the same player
            # If Hand 1 or Hand 2 is empty,
            # print "GAME ENDED, WINNER : (player)"
            # set WIN flag to true

main()
