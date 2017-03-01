import threading
import json

admins = ["faroeson#2506"]

#Extensions to load
extensions_dir = "extensions"
startup_extensions = ["admin", "pet", "inventory", "egg", "store"]

MAX_HUNGER = 10
MAX_HAPPY = 10
user_data_json_file = "vocamon.json"


#mood status in order from worst [0] to best [10] messages
mood_msg = [" is isn't afraid of death.",
            " wonders if a gun to the head will be swift and painless.",
            " appears to be reading a book about tying knots.",
            " is feeling a little suicidal today.",
            " doesn't believe in love anymore.",
            " wishes it was born to a different owner.",
            " stares at you. 'Meh.'",
            " doesn't mind being around you.",
            " is fairly content.",
            " is beaming with happiness!"
            " calls its owner senpai."]



#READ JSON FILE TO LOAD SAVED DATA, ELSE, START NEW
def load_data():
    try:
        with open(user_data_json_file) as json_file:
            user_data = json.load(json_file)
        print('Save data loaded.')
    except :
        print('Unable to read save data or none supplied.')
        user_data = {'players': {}, 'store': {}}
    return user_data

#save data to file
def save_data():
    with open(user_data_json_file, 'w') as outfile:
        json.dump(user_data, outfile)


##################### dont fucking touch this line.
##################### it's gotta be after load_data but before anything else.

user_data = load_data() 

####################

#takes a string as input and creates save data for it. 
#if the user existed, it returns True, else, false.
def mother_exists(player):
    if player not in user_data['players']:
        user_data['players'][player] = {}
        player_info = user_data['players'][player]
        player_info['egg'] = {'type': 0}
        player_info['mon'] = {'name': 0, 'type': 0, 'hunger': 0, 'happy': 0}
        player_info['inventory'] = {'food': 5, 'egg': 0, 'stars': 0}
        return False
    return True

#takes a player name as a string and checks if the user has an egg.
def has_egg(player):
    if mother_exists(player):
        if user_data['players'][player]['inventory']['egg'] != 0:
            return True
    return False

#takes a player name as a string and checks if the user has a mon.
def has_mon(player):
    if mother_exists(player):
        if user_data['players'][player]['mon']['type'] != 0:
            return True
    return False

#takes a player name as a string and checks if the user has any food.
def has_food(player):
    if mother_exists(player):
        if user_data['players'][player]['inventory']['food'] != 0:
            return True
    return False


################TIMER STUFF

#subtract a point of hunger or happiness (hoh)
def minus_hoh(pet, hoh):
    if (hoh != 'hunger') and (hoh != 'happy'):
        print("invalid hoh value supplied: must be 'hunger' or 'happy'")
    elif pet[hoh] <= 0:
        pet[hoh] = 0
        return False
    else:
        pet[hoh] -= 1
        return True

#add a point of hunger or happiness (hoh)
#returns True if successful, False if not.
#-The only reason hunger/happiness are split in this one and not in minus_hoh
#-is because MAX_HUNGER/MAX_HAPPY may be different values, but 0 will always
#-be the lowest.
def add_hoh(pet, hoh):
    if (hoh != 'hunger') and (hoh != 'happy'):
        print("invalid hoh value supplied: must be 'hunger' or 'happy'")
    elif hoh == 'hunger':
        if pet[hoh] >= MAX_HUNGER:
            pet[hoh] = MAX_HUNGER
            return False
        else:
            pet[hoh] += 1
            return True
    elif hoh == 'happy':
        if pet[hoh] >= MAX_HAPPY:
            pet[hoh] = MAX_HAPPY
            return False
        else:
            pet[hoh] += 1
            return True

#every 1 minute, give everyone 10 stars.
def update_stars():
    threading.Timer(10.0,update_stars).start()

    for player_name in user_data['players']:
        user_data['players'][player_name]['inventory']['stars'] += 10
        save_data()

#every 1 hour(s), remove 1 hunger point from each mon.
#if the mon is hungry, remove a happy point.
def update_hunger():
    threading.Timer(3600.0, update_hunger).start()

    for player_name in user_data['players']:
        if has_mon(player_name):
            pet = user_data['players'][player_name]['mon']
            minus_hoh(pet, 'hunger')
            if pet['hunger'] <= 0:
                minus_hoh(pet, 'happy')
                minus_hoh(pet, 'happy')
            elif pet['hunger'] < 3:
                minus_hoh(pet, 'happy')
            save_data()

#every 3 hour(s), remove 1 happy point from each mon.
def update_happy():
    threading.Timer(10800.0, update_hunger).start()

    for player_name in user_data['players']:
        if has_mon(player_name):
            pet = user_data['players'][player_name]['mon']
            minus_hoh(pet, 'happy')
            save_data()

#start all update threads
def update_timer():
    #may need threading.Lock()
    update_stars()
    update_hunger()
    update_happy()

