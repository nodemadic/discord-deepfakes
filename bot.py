import discord
import requests

client = discord.Client()

API_ENDPOINT = "API_ENDPOINT HERE"

@client.event
async def on_message(message):
    if message.content.startswith('!play'):
        # Get the phrase from the user input
        phrase = message.content.split('!play ')[1]

        # Send a request to the API endpoint with the phrase as a parameter
        request_data = {
            "text": phrase,
            "voice_settings": {
                "stability": 0,
                "similarity_boost": 0
            }
        }
        response = requests.post(API_ENDPOINT, json=request_data)

        # Check if the response was successful
        if response.ok:
            # Play the audio stream in the user's voice channel
            if message.author.voice:
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

client.run('YOUR_BOT_TOKEN')
