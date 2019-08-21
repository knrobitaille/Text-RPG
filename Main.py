"""
A basic text RPG created to help my learning of Python.

Created the framework of the game using the following tutorial:
https://www.youtube.com/playlist?list=PL1-slM0ZOosXf2oQYZpTRAoeuo0TPiGpm

Once I had the framework, I wanted to dive in and make the game actual playable while learning more about Python.
I have played and tested this game one in my IDE (Spyder).

@author: kevin
"""

### IMPORT ###
import cmd # not currently used, from tutorial
import textwrap # not currently used, from tutorial
import sys
import os
import time
import random # not currently used, from tutorial

### TEXT EFFECT FUNCTION ###
def texteffect(string, n = 0.05):
    """
    Function takes a string and float
    It will slowly print out string, creating a neat effect
    Speed of print determined by float - smaller number is faster
    This concept was taken from the tutorial linked above and
    I figured it was a good idea to make it a function
    """
    q = string
    for character in q:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(n)


### SET SCREEN WIDTH ###
screen_width = 100


####################
### MENU SCREENS ###
####################

### TITLE SCREEN SELECTIONS FUNCTION ###
def title_screen_selections():
    """
    Creates options for the title screen
    """
    option = ""
    while option.lower not in ["help", "quit", "play"]:
        print("Please enter play, help, or quit")
        option = input("> ")
        if option.lower() == "play":
            setup_game()
        elif option.lower() == "help":
            help_menu()
        elif option.lower() == "quit":
            sys.exit()
            
####################            
### TITLE SCREEN ###                   
def title_screen():
    """
    Creates the title screen
    """
    #os.system('cls')#this was added in tutorial, not sure I need it
    print('\n################################')
    print('###    Welcome to the Game   ###')      
    print('################################')      
    print(' -            .Play.           - ')
    print(' -            .Help.           - ')
    print(' -            .Quit.           - ')
    print('################################\n') 
    title_screen_selections()

#################   
### HELP MENU ###   
def help_menu():
    """
    Creates the help menu
    """
    print('\n##################################################')
    print('################     Help Menu     ###############')  
    print('##################################################')
    print(' Type move or examine for each turn')      
    print(' If moving, type up, down, left, or right')
    print(' If examining, you may need to answer yes or no')
    print('##################################################\n')
    title_screen_selections()
    
    
    
  
####################
### GAME BACKEND ###
####################
       
    ### PLAYER SET UP ###
class player:
    def __init__(self):
        self.name = ''
        self.job = ''
        self.hp = 0 #set during tutorial but doesn't factor into gameplay
        self.pp = 0 #set during tutorial but doesn't factor into gameplay
        self.status_effects = [] #not currently used at all
        self.location = 'a1'
        self.haskey = False
        self.hasmanual = False
        self.specialmove = ''
        self.gameover = False        
myPlayer = player()

    
### EXAMPLE OF MAP ###    
    
"""
    
    A   B   C
  -------------
1 |   |   |   |
  -------------
2 |   |   |   |
  -------------
3 |   |   |   |
  -------------

  
"""
    
### FUNCTION TO PRINT MAP ###
# I am sure there is a much more eloquent way to do this, but this works #
def printmap():
    """
    Prints map (3x3 grid) based on player location
    """
    print("    A   B   C ")
    print("  -------------")
    if myPlayer.location == 'a1':
        print("1 | x |   |   |")
    elif myPlayer.location == 'b1':
        print("1 |   | x |   |")
    elif myPlayer.location == 'c1':
        print("1 |   |   | x |")
    else:
        print("1 |   |   |   |")
    print("  -------------")
    if myPlayer.location == 'a2':
        print("2 | x |   |   |")
    elif myPlayer.location == 'b2':
        print("2 |   | x |   |")
    elif myPlayer.location == 'c2':
        print("2 |   |   | x |")
    else:
        print("2 |   |   |   |")
    print("  -------------")
    if myPlayer.location == 'a3':
        print("3 | x |   |   |")
    elif myPlayer.location == 'b3':
        print("3 |   | x |   |")
    elif myPlayer.location == 'c3':
        print("3 |   |   | x |")
    else:
        print("3 |   |   |   |")
    print("  -------------")


### CREATING ZONES FOR MAP ###
ZONENAME = ''
DESCRIPTION = 'description'
EXAMINATION = 'examine'

UP = 'up','north'
DOWN = 'down','south'
LEFT = 'left','west'
RIGHT = 'right','east'    


########################################
### DICTIONARY WITH ZONE INFORMATION ###
### EACH ZONE IS ONE SPOT ON THE MAP ###
### MAP IS 3X3 GRID  =  9 ZONES ########
########################################
zone_map = {
    'a1':{
        ZONENAME: 'Home',
        DESCRIPTION: 'This is your home.',
        EXAMINATION: '',
        UP: '',
        DOWN: 'a2',
        LEFT: '',
        RIGHT: 'b1'   
            },
    'b1':{
        ZONENAME: 'Training Ground',
        DESCRIPTION: 'This is the training ground where everyone hones their power and skills',
        EXAMINATION: "The dojo looks like he could teach you a new move! That can't be cheap\nThere is a sign that says training is sponsored by the mayor.",
        UP: '',
        DOWN: 'b2',
        LEFT: 'a1',
        RIGHT: 'c1'         
            },    
    'c1':{
        ZONENAME: 'Town Hall',
        DESCRIPTION: 'This is Town Hall, where the mayor lives.',
        EXAMINATION: 'Are the pubic allowed inside this place?',
        UP: '',
        DOWN: 'c2',
        LEFT: 'b1',
        RIGHT: ''
            },
            
    'a2':{
        ZONENAME: 'Neighbors House',
        DESCRIPTION: 'This is your neighbors house.',
        EXAMINATION: 'Your neighbor suggests you go check out Town Square - to the east.',
        UP: 'a1',
        DOWN: 'a3',
        LEFT: '',
        RIGHT: 'b2'         
            },
    'b2':{
        ZONENAME: 'Town Square',
        DESCRIPTION: 'This is Town Square.',
        EXAMINATION: 'It is bustling with activity',
        UP: 'b1',
        DOWN: 'b3',
        LEFT: 'a2',
        RIGHT: 'c2'      
            },    
    'c2':{
        ZONENAME: 'Woods',
        DESCRIPTION: 'You are deep in the woods.',
        EXAMINATION: 'The woods are dense, there seems to be an old, overgrown gate to the south.',
        UP: 'c1',
        DOWN: 'c3',
        LEFT: 'b2',
        RIGHT: ''         
            },
            
    'a3':{
        ZONENAME: 'Field',
        DESCRIPTION: 'This is the southwestern field.',
        EXAMINATION: 'It is open and lush.',
        UP: 'a2',
        DOWN: '',
        LEFT: '',
        RIGHT: 'b3'         
            },
    'b3':{
        ZONENAME: 'Woods',
        DESCRIPTION: 'You are deep in the woods.',
        EXAMINATION: 'The woods are dense.',
        UP: 'b2',
        DOWN: '',
        LEFT: 'a3',
        RIGHT: 'c3'         
            },    
    'c3':{
        ZONENAME: 'Dungeon',
        DESCRIPTION: 'This is the storied town dungeon!',
        EXAMINATION: 'Could there be treasure here?',
        UP: 'c2',
        DOWN: '',
        LEFT: 'b3',
        RIGHT: ''         
            } 
    }
    
    
##############################        
##### GAME FUNCTIONALITY #####
##############################  




### STARTS THE GAME ###    
def setup_game():
    """
    This function sets up the game and then calls main game loop
    """
    #os.system('cls')#this was added in tutorial, not sure I need it
    
    ## NAME COLLECTING ##
    texteffect("\nHello, what is your name?\n",0.05)
    player_name = input("> ")
    myPlayer.name = player_name.capitalize()
    
    ## JOB COLLECTING ##
    texteffect("\nWhat class do you want to be: warrior, archer, or mage?\n",0.05)
    player_job = input("> ").lower()
    valid_jobs = ['warrior', 'archer', 'mage']
    if player_job in valid_jobs:
        myPlayer.job = player_job
    while player_job not in valid_jobs:
        texteffect("\nPlease select from: warrior, archer, or mage.\n",0.05)
        player_job = input("> ").lower()
        if player_job.lower() in valid_jobs:
            myPlayer.job = player_job
            
    ## JOB STATS ##    
    ### Currently, hp and pp do nothing
    if myPlayer.job == 'warrior':
        myPlayer.hp = 100
        myPlayer.pp = 50
    elif myPlayer.job == 'archer':
        myPlayer.hp = 75
        myPlayer.pp = 75
    elif myPlayer.job == 'mage':
        myPlayer.hp = 50
        myPlayer.pp = 100
    
    ## JOB PRINT - a vs an ##
    ### Currently, hp and pp do nothing
    
