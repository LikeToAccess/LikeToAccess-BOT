from discord.ext import commands, tasks
from functions import get_players, read_file
import discord


bot = commands.Bot(command_prefix=['n!', 'nl!', 'neldog!', 'nelson!'], help_command=None, case_insensitive=True)


@bot.event
async def on_ready():
	print(f"{bot.user} status pending!")
	players = get_players()
	if players[:1] == "0":
		await bot.change_presence(status=discord.Status.idle, activity=discord.Game("0/10"))
	else:
		await bot.change_presence(status=discord.Status.online, activity=discord.Game(players))
	quit()

token = read_file("token.txt")[0]
bot.run(token)
