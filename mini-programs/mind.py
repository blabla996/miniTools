import random

num_players = int(input("Number of players (min 2): "))
level = int(input("Level (min 1): "))

numbers = random.sample(range(1, 101), num_players * level)

player_numbers = []

for i in range(num_players):
    player_numbers.append(
        numbers[i * level:(i + 1) * level]
    )

for i in range(num_players):
    print("\n" * 50)
    print(f"=== PLAYER {i + 1} ===")
    input("Press Enter to read your numbers")

    print(player_numbers[i])

    input("\nPress Enter for the next player")

print("\n" * 50)
print("All players have seen their numbers! Ready to start the game.")