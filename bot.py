import discord
import requests
import asyncio
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()
print("loading dotenv")

intents = discord.Intents.default()
intents = discord.Intents.message_content()
intents.members = True

client = discord.Client(intents=intents)
print("client class created")

API_ENDPOINTS = {
    '.trump': 'https://api.elevenlabs.io/v1/text-to-speech/ws3k037rKhKuz8MEyprg/stream',
    '.biden': 'https://api.elevenlabs.io/v1/text-to-speech/IlHFNE62tMNgCbPKR5Xs/stream',
    '.shinzo': 'https://api.elevenlabs.io/v1/text-to-speech/SHINZO/stream'
}

# Get the Discord bot token and API key from the environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
print("beginning client event")


@client.event
async def on_message(message):
    print("detected a message")
    print(message)
    if message.content.startswith('.'):
        print("inside the '.' conditional")
        # Get the command and phrase from the user input
        parts = message.content.split()
        command = parts[0]
        phrase = ' '.join(parts[1:])

        # Check if the command is valid
        if command not in API_ENDPOINTS:
            print("did not detect valid api endpoint")
            return

        # Send a request to the API endpoint
        print("sending a request to API endpoint")
        api_endpoint = API_ENDPOINTS[command]
        headers = {
            'accept': '*/*',
            'xi-api-key': API_KEY,
            'Content-Type': 'application/json'
        }
        request_data = {
            "text": phrase,
            "voice_settings": {
                "stability": 0,
                "similarity_boost": 0
            }
        }
        response = requests.post(api_endpoint, headers=headers, json=request_data)
        print("the response: " + response)

        # Check if the response was successful
        print("checking response")
        if response.ok:
            print("response ok")
            # Play the audio stream in the user's voice channel
            if message.author.voice:
                print("if command auther is in voice")
                voice_channel = message.author.voice.channel
                voice_client = await voice_channel.connect()
                voice_client.play(discord.FFmpegPCMAudio(response.content))
                while voice_client.is_playing():
                    await asyncio.sleep(1)
                await voice_client.disconnect()
        else:
            # If the response was not successful, print the error message
            error_message = response.json()["detail"][0]["msg"]
            print(f"Error: {error_message}")

client.run(DISCORD_BOT_TOKEN)
