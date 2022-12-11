#!/usr/bin/env python3

from discord.ext import commands
import discord
import config

class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('..'), intents=intents, **kwargs)

    async def setup_hook(self):
        for cog in config.cogs:
            try:
                await self.load_extension(cog)
            except Exception as exc:
                print(f'Could not load extension {cog} due to {exc.__class__.__name__}: {exc}')

    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')


intents = discord.Intents.default()
intents.message_content = True
bot = Bot(intents=intents)

# write general commands here
@bot.command()
async def ping(ctx):
    await ctx.send("Pong :ping_pong:")
    # await ctx.send(f"`{round(bot.latency * 1000)}ms`")

@bot.event
async def on_message(message):
    """
    Filter banned words
    """

    banned_words_wildcard = [
        "sex",
        "fuck",
    ]

    for word in banned_words_wildcard:
        if word.lower() in message.content.lower():
            await message.reply(f"{message.author.mention} Please watch your language")
            await message.delete()

    banned_words_exact = [
        "noice",
        "bruh",
    ]

    for word in message.content.lower().split(" "):
        if word.lower() in banned_words_exact:
            await message.reply(f"{message.author.mention} Please watch your language")
            await message.delete()

    await bot.process_commands(message)

bot.run(config.token)
