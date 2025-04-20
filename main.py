import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== واجهة العودة للقائمة الرئيسية =====
class BackToMenu(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=None)
        self.author = author
        self.add_item(BackButton(author))

class BackButton(discord.ui.Button):
    def __init__(self, author):
        super().__init__(label="🔙 العودة للقائمة", style=discord.ButtonStyle.secondary)
        self.author = author

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.author:
            await interaction.response.send_message("❌ لا يمكنك التفاعل مع هذا الزر.", ephemeral=True)
            return
        await interaction.response.edit_message(embed=main_menu_embed(), view=MainMenu(interaction.user))

# ===== قائمة اختيار الأنمي =====
class AnimeSelect(discord.ui.Select):
    def __init__(self, author):
        self.author = author
        options = [
            discord.SelectOption(label="Solo Leveling", description="أنمي الأكشن والخيال", value="solo")
        ]
        super().__init__(placeholder="اختر الأنمي 🎬", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.author:
            await interaction.response.send_message("❌ لا يمكنك التفاعل مع هذا الأمر.", ephemeral=True)
            return

        embed = discord.Embed(
            title="📂 مجلد حلقات Solo Leveling",
            description="[اضغط هنا لمشاهدة الحلقات على Google Drive](https://drive.google.com/drive/folders/1TmZOkeiryW9ewEfMM2tfxchraU6s_U-M?usp=sharing)",
            color=discord.Color.purple()
        )
        embed.set_footer(text="جميع الحقوق محفوظة لدى يو انمي © 2025")
        await interaction.response.edit_message(embed=embed, view=BackToMenu(self.author))

# ===== القائمة الرئيسية =====
class MainMenu(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=None)
        self.add_item(AnimeSelect(author))

def main_menu_embed():
    embed = discord.Embed(
        description="**مرحبا بك في بوت يو انمي 🎬 اختر الأنمي الذي ترغب في مشاهدته.\nالبوت قيد التطوير حالياً ✨**",
        color=discord.Color.dark_theme()
    )
    embed.set_image(url="attachment://logo.jpg")
    embed.set_footer(text="جميع الحقوق محفوظة لدى يو انمي © 2025")
    return embed

# ===== عند تشغيل البوت =====
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

# ===== أمر /مشاهدة =====
@bot.tree.command(name="مشاهدة", description="القائمة الرئيسية لمشاهدة الأنمي")
async def watch(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    file = discord.File("logo.jpg", filename="logo.jpg")
    await interaction.followup.send(embed=main_menu_embed(), view=MainMenu(interaction.user), file=file, ephemeral=True)

# ===== شغّل البوت =====
bot.run("MTM2MzIwMTEzOTA1MDQxNDExMA.Gnydn4.793h0mjsWcClEjxGDXa0lFzxYT-Vt_j5XKyHvs")
