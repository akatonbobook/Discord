import datetime
import io
import os

import discord
import pdf2image
import requests
from discord.ext import commands


class PdfCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        poppler_path = os.path.join(self.bot.path, "poppler-0.68.0", "bin")
        os.environ["PATH"] += os.pathsep + poppler_path

        attach = message.attachments
        if len(attach) == 1:
            if '.pdf' == attach[0].filename[-4:]:
                print("pdf was uploaded!")
                r = requests.get(attach[0].url, stream=True)
                if r.status_code == 200:
                    print("download as " + attach[0].filename + " from " + attach[0].url)
                    pdfimages = pdf2image.convert_from_bytes(r.content, fmt="jpg")
                    
                    pages = len(pdfimages)
                    askembed = discord.Embed(title="pdf to jpg")
                    askembed.add_field(name="このpdfを変換しますか?", value=attach[0].filename + " " + str(pages) + "ページ分")
                    msg = await message.channel.send(embed=askembed)

                    await msg.add_reaction('🙋‍♂️')

                    limit = datetime.datetime.now() + datetime.timedelta(seconds=300)

                    def check(reaction, user):
                        return user != message.author.bot and str(reaction.emoji) == '🙋‍♂️'

                    while datetime.datetime.now() < limit:
                        try:
                            reaction, user = await self.bot.wait_for("reaction_add", timeout=5, check=check)
                        except:
                            continue
                        else:
                            if(user.bot):
                                continue

                            print(user.display_name, datetime.datetime.now().strftime('%H:%M:%S'), "add reactioin")

                            dm = await user.create_dm()
                            
                            for idx, image in enumerate(pdfimages):
                                imgByteArr = io.BytesIO()
                                image.save(imgByteArr, format=image.format)
                                imgByteArr = imgByteArr.getvalue()
                                await dm.send(file=discord.File(io.BytesIO(imgByteArr), filename="pdf-image-" + str(idx) + ".jpg"))

                    try:
                        await msg.delete()
                        print("delete message")
                    except Exception:
                        pass


def setup(bot):
    bot.add_cog(PdfCog(bot))