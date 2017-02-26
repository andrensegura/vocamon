#!/home/andre/bin/python3

import discord
from discord.ext import commands
import common

class Store():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def store(self, ctx):
        """View, buy, and sell things at the store."""
        if ctx.invoked_subcommand is None:
            store = common.user_data['store']
            msg = "Welcome to the store!\n------------"
            for item in store:
                msg += "\n{0}: {1} in stock, {2}:star: each".format(item, store[item]['quantity'],store[item]['price'])
            await self.bot.say(msg)

    @store.command(name='add', pass_context=True)
    async def _add(self,ctx):
        """Add items to the store. Admin only."""
        user = ctx.message.author
        if str(user) in common.admins:
            data = ctx.message.content.split()
            if len(data) < 5:
                await self.bot.say("item quantity price")
                return
            item = data[2]
            quantity = int(data[3])
            price = int(data[4])
            store = common.user_data['store']

            if item not in store:
                store[item] = {"quantity": quantity, "price": price}
            else:
                store[item]['quantity'] = quantity
                store[item]['price'] = price

def setup(bot):
    bot.add_cog(Store(bot))
