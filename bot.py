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

#Extensions to load
extensions_dir = "extensions"
startup_extensions = ["admin", "pet", "inventory", "egg"]

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

#################

@bot.command(pass_context=True)
async def fuck(ctx):
    #In python, three double quotes turn what is within them into
    #'documentation.' The bot uses the documentation as a
    # description for the command. Pretty rad.
    """'Accidentaly' make an egg with someone.
    Mention another user to get started ( ͡° ͜ʖ ͡°)"""

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
    common.mother_exists(mother.name)
    
    if common.has_egg(mother.name):
        await bot.say('{0}, you already have an egg.'.format(mother.mention))
        await bot.say('You already {0} eggs.'.format(common.user_data[mother.name]['inventory']['egg']))
        return
    else: 
        common.user_data[mother.name]['inventory']['egg'] = 1
        common.user_data[mother.name]['egg']['type'] = egg_type
    
        await bot.say('{0} tripped and accidentally put their dick in {1}. Whoops! {0} got an egg!'.format(mother.name, dad.name))

##############

if __name__ == "__main__":

    #LOAD EXTENSIONS
    for extension in startup_extensions:
        try:
            extension = extensions_dir + "." + extension
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run('MjU1NjcxMjkwODc3MzEzMDI1.CyhCkQ.NVxJ5wk2xQAZtJ_xvp4mAvfsJus')
