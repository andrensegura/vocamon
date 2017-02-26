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

    @store.command(name='adjust', pass_context=True)
    async def _add(self,ctx):
        """Add/change items in the store. Admin only."""
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

    @store.command(name='remove', pass_context=True)
    async def _remove(self, ctx):
        user = ctx.message.author
        store = common.user_data['store']
        if str(user) in common.admins:
            data = ctx.message.content.split()
            if len(data) < 3:
                await self.bot.say("item name needed")
                return
            item = data[2]
            try:
                del store[item]
            except Exception as e:
                await self.bot.say(str(e))


def setup(bot):
    bot.add_cog(Store(bot))
