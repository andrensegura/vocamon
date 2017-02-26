#!/home/andre/bin/python3

import os, sys
import discord
from discord.ext import commands
import common

#Note:
# We can import common even though it is a directory above us
# because it exists where the original process is started.
#
# In addition, if you use "from x import y", you get the variable
# in it's state in x, not whatever the current value in memory is.
#

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
        if str(user) in common.admins:
            print("Restart command received. Restarting...")
            await self.bot.say("Bot restarting...")
            common.save_data()

            import sys
            python = sys.executable
            sys.stdout.flush()
            os.execl("bot.py", python)
        else:
            await self.bot.say("{0} is not an administrator".format(user))

    @admin.command(name='loadavg', pass_context=True)
    async def _loadavg(self,ctx):
        """Check the server load."""
        user = ctx.message.author
        if str(user) in common.admins:
            await self.bot.say("`{0}`".format(os.getloadavg()))

    @admin.command(name='shutdown', pass_context=True)
    async def _shutdown(self,ctx):
        """Shut down the bot."""
        user = ctx.message.author
        if str(user) in common.admins:
            common.save_data()
            await self.bot.say("Goodbye!\nVocamon has shut down.")
            import sys
            sys.exit(0)

def setup(bot):
    bot.add_cog(Admin(bot))
