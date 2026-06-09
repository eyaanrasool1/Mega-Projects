import random
import time


# =========================
# ITEM
# =========================
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description


# =========================
# ENEMY
# =========================
class Enemy:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


# =========================
# ROOM
# =========================
class Room:
    def __init__(self, name, description, locked=False, required_item=None):
        self.name = name
        self.description = description
        self.locked = locked
        self.required_item = required_item

        self.items = []
        self.enemy = None

        self.up = None
        self.down = None
        self.forward = None
        self.backward = None

    def look(self):
        print("\n====================")
        print(self.name)
        print(self.description)

        exits = []
        if self.up: exits.append("up")
        if self.down: exits.append("down")
        if self.forward: exits.append("forward")
        if self.backward: exits.append("backward")

        print("Exits:", exits)

        if self.items:
            print("Items:", [i.name for i in self.items])

        if self.enemy:
            print("Enemy:", self.enemy.name)


# =========================
# PLAYER
# =========================
class Player:
    def __init__(self, hp, current_room):
        self.hp = hp
        self.current_room = current_room
        self.inventory = []

    def take_damage(self, dmg):
        self.hp -= dmg
        print(f"💔 HP: {self.hp}")

    def show_inventory(self):
        print("🎒 Inventory:", [i.name for i in self.inventory])

    def take_item(self, name):
        for item in self.current_room.items:
            if item.name.lower() == name.lower():
                self.inventory.append(item)
                self.current_room.items.remove(item)
                print("📦 Picked:", item.name)
                return
        print("❌ Not found")

    def move(self, direction):
        room = getattr(self.current_room, direction)

        if not room:
            print("❌ Can't go there")
            return

        if room.locked:
            if not any(i.name == room.required_item for i in self.inventory):
                print("🔒 Locked! Need:", room.required_item)
                return

        self.current_room = room
        print("\n➡️ Moved to:", room.name)
        room.look()

        if room.enemy:
            combat(self, room.enemy)


# =========================
# COMBAT
# =========================
def combat(player, enemy):
    words = ["apple", "stone", "river", "light", "green", "metal"]
    word = random.choice(words)

    print(f"\n⚔️ {enemy.name} ATTACKS!")
    print("TYPE THIS:", word)

    start = time.time()
    user = input("> ")
    end = time.time()

    if user != word:
        player.take_damage(enemy.damage)
        return

    if end - start > 5:
        player.take_damage(enemy.damage)
        return

    print("✅ Enemy defeated!")


# =========================
# WORLD (YOUR EXACT MAP LOGIC)
# =========================
def create_world():

    start = Room("START ROOM", "Starting point")
    meeting = Room("MEETING HALL", "Meeting area")

    hallway = Room("HALLWAY", "Long corridor")
    garage = Room("OLD GARAGE", "Old garage", True, "Blue Key")
    kitchen = Room("KITCHEN", "Food area", True, "Red Key")
    escape = Room("ESCAPE", "Final Exit")

    studio = Room("STUDIO", "Creative room")
    bedroom = Room("BED ROOM", "Rest area")

    # =========================
    # MAIN STRUCTURE (YOUR MAP)
    # =========================

    # START → HALLWAY → GARAGE → ESCAPE
    start.forward = hallway
    hallway.backward = start

    hallway.forward = garage
    garage.backward = hallway

    garage.forward = escape
    escape.backward = garage

    # MEETING HALL → KITCHEN (TOP BRANCH)
    meeting.backward = start
    start.up = meeting
    meeting.forward = kitchen
    kitchen.backward = meeting

    # STUDIO → BEDROOM (BOTTOM BRANCH)
    studio.backward = start
    start.down = studio
    studio.forward = bedroom
    bedroom.backward = studio

    # CONNECT BEDROOM TO GARAGE (as in your map)
    bedroom.up = garage
    garage.down = bedroom

    # =========================
    # ENEMIES (AS YOU WANTED)
    # =========================
    hallway.enemy = Enemy("Monster", 10)
    garage.enemy = Enemy("Beast", 15)

    # =========================
    # ITEMS (AS YOU WANTED)
    # =========================

    # BLUE KEY (opens garage)
    meeting.items.append(Item("Blue Key", "Opens Garage"))

    # RED KEY (in garage)
    garage.items.append(Item("Red Key", "Opens Kitchen"))

    # MEDKIT (bed room)
    bedroom.items.append(Item("Medkit", "Heals HP"))

    # ESCAPE KEY (kitchen)
    kitchen.items.append(Item("Escape Key", "Win item"))

    return start, [
        start, meeting, hallway, garage,
        kitchen, escape, studio, bedroom
    ]


# =========================
# MAP (YOUR EXACT STRUCTURE)
# =========================
def print_map():
    print("\n====== DUNGEON MAP ======\n")

    print("     -------- [MEETING HALL] -- [KITCHEN]")
    print("     |")
    print("[START ROOM] -- [HALLWAY] -- [OLD GARAGE] -- [ESCAPE]")
    print("      |                           |")
    print("       -------- [STUDIO]  --  [BED ROOM]")


# =========================
# GAME
# =========================
class Game:
    def start(self):
        start, rooms = create_world()

        print_map()

        player = Player(100, start)

        print("\nCommands:")
        print("up / down / forward / backward")
        print("pick <item>")
        print("inventory")
        print("look")

        while True:
            cmd = input("\n> ").lower()

            if cmd in ["up", "down", "forward", "backward"]:
                player.move(cmd)

            elif cmd.startswith("pick"):
                player.take_item(cmd.replace("pick", "").strip())

            elif cmd == "inventory":
                player.show_inventory()

            elif cmd == "look":
                player.current_room.look()

            elif player.hp <= 0:
                print("\n💀 YOU DIED")
                break

            elif player.current_room.name == "ESCAPE":
                if any(i.name == "Escape Key" for i in player.inventory):
                    print("\n🏆 YOU WIN!")
                    break


# =========================
# RUN GAME
# =========================
Game().start()