import os
import discord
import yt_dlp
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import ffmpeg

# โหลด environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True  # เพิ่ม intent นี้สำหรับการรับข้อความ

bot = commands.Bot(command_prefix='!', intents=intents)

# //////////////////// Bot Event /////////////////////////
@bot.event
async def on_ready():
    print(f"Bot Online! Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()  # Syncing slash commands
        print(f"{len(synced)} command(s) synced")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# แจ้งคนเข้า - ออกจากเซิร์ฟเวอร์
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1140633489520205934)  # ตรวจสอบว่า ID นี้ถูกต้อง
    if channel:
        text = f"Welcome to the server, {member.mention}!"
        embed = discord.Embed(title="Welcome to the server!",
                              description=text,
                              color=0x66FFFF)
        await channel.send(embed=embed)
        await member.send(text)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1140633489520205934)
    if channel:
        text = f"{member.name} has left the server!"
        await channel.send(text)

# คำสั่ง chatbot
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    mes = message.content.lower()
    if mes == 'hello':
        await message.channel.send("Hello It's me")
    elif mes == 'hi bot':
        await message.channel.send(f"Hello, {message.author.name}")

    await bot.process_commands(message)  # This is important for processing commands

# ///////////////////// Commands /////////////////////
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")

@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)

# ///////////////////// Music Command /////////////////////

# ฟังก์ชันสำหรับเชื่อมต่อกับช่องเสียง
async def connect_to_voice_channel(ctx):
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    return voice_client

# ฟังก์ชันดาวน์โหลดเพลงจาก URL
def download_song(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,  # Extract audio only
        'audioquality': 1,  # Best quality
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Save with video id as filename
        'restrictfilenames': True,
        'noplaylist': True,  # Disable playlist downloads
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# ฟังก์ชันสำหรับเล่นเพลง
@bot.command()
async def play(ctx, url: str):
    voice_client = await connect_to_voice_channel(ctx)
    song_path = download_song(url)

    # เล่นเพลงที่ดาวน์โหลด
    voice_client.play(discord.FFmpegPCMAudio(song_path), after=lambda e: print('done', e))

    await ctx.send(f"Now playing: {url}")

# ฟังก์ชันสำหรับหยุดเพลง
@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    await voice_client.disconnect()
    await ctx.send("Stopped the music and disconnected.")

# Slash Commands
@bot.tree.command(name='hellobot', description='Replies with Hello')
async def hellocommand(interaction: discord.Interaction):
    await interaction.response.send_message("Hello It's me BOT DISCORD")

@bot.tree.command(name='name')
@app_commands.describe(name="What's your name?")
async def namecommand(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}")

# Embeds
@bot.tree.command(name='help', description='Bot Commands')
async def helpcommand(interaction: discord.Interaction):
    embed = discord.Embed(title='Help Me! - Bot Commands',
                          description='Bot Commands',
                          color=0x66FFFF,
                          timestamp=datetime.datetime.utcnow())

    embed.add_field(name='/hellobot', value='Hello Command', inline=True)
    embed.add_field(name='/name', value='Name Command', inline=True)
    embed.add_field(name='/help', value='Show commands', inline=False)
    embed.add_field(name='/play <url>', value='Play music from YouTube', inline=True)
    embed.add_field(name='/stop', value='Stop the music and disconnect', inline=True)

    embed.set_footer(text='Bot by YourName')

    await interaction.response.send_message(embed=embed)

# รันบอทด้วย Token
if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR: Token not found! Please check your environment variables.")
