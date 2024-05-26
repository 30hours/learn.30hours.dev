# Generate audio for FM modulation.

# Author: OpenAI, 30hours

from openai import OpenAI

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1-hd",
    voice="onyx",
    speed=0.8,
    input="Hello world! The flag is chocolate underscore milkshake.",
)

response.stream_to_file("audio.mp3")
