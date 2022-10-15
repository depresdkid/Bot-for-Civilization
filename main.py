import discord
import random
from discord.ui import Button, View
from discord.ext import commands

TOKEN = 'MTAzMDU5OTIyMDk1NDEzNjYxNg.GVzGXK.Mj2YkeLgYSIZVdzWAGyfAv_1yLsIseAnSjMbO4'

config = {
    'token': TOKEN,
    'prefix': ['-', '!'],
}

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("command not found error " + ctx.message.content)

@bot.command()
async def test(ctx, *arg):
    await ctx.message.reply('Метод вызван')
    buttons = [
        {
            'button': Button(label='Accept', style=discord.ButtonStyle.success),
            'callback': callBackAccept
        },
        {
            'button': Button(label='Disime', style=discord.ButtonStyle.danger),
            'callback': callBackDisime
        },
    ]

    view = View()
    for item in buttons:
        item.get('button').callback = item.get('callback')
        view.add_item(item.get('button'))
    await ctx.message.reply('Я работаю', view=view)

async def callBackAccept(interaction):
    await interaction.response.edit_message(content='callBack на поддверждение вызван!', view=None)

async def callBackDisime(interaction):
    await interaction.response.edit_message(content='callBack на отмену вызван!', view=None)

@bot.command()
async def chat(ctx, *arg):
    name = ctx.message.author.display_name
    overwrites = {
        ctx.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.message.guild.me: discord.PermissionOverwrite(read_messages=True),
        ctx.message.author: discord.PermissionOverwrite(read_messages=True)
    }
    for mention in ctx.message.mentions:
        if mention == ctx.message.author:
            continue
        overwrites[mention] = discord.PermissionOverwrite(read_messages=True)
        await mention.send('Hi')
        name += ' ' + mention.display_name

    await ctx.message.guild.create_text_channel(name, overwrites=overwrites)

@bot.command()
async def SendMessage(ctx, *arg):
    await ctx.message.author.send('Some text')

bot.run(config['token'])