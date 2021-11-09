import json
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import youtube_dl

guilds_ids = [
    # enter yere guild ids
]

with open('token.json') as jj:
    data = json.load(jj)
    tk = data[0]['token']

bot = commands.Bot(command_prefix='>')
slash = SlashCommand(client=bot, sync_commands=True)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name='/play'))
    print('ready')


@slash.slash(
    name='join',
    description='Joins To Your Channel',
    guild_ids=guilds_ids
)
async def _join(ctx: SlashContext):
    if ctx.author.voice is None:
        await ctx.send(':no_entry_sign: - You arent in the voice channel!')

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
        await ctx.send(f':thumbsup: - Joined to `{ctx.author.voice.channel.name}`')
    else:
        await ctx.send(':no_entry_sign: - Other user is using this bot!')


@slash.slash(
    name='disconnect',
    description='Disconnects Of Your Channel',
    guild_ids=guilds_ids
)
async def _disconnect(ctx: SlashContext):
    await ctx.voice_client.disconnect()
    await ctx.send(':thumbsup: - Disconnected!')


@slash.slash(
    name='play',
    description='Plays Music',
    guild_ids=guilds_ids,
    options=[
        create_option(
            name='url',
            description='Youtube URL',
            option_type=str,
            required=True
        )
    ]
)
async def _play(ctx: SlashContext, url: str):
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


@slash.slash(
    name='pause',
    description='Pauses Music',
    guild_ids=guilds_ids
)
async def _pause(ctx: SlashContext):
    await ctx.voice_client.pause()
    await ctx.send(':thumbsup: - Paused!')


@slash.slash(
    name='resume',
    description='Resumes Music',
    guild_ids=guilds_ids
)
async def _pause(ctx: SlashContext):
    await ctx.voice_client.resume()
    await ctx.send(':thumbsup: - Paused!')
    

bot.run(tk)
