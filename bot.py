import discord
import config
import selenium
import urllib
import asyncio
from discord import app_commands
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

# async def send_message(message, user_message, is_private):
#     try:
#         response = responses.get_response(user_message)
#         await message.author.send(response) if is_private else await message.channel.send(response)

#     except Exception as e:
#         print(e)


def run_discord_bot():
    TOKEN = config.DISCORD_TOKEN
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix = "!", intents = intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f'{username} said: "{user_message}" ({channel})')
        # await message.channel.send_message("Noted")


    @bot.event
    async def on_member_join(member):
        await bot.get_channel('isagoat').send(f"{member.name} has entered blue lock.")

    @bot.tree.command(name = 'egoist')
    async def egoist(interaction):
        await interaction.response.send_message("You are an egoist.")

    @bot.tree.command(name = "devour")
    @app_commands.describe(who = 'Who is to be devoured?')
    async def devour(interaction: discord.Interaction, who: str):
        await interaction.response.send_message(f"{interaction.user.name} devoured {who}")

    @bot.tree.command(name = "search")
    @app_commands.describe(what = 'What do you want to see, egoist?')
    async def search(interaction: discord.Interaction, what: str):

        try:
            await interaction.response.defer(thinking=True)
            await asyncio.sleep(3)
            op = webdriver.ChromeOptions()
            op.add_argument('headless')
            driver = webdriver.Chrome(options = op)
            driver.get(f'https://www.google.com/search?q={what}&hl=en&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiex4Puzrn9AhUlC0QIHdeJC3kQ_AUoAXoECAEQAw&biw=1280&bih=616&dpr=1.5')
            
            #Download first image
            first_link = driver.find_element(By.XPATH, '//div[@id = "islrg"]//img').get_attribute('src')
            extension = first_link.split('/')[1].split(';')[0]
            urllib.request.urlretrieve(first_link, f"images/temp.{extension}")

        except Exception as e:
            print(e)
        
        # await interaction.response.send_message(file = discord.File(f'images/temp.{extension}'))
        
        await interaction.followup.send(file = discord.File(f'images/temp.{extension}'))
        

    # @app_commands.command(name="rps")
    # @app_commands.choices(choices=[
    #     app_commands.Choice(name="Rock", value="rock"),
    #     app_commands.Choice(name="Paper", value="paper"),
    #     app_commands.Choice(name="Scissors", value="scissors"),
    #     ])
    # async def rps(self, i: discord.Interaction, choices: app_commands.Choice[str]):
    #     if (choices.value == 'rock'):
    #         counter = 'paper'
    #     elif (choices.value == 'paper'):
    #         counter = 'scissors'
    #     else:
    #         counter = 'rock'

    bot.run(TOKEN)