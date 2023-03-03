import random
print("Welcome to snake water gun game")
n = int(input("Enter the number of Rounds:"))
option = ['s','w','g']
Rounds = 1
computer_win = 0
player_win = 0
while Rounds <= n:
    print(f"Round:{Rounds}\nSnake-'s'\nWater-'w'\nGun-'g'")
    try:
        player = input("Chose your option: ")
    except EOFError as e:
        print(e)      
    
    if player!='s' and player!='g' and player!='w':
        print("Invalid Input , Try again!") 
        continue       

    computer = random.choice(option)
    
    if computer=='s':
        if player=='w':
            computer_win+=1
        elif player=='g':
            player_win+=1
    elif computer=='w':
        if player=='g':
            computer_win+=1
        elif player=='s':
            player_win+=1
    elif computer=='g':
        if player=='s':
          player_win+=1
        elif player=='w':
            computer_win+=1

    if player_win>computer_win:
        print(f"You won the round {Rounds}\n")
    elif computer_win>player_win:
        print(f"Computer won the round {Rounds}\n")
    else:
        print("Draw!\n")
    Rounds+=1

if player_win>computer_win:
    print("Congratulation ! you won the game ")
elif computer_win>player_win:
    print("You loss !")
else:
    print("Match Draw !")



