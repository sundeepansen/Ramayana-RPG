import random
import time
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

# Function to generate content using ChatGPT
def generate_content(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()

# Function to simulate a battle between player and enemy
def battle(player: Player, enemy: Enemy) -> bool:
    print(f"A wild {enemy.name} appears!")
    time.sleep(1)
    while player.health > 0 and enemy.health > 0:
        print(f"{player.name}: Health = {player.health}, Attack = {player.attack}, Defense = {player.defense}")
        print(f"{enemy.name}: Health = {enemy.health}, Attack = {enemy.attack}, Defense = {enemy.defense}")
        print("-------------------------------")

        # Player's turn
        player_attack = max(0, player.attack - enemy.defense)
        enemy.take_damage(player_attack)
        print(f"{player.name} attacked {enemy.name} and dealt {player_attack} damage.")
        if enemy.health <= 0:
            print(f"{player.name} defeated {enemy.name}! You win!")
            return True

        # Enemy's turn
        enemy_attack = max(0, enemy.attack - player.defense)
        player.take_damage(enemy_attack)
        print(f"{enemy.name} attacked {player.name} and dealt {enemy_attack} damage.")
        if player.health <= 0:
            print(f"{player.name} was defeated! You lose!")
            return False

        print("-------------------------------")
        time.sleep(1)

# Game loop
def game_loop(player: Player) -> None:
    print("Welcome to the Text-Based RPG!")
    print("-------------------------------")
    time.sleep(1)
    while True:
        # Generate content using ChatGPT
        prompt = "You find yourself in a new area. What do you do?"
        print("You find yourself in a new area. What do you do?")
        content = generate_content(prompt)
        print(content)
        time.sleep(1)

        # Simulate battle or other events
        if random.random() < 0.5:
            enemy = Enemy("Enemy", random.randint(50, 100), random.randint(8, 12), random.randint(3, 6))
            if not battle(player, enemy):
                break
        else:
            # Add other events or encounters here
            pass

# Entry point
def main() -> None:
    player = Player("Player", 100, 10, 5)
    game_loop(player)

if __name__ == "__main__":
    main()
