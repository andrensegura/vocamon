import discord
from discord.ext import commands
import common


class Egg():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def egg(self, ctx):
        """Perform various actions with/to your egg.
            Mention someone to throw your egg at them."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("see '.help egg'")
            
    @egg.command(name='throw', pass_context=True)
    async def throw(self, ctx):
        """Throw an egg at someone."""
        try:
            victim = ctx.message.mentions[0]
            perp = ctx.message.author
            if common.has_egg(str(perp)):
                common.user_data['players'][str(perp)]['inventory']['egg'] = 0
                await self.bot.say('{0} threw their egg at {1}! Talk about hazukashi. LOL'.format(str(perp), victim.mention))
                await self.bot.send_file(ctx.message.channel, 'res/smug.png')
                return
            await self.bot.say("Ghost eggs don't work. Go fuck somebody.")
        except:
            await self.bot.say("see '.help egg'")

    @egg.command(name='eat', pass_context=True)
    async def _eat(self, ctx):
        """Eat your egg, you monster."""
        mother = ctx.message.author
        if common.has_egg(str(mother)):
            common.user_data['players'][str(mother)]['inventory']['egg'] = 0
            await self.bot.say("{0}, you've eaten your egg :(".format(mother.mention))
        else:
            await self.bot.say('{0}, you have no eggs. Go fuck somebody.'.format(mother.mention))
        
    @egg.command(name='hatch', pass_context=True)
    async def _hatch(self, ctx):
        """Hatches an egg if you have one.
        Does not work if you already have an active pet."""
    
        mother = ctx.message.author
        mother_data = common.user_data['players'][str(mother)]
        if common.has_egg(str(mother)):
            if not common.has_mon(str(mother)):
                pet = mother_data['mon']
                pet['hunger'] = 2
                pet['happy'] = 5
                pet['type'] = pet['name'] = mother_data['egg']['type']
                mother_data['inventory']['egg'] = 0
                await self.bot.say('Congratulations! Your egg hatched into a beautiful baby {0}!'.format(mother_data['mon']['type']))
            else:
                await self.bot.say('{0}, you already have a pet.'.format(mother.mention))
        else:
            await self.bot.say('{0}, you have no eggs. Go fuck somebody.'.format(mother.mention))


def setup(bot):
    bot.add_cog(Egg(bot))
