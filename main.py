import code
from ntpath import join
import discord
import youtube_dl 
#pip install youtube_dl (2021.12.17)
from datetime import datetime
import os
import random
import re  #regex
import asyncio
import winsound
import json

configfilepath = '.\config.json'
secretfilepath = '.\secret.json'

configfile = open(configfilepath)
secretfile = open(secretfilepath)

jsonconfig = json.load(configfile)
jsonsecret = json.load(secretfile)

ytdl_format_options = {
    #'format': 'bestaudio/best',
    'format': 'worstaudio/worst',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()

        #print('####################################test: ')
        #print(url)
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        #print('###################### todo: ###########################')
        #print(data)

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

myintents = discord.Intents.default()
myintents.members = True #usefull for for member in guild.members: 
client = discord.Client(intents=myintents)

timeformat= "%H:%M:%S.%f: "
alarmFrequency = 2500  # Set Frequency To 2500 Hertz
alarmDuration = 3000  # Set Duration To 1000 ms == 1 second




@client.event
async def on_ready():
    snow = datetime.now()
    print(snow.strftime(timeformat) ,"ready")

    #guild = client.get_guild(840610295353311263)
    for guild in client.guilds:
        print("nummber of member of the guild " + str(guild.name) + ' [' + str(guild.id) + '] : ' +  str(guild.member_count))
        for member in guild.members: 
             
            print(str(member.name) + ': ' + str(member.id))

        channel = discord.utils.find(lambda c: c.name == 'dev',guild.channels)

        if channel != None:
            #await channel.send(':robot: initialized! :robot:', tts=False)
            await client.change_presence(activity=discord.Game(name="Python"))
    
    
@client.event
async def on_message(message):
    print(str(message.edited_at) + str(message.content))

    regex = "....-....-....-...."

    codebdo = re.findall(regex, message.content)
    if (codebdo != ''):
        for x in range(len(codebdo)):
            print('BDO code detected: ', codebdo[x])
            winsound.Beep(alarmFrequency, alarmDuration)
        #print(' '.join(codebdo))

    if(message.content == jsonconfig['prefix'] + 'help'):
        await message.channel.send('```markdown\r\n# !stream [yt url]\r\n(bot will join member in voice channel and play url) \r\n# !roll [xdx where x is integer]\r\n(roll specified dice(s))\r\n# !leave\r\n(bot will leave voice channel)' +  '\r\n```')

    if(message.content == jsonconfig['prefix'] + 'hi'):
        
        myhianswer = 'hi! im a Python bot (better than js bot!)😋'
        await message.channel.send('```diff\r\n- ' + myhianswer + '\r\n```')
        #print(message.autor)

    if(message.content == jsonconfig['prefix'] + 'seeu'):
        
        await message.channel.send('babye! :wave: ')
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if (voice != None):
            if voice.is_connected():
                await voice.disconnect()
        await client.close()

    if(message.content == jsonconfig['prefix'] + 'CheckBitRate'):
        print('in Check')


    if(message.content.startswith(jsonconfig['prefix'] + 'play')):
        print('in play')
        user = await client.fetch_user(message.author.id)
        print(user.name)
        url = message.content
        arg = re.split('\s+', url)
        print(arg)

        #await play(message, arg[1]) 
        await play(message) 

    #'https://www.youtube.com/watch?v=oS-acFo_omQ&t=37s'

    if(message.content.startswith(jsonconfig['prefix'] + 'stream')):
        print('in load')
        url = message.content
        arg = re.split('\s+', url)
        print(arg)
        await stream(message, arg[1])
    
    if(message.content.startswith(jsonconfig['prefix'] + 'load')):
        print('in load')
        url = message.content
        arg = re.split('\s+', url)
        print(arg)
        await load(message, arg[1])

    if(message.content.startswith(jsonconfig['prefix'] + 'roll')):
        #TODO test roll!
        arg = message.content
        arg = re.split('\s+', arg)

        score = 0
        if arg[1] != '':
           dicearg = re.split('d', arg[1]) 
           numdice = dicearg[0]
           dice = dicearg[1]
           for i in range(int(numdice)):           
            score = score + random.randint(1,int(dice))
        else:
           score = random.randint(1,100)

            
        #await message.channel.send(score)
        await message.channel.send('```markdown\r\n'+ '# ' + str(score) + '\r\nDetails:['+ numdice +'d' + dice + ' (' + str(score) + ')' + ']'+ '\r\n```')
    
    if(message.content == jsonconfig['prefix'] + 'leave'):
        print('in leave')
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        #if voice.is_connected():
        await voice.disconnect()
        #else:
        #    await message.send("The bot is not connected to a voice channel.")

    if(message.content == jsonconfig['prefix'] + 'TestMyRNG'):
        counter = 0
        for i in range(1000):
            score = random.randint(1,100)
            if(score > 30):
                counter = counter + 1
        await message.channel.send('1000d100 gives you: ' + str(counter) + ' scores >30 !')


async def load(ctx, url : str):
    channelName = ctx.channel.name
    print('in load', channelName)
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

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

    filename = ''
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            print(file)
            filename = file
            os.rename(file, "song.mp3")
    
    channel = discord.utils.get(ctx.guild.channels, name=channelName)
    

    sout = ':notes: file loaded: ' + filename
    await channel.send(sout)

    
 

async def play(ctx):
    print('in play', os.path)
    
    
    
    print('now play')
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='voc-dev')
    
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

    
async def stream(ctx, url):
        #"""Streams from a url (same as yt, but doesn't predownload)"""
        player = await YTDLSource.from_url(url, loop=None, stream=True)

        user = await client.fetch_user(ctx.author.id)
        print(user.name)
        print(user.id)
        print('***')
        voiceChannel = None

        #voiceChannel = member(user).voice.channel

        for guild in client.guilds:
            #print(guild.name)
            #print('###')
            for member in guild.members:  
                #print(member.id)
                #print('---') 
                if member.id == user.id:
                    #print('match!!!')
                    if member.voice != None:
                        voiceChannel = member.voice.channel

        await ctx.channel.send('*' + user.name + "* Thank you for sharing with us: _*"  + player.title + '*_\r\n'+ ":headphones: :musical_keyboard: :musical_note: :guitar: :notes: :drum: :headphones: :musical_keyboard: :musical_note: :guitar: :notes: :drum: ")

        #await ctx.channel.send(user.name + " Thank you for sharing with us: "  + player.title + " :headphones: :musical_keyboard: :musical_note: :guitar: :notes: :drum: ")


        if voiceChannel != None:

            #TODO: check if bot is already in voicechan and disconnect before
            for member in voiceChannel.members:
                if member.id == 942539082574204929:  #attention id du bot! à améliorer!!!
                    await voiceChannel.disconnect()

            await voiceChannel.connect()
        else:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='voc-dev')
            await voiceChannel.connect()

        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        #await ctx.send(f'Now playing: {player.title}')

#print('token: ' + jsonsecret['token'])

client.run(jsonsecret['token'])
#bot id: 942539082574204929

