import random
import time
import matplotlib.pyplot as plt
import openai

# Set your OpenAI API key here
API_KEY = "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"

# Configure OpenAI API
openai.api_key = API_KEY

# Character class
class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

# Player class (inherits from Character)
class Player(Character):
    def __init__(self, name, health, attack, defense):
        super().__init__(name, health, attack, defense)

# Enemy class (inherits from Character)
class Enemy(Character):
    def __init__(self, name, health, attack, defense):
        super().__init__(name, health, attack, defense)

# Function to simulate a battle between player and enemy
def battle(player: Player, enemy: Enemy) -> bool:
    print(f"A wild {enemy.name} appears!")
    time.sleep(1)

    # Lists to store health values for graph plotting
    player_health_history = [player.health]
    enemy_health_history = [enemy.health]

    while player.health > 0 and enemy.health > 0:
        print(f"{player.name}: Health = {player.health}, Attack = {player.attack}, Defense = {player.defense}")
        print(f"{enemy.name}: Health = {enemy.health}, Attack = {enemy.attack}, Defense = {enemy.defense}")
        print("-------------------------------")

        # Player's turn
        player_attack = max(0, player.attack - enemy.defense)
        enemy.take_damage(player_attack)
        print(f"{player.name} attacked {enemy.name} and dealt {player_attack} damage.")
        player_health_history.append(player.health)
        enemy_health_history.append(enemy.health)
        if enemy.health <= 0:
            print(f"{player.name} defeated {enemy.name}! You win!")
            plot_battle(player_health_history, enemy_health_history)
            return True

        # Enemy's turn
        enemy_attack = max(0, enemy.attack - player.defense)
        player.take_damage(enemy_attack)
        print(f"{enemy.name} attacked {player.name} and dealt {enemy_attack} damage.")
        player_health_history.append(player.health)
        enemy_health_history.append(enemy.health)
        if player.health <= 0:
            print(f"{player.name} was defeated! You lose!")
            plot_battle(player_health_history, enemy_health_history)
            return False

        print("-------------------------------")
        time.sleep(1)

# Function to plot battle progress
def plot_battle(player_health_history, enemy_health_history):
    plt.plot(player_health_history, label="Player")
    plt.plot(enemy_health_history, label="Enemy")
    plt.xlabel("Turn")
    plt.ylabel("Health")
    plt.title("Battle Progress")
    plt.legend()
    plt.show()

# Function to generate a response from ChatGPT
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# Game loop
def game_loop(player: Player) -> None:
    print("Welcome to the Ramayana RPG!")
    print("-------------------------------")
    time.sleep(1)
    while True:
        # Generate a random enemy
        enemy_name = random.choice(["Ravana", "Kumbhakarna", "Indrajit"])
        enemy_health = random.randint(50, 100)
        enemy_attack = random.randint(8, 12)
        enemy_defense = random.randint(3, 6)
        enemy = Enemy(enemy_name, enemy_health, enemy_attack, enemy_defense)

        battle(player, enemy)

        # Reset player's health for the next battle
        player.health = 100

        print("-------------------------------")
        time.sleep(1)

        # Prompt player for their next action using ChatGPT
        prompt = f"You defeated {enemy.name}. What do you do next?"
        response = generate_response(prompt)

        # Process ChatGPT response and determine player's action
        if "1. Explore further" in response:
            print("You decide to explore further.")
            # Continue the game loop
        elif "2. Return to town" in response:
            print("You choose to return to town.")
            # Implement logic to return to town
        elif "3. Rest and heal" in response:
            print("You decide to rest and heal.")
            # Implement logic to rest and heal
        else:
            print("I'm sorry, I didn't understand your action. Please try again.")
            # Continue the game loop

        print("-------------------------------")
        time.sleep(1)

# Entry point
def main() -> None:
    player = Player("Player", 100, 10, 5)
    game_loop(player)

if __name__ == "__main__":
    main()
