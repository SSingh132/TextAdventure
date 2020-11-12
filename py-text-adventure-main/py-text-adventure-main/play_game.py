import json
import time #https://www.youtube.com/watch?v=Q9qp4CVngKE
import os
import random

start = time.time()

def main():
    # TODO: allow them to choose from multiple JSON files?
    print("What game would you like to play?")
    count = 0
    for name in os.listdir():
        if name.endswith('.json'):
            count += 1
            print(count, ".", name[:-5])
    game_to_play = input("What game would you like to play? ")
    if game_to_play == "1":
        with open('adventure.json') as fp:
            game = json.load(fp)
    if game_to_play == "2":
        with open('spooky_mansion.json') as fp:
            game = json.load(fp)
        
        
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)


def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    my_items = ['Cell Phone; no signal or battery...']
    cat_seen = False
    
    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])

        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.
        room_items = here['items']
        #if current_place == rooms['balcony']:
        #   room_items = ["Mansion Key"]
        #my_items = here["items"]
        
        cat = False
    
        cat_or_no = random.randint(0, 10)
        
        if cat_or_no > 5:
            cat = True
            
        if cat == True:
            if cat_seen == False:
                print("A black cat is roaming around the room. It looks you in the eye...")
                cat_seen = True
            else:
                print("The black cat followed you here")
            
        
        for i in range(len(room_items)):
            if room_items[i] in my_items:
                print("You have taken this room's items")
                break
            else:
                print("There is a", room_items[i])

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, my_items)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()
        
        if action == "help":
            print_instructions()
            continue

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        
        if action == "stuff":
            #print("You don't have stuff")
            if len(my_items) == 0:
                print("You have no items")
            else:
                for i in range(len(my_items)):
                    print("You have", my_items[i])
            continue
        
        if action == "take":
            for i in range(len(room_items)):
                my_items.append(room_items[i])
            for i in range(len(my_items)):
                print("You now have", my_items[i])
            continue
        
        if action == "drop":
            answer = input("What would you like to drop? ")
            for i in range(len(my_items)):
                if answer in my_items[i]:
                    room_items.append(my_items[i])
                    my_items.remove(my_items[i])
            continue
        
#             if answer in my_items:
#                 my_items.remove(answer)
#             for i in range(len(my_items)):
#                 print("You now have", my_items[i])
#             room_items.append(answer)
                        
            
        
        
        # Try to turn their action into an exit, by number.
        
        try:
            num = int(action) - 1
            selected = usable_exits[num]
#             if exit["required_key"] not in stuff:
#                 print("You try to open the door, but it's locked")
#                 continue
            if 'required_key' in selected:
                if selected['required_key'] not in my_items:
                    print("This door is locked")
                    continue
            current_place = selected['destination']
            print("...")
        except:
            counter = 0
            for exits in usable_exits:
                counter += 1
                if action in exits['description']:
                    current_place = usable_exits[counter-1]['destination']
                    continue
                continue
            continue
#             if action == "down":
#                 current_place = usable_exits[0]['destination']
#                 continue
#             elif action == "up":
#                 current_place = usable_exits[1]['destination']
#                 continue
#             elif action == "red":
#                 current_place = usable_exits[2]['destination']
#                 continue
#             elif action == "front":
#                 current_place = usable_exits[3]['destination']
#                 continue
#             elif type(action) is str:
#                 counter = 0
#                 for i in range(len(usable_exits)):
#                     for x in range(len(action)):
#                         if action[x] == usable_exits[i]["description"][x]:
#                             counter += 1
#                         if counter >= .9 * len(usable_exits[i]["description"]):
#                             current_place = usable_exits[i]["destination"]
#                             continue
            
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")    
    print("=== GAME OVER ===")
    
    end = time.time()
    
    time_elapsed = (end - start)
    if time_elapsed > 60:
        time_elapsed_minutes = (end - start) // 60
        time_elapsed_seconds = time_elapsed - (time_elapsed_minutes * 60)
    else:
        time_elapsed_minutes = 0
        time_elapsed_seconds = time_elapsed
        
    print("It took you", time_elapsed_minutes, "minutes and", time_elapsed_seconds,
          "seconds to complete the game")


def find_usable_exits(room, my_items):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            usable.append(exit)
            continue
#         if "required_key" in exit:
#             #if exit["required_key"] in stuff:
#             usable.append(exit)
            continue
        usable.append(exit)
        
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()


#for exit in exits
    #for word in exit[description].split():
    #if word in action.split() == word
    
    #if action in exit[description]
    #make matching[] list