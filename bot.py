#!/home/andre/bin/python3

import discord
from discord.ext import commands
import os
import json
import picgen
import threading

#READ JSON FILE TO LOAD SAVED DATA, ELSE, START NEW
user_data_json_file = "vocamon.json"
try:
    with open(user_data_json_file) as json_file:
        user_data = json.load(json_file)
    print('Save data loaded.')
except :
    print('Unable to read save data or none supplied.')
    user_data = {}



###############
# READY UP
###############        
        
description = '''Vocamon is a game you can play from within the Discord client.
It provides users a virtual pet and allows for some interaction like battling/trading with other users.'''
bot = commands.Bot(command_prefix='.', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    update_timer()
    print('------')

################
# FUNCTIONS
################
#LOG DATA
def save_data():
    with open(user_data_json_file, 'w') as outfile:
        json.dump(user_data, outfile)
        

def update_timer():
    threading.Timer(180.0,update_timer).start()

    for player_name in user_data:
        user_data[player_name]['inventory']['stars'] += 10
        save_data()

#RESTART BOT
def restart_bot():
    import sys
    python = sys.executable
    os.execl("bot.py", python)

#takes a string as input and creates save data for it. if the user existed, it returns True, else, false.
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
    
################
# COMMANDS
################

#ADMIN COMMANDS
@bot.group(pass_context=True)
async def admin(ctx):
    """Perform administrative actions."""
    if ctx.invoked_subcommand is None:
        await bot.say("See '.help admin'")

@admin.command(name='restart', pass_context=True)
async def _restart(ctx):
    """Restart the bot."""
    user = ctx.message.author
    if str(user) == "faroeson#2506":
        await bot.say("Bot restarting...")
        save_data()
        os.fsync()
        restart_bot()
    else:
        await bot.say("{0} is not an administrator".format(user))

@admin.command(name='loadavg', pass_context=True)
async def _loadavg(ctx):
    """Check the server load."""
    user = ctx.message.author
    if str(user) == "faroeson#2506":
        await bot.say("`{0}`".format(os.getloadavg()))

@admin.command(name='shutdown', pass_context=True)
async def _shutdown(ctx):
    """Shut down the bot."""
    user = ctx.message.author
    if str(user) == "faroeson#2506":
        await bot.say("Goodbye!\nVocamon has shut down.")
        from sys import exit
        exit(0)

#################

@bot.command(pass_context=True)
async def fuck(ctx):
    #In python, three double quotes turn what is within them into 'documentation.' The bot uses
    #the documentation as a description for the command. Pretty rad.
    """'Accidentaly' make an egg with someone.
    Mention another user to get started ( ͡° ͜ʖ ͡°)"""

    try:
        dad = ctx.message.mentions[0].name
    except:
        await bot.say("Whom did you want to fuck? (see '.help fuck')")
        return
        
    mother = ctx.message.author
    egg_type = dad + "mon" #make this a weighted choice, later
    
    #mother_exists only being called to create the mother entry in this case.
    mother_exists(mother.name)
    
    if has_egg(mother.name):
        await bot.say('{0}, you already have an egg.'.format(mother.mention))
        await bot.say('You already {0} eggs.'.format(user_data[mother.name]['inventory']['egg']))
        return
    else: 
        user_data[mother.name]['inventory']['egg'] = 1
        user_data[mother.name]['egg']['type'] = egg_type
    
        await bot.say('{0} tripped and accidentally put their dick in {1}. Whoops! {0} got an egg!'.format(mother.name, dad))

###########
# EGG specific commands
###########

@bot.group(pass_context=True)
async def egg(ctx):
    """Perform various actions with/to your egg.
        Mention someone to throw your egg at them."""
    if ctx.invoked_subcommand is None:
        #throw an egg if someone is mentioned
        try:
            victim = ctx.message.mentions[0]
            perp = ctx.message.author
            if has_egg(perp.name):
                user_data[perp.name]['inventory']['egg'] = 0
                await bot.say('{0} threw their egg at {1}! Talk about hazukashi. LOL'.format(perp.mention, victim.mention))
                await bot.send_file(ctx.message.channel, 'smug.png')
                return
            await bot.say("Ghost eggs don't work. Go fuck somebody.")
        except:
            await bot.say("I couldn't understand your command. (see '.help egg')")
        
@egg.command(name='eat', pass_context=True)
async def _eat(ctx):
    """Eat your egg, you monster."""
    mother = ctx.message.author
    if has_egg(mother.name):
        user_data[mother.name]['inventory']['egg'] = 0
        await bot.say("{0}, you've eaten your egg :(".format(mother.mention))
    else:
        await bot.say('{0}, you have no eggs. Go fuck somebody.'.format(mother.mention))
    
@egg.command(name='hatch', pass_context=True)
async def _hatch(ctx):
    """Hatches an egg if you have one.
    Does not work if you already have an active pet."""

    mother = ctx.message.author
    if has_egg(mother.name):
        if not has_mon(mother.name):
            pet = user_data[mother.name]['mon']
            pet['type'], pet['name'] = user_data[mother.name]['egg']['type']
            user_data[mother.name]['inventory']['egg'] = 0
            await bot.say('Congratulations! Your egg hatched into a beautiful baby {0}!'.format(user_data[mother.name]['mon']['type']))
        else:
            await bot.say('{0}, you already have a pet.'.format(mother.mention))
    else:
        await bot.say('{0}, you have no eggs. Go fuck somebody.'.format(mother.mention))

####
#### Pet specific commands and sub commands
####
@bot.group(pass_context=True)
async def pet(ctx):
    """Interact with your pet."""
    if ctx.invoked_subcommand is None:
        await bot.say("See '.help pet'")
    
@pet.command(name='name', pass_context=True)
async def _name(ctx, new_name: str):
    """Rename your pet.
    Can only be a single word... for now."""
    mother = ctx.message.author
    if has_mon(mother.name):
        user_data[mother.name]['mon']['name'] = new_name
        await bot.say("Congratulations, {0}, your mon has been named {1}!".format(mother.mention, new_name))
    else:
        await bot.say("{0}, you have no mon. You need to hatch an egg first.".format(mother.name))
        
@pet.command(name='stats', pass_context=True)
async def _stats(ctx):
    """Check your pets stats."""
    mother = ctx.message.author
    if has_mon(mother.name):
        pet = user_data[mother.name]['mon']
        await bot.say("```Name:   {0}\nType:   {1}\nHunger: {2}\nHappy:  {3}```".format(pet['name'], pet['type'], pet['hunger'], pet['happy']))
    else:
        await bot.say("{0}, you don't have a pet. Hatch an egg!".format(mother.mention))
    
@pet.command(name='stats2', pass_context=True)
async def _stats2(ctx):
    """Check your pets stats."""
    mother = ctx.message.author
    if has_mon(mother.name):
        pet = user_data[mother.name]['mon']
        #picgen should be updated to create unique filenames and return the name
        picgen.generate_mon_badge(pet)
        await bot.send_file(ctx.message.channel, 'out.png')
    else:
        await bot.say("{0}, you don't have a pet. Hatch an egg!".format(mother.mention))

@pet.command(name='feed', pass_context=True)
async def _feed(ctx):
    """Feed your pet if you have food."""
    mother = ctx.message.author
    if has_mon(mother.name):
        if has_food(mother.name):
            user_data[mother.name]['inventory']['food'] -= 1
            pet = user_data[mother.name]['mon']
            pet['hunger'] += 1
            await bot.say("{0} has been fed!".format(pet['name']))
        else:
            await bot.say("{0}, you don't have any food!".format(mother.mention))
    else:
        await bot.say("{0}, you don't have a pet. Hatch an egg!".format(mother.mention))

#commands to add: feed, love, attack


bot.run('MjU1NjcxMjkwODc3MzEzMDI1.CyhCkQ.NVxJ5wk2xQAZtJ_xvp4mAvfsJus')
