import io

import discord
import requests
from discord.ext import commands

url = 'https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={d}'

class QrCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def qr(self, ctx, data):
        if ctx.author.bot:
            return
        r = requests.get(url.format(d=data))
        if r.status_code == 200:
            with open('qr.png', 'bw') as f:
                f.write(r.content)
            await ctx.channel.send(file=discord.File(io.BytesIO(r.content), 'qr.png'))


def setup(bot):
    bot.add_cog(QrCog(bot))