import discord
from discord import app_commands
from discord.ext import commands
from discord import ui
import mysql.connector
import random
import requests

connection = mysql.connector.connect(
    host="your-host",
    user="your-username",
    password="your-password",
    database="your-database"
    )

words = ["jablko", "gruszka", 'telefon', "woda", "telewizor", "komputer", "ananas", "zegar", "auto"]

dataid = {}
dataword = {}

bot = commands.Bot(command_prefix="!", intents= discord.Intents.default())

query = connection.cursor()
checkdb = connection.cursor()
verifyquery = connection.cursor()
deletequery = connection.cursor()

guild = None

class VerificationModal(ui.Modal, title='Zweryfikuj swoje konto Roblox!'):
    RobloxID = ui.TextInput(label='Podaj ID swojego profilu Roblox')


    async def on_submit(self, interaction: discord.Interaction):
        if requests.get(url=f"https://www.roblox.com/users/{self.RobloxID.value}/profile").status_code == 200:
            checkdb.execute(f"SELECT * FROM Users WHERE DiscordID = '{interaction.user.id}';")
            results = checkdb.fetchall()

            if results:
                print("abc")
                await interaction.response.send_message(f"Jesteś już zweryfikowany na naszym serwerze! Jeżeli wystąpił błąd skontaktuj się z naszą adminstracją! ", ephemeral=True)
            else:
                print("bcb")
                robloxname = requests.get(f"https://users.roblox.com/v1/users/{self.RobloxID.value}").json()["name"]
                query.execute(f"INSERT INTO Users (RobloxID, DiscordID, Zweryfikowany, NickRoblox, NickDiscord) VALUES ('{self.RobloxID.value}', '{interaction.user.id}', 0, '{robloxname}', '{interaction.user}');")
                connection.commit()
                dataid[int(interaction.user.id)] = [self.RobloxID.value]
                verificationoptionsembed = discord.Embed(title="Sposoby weryfikacji konta", description=f"1. Zmień opis swojego profilu Roblox! Wygeneruj losowe słowo oraz dodaj je do opisu, nic prostszego! \n 2. Dołącz na grę weryfikacji! Dołącz na grę i podaj swój nick Discord! [NIEDOSTĘPNE]")
                optionsbutton = OptionsButtons()

                await interaction.response.send_message(embed=verificationoptionsembed, view=optionsbutton, ephemeral=True)
        else:
            await interaction.response.send_message(content="Nie znaleziono profilu gracza! Upewnij się że wpisałeś ID konta Roblox, w razie problemów zajrzyj na kanał pomocy z weryfikacją!", ephemeral=True)
        

class VerificationButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Weryfikuj", emoji="✅", style=discord.ButtonStyle.green, custom_id="main")
    async def werifikuj(self, interaction : discord.Interaction, Button: discord.ui.Button):
        await interaction.response.send_modal(VerificationModal())
        
class OptionsButtons(discord.ui.View):

    class CheckButtons(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        
        @discord.ui.button(label="Sprawdź opis!", emoji="✅", style=discord.ButtonStyle.green, custom_id="main")
        async def check(self, interaction : discord.Interaction, Button: discord.ui.Button):
            print(dataid)
            valuelist = dataid[interaction.user.id][0]
            req = requests.get(url=f"https://www.roblox.com/users/{valuelist}/profile").text

            if dataword[int(interaction.user.id)][0] == None:
                await interaction.response.send_message(f"Wystąpił błąd, skontaktuj się z administracją Aurus Verification! Kod błedu : 801", ephemeral=True)

            if dataword[interaction.user.id][0] in requests.get(f"https://users.roblox.com/v1/users/{valuelist}").json()["description"]:

                print("znaleziono")
                await interaction.user.add_roles(interaction.guild.get_role(1174021413515051058), reason="Pomyślna weryfikacja - AurusVerification")

                verifyquery.execute(f"UPDATE Users SET Zweryfikowany = 1 WHERE DiscordID = '{interaction.user.id}';")
                connection.commit()
                await interaction.response.send_message(f"Pomyślnie zweryfikowałeś się na AurusVerification! Powinieneś dostać Whiteliste na grze. Gdyby wystąpiły problemy skontaktuj się z administracją bota!", ephemeral=True)

            else:
                await interaction.response.send_message(f"Nie znaleziono słowa {dataword[int(interaction.user.id)][0]} w opisie twojego profilu!", ephemeral=True)


    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="1. Zmień opis profilu", emoji="💬", style=discord.ButtonStyle.blurple, custom_id="describeprofile")
    async def describeprofile(self, interaction : discord.Interaction, Button: discord.ui.Button):
        randomword = random.choice(words)
        dataword[int(interaction.user.id)] = [randomword]
        checkbutton = self.CheckButtons()
        await interaction.response.send_message(f"Zmień opis swojego profilu na roblox na taki zawierający słowo '{randomword}'! Po zmienieniu opisu dotknij przycisku 'Sprawdź opis', gdyby wystąpiły problemy skontaktuj się z administracją!", view=checkbutton, ephemeral=True)
        print("describe")

    @discord.ui.button(label="2. Dołącz na grę!", emoji="🎮", style=discord.ButtonStyle.blurple, custom_id="playgame", disabled=True)
    async def playgame(self, interaction : discord.Interaction, Button: discord.ui.Button):
        print("playgame")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    try:
        synced = await bot.tree.sync()
        print("synced") 
    except Exception as e:
        print(e)

    


@bot.tree.command(name="info", description="Sprawdź informacje o bocie!")
async def info(interaction: discord.Interaction):
    info = discord.Embed(title="INFORMACJE O BOCIE", color=0x00ff00, description=f"Bot jest w pełni open-sourced oraz działa na licencji MIT. \n Napisany przez @najkej_ (nick Discord), wykorzystuje technologie FastAPI, MySQL oraz Discord.py. Jest napisany głównie w Python oraz Lua (dla obsługi zapytań gier). \n Github : https://github.com/Najkej/AurusVerification/tree/main")

    await interaction.response.send_message(embed=info, ephemeral=True)



@bot.tree.command(name="verify", description="Zweryfikuj swoje konto Roblox oraz dostań się na Whiteliste!")

async def zapis(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Weryfikacja AurusVerification",
        description="Aby się zweryfikować kliknij przycisk poniżej oraz podążaj zgodnie z poleceniami. W razie problemów skontaktuj się z administracją bota!",
        color=discord.Color.brand_green()
    )

    button = discord.ui.button(label="Zweryfikuj się!")

    guild = interaction.guild
    
    await interaction.response.send_message(embed=embed, view=VerificationButtons(), ephemeral=True)


@bot.tree.command(name="deleteverification", description="Usuwa weryfikacje, tylko z permisjami admina.")
@app_commands.describe(id = "ID użytkownika którego weryfikacje chcesz usunąć!")
async def deleteverification(interaction: discord.Interaction, id: str):
    if interaction.user.guild_permissions.administrator:
        try:
            deletequery.execute(f"DELETE FROM Users WHERE DiscordID = '{id}'")
            connection.commit()
            await interaction.response.send_message(content="Usunięto weryfikacje osobie!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(content=f"Nie udało sie usunąć weryfikacji! {e}", ephemeral=True)
    else:
        await interaction.response.send_message(content="Nie masz wystarczających uprawnień!", ephemeral=True)



bot.run('Your_bot_token')
