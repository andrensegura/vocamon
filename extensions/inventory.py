#!/home/andre/bin/python3

import discord
from discord.ext import commands
import common

class Inventory():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def inventory(self, ctx):
        """View/manipulate your inventory."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("See '.help inventory'")

    @inventory.command(name="show", pass_context=True)
    async def _show(self, ctx):
        """Show items in inventory."""
        user = ctx.message.author
        inv = common.user_data[user.name]['inventory']

        inv_message = "__**Inventory:**__"
        #the following code can be used to simply iterate through and print
        #everything out. but i want emotes.
        #for item, amount in inv.items():
        #    inv_message += "\n" + item + ": " + str(amount)
        inv_message += "\n:poultry_leg: " + str(inv['food'])
        inv_message += "\n:egg: " + str(inv['egg'])
        inv_message += "\n:star: " + str(inv['stars'])

        await self.bot.say(inv_message)


def setup(bot):
    bot.add_cog(Inventory(bot))
