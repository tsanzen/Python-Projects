import random
import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_game():
    clear()
    print("Welcome to the Number Guessing Game!")
    print("Choose your difficulty:")
    print("1. Easy (1–10)  |  Attempts: 6")
    print("2. Medium (1–25) |  Attempts: 5")
    print("3. Hard (1–50)   |  Attempts: 4")
    print("4. Impossible (1–100) | Attempts: 3")

    # Difficulty selection
    while True:
        choice = input("\nEnter difficulty (1-4): ")
        if choice == '1':
            max_num, attempts_left, difficulty = 10, 6, "Easy"
            break
        elif choice == '2':
            max_num, attempts_left, difficulty = 25, 5, "Medium"
            break
        elif choice == '3':
            max_num, attempts_left, difficulty = 50, 4, "Hard"
            break
        elif choice == '4':
            max_num, attempts_left, difficulty = 100, 3, "Impossible"
            break
        else:
            print("Invalid choice, try again.")

    number_to_guess = random.randint(1, max_num)
    clear()
    print(f"{difficulty} mode selected! Guess a number between 1 and {max_num}.")
    print(f"You have {attempts_left} attempts. Good luck!")

    while attempts_left > 0:
        try:
            guess = int(input("Enter your guess: "))
            attempts_left -= 1

            if guess < number_to_guess:
                print("Too low!")
            elif guess > number_to_guess:
                print("Too high!")
            else:
                print(f"Correct! You guessed the number {number_to_guess}!")
                time.sleep(7)
                return
            if attempts_left > 0:
                print(f"Attempts left: {attempts_left}")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"Out of attempts! The number was {number_to_guess}.")
    time.sleep(2)

# Replay loop
while True:
    play_game()
    clear()
    again = input("Do you want to play again? (y/n): ").lower()
    if again != 'y':
        clear()
        print("Thanks for playing! See you next time!")
        break
