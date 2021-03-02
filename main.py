from discord.ext import commands
import json
import os

dir_name = os.path.dirname(__file__)
config_file_name = 'config.json'
config_file = f'{dir_name}/{config_file_name}'
print(config_file)
config = json.load(open(config_file, 'r'))

prefix = config.get('COMMAND_PREFIX')
bot = commands.Bot(command_prefix=prefix)

BOT_TOKEN = config.get("BOT_TOKEN")


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

extensions = ['vps_commands']
for ext in extensions:
    bot.load_extension(f'extensions.{ext}')
bot.run(BOT_TOKEN)
