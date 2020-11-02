import os
import random

from discord.ext import commands


class QuizCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.active = {}

    @commands.command()
    async def quiz(self, ctx, loop=""):

        # 送信者がぼっとなら終了
        if ctx.author.bot:
            return

        # 引数があった場合，ループをTrueに
        if loop != "":
            loop = "True"

        guild = ctx.guild
        self.active.setdefault(guild, False)

        # 問題出題中なら終了，そうでなければ出題中に変更
        if self.active[guild]:
            await ctx.send("すでに問題を出題中です")
            return
        else:
            self.active[guild] = True

        # ファイルを確認し，存在しない場合は終了
        filepath = os.path.join(self.bot.path, "quiz", "quiz.txt")
        if not os.path.exists(filepath):
            await ctx.send("問題が見つからなかったよ")
            self.active[guild] = False
            return

        # ファイルからデータ取得
        with open(filepath, encoding="utf_8") as f:
            raw_data = [line.strip() for line in f.readlines()]

        # ランダムに問題を選択
        r = random.randrange(len(raw_data) // 2)
        question, answer = raw_data[r * 2], raw_data[r * 2 + 1].split(" ")

        # 表示
        await ctx.send("[問題] " + question)

        # 解答チェック関数
        def check(m):
            if m.author.bot:
                return False
            return m.content in answer

        try:
            print("wait")
            message = await self.bot.wait_for("message", timeout=30, check=check)
            await ctx.send(message.author.mention + " 正解です！")
            # 問題出題中をFalseに
            self.active[guild] = False
        except:
            await ctx.send("正解は " + answer[0] + " でした")
            # 問題出題中をFalseに
            self.active[guild] = False
            return

        # ループがTrueならループ
        if loop != "":
            await self.quiz(ctx, loop)



def setup(bot):
    bot.add_cog(QuizCog(bot))
