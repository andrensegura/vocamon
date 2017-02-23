#!/home/andre/bin/python3

import os, sys
import discord
from discord.ext import commands

#ADMIN COMMANDS
class Admin():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def admin(self, ctx):
        """Perform administrative actions."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("See '.help admin'")

    @admin.command(name='restart', pass_context=True)
    async def _restart(self,ctx):
        """Restart the bot."""
        user = ctx.message.author
        if str(user) == "faroeson#2506":
            await self.bot.say("Bot restarting...")
            #save_data()

            import sys
            python = sys.executable
            os.fsync()
            os.execl("bot.py", python)
        else:
            await self.bot.say("{0} is not an administrator".format(user))

    @admin.command(name='loadavg', pass_context=True)
    async def _loadavg(self,ctx):
        """Check the server load."""
        user = ctx.message.author
        if str(user) == "faroeson#2506":
            await self.bot.say("`{0}`".format(os.getloadavg()))

    @admin.command(name='shutdown', pass_context=True)
    async def _shutdown(self,ctx):
        """Shut down the bot."""
        user = ctx.message.author
        if str(user) == "faroeson#2506":
            #save_data()
            await self.bot.say("Goodbye!\nVocamon has shut down.")
            from sys import exit
            sys.exit(0)

def setup(bot):
    bot.add_cog(Admin(bot))
