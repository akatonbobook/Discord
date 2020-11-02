import re

import discord
from discord.ext import commands
from googletrans import Translator
from langdetect import detect


class TranslateCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trans(self, ctx, text, target=None):
        source = detect(text)
        if target is None:
            if source == "ja":
                target = 'en'
            else:
                target = 'ja'
        result = None
        count = 0
        while True:
            count += 1
            try:
                translator = Translator()
                result = translator.translate(text, dest=target)
                break
            except Exception as e:
                if count > 10:
                    await ctx.send("翻訳できませんでした")
                    return
                print("try again")
                continue
        embed = discord.Embed(title=source + "から" + target + "へ翻訳")
        embed.add_field(name=result.origin, value=result.text)
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        text = message.content
        p = re.compile('[a-zA-Z0-9]+')
        if len(text) > 1:
            if text[0] == self.bot.command_prefix:
                return
            if not p.match(text[0]):
                return
        if len(text) > 4:
            if text[:4] == "http":
                return
        try:
            source = detect(text)
        except:
            return
        if source != "ja":
            result = None
            count = 0
            while True:
                count += 1
                try:
                    translator = Translator()
                    result = translator.translate(text, dest="ja")
                    break
                except Exception:
                    if count > 10:
                        await message.channel.send("翻訳できませんでした")
                        return
                    print("try again")
                    continue
            embed = discord.Embed(title=source + "から" + "ja" + "へ翻訳")
            embed.add_field(name=result.origin, value=result.text)
            await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(TranslateCog(bot))
