import os
import discord
from discord.ext import commands

from myserver import server_on
# ใส่โทเคนของบอทคุณที่นี่
GUILD_ID = 1247621475863756810  # ใส่ ID ของเซิร์ฟเวอร์
TARGET_CHANNEL_ID = 1256147490994917458  # ใส่ ID ของช่องที่ต้องการส่งข้อมูลที่กรอก
ROLE_NAME = '[ MEMBER ] สมาชิก'  # ใส่ชื่อยศที่ต้องการให้

intents = discord.Intents.default()
intents.members = True  # เปิดใช้งาน permissions สำหรับสมาชิก
intents.message_content = True  # เปิดใช้งาน permissions สำหรับเนื้อหาข้อความ

bot = commands.Bot(command_prefix='!', intents=intents)

class NameModal(discord.ui.Modal, title='กรุณากรอกข้อมูลของคุณ'):
    name = discord.ui.TextInput(label='ชื่อ', placeholder='กรอกชื่อของคุณที่นี่')
    age = discord.ui.TextInput(label='อายุ', placeholder='กรอกอายุของคุณที่นี่', style=discord.TextStyle.short)
    character_name = discord.ui.TextInput(label='ชื่อตัวละคร', placeholder='กรอกชื่อตัวละครของคุณที่นี่')

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="ข้อมูลผู้ใช้ใหม่", color=discord.Color.blue())
        embed.add_field(name="ชื่อ", value=self.name.value, inline=False)
        embed.add_field(name="อายุ", value=self.age.value, inline=False)
        embed.add_field(name="ชื่อตัวละคร", value=self.character_name.value, inline=False)
        embed.set_footer(text=f"ส่งโดย {interaction.user.display_name}", icon_url=interaction.user.avatar.url)

        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        if target_channel:
            await target_channel.send(f"{interaction.user.mention} ได้ส่งข้อมูลใหม่", embed=embed)
        else:
            await interaction.response.send_message('ไม่สามารถส่งข้อมูลไปยังช่องที่ระบุได้', ephemeral=True)

        guild = bot.get_guild(GUILD_ID)
        if guild:
            member = guild.get_member(interaction.user.id)
            role = discord.utils.get(guild.roles, name=ROLE_NAME)

            if role:
                await member.add_roles(role)
                await interaction.response.send_message(f'คุณ {self.name.value} ได้รับยศ {role.name} แล้ว!', ephemeral=True)
            else:
                await interaction.response.send_message(f'ไม่พบยศ {ROLE_NAME}', ephemeral=True)
        else:
            await interaction.response.send_message('ไม่พบเซิร์ฟเวอร์ที่ระบุ', ephemeral=True)

class GreetView(discord.ui.View):
    @discord.ui.button(label='คลิกเพื่อกรอกข้อมูล', style=discord.ButtonStyle.primary)
    async def greet_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def greet(ctx):
    embed = discord.Embed(
        title="Introduce YourSelf",
        description="กดปุ่มด้านล่างเพื่อยืนยันแนะนำตัวครับ !!!",
        color=discord.Color.from_rgb(255, 0, 0)
    )
    embed.set_image(url='https://share.creavite.co/667e71a1d904d516321b5ff1.gif')  # ใส่ URL ของรูปภาพที่คุณต้องการใช้
    embed.set_footer(text=  "SYSTEM BY WPDEVELOPER")

    view = GreetView()
    await ctx.send(embed=embed, view=view)

    server_on()

bot.run(os.getenv('TOKEN'))