#    if myPlayer.job == 'archer':
#        texteffect("You are an " + player_job + "! " + "You have " + str(myPlayer.hp) + "hp and " + str(myPlayer.pp) + "pp.\n\n",0.05)
#    elif myPlayer.job == 'warrior' or 'mage':
#        texteffect("You are a " + player_job + "! " + "You have " + str(myPlayer.hp) + "hp and " + str(myPlayer.pp) + "pp.\n\n",0.05)
    
    ## INTRO ##
    texteffect("\nWelcome " + myPlayer.name + ", the " + player_job + ".\n",0.05)
    texteffect("Good luck navigating this world.\n",0.05)
    texteffect("Your goal is to uncover all the secrets...\n\n\n\n\n",0.08)
        
    
    #os.system('cls') #this was added in tutorial, not sure I need it
    print("#############################")
    print("#  The game will now begin  #")
    print("#############################")
    texteffect("\n\n\n\n",.3)
          
    movement_handler(myPlayer.location)
    main_game_loop()
    
def main_game_loop():
    """
    The whole game runs through this function
    calls prompt which then calls the move or examine functions
    
    I wonder if I could conDense some of these function? What is best practice?
    """
    turncount = 0
    while myPlayer.gameover is False:
        prompt()
        turncount += 1
    texteffect("\nHopefully, you enjoyed the game. It took you " + str(turncount) +" turns to finish the game!\nYou will soon return to the title screen.\n3... 2... 1...\n\n\n",.05)
    title_screen()
  
    
##########################    
### GAME INTERACTIVITY ###
##########################
    
### SOME VARIABLES ###
c2_gateopen = False
b3_pathblock = True
# these are global variables but are called in functions where they are modified locally
# better way to handle this?
 
    
### FUNCTION FOR EACH "TURN" ###
def prompt():
    """
    This function creates each turn for the game.
    Depending on user input it directs to proper function
    """
    print('\n' + '============================')
    print("What would you like to do?\nEnter move, examine, or quit.")
    action = input ("> ")
    acceptable_actions = ['move', 'm', 'go', 'travel', 'walk', 'examine', 'e','inspect', 'interact', 'look', 'quit']
    while action.lower() not in acceptable_actions:
        print("Unknown action, please try again.\n")
        action = input ("> ")
    if action.lower() == 'quit':
        sys.exit()
    elif action.lower() in ['move', 'm', 'go', 'travel', 'walk']:
        player_move(action.lower())
    elif action.lower() in ['examine', 'e', 'inspect', 'interact', 'look']:
        player_examine(action.lower())

### PRINTS PLAYER LOCATION ###
def movement_handler(destination):
    """
    When the player moves, this function print out everything properly
    """
    myPlayer.location = destination
    print('\n' + ('#' * (4 + len(zone_map[myPlayer.location][ZONENAME]))))
    print('# ' + zone_map[myPlayer.location][ZONENAME] + ' #')
    print(('#' * (4 + len(zone_map[myPlayer.location][ZONENAME])))) 
    #print ('########################')
    print ("You are now in block " + destination + '.\n')
    printmap()
    print ('\n' + 'x ' + zone_map[myPlayer.location][DESCRIPTION])
        
### HANDLES PLAYER MOVEMENT ###           
def player_move(moveAction):
    """
    This function handles player movement
    """
    properdirection = False
    while properdirection == False:
        ask = "Where would you like to move to?\n"
        dest = input(ask)
        if dest not in ['up', 'north', 'down', 'south', 'left', 'west', 'right', 'east']:
            print("Invalid direction, please use up, down, left, or right.")  
            
        elif dest in ['up', 'north']:
            destination = zone_map[myPlayer.location][UP]
            if destination == 'c3' and c2_gateopen == False:
                print("You cannot move that way, please try again. The gate is locked.")
                prompt()
            elif destination == '':
                print("You cannot move that way, please try again.")
            else:
                properdirection = True
                movement_handler(destination)
        elif dest in ['down', 'south']:
            destination = zone_map[myPlayer.location][DOWN]
            if destination == 'c2' and c2_gateopen == False:
                print("You cannot move that way, please try again. The gate is locked.")
                prompt()
            elif destination == '':
                print("You cannot move that way, please try again.")
            else:
                properdirection = True
                movement_handler(destination)
        elif dest in ['left', 'west']:
            destination = zone_map[myPlayer.location][LEFT]
            if destination == 'b3' and b3_pathblock == True:
                print("You cannot move that way, please try again. A monster blocks the path.")   
                prompt()
            elif destination == '':
                print("You cannot move that way, please try again.")
            else:
                properdirection = True
                movement_handler(destination)
        elif dest in ['right', 'east']:
            destination = zone_map[myPlayer.location][RIGHT]
            if destination == 'c3' and b3_pathblock == True:
                print("You cannot move that way, please try again. A monster blocks the path.")   
                prompt()
            elif destination == '':
                print("You cannot move that way, please try again.")
            else:
                properdirection = True
                movement_handler(destination)
        
### HANDLES PLAYER EXAMINATION ###   
# try to do by zone, there must be a better way
            
def player_examine(examineAction):
    """
    This function handles player examination
    A lot of the main game content is inside this function
    """
    ### is global a bad idea here? how to fix?
    global c2_gateopen
    global b3_pathblock
    
    print(zone_map[myPlayer.location][EXAMINATION])

###  A1  ###
    if myPlayer.location == 'a1':
        print("You have a quite comfortable home.")
        homesleep = input("Do you want to take a nap?\n").lower()
        while homesleep not in ['y', 'yes', 'n', 'no']:
            print("Invalid input. Please enter yes or no.") 
            homesleep = input("Do you want to take a nap?\n").lower()
        if homesleep in ['y', 'yes']:
            print("You nap and wake up an hour later. You are well rested!")
            if myPlayer.job == 'warrior':
                myPlayer.hp = 100
                myPlayer.pp = 50
            elif myPlayer.job == 'archer':
                myPlayer.hp = 75
                myPlayer.pp = 75
            elif myPlayer.job == 'mage':
                myPlayer.hp = 50
                myPlayer.pp = 100
        elif homesleep in ['n', 'no']:
                print("You don't need a nap, you already feel great!")
        print("")

###  B1  ###
    elif myPlayer.location == 'b1':
        if myPlayer.specialmove == '':
            if myPlayer.hasmanual == True:
                trainingquestion = input("Do you want to give the dojo the manual found in the mayors house so you can train?\n").lower()
                while  trainingquestion not in ['y', 'yes', 'n', 'no']:
                    print("Invalid input. Please enter yes or no.")
                    trainingquestion = input("Do you want to give the dojo the manual found in the mayors house so you can train?\n").lower()
                if trainingquestion in ['y', 'yes']:
                    if myPlayer.job == 'warrior':
                        myPlayer.specialmove = "Sword Smash"
                        print("You train with the dojo and have learned Sword Smash!")
                    elif myPlayer.job == 'archer':
                        myPlayer.specialmove = "Accurate Arrow"
                        print("You train with the dojo and have have learned Accurate Arrow!")
                    elif myPlayer.job == 'mage':
                        myPlayer.specialmove = "Super Spell"
                        print("You train with the dojo and have have learned Super Spell!")
                elif trainingquestion in ['n', 'no']:
                    print("")
            else:
                print("")
        else: print("You have already learned all the dojo has to teach! You know " + myPlayer.specialmove + "!")

###  C1  ###
    elif myPlayer.location == 'c1':
        townhallquestion = input("Do you want to enter Town Hall?\n").lower()
        while townhallquestion not in ['y', 'yes', 'n', 'no']:
            print("Invalid input. Please enter yes or no.") 
            townhallquestion = input("Do you want to enter Town Hall?\n").lower()
        if townhallquestion in ['y', 'yes']:
            print("You enter town hall, it seems the mayor is away. You walk up to their desk.\n")
            townhalldesk = input("Do you search the desk?\n").lower()
            while townhalldesk not in ['y', 'yes', 'n', 'no']:
                print("Invalid input. Please enter yes or no.") 
                townhalldesk = input("Do you search the desk?\n").lower()
            if townhalldesk in ['y', 'yes']:
                print("You find a manual for free training at the training ground!")
                myPlayer.hasmanual = True
            elif townhalldesk in ['n', 'no']:
                print("You walk away empty handed...")   
        elif townhallquestion in ['n', 'no']:
            print("")        

   
###  A2  ### 
    elif myPlayer.location == 'a2':
        if myPlayer.haskey == False:
            askwhyanswer = input("Do you want to ask why?\n").lower()
            while askwhyanswer not in ['y', 'yes', 'n', 'no']:
                print("Invalid input. Please enter yes or no.") 
                askwhyanswer = input("Do you want to ask why?\n").lower()
            if askwhyanswer in ['y', 'yes']:
                print("He says people have been discussing the town's secret treasure!")
            elif askwhyanswer in ['n', 'no']:
                print("You just nod, saying nothing.")
        elif myPlayer.haskey == True:
            print("Your neighbor notices your key and now strongly suggests you check out Town Square!")
                
###  B2  ### 
    elif myPlayer.location == 'b2':
        if myPlayer.haskey == False:
            print("You hear townsfolk talking about something shiny they saw in the southwestern field.")
        else:
            print("A townsperson spots the key on your belt. They tell you the legend of a secret gate to the east.")
   
###  C2  ### 
    elif myPlayer.location == 'c2':
        if myPlayer.haskey == True:
            if c2_gateopen == True:
                print("The gate has been opened!")
            else:
                opengateq = input("Do you want to try to open the gate with the key you found in the field?\n").lower()
                while opengateq not in ['y', 'yes', 'n', 'no']:
                    print("Invalid input. Please enter yes or no.") 
                    opengateq = input("Do you want to try to open the gate with the key you found in the field?\n").lower()
                if opengateq in ['y', 'yes']:
                    c2_gateopen = True
                    print("The gate has been opened!")
                elif opengateq in ['n', 'no']:
                        print("You walk away, leaving the gate untouched.")
  
  
###  A3  ### 
    elif myPlayer.location == 'a3':
        if myPlayer.haskey == False:
            haskeyquestion = input("You see something shiny. Do you pick it up?\n").lower()
            while haskeyquestion not in ['y', 'yes', 'n', 'no']:
                print("Invalid input. please enter yes or no.") 
                haskeyquestion = input("You see something shiny. Do you pick it up?\n").lower()
            if haskeyquestion in ['y', 'yes']:
                myPlayer.haskey = True
                print("It was a key! You clip the key on your belt.")
            elif haskeyquestion in ['n', 'no']:
                print("")

###  B3  ### 
    elif myPlayer.location == 'b3':
        if myPlayer.specialmove == '':
            print("There is a monster to the east. You should train before fighting the monster.")
        elif b3_pathblock == True:
            monsterfight = input("There is a monster to the east. Do you to fight the monster?\n").lower()
            while monsterfight not in ['y', 'yes', 'n', 'no']:
                print("Invalid input. Please enter yes or no.") 
                monsterfight = input("Do you to fight the monster?\n").lower()
            if monsterfight in ['y', 'yes']:
                print("You engage the monster and use your special skill, " + myPlayer.specialmove)
                texteffect("It is a tough battle... but... you... prevail! The monster is defeated!",.05)
                b3_pathblock = False
                print("The path has cleared!")
            elif monsterfight in ['n', 'no']:
                print("You leave the monster alone")
        else:
            print("A monster used to live here, but a brave soul defeated it!")
  
###  C3  ### 
    elif myPlayer.location == 'c3':
        test = 0
        print("This is the dungeon! You will need skill and power to discover the treasure!")
        testworth = input("Are you ready to test your worth?\n").lower()
        while testworth not in ['y', 'yes', 'n', 'no']:
            print("Invalid input. please enter yes or no.") 
            testworth = input("Are you ready to test your worth?\n").lower()
        if testworth in ['y', 'yes']:
            if myPlayer.specialmove == '':
                texteffect("You are not strong enough yet! Perhaps you should do some training!\n",.05)
            else:
                texteffect("You are strong! Your strength is worthy of the treasure!\n",.08)
                test += 1
            if myPlayer.haskey == False:
                texteffect("You are not powerful or influential enough yet! Perhaps you should do talk to the townsfolk at the Square!\n",.05)
            else:
                texteffect("You are powerful and influential! These attributes are worthy of the treasure!",.08)
                test += 1           
        elif testworth in ['n', 'no']:
            print("Keep training and exploring, you can test your worth later!")
        if test == 2:
            texteffect("\nCONGRATULATIONS!!! You have earned the treasure and won the game!\n",.05)
            myPlayer.gameover = True 
  
    else:
        print("")
        


#######################   
### STARTS THE GAME ###
#######################
        
title_screen()

#######################
