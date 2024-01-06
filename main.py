#汎用ライブラリのインポート
import os

import discord
from discord.ext import commands
from discord.ext.commands.core import bot_has_any_role

#作成したファイルのインポート
from SleepUser import SleepUser
from Exam import Exam
from keep_alive import keep_alive

#botの設定
intents = discord.Intents.all()
PREFIX = os.environ['PREFIX']
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
client = discord.Client(intents=intents)

#Channel設定　複数サーバーで動かす場合はこの値をjsonで管理することになりそう。
SleepConfig = {
    'SleepTC_ID': 1181401463386275871,
    'SleepVC_ID': 1181553105515577394
}

ExamConfig = {
    'ProfileTC_ID': 1183028925903941672,
    'VotePanel_ID': 1183028960527921162,
    'ResultPanel_ID': 1188185798747619339
}

sleep_instance = SleepUser(bot, SleepConfig)
exam_instance = Exam(bot, ExamConfig)


@bot.event
async def on_ready():
    channel = bot.get_channel(1181401463386275871)
    if channel and isinstance(channel, discord.TextChannel):
        await channel.send('ボットが起動しました')
    else:
        print("Text channel not found")


@bot.event
async def on_message(message):
    if not message.author.bot:
        await sleep_instance.MoveUser(message)
        await exam_instance.VoteStart(message)


keep_alive()
TOKEN = os.getenv("TOKEN")
try:
    bot.run(TOKEN)
except:
    os.system("kill")
