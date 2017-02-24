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
startup_extensions = ["admin", "pet", "inventory"]

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
            if common.has_egg(perp.name):
                common.user_data[perp.name]['inventory']['egg'] = 0
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
    if common.has_egg(mother.name):
        common.user_data[mother.name]['inventory']['egg'] = 0
        await bot.say("{0}, you've eaten your egg :(".format(mother.mention))
    else:
        await bot.say('{0}, you have no eggs. Go fuck somebody.'.format(mother.mention))
    
@egg.command(name='hatch', pass_context=True)
async def _hatch(ctx):
    """Hatches an egg if you have one.
    Does not work if you already have an active pet."""

    mother = ctx.message.author
    if common.has_egg(mother.name):
        if not common.has_mon(mother.name):
            pet = common.user_data[mother.name]['mon']
            pet['hunger'] = 2
            pet['happy'] = 5
            pet['type'] = pet['name'] = common.user_data[mother.name]['egg']['type']
            common.user_data[mother.name]['inventory']['egg'] = 0
            await bot.say('Congratulations! Your egg hatched into a beautiful baby {0}!'.format(common.user_data[mother.name]['mon']['type']))
        else:
            await bot.say('{0}, you already have a pet.'.format(mother.mention))
    else:
        await bot.say('{0}, you have no eggs. Go fuck somebody.'.format(mother.mention))

#commands to add: love, attack


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
