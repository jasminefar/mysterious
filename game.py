import json

# Player Class
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.current_room = None

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def add_item(self, item):
        self.inventory.append(item)

    def __str__(self):
        return f"{self.name} (Health: {self.health}, Inventory: {self.inventory})"

# Room Class
class Room:
    def __init__(self, name, description, items=None):
        self.name = name
        self.description = description
        self.items = items if items else []
        self.connections = {}

    def connect(self, direction, room):
        self.connections[direction] = room

    def __str__(self):
        room_info = f"{self.name}\n{self.description}\nItems: {', '.join(self.items)}"
        connections_info = f"Exits: {', '.join(self.connections.keys())}"
        return f"{room_info}\n{connections_info}"

# Game Class
class Game:
    def __init__(self, player):
        self.player = player
        self.rooms = self.create_rooms()
        self.player.current_room = self.rooms["Foyer"]

    def create_rooms(self):
        foyer = Room("Foyer", "A small foyer with a dusty chandelier. There's a staircase leading up.")
        kitchen = Room("Kitchen", "A kitchen with old, rusty appliances. There's a door to the backyard.", ["Knife"])
        library = Room("Library", "A library filled with ancient books and a mysterious aura.", ["Old Book"])
        backyard = Room("Backyard", "A neglected backyard with overgrown grass and a shed.", ["Shovel"])

        foyer.connect("north", kitchen)
        foyer.connect("east", library)
        kitchen.connect("south", foyer)
        library.connect("west", foyer)
        kitchen.connect("east", backyard)
        backyard.connect("west", kitchen)

        return {
            "Foyer": foyer,
            "Kitchen": kitchen,
            "Library": library,
            "Backyard": backyard
        }

    def start_game(self):
        print("Welcome to the Mystery Adventure!")
        while self.player.health > 0:
            print(self.player.current_room)
            action = input("What would you like to do? (move/take/use/look/inventory/quit): ").lower()
            if action == "move":
                direction = input("Enter direction (north/east/south/west): ").lower()
                self.move_player(direction)
            elif action == "take":
                item = input("Enter the item to take: ").capitalize()
                self.take_item(item)
            elif action == "use":
                item = input("Enter the item to use: ").capitalize()
                self.use_item(item)
            elif action == "look":
                print(self.player.current_room)
            elif action == "inventory":
                print(f"Inventory: {self.player.inventory}")
            elif action == "quit":
                self.save_game()
                print("Game saved. Thanks for playing!")
                break
            else:
                print("Invalid action. Please try again.")

        if self.player.health <= 0:
            print("You have lost all your health. Game Over.")

    def move_player(self, direction):
        if direction in self.player.current_room.connections:
            self.player.current_room = self.player.current_room.connections[direction]
            print(f"You move to the {self.player.current_room.name}.")
        else:
            print("You can't move in that direction.")

    def take_item(self, item):
        if item in self.player.current_room.items:
            self.player.add_item(item)
            self.player.current_room.items.remove(item)
            print(f"You take the {item}.")
        else:
            print(f"There is no {item} here.")

    def use_item(self, item):
        if item in self.player.inventory:
            if item == "Knife" and self.player.current_room.name == "Backyard":
                print("You use the knife to cut through the overgrown grass and find a hidden key!")
                self.player.add_item("Key")
            elif item == "Old Book" and self.player.current_room.name == "Library":
                print("You read the old book and discover a hidden passage behind a bookshelf!")
                self.player.current_room.connect("north", self.rooms["Secret Room"])
                self.rooms["Library"].description += " There's a hidden passage to the north."
            else:
                print(f"You can't use the {item} here.")
        else:
            print(f"You don't have a {item}.")

    def save_game(self):
        save_data = {
            "name": self.player.name,
            "health": self.player.health,
            "inventory": self.player.inventory,
            "current_room": self.player.current_room.name
        }
        with open("save_game.json", "w") as file:
            json.dump(save_data, file)
        print("Game saved successfully.")

    def load_game(self):
        try:
            with open("save_game.json", "r") as file:
                save_data = json.load(file)
                self.player = Player(save_data["name"])
                self.player.health = save_data["health"]
                self.player.inventory = save_data["inventory"]
                self.rooms = self.create_rooms()
                self.player.current_room = self.rooms[save_data["current_room"]]
            print("Game loaded successfully.")
        except FileNotFoundError:
            print("No saved game found.")

# Main Game Loop
def main():
    print("Welcome to the Mystery Adventure Game!")
    print("1. New Game")
    print("2. Load Game")
    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter your character's name: ")
        player = Player(name)
        game = Game(player)
    elif choice == "2":
        game = Game(None)
        game.load_game()
        player = game.player
    else:
        print("Invalid choice.")
        return

    game.start_game()

if __name__ == "__main__":
    main()
