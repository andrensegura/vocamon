import threading
import json

user_data_json_file = "vocamon.json"

#READ JSON FILE TO LOAD SAVED DATA, ELSE, START NEW
def load_data():
    try:
        with open(user_data_json_file) as json_file:
            user_data = json.load(json_file)
        print('Save data loaded.')
    except :
        print('Unable to read save data or none supplied.')
        user_data = {}
    return user_data

#save data to file
def save_data():
    with open(user_data_json_file, 'w') as outfile:
        json.dump(user_data, outfile)


##################### dont fucking touch this line.

user_data = load_data() 

####################


#every 3 mins, give everyone 10 stars.
def update_timer():
    threading.Timer(10.0,update_timer).start()

    for player_name in user_data:
        user_data[player_name]['inventory']['stars'] += 10
        save_data()

#takes a string as input and creates save data for it. 
#if the user existed, it returns True, else, false.
def mother_exists(player):
    if player not in user_data:
        user_data[player] = {}
        user_data[player]['egg'] = {'type': 0}
        user_data[player]['mon'] = {'name': 0, 'type': 0, 'hunger': 0, 'happy': 0}
        user_data[player]['inventory'] = {'food': 5, 'egg': 0, 'stars': 0}
        return False
    return True

#takes a player name as a string and checks if the user has an egg.
def has_egg(player):
    if mother_exists(player):
        if user_data[player]['inventory']['egg'] != 0:
            return True
    return False

#takes a player name as a string and checks if the user has a mon.
def has_mon(player):
    if mother_exists(player):
        if user_data[player]['mon']['type'] != 0:
            return True
    return False

#takes a player name as a string and checks if the user has any food.
def has_food(player):
    if mother_exists(player):
        if user_data[player]['inventory']['food'] != 0:
            return True
    return False

