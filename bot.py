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

# write general commands here
@bot.command()
async def ping(ctx):
    await ctx.send("Pong :ping_pong:")
    # await ctx.send(f"`{round(bot.latency * 1000)}ms`")

intents = discord.Intents.default()
intents.message_content = True
bot = Bot(intents=intents)

bot.run(config.token)
