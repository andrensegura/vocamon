import discord
from discord.ext import commands
import common
import picgen


class Pet():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def pet(self,ctx):
        """Interact with your pet."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("See '.help pet'")

    @pet.command(name='name', pass_context=True)
    async def _name(self, ctx, new_name: str):
        """Rename your pet.
        Can only be a single word... for now."""
        mother = ctx.message.author
        if common.has_mon(str(mother)):
            common.user_data['players'][str(mother)]['mon']['name'] = new_name
            await self.bot.say("Congratulations, {0}, your mon has been named {1}!".format(mother.mention, new_name))
        else:
            await self.bot.say("{0}, you have no mon. You need to hatch an egg first.".format(mother.mention))
    
    @pet.command(name='stats', pass_context=True)
    async def _stats(self, ctx):
        """Check your pets stats."""
        mother = ctx.message.author
        if common.has_mon(str(mother)):
            pet = common.user_data['players'][str(mother)]['mon']
            await self.bot.say("```Name:   {0}\nType:   {1}\nHunger: {2}\nHappy:  {3}```".format(pet['name'], pet['type'], pet['hunger'], pet['happy']))
        else:
            await self.bot.say("{0}, you don't have a pet. Hatch an egg!".format(mother.mention))
    
    @pet.command(name='stats2', pass_context=True)
    async def _stats2(self, ctx):
        """Check your pets stats."""
        mother = ctx.message.author
        if common.has_mon(str(mother)):
            pet = common.user_data['players'][str(mother)]['mon']
            picname = picgen.generate_mon_badge(str(mother), pet)
            await self.bot.send_file(ctx.message.channel, picname)
        else:
            await self.bot.say("{0}, you don't have a pet. Hatch an egg!".format(mother.mention))
    
    @pet.command(name='feed', pass_context=True)
    async def _feed(self, ctx):
        """Feed your pet if you have food."""
        mother = ctx.message.author
        if common.has_mon(str(mother)):
            mother_data = common.user_data['players'][str(mother)]
            pet = mother_data['mon']
            if common.has_food(str(mother)):
                if pet['hunger'] < common.max_hunger:
                    mother_data['inventory']['food'] -= 1
                    pet['hunger'] += 1
                    await self.bot.say("{0} has been fed!".format(pet['name']))
                else:
                    await self.bot.say("{0} isn't hungry!".format(pet['name']))
            else:
                await self.bot.say("{0}, you don't have any food!".format(mother.mention))
        else:
            await self.bot.say("{0}, you don't have a pet. Hatch an egg!".format(mother.mention))

    @pet.command(name='kill', pass_context=True)
    async def _kill(self, ctx):
        """Brutally slaughter your pet."""
        mother = ctx.message.author
        if common.has_mon(str(mother)):
            pet = common.user_data['players'][str(mother)]['mon']
            name = pet['name']
            pet['name'] = pet['type'] = pet['hunger'] = pet['happy'] = 0
            await self.bot.say("Your {0} is dead. I hope you're happy :(".format(name))

def setup(bot):
    bot.add_cog(Pet(bot))
