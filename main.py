import os
import discord
import datetime
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

from myserver import server_on  # ตรวจสอบว่าไฟล์นี้มีอยู่จริง

# โหลด environment variables
load_dotenv()

# ตั้งค่าบอท
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


# //////////////////// Bot Event /////////////////////////
@bot.event
async def on_ready():
    print("Bot Online!")
    print("555")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s)")


# แจ้งคนเข้า - ออกจากเซิร์ฟเวอร์
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1140633489520205934)  # ใส่ ID ห้องให้ถูกต้อง
    if channel:
        text = f"Welcome to the server, {member.mention}!"
        embed = discord.Embed(title="Welcome to the server!",
                              description=text,
                              color=0x66FFFF)

        await channel.send(text)  # ส่งข้อความไปที่ห้องนี้
        await channel.send(embed=embed)  # ส่ง Embed ไปที่ห้องนี้
        await member.send(text)  # ส่งข้อความไปที่แชทส่วนตัวของ member


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

    mes = message.content.lower()  # ใช้ lower() เพื่อรองรับ case-insensitive
    if mes == 'hello':
        await message.channel.send("Hello It's me")

    elif mes == 'hi bot':
        await message.channel.send(f"Hello, {message.author.name}")

    await bot.process_commands(message)  # ให้ bot รัน commands ด้วย


# ///////////////////// Commands /////////////////////

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}!")


@bot.command()
async def test(ctx, arg):
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

    embed.add_field(name='/hello1', value='Hello Command', inline=True)
    embed.add_field(name='/hello2', value='Hello Command', inline=True)
    embed.add_field(name='/hello3', value='Hello Command', inline=False)

    embed.set_author(name='Author',
                     url='https://www.youtube.com/@maoloop01/channels',
                     icon_url='https://yt3.googleusercontent.com/...')

    embed.set_thumbnail(url='https://yt3.googleusercontent.com/...')
    embed.set_image(url='https://i.ytimg.com/vi/KZRa9DQzUpQ/hq720.jpg')

    embed.set_footer(text='Footer',
                     icon_url='https://yt3.googleusercontent.com/...')

    await interaction.response.send_message(embed=embed)


# เปิดเซิร์ฟเวอร์ (ถ้ามี)
server_on()

# รันบอทด้วย Token
bot.run(os.getenv('TOKEN'))