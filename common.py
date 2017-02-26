import threading
import json

max_hunger = max_happy = 10
user_data_json_file = "vocamon.json"

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
    pet[hoh] -= 1
    if pet[hoh] < 0:
        pet[hoh] = 0

#every 1 minute, give everyone 10 stars.
def update_stars():
    threading.Timer(3600.0,update_stars).start()

    for player_name in user_data['players']:
        user_data['players'][player_name]['inventory']['stars'] += 10
        save_data()

#every 1 hour(s), remove 1 hunger point from each mon.
#if the mon is hungry, remove a happy point.
def update_hunger():
    threading.Timer(10.0, update_hunger).start()

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

