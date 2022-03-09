import youtube_dl 
import os
import asyncio



async def play(ctx, url : str):
    print('in play', os.path)
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        #await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    #voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='voc-dev')
    #await voiceChannel.connect()
    #voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    #voice.play(discord.FFmpegPCMAudio("song.mp3"))

asyncio.run(play('','https://www.youtube.com/watch?v=oS-acFo_omQ&t=37s'))