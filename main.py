import discord
import random
from discord import Message, Member
from discord.ui import Button, View
from discord.ext import commands


TOKEN = 'MTAzMDU5OTIyMDk1NDEzNjYxNg.GfnV5j._GhNCCNbnqR8xJM-3R5ihEHwhQzr_-yryd6y9g'

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


class AcceptButton(Button):
    def __init__(self, guild_id, chat_id):
        super().__init__(label='Принять', style=discord.ButtonStyle.success)
        self.guild_id = guild_id
        self.chat_id = chat_id

    async def callback(self, interaction):
        await interaction.response.edit_message(content=interaction.message.content + '\nВы прияли приглашение', view=None)
        await update_permission(self.guild_id, self.chat_id, interaction.user)


class DismissButton(Button):
    def __init__(self):
        super().__init__(label='Отклонить', style=discord.ButtonStyle.danger)

    async def callback(self, interaction):
        await interaction.response.edit_message(content=interaction.message.content + '\nВы отклонили приглашение', view=None)

async def update_permission(guild_id, chat_id, user):
    guild = bot.get_guild(guild_id)
    chat = guild.get_channel(chat_id)
    overwrite = discord.PermissionOverwrite(read_messages=True)
    await chat.set_permissions(user, overwrite=overwrite)

@bot.command()
async def chat(ctx, *arg):
    createadChat = await create_chat(ctx)
    await send_dm_invite(ctx, createadChat.guild.id, createadChat.id)

@bot.command()
async def voice(ctx, *arg):
    createadChat = await create_voice(ctx)
    await send_dm_invite(ctx, createadChat.guild.id, createadChat.id)

async def create_voice(ctx):
    name = ctx.message.author.display_name

    overwrites = {
        ctx.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.message.guild.me: discord.PermissionOverwrite(read_messages=True),
        ctx.message.author: discord.PermissionOverwrite(read_messages=True)
    }

    if len(ctx.message.mentions) == 0:
        await ctx.message.reply("Не забудте упомянуть как минимум одного пользователя")
        return

    for mention in ctx.message.mentions:
        if mention == ctx.message.author:
            continue
        name += ' ' + mention.display_name

    print("chat name:" + name)
    chat = await ctx.message.guild.create_voice_channel(name, overwrites=overwrites)
    return chat

async def create_chat(ctx):
    name = ctx.message.author.display_name

    overwrites = {
        ctx.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.message.guild.me: discord.PermissionOverwrite(read_messages=True),
        ctx.message.author: discord.PermissionOverwrite(read_messages=True)
    }

    if len(ctx.message.mentions) == 0:
        await ctx.message.reply("Не забудте упомянуть как минимум одного пользователя")
        return

    for mention in ctx.message.mentions:
        if mention == ctx.message.author:
            continue
        name += ' ' + mention.display_name

    print("chat name:" + name)
    chat = await ctx.message.guild.create_text_channel(name, overwrites=overwrites)
    return chat

async def send_dm_invite(ctx, guild_id, chat_id):
    buttons = [
        AcceptButton(guild_id, chat_id),
        DismissButton()
    ]

    view = View()
    for item in buttons:
        view.add_item(item)

    authorName = ctx.message.author.display_name
    message = authorName + ' приглашает вас вступить в переговоры: '
    for mention in ctx.message.mentions:
        message += mention.display_name
        message += ' - '
    message += authorName

    for mention in ctx.message.mentions:
        if mention == ctx.message.author:
            continue
        await mention.send(message, view=view) # ephemeral=True


bot.run(config['token'])
