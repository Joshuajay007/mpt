import turtle as t
from time import sleep
from tkinter import messagebox
from random import choice
import pickle

# Import functions from the loacal package
from mptpkg import voice_to_text, print_say

# Set up the screen
t.setup(700,600, 10, 70)
t.hideturtle()
t.tracer(False)
t.bgcolor("lightgreen")
t.title("Connect Four in Turtle Graphics")
# Draw six thick vertical lines
t.pensize(5)
for i in range(-250,350,100):  
    t.up()
    t.goto(i, -350)
    t.down()
    t.goto(i, 350)
    t.up()
# Draw five thin gray horizontal lines to form grid    
t.pensize(1)
t.pencolor("grey")
for i in range(-200,300,100):  
    t.up()
    t.goto(-350,i)
    t.down()
    t.goto(350,i)
    t.up()
# Write column numbers on the board
colnum=1
for x in range(-300, 350, 100):
    t.goto(x,270)
    t.write(colnum,font=('Arial',20,'normal'))
    colnum += 1
# The red player moves first
turn="red"
# The x-coordinates of the center of the 7 columns
xs=[-300,-200,-100,0,100,200,300]
# The y-coordinates of the center of the 6 rows
ys=[-250,-150,-50,50,150,250]
# Keep track of the occupied cells
occupied=[list(),list(),list(),list(),list(),list(),list()]
# Create a second turtle to show disc falling
fall=t.Turtle()
fall.up()
fall.hideturtle()
# Create a list of valid moves
validinputs=[1,2,3,4,5,6,7]
# Define a win_game() function to check if someone wins the game
def win_game(num, color, lst):
    win=False
    # Convert column and row numbers to indexes in the list of lists lst
    x=num-1
    y=len(lst[x])
    # Check if the disc forms four in a row vertically
    try:
        if lst[x][y-1]==color and lst[x][y-2]==color and lst[x][y-3]==color and y>=3:
                win=True     
    except IndexError:
        pass  
    # Check if the disc forms four in a row horizontally
    try:
        if lst[x-3][y]==color and lst[x-2][y]==color and lst[x-1][y]==color and x>=3:
                win=True            
    except IndexError:
        pass
    try:
        if lst[x-2][y]==color and lst[x-1][y]==color and lst[x+1][y]==color and x>=2:
                win=True            
    except IndexError:
        pass
    try:
        if lst[x-1][y]==color and lst[x+1][y]==color and lst[x+2][y]==color and x>=1:
                win=True          
    except IndexError:
        pass
    try:
        if lst[x+1][y]==color and lst[x+2][y]==color and lst[x+3][y]==color:
                win=True        
    except IndexError:
        pass
    # Check if the disc forms four in a row diagonally in / shape
    try:
        if lst[x+1][y+1]==color and lst[x+2][y+2]==color and lst[x+3][y+3]==color:
                win=True       
    except IndexError:
        pass
    try:
        if lst[x-1][y-1]==color and lst[x+1][y+1]==color and lst[x+2][y+2]==color  and x>=1 and y>=1:
                win=True      
    except IndexError:
        pass
    try:     
        if lst[x-1][y-1]==color and lst[x-2][y-2]==color and lst[x+1][y+1]==color  and x>=2 and y>=2:
                win=True
    except IndexError:
        pass
    try:
        if lst[x-1][y-1]==color and lst[x-2][y-2]==color and lst[x-3][y-3]==color  and x>=3 and y>=3:
                win=True      
    except IndexError:
        pass
    # Check if the disc forms four in a row diagonally in \ shape
    try:
        if lst[x+1][y-1]==color and lst[x+2][y-2]==color and lst[x+3][y-3]==color and y>=3:
                win=True         
    except IndexError:
        pass
    try:
        if lst[x-1][y+1]==color and lst[x+1][y-1]==color and lst[x+2][y-2]==color and x>=1 and y>=2:
                win=True      
    except IndexError:
        pass
    try:
        if lst[x-1][y+1]==color and lst[x-2][y+2]==color and lst[x+1][y-1]==color and x>=1 and y>=1:
                win=True      
    except IndexError:
        pass
    try:
        if lst[x-1][y+1]==color and lst[x-2][y+2]==color and lst[x-3][y+3]==color  and x>=3:
                win=True        
    except IndexError:
        pass
    # Return the value stored in win
    return win
# Count the number of rounds
rounds=1
# A history of moves moade
moves_made=[]
# Obtain gamedata
with open('conn_simulates.pickle', 'rb') as fp:
    gamedata=pickle.load(fp)
# Define the best_move() function
def best_move():
    # Take column 4 in the first move
    if len(occupied[3])==0:
        return 4
    # If there is only one column has free slots, use the column
    if len(validinputs)==1:
        return validinputs[0]
    simu=[]
    for y in gamedata:
       if y[1:len(moves_made)+1]==moves_made:
           simu.append(y)
    # Now we look at the next move;           
    outcomes={x:[] for x in validinputs} 
    # We collect all the outcomes for each next move
    for y in simu:
       outcomes[y[len(moves_made)+1]].append(y[0])
    # Set the initial value of bestoutcome        
    bestoutcome=-2;
    # Randomly select a move to be best_move
    best_move=validinputs[0]
    # iterate through all possible next moves 
    for move in validinputs:
        if len(outcomes[move])>0:
            outcome=sum(outcomes[move])/len(outcomes[move])
            # If the average outcome from that move beats the current best move
            if outcome>bestoutcome:
                # Update the bestoutcome
                bestoutcome=outcome
                # Update the best move
                best_move=move
    return best_move
def computer_move():
    global turn, rounds, validinputs
    # Choose the best move
    col = best_move()
    if col==None:
        col = choice(validinputs)
    print_say(f"The computer chooses column {col}.")
    # Calculate the lowest available row number in that column
    row=1+len(occupied[col-1])
    # Show the disc fall from the top
    if row<6:
        for i in range(6,row,-1):
            fall.goto(xs[col-1],ys[i-1])
            fall.dot(80,turn)
            t.update()
            sleep(0.05)
            fall.clear()
    # Go to the cell and place a dot of the player's color
    t.up()
    t.goto(xs[col-1],ys[row-1])
    t.dot(80,turn)
    t.update()
    moves_made.append(col)
    # Check if the player has won
    if win_game(col, turn, occupied)==True:
        # If a player wins, invalid all moves, end the game
        validinputs=[]
        messagebox.showinfo("End Game",f"Congrats player {turn}, you won!")
    # If all cellls are occupied and no winner, it's a tie
    if rounds==42 and win_game(col, turn, occupied)==False:
        messagebox.showinfo("Tie Game","Game over, it's a tie!")
    # Counting rounds
    rounds += 1
    # Add the move to the occupied list to keep track
    occupied[col-1].append(turn)
    # Update the list of valid moves
    if len(occupied[col-1])==6 and col in validinputs:
        validinputs.remove(col)        
    # Give the turn to the other player
    if turn=="red":
        turn="yellow"
    else:
        turn="red"     
# Computer moves first
computer_move()
# Start an infinite loop to take voice inputs
while len(validinputs)>0:
    # Ask for your move
    print_say(f"Player {turn}, what's your move?")
    # Capture your voice input
    inp=voice_to_text().lower()
    print_say(f"You said {inp}.")
    inp=inp.replace('number ','')
    inp=inp.replace('one','1')   
    inp=inp.replace('two','2')
    inp=inp.replace('three','3')
    inp=inp.replace('four','4')
    inp=inp.replace('five','5')
    inp=inp.replace('six','6')
    inp=inp.replace('seven','7')
    # If your voice input is a valid column number, play the move
    try:    
        if int(inp) in validinputs:
            col=int(inp)
            # Calculate the lowest available row number in that column
            row=len(occupied[col-1])+1
            # Show the disc fall from the top
            if row<6:
                for i in range(6,row,-1):
                    fall.goto(xs[col-1],ys[i-1])
                    fall.dot(80,turn)
                    t.update()
                    sleep(0.05)
                    fall.clear()
            # Go to the cell and place a dot of the player's color
            t.up()
            t.goto(xs[col-1],ys[row-1])
            t.dot(80,turn)
            t.update()
            moves_made.append(col)
            # Check if the player has won
            if win_game(col, turn, occupied)==True:
                # If a player wins, invalid all moves, end the game
                validinputs=[]
                print_say(f"Congrats player {turn}, you won!")
                messagebox.showinfo("End Game",f"Congrats player {turn}, you won!")
                break
            # If all cellls are occupied and no winner, it's a tie
            if rounds==42:
                print_say("Game over, it's a tie!")
                messagebox.showinfo("Tie Game","Game over, it's a tie!")
                break
            # Counting rounds
            rounds += 1
            # Add the move to the occupied list to keep track
            occupied[col-1].append(turn)
            # Update the list of valid moves
            if len(occupied[col-1])==6:
                validinputs.remove(str(col))        
            # Give the turn to the other player
            if turn=="red":
                turn="yellow"
            else:
                turn="red" 
            # The computer moves
            if len(validinputs)>0:
                computer_move()
    # If input is not a valid move, try again
    except:
        print_say("Sorry, that's an invalid move!")    
t.done()        
try:
    t.bye()
except t.Terminator:
    print('exit turtle')
