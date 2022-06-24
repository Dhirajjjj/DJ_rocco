import os
import random
import asyncio
from functools import partial
import itertools
import sys
import traceback
from async_timeout import timeout

import discord
import youtube_dl
from youtube_dl import YoutubeDL

from dotenv import load_dotenv
from discord.ext import commands

from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

from discord import FFmpegPCMAudio
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #Enter your Discord token ID
GUILD = os.getenv('DISCORD_GUILD') #Enter your Discord server name

song_queue = []

#client = discord.Client()
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print("rocco online")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    rocco_reply = os.getenv('ROCCO_REPLIES') # set custom replies to direct messages

    if message.content == 'hi rocco':
        response = random.choice(rocco_reply) 
        await message.channel.send(response)

    if "fuck off" in message.content:
        await message.channel.send("the only thing getting fucked tonight is you <a:smirk:930742257081012234>")

    await bot.process_commands(message)

@bot.command(name='speak', help='you get a dog')
async def bot_speak(ctx):
    print('understands')
    await ctx.send("woof")

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.command(name='join')
async def join_voice(ctx,  url='https://www.youtube.com/watch?v=Z8JnZm56MQU'):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@bot.command(name = 'leave')
async def leave_voice(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else: 
        await ctx.send("I'm not in a voice channel")

@bot.command(name = 'gaana')
async def play(self, ctx, *, url):

    try:

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

            if len(self.queue) == 0:

                self.start_playing(ctx.voice_client, player)
                #await ctx.send(f':mag_right: **Searching for** ``' + url + '``\n<:youtube:763374159567781890> **Now Playing:** ``{}'.format(player.title) + "``")

            else:
                
                self.queue[len(self.queue)] = player
                #await ctx.send(f':mag_right: **Searching for** ``' + url + '``\n<:youtube:763374159567781890> **Added to queue:** ``{}'.format(player.title) + "``")

    except:

        await ctx.send("Somenthing went wrong - please try again later!")

def start_playing(self, voice_client, player):

    self.queue[0] = player

    i = 0
    while i <  len(self.queue):
        try:
            voice_client.play(self.queue[i], after=lambda e: print('Player error: %s' % e) if e else None)

        except:
            pass
        i += 1

@bot.command(name = 'p')
async def regather_stream(ctx, video_link):
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_link, download=False)
            URL = info['formats'][0]['url']
        voice = get(bot.voice_clients, guild=ctx.guild)

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command(name = 'pause')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client                
    voice_channel.pause()

@bot.command(name = 'play')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.resume()

bot.run(TOKEN)



"""

    # youtube_dl.utils.bug_reports_message = lambda: ''

    # ytdlopts = {
    #     'format': 'bestaudio/best',
    #     'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    #     'restrictfilenames': True,
    #     'noplaylist': True,
    #     'nocheckcertificate': True,
    #     'ignoreerrors': False,
    #     'logtostderr': False,
    #     'quiet': True,
    #     'no_warnings': True,
    #     'default_search': 'auto',
    #     'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
    # }

    # ffmpegopts = {
    #     'before_options': '-nostdin',
    #     'options': '-vn'
    # }

    # ytdl = YoutubeDL(ytdlopts)

        # player = ctx.guild.voice_client
        # options = {
        #     "postprocessors":[{
        #         "key": "FFmpegExtractAudio", # download audio only
        #         "preferredcodec": "mp3", # other acceptable types "wav" etc.
        #         "preferredquality": "192" # 192kbps audio
        #     }],
        #     "format": "bestaudio/best",
        #     "outtmpl": "yt_song.mp3" # downloaded file name
        # }

        # with youtube_dl.YoutubeDL(options) as dl:
        #     dl.download([url])
        # player.play(discord.FFmpegPCMAudio("yt_song.mp3"))
        # playing = player.is_playing()
        # while playing: # not compulsory
        #     await asyncio.sleep(1)
        #     playing = player.is_playing()
        # os.remove("yt_song.mp3") # delete the file after use

    # source = FFmpegPCMAudio('https://www.youtube.com/watch?v=srxa-cWPJTo')
    # player = voice.play(source)

"""