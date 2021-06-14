# -*- coding: utf-8 -*-
# filename		  : main.py
# description	   : Discord interface for NelsonMC
# author			: LikeToAccess
# email			 : liketoaccess@protonmail.com
# date			  : 01-06-2021
# version		   : v1.0
# usage			 : python main.py
# notes			 : 
# license		   : MIT
# py version		: 3.7.9 (must run on 3.6 or higher)
#==============================================================================
from discord.ext import commands, tasks
from time import sleep
from functions import filter_file, read_file, append_file, log, kill_token, get_players, run
import discord
import os
import random
import youtube_dl

version = os.system("python -V")
# if version[:2] != "3.":
# 	print("Please run on python version 3.7.9 for the pest experience!")
# print(version[:2])
bot = commands.Bot(command_prefix=['n!', 'nl!', 'neldog!', 'nelson!', "please "], help_command=None, case_insensitive=True)
client = discord.Client()
allowed_users = filter_file(None, "allowed_users.txt")
kill_token = kill_token()
print(kill_token)
timings = {1:5, 2:7, 3:3, 4:3}
# print(allowed_users)

#==============================================================================

@bot.event
async def on_ready():
	# status.start()
	print(f"{bot.user} successfuly connected!")

@tasks.loop(seconds=20)
async def status():
	players = get_players()
	try:
		if int(players[:1]) == 0:
			await bot.change_presence(status=discord.Status.idle, activity=discord.Game("0/10"))
		else:
			await bot.change_presence(status=discord.Status.online, activity=discord.Game(players))
	except ValueError as e:
		await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Server Offline"))

@bot.command(name="kill")
async def kill(ctx, arg):
	if check_perms(ctx):
		if arg == kill_token:
			print("Killing the bot!")
			await ctx.message.delete()
			await ctx.send("Killing the bot!")
			quit()
		else:
			await ctx.send("Wrong token!\nThis event will be logged.")
			log(ctx)
			await ctx.message.delete()
	else:
		await ctx.message.delete()
		await ctx.send(f"User \"{ctx.author}\" is not in the allowed users list!\nThis event will be logged.")

@bot.command(name="list")
async def list(ctx):
	await ctx.message.delete()
	await ctx.send(run("/list"))

@bot.command(pass_context = True, aliases=["disconnect"])
async def leave(ctx, name="leave"):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	await voice.disconnect()
	await ctx.message.delete()
	print("SUCCESS: left VC.")

@bot.command(name="join")
async def join(ctx, user: discord.Member):
	channel = ctx.author.voice.channel
	voice_channel = await channel.connect()
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

@bot.command(name="kick", aliases=["silence"])
async def kick(ctx, user: discord.Member):
	await ctx.message.delete()
	if check_perms(ctx):
		log(ctx)
		sound_number = random.randint(1,4)
		song = f"sound ({sound_number}).mp3"
		channel = ctx.author.voice.channel
		voice_channel = await channel.connect()
		voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
		voice.play(discord.FFmpegPCMAudio(song))
		sleep(timings[sound_number])
		print(sound_number)
		await user.move_to(bot.get_channel(464479155350929428))
		await voice.disconnect()
	else:
		await ctx.send(f"User \"{ctx.author}\" is not in the allowed users list!\nThis event will be logged.")

@bot.command(name="op")
async def op(ctx, user: discord.Member):
	await ctx.message.delete()
	if check_perms(ctx):
		msg = f"\n#{user.name}\n{user.id}\n"
		append_file("allowed_users.txt", msg)
	else:
		await ctx.send(f"User \"{ctx.author}\" is not in the allowed users list!\nThis event will be logged.")
	log(ctx)

@bot.command(name="name", pass_context=True)
async def name(ctx, arg, member: discord.Member, nick):
	await ctx.message.delete()
	if check_perms(ctx):
		log(ctx)
		await member.edit(nick=nick)
	else:
		await ctx.send(f"User \"{ctx.author}\" is not in the allowed users list!\nThis event will be logged.")

@bot.command(name="test")
async def test(ctx):
	log(ctx)
	await ctx.message.delete()
	print("I'm working!")
	await ctx.send("I'm working!")

@bot.command(name="ban")
async def ban(ctx, arg):
	if check_perms(ctx):
		log(ctx)
		msg = run(f"/ban {arg}")
		await ctx.send(msg)
	else:
		await ctx.send(f"User \"{ctx.author}\" is not in the allowed users list!\nThis event will be logged.")
	await ctx.message.delete()

@bot.command(name="unban")
async def unban(ctx, arg):
	if check_perms(ctx):
		log(ctx)
		msg = run(f"/pardon {arg}")
		await ctx.send(msg)
	else:
		await ctx.send(f"User \"{ctx.author}\" is not in the allowed users list!\nThis event will be logged.")
	await ctx.message.delete()

@bot.command(name="say")
async def say(ctx, arg):
	await ctx.message.delete()
	run(f"/say {arg}")
	await ctx.send(f"Sent message: {arg}")

# Credit to Crazy#9999
@bot.command(name="carson")
async def test(ctx):
	await ctx.message.delete()
	print("I'm gunna fuck a child!")
	await ctx.send("I'm gunna fuck a child!")

@bot.command(name="stop", pass_context=True)
async def stop(ctx):
	if check_perms(ctx):
		print("Stopping the server!")
		run("/stop")
	else:
		await ctx.message.delete()
		await ctx.send(f"User \"{ctx.author}\" is not in the allowed users list!\nThis event will be logged.")

@bot.command(name="play", pass_context=True)
async def play(ctx, url):
	song = os.path.isfile("song.mp3")
	try:
		if song:
			os.remove("song.mp3")
	except PermissionError:
		await ctx.send("oops")
		return
	# voice_channel = discord.utils.get(ctx.guild.voice_channels, name="▶voice-chat")
	voice_channel = ctx.author.voice.channel
	await voice_channel.connect()
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	ydl_opts = {
		"format": "bestaudio/best",
		"postprocessors": [{
			"key": "FFmpegExtractAudio",
			"preferredcodec": "mp3",
			"preferredquality": "96",
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			os.rename(file, "song.mp3")
	voice.play(discord.FFmpegPCMAudio("song.mp3"))
	await ctx.message.delete()
	print("SUCCESS: played audio.")

@bot.command()
async def pause(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	voice.pause()
	await ctx.message.delete()
	print("SUCCESS: paused audio.")

@bot.command()
async def resume(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	voice.resume()
	await ctx.message.delete()
	print("SUCCESS: unpaused audio.")

#==============================================================================

def check_perms(ctx):
	author = ctx.message.author
	if str(author.id) in allowed_users:
		return True
	else:
		log(ctx)
		return False

#==============================================================================

token = read_file("token.txt")[0]
bot.run(token)
