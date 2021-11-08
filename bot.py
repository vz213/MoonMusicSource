import discord
import youtube_dl
from discord.ext import commands
import json

with open('token.json') as tokeng:
    tokg = json.load(tokeng)
    tk = tokg[0]['token']

bot = commands.Bot(command_prefix='+')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.listening,name='MoonMusicSource'))
    print('MoonMusicSource')
    print('GitHub: github.com/vz213/MoonMusicSource.git')
    print('Commands: moonmusic.netlify.app/cmds')
    print(f'Tag: {bot.user}')
    print(f'Prefix: {bot.command_prefix}')
    print()
    print(f'invite: discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=3147776&scope=bot')

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send(':no_entry_sign: - You arent in the voice channel!')

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
        await ctx.send(f':thumbsup: - Joined to `{ctx.author.voice.channel.name}`')
    else:
        await ctx.send(':no_entry_sign: - Other user is using this bot!')

@bot.command()
async def j(ctx):
    if ctx.author.voice is None:
        await ctx.send(':no_entry_sign: - You arent in the voice channel!')

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
        await ctx.send(f':thumbsup: - Joined to `{ctx.author.voice.channel.name}`')
    else:
        await ctx.send(':no_entry_sign: - Other user is using this bot!')

@bot.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send(':thumbsup: - Disconnected!')

@bot.command()
async def d(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send(':thumbsup: - Disconnected!')

@bot.command()
async def play(ctx, url):
    if ctx.author.voice is None:
        await ctx.send(':no_entry_sign: - You arent in the voice channel!')
    
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
        await ctx.send(f':thumbsup: - Joined to `{ctx.author.voice.channel.name}`')
    
    FFMPEG_OPTIONS = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    YDL_OPTIONS = {'format': "bestaudio"}
    await ctx.send(f'**Searching** :link: `{url}`...')
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)
        await ctx.send(f'**Playing** :notes: `{url}` - Now!')


@bot.command()
async def p(ctx, url):
    if ctx.author.voice is None:
        await ctx.send(':no_entry_sign: - You arent in the voice channel!')
    
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
        await ctx.send(f':thumbsup: - Joined to `{ctx.author.voice.channel.name}`')
    
    FFMPEG_OPTIONS = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    YDL_OPTIONS = {'format': "bestaudio"}
    await ctx.send(f'**Searching** :link: `{url}`...')
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)
        await ctx.send(f'**Playing** :notes: `{url}` - Now!')

@bot.command()
async def pause(ctx):
    await ctx.send(':thumbsup: - Paused!')
    await ctx.voice_client.pause()

@bot.command()
async def resume(ctx):
    await ctx.send(':thumbsup: - Resumed!')
    await ctx.voice_client.resume()

bot.run(tk)
