import discord

class Exam:
    def __init__(self, bot, config):
        self.bot = bot
        self.Profile = config['ProfileTC_ID']
        self.Vote = config['VotePanel_ID']
        self.Result = config['ResultPanel_ID']

    async def VoteStart(self,message):
        if message.channel.id != self.Profile:
            return

        #各埋め込みの送信
        await self.VotePanelSend(message)
        await self.ResultPanelSend(message)

        #各ボタンの配置
        await self.VoteButtonCreate(message)
        await self.ResultButtonCreate(message)
        
    async def VotePanelSend(self,message):
        #埋め込みの作成
        embed = discord.Embed(
            title = message.author.display_name + '(' + message.author.name + ')',
            description = message.content,
            color = 0x00ff00
        )
        embed.set_thumbnail(url=message.author.avatar.url)

        VoteTC = self.bot.get_channel(self.Vote)
        self.VoteMessage = await VoteTC.send(embed=embed)

    async def ResultPanelSend(self,message):
        #埋め込みの作成
        embed = discord.Embed(
            title = message.author.display_name + '(' + message.author.name + ')',
            description = '投票結果',
            color = 0x00ff00
        )
        embed.set_thumbnail(url=message.author.avatar.url)

        ResultTC = self.bot.get_channel(self.Result)
        self.ResultMessage = await ResultTC.send(embed=embed)

    async def VoteButtonCreate(self,message):
        #ボタンの設定
        view = VoteButton(self.VoteMessage, self.ResultMessage, timeout=None)
        await self.VoteMessage.edit(view=view)

    async def ResultButtonCreate(self,message):
        #ボタンの設定
        view = ResultButton(self.VoteMessage, self.ResultMessage, timeout=None)
        await self.ResultMessage.edit(view=view)

class VoteButton(discord.ui.View):
    def __init__(self, VoteMessage, ResultMessage, timeout=180):
        super().__init__(timeout=timeout)
        self.VoteMessage = VoteMessage
        self.ResultMessage = ResultMessage
        self.ResultDescription = self.ResultMessage.embeds[0].description
        self.votearray = {}

    @discord.ui.button(label="〇", style=discord.ButtonStyle.success, custom_id = "OK")
    async def OK(self, interaction: discord.Interaction, button: discord.ui.Button):
        #変数の取り込み
        label = button.label
        custom_id = button.custom_id

        await self.response_message(interaction, label, custom_id)
        await self.edit_embed()
        
    @discord.ui.button(label="×", style=discord.ButtonStyle.gray, custom_id="NG")
    async def NG(self, interaction: discord.Interaction, button: discord.ui.Button):
        #変数の取り込み
        label = button.label
        custom_id = button.custom_id

        await self.response_message(interaction, label, custom_id)
        await self.edit_embed()

    async def response_message(self, interaction, label, custom_id):
        title = self.VoteMessage.embeds[0].title

        #メッセージを数秒間で自動で消えるように設定する。
        if interaction.user.display_name in self.votearray:
            if self.votearray[interaction.user.display_name] == label:
                await interaction.response.send_message(f"既に{title}に{label}の投票をしているよ！", ephemeral=True)
            else:
                await interaction.response.send_message(f"{title}の投票を{label}に変更したよ！", ephemeral=True)
        else:
            await interaction.response.send_message(f"{title}に{label}の投票をしたよ！", ephemeral=True)

        self.votearray[interaction.user.display_name] = label
    
    async def edit_embed(self):
        #文字列の生成
        ResultDescription = "投票結果"
        total = {}
        for key, value in self.votearray.items():
            ResultDescription += '\r\n' + key + ' : ' + value
            if value in total:
                total[value] += 1
            else:
                total[value] = 1

        ResultDescription += '\r\n\r\n'
        for key, value in total.items():
            ResultDescription += key + ' : ' + str(value) + '票\r\n'

        #埋め込みの作成
        embed = discord.Embed(
            title = self.VoteMessage.embeds[0].title,
            description = ResultDescription,
            color = self.VoteMessage.embeds[0].color,
        )
        embed.set_thumbnail(url=self.VoteMessage.embeds[0].thumbnail.url)
        await self.ResultMessage.edit(embed=embed)


class ResultButton(discord.ui.View):
    def __init__(self, VoteMessage, ResultMessage, timeout=180):
        super().__init__(timeout=timeout)
        self.VoteMessage = VoteMessage
        self.ResultMessage = ResultMessage
    
    @discord.ui.button(label="投票終了", style=discord.ButtonStyle.primary, custom_id = "result")
    async def result(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete(delay=3)
        await self.VoteMessage.delete(delay=3)