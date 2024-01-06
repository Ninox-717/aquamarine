class SleepUser:
    def __init__(self, bot, config):
        self.bot = bot
        self.SleepTC = config['SleepTC_ID']
        self.SleepVC = config['SleepVC_ID']

    async def MoveUser(self, message):
        if message.channel.id != self.SleepTC:  # ここにメンションを確認するチャンネルのIDを指定
            return

        if not message.mentions:
            await message.channel.send('メンションがありません.')
            await message.delele(delay=5)
            return
            
        target = message.mentions[0]
        author = message.author
        if target.voice and author.voice.channel == target.voice.channel:
            afk_vc = self.bot.get_channel(self.SleepVC)  # ここにAFK用のVCのIDを指定
            await target.move_to(afk_vc)
            await message.channel.send(f'{target.mention}を寝落ち部屋に送ったよ！')
        else:
            await message.channel.send(f'{author.mention}と{target.mention}は同じVCに接続していません.')