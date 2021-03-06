#!/home/andre/bin/python3

import discord
from discord.ext import commands
import random
import common



###############
# READY UP
###############        
        
###############
# "common" module contains the var "user_data", which contains all the
# valuable user data and is accessible to all modules
###############


all_egg_types = ['gumi','ia','luka','miku']

description = '''Vocamon is a game you can play from within the Discord client.
It provides users a virtual pet and allows for some interaction like battling/trading with other users.'''
bot = commands.Bot(command_prefix='.', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    common.update_timer()
    await bot.send_message(bot.get_channel("264475422001987584"),
        "Vocamon started up.")
    print('------')

################
# COMMANDS
################

#This file contains the commands that the player itself can make.
#Current commands include:
# - fuck
#

#
# fuck another member on the server and receive an egg.
#
@bot.command(pass_context=True)
async def fuck(ctx):
    #In python, three double quotes turn what is within them into
    #'documentation.' The bot uses the documentation as a
    # description for the command. Pretty rad.
    """'Accidentaly' make an egg with someone.
    Mention another user to get started ( ͡° ͜ʖ ͡°)"""

    if ctx.message.channel.is_private:
        await bot.say("This does not work in private channels!")

    try:
        dad = ctx.message.mentions[0]
    except:
        await bot.say("Whom did you want to fuck? (see '.help fuck')")
        return
        
    mother = ctx.message.author

    #determine egg type
    parent_roles = []
    for role in (mother.roles + dad.roles):
        parent_roles.append(str(role).lower())
    possible_types = set(parent_roles) & set(all_egg_types)
    while len(possible_types) < 2:
        possible_types.add(random.sample(all_egg_types,1)[0])
    egg_type = (random.sample(possible_types,1))[0]
    
    #mother_exists only being called to create the mother entry in this case.
    common.mother_exists(str(mother))
    player = common.user_data['players'][str(mother)]

    if common.has_egg(str(mother)):
        await bot.say('{0}, you already have an egg.'.format(mother.mention))
        return
    else: 
        player['inventory']['egg'] = 1
        player['egg']['type'] = egg_type
    
        await bot.say('{0} tripped and accidentally put their dick in {1}. Whoops! {0} got an egg!'.format(mother.mention, dad.mention))

#
# hit another user's mon and lower it's happiness.
#
@bot.command(pass_context=True)
async def hit(ctx):
    """Hit another player's mon. This makes the mon sad :("""
    if ctx.message.channel.is_private:
        await bot.say("This does not work in private channels!")

    try:
        victim = ctx.message.mentions[0]
    except:
        await bot.say("You need to mention another player!")
        return

    player = ctx.message.author

    if not common.has_mon(str(victim)):
        await bot.say("{0}, {1} has no mon to hit.".format(player.mention, victim.mention))
        return

    pet = common.user_data['players'][str(victim)]['mon']

    if common.minus_hoh(pet, 'happy'):
        await bot.say("{0} viciously stikes {1}'s {2}! How mean!".format(player.mention, victim.mention, pet['name']))
    else:
        await bot.say("{0} looks back at {1} after being struck. The idea that it could be in any more pain amuses it, but it does not laugh.".format(pet['name'], player.mention))


##############

if __name__ == "__main__":

    #LOAD EXTENSIONS
    for extension in common.startup_extensions:
        try:
            extension = common.extensions_dir + "." + extension
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run('MjU1NjcxMjkwODc3MzEzMDI1.CyhCkQ.NVxJ5wk2xQAZtJ_xvp4mAvfsJus')
