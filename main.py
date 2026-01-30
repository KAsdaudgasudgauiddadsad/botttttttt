import discord
from discord import app_commands
from discord.ui import View
import asyncio

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"AĞA BOTU HAZIR: {self.user}")

class AnonimButonView(View):
    def __init__(self, mesaj_icerigi):
        super().__init__(timeout=None)
        self.mesaj_icerigi = mesaj_icerigi

    @discord.ui.button(label="GÖNDER", style=discord.ButtonStyle.green)
    async def gonder_butonu(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Önce butona basıldığını gizlice onayla, "Etkileşim başarısız" demesin
        await interaction.response.defer(ephemeral=True)
        
        # 5 Mesajı seri şekilde fırlatıyoruz
        for _ in range(5):
            try:
                # followup.send kullanarak 403 hatasını ve tek mesaj sınırını aşıyoruz
                await interaction.followup.send(content=self.mesaj_icerigi, ephemeral=False)
                # Aradaki bekleme süresini çok kısalttım (0.2 saniye)
                await asyncio.sleep(0.2) 
            except Exception as e:
                print(f"Hata: {e}")

client = MyClient()

@client.tree.command(name="spamz", description="Seri mesaj butonu")
@app_commands.describe(mesaj="Ne yazılacak?")
async def spamz(interaction: discord.Interaction, mesaj: str):
    # Ayarlarınla uyumlu
    view = AnonimButonView(mesaj)
    # Tertemiz görünüm için sadece nokta
    await interaction.response.send_message(content=".", view=view, ephemeral=True)

# Kurulum ayarlarını koda gömüyoruz
spamz.allowed_installs = app_commands.AppInstallationType(user=True, guild=True)
spamz.allowed_contexts = app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True)

client.run('MTQ1OTQ4NzE2OTEzNDU5MjE4Mw.GXE7fK.XKmaxdeHXJQ1HK3YjfvGqOcSBjw9gzWOYhUVfA')