from discord.ext import commands
import psutil
import os
import asyncio
import subprocess
import json


class VPSCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('config.json'))
        self.bot_location = self.config.get("BOT_LOCATION")
        self.python_interpreter = self.config.get(
            "PYTHON_INTERPRETER_LOCATION")

    @commands.command(name='check_bot_status')
    async def check_status(self, ctx):
        if await self.is_bot_running():
            await ctx.send('The bot is running ..')
            return
        await ctx.send('The bot is not running ..')

    async def is_bot_running(self):
        for p in psutil.process_iter():
            if p.name().lower() == 'python':
                command = p.cmdline()
                if self.bot_location in command:
                    return True
        return False

    @commands.command(name='start_bot')
    async def start_bot(self, ctx):
        if await self.is_bot_running():
            await ctx.send('The bot already running ..')
            return
        await ctx.send('Please wait while starting the bot...')
        cmd = f'nohup {self.python_interpreter} {self.bot_location} &'
        subprocess.Popen(cmd, shell=True)
        await asyncio.sleep(5)
        if await self.is_bot_running():
            await ctx.send('Bot started successfully!')
            return
        await ctx.send('Could not start the bot for some reason ..\
\nPlease try to start the bot from the server manually...')

    @commands.command(name='stop_bot')
    async def stop_bot(self, ctx):
        if not await self.is_bot_running():
            await ctx.send('The bot is not running!')
            return
        for p in psutil.process_iter():
            if p.name().lower() == 'python':
                command = p.cmdline()
                if self.bot_location in command:
                    p.kill()
                    await asyncio.sleep(3)
                    await ctx.send('Bot shut down complete!')
                    return


def setup(bot):
    bot.add_cog(VPSCommands(bot))
    print('VPSCommands extension has been loaded!')
