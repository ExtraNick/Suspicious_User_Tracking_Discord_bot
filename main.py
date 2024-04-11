from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import discord
from responses import get_response
from responses import sus_users #Imports the list containing suspicious 

Bot_channel = 1226380484020404304


#Loading token from the .env file located at this very folder
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(TOKEN)

#Setting up bot 
#Intents are required for the Bot to have permissions for any actions
intents: Intents = Intents.default() #This sets the intents to the bot's default (defined at the developer/applications page)
intents.message_content = True 
client: Client = Client(intents=intents)


#Define the ability for the bot to read and send messages
async def send_message(message: Message, user_message: str, channel: str) -> None:
    if not user_message:
        print ('(Message was empty because intents were not enabled probably)')
        return

    try:
        response: str = get_response(user_message, channel)
        # await message.author.send(response) if is_private else 
        channel = client.get_channel(Bot_channel)
        await channel.send(response)
    except Exception as e:
        print(e)

#This will define events for when the bot goes online (mainly for feedback here)

async def on_ready() -> None:
    print(f'{client.user} is now running!')


#This reads coming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = message.channel.id

    print(f'[{channel} {username}: "{user_message}"]')
    await send_message(message, user_message, channel)
    

    if message.author.id in list(map(int, sus_users)): #If the user's ID of whom sent the message is in the list "sus_users", the bot sends a message in the chat
        channel = client.get_channel(Bot_channel)
        embed = discord.Embed( #Embed is used to make the message pretty
            colour = 0xFEE75C,
            description=message.content,
        )
        embed.set_author(name=message.author) #username
        embed.set_thumbnail(url=message.author.avatar) #profile picture
        embed.add_field(name="Message link", value=str(message.jump_url)) #Jump to message button
        embed.add_field(name="Channel link", value=str(message.channel.jump_url)) #Jump to channel 
        embed.set_footer(text="User ID: " + str(message.author.id)) #lists the user ID on the footer for ease of actions
        await channel.send("Message by suspicious user " + str(message.author) + " detected") #bot sends a message (The purpose of this is for using the search function)
        await channel.send(embed=embed) #The bot embeds everything that was defined abovezzz



#This starts the bot
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
