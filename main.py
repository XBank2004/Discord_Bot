import os
import discord
import datetime
from discord.ext import commands
from discord import app_commands

# โหลด environment variables
TOKEN = os.getenv('TOKEN')

# ตั้งค่าบอท
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
    await ctx.send(f"hello {ctx.author.name}!")

@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)

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

    embed.set_footer(text='Bot by YourName')

    await interaction.response.send_message(embed=embed)

# รันบอทด้วย Token
if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR: Token not found! Please check your environment variables.")
