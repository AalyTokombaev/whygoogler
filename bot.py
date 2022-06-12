import time
import sys
import random

try:
    import discord
    from discord.ext.commands import Bot
    from googlesearch import search 
    import re
except ImportError:
    print("missing dependensies\n please run: \n \t  pip install -r requirements.txt")

start_time = time.time()


bot = Bot(command_prefix='-')

whilelist =  [844698260564213780, 836982970811416656, 317726369284882433]
debug_mode = False
admin_ids = [138001563158446081, 376500050320293888, 349829722651361282]

@bot.event
async def on_ready():
    print(f'Lodded in as {bot.user.name}')



words = [
        'how',
        'hvordan', 
        'hvem', 
        'what', 
        'hva', 
        'why', 
        'hvorfor', 
        'is', 
        'er', 
        'are',
        'does',
        'gjør'
        ]

def searcher(msg):
    global words
    # cursed fstring regex
    regex = fr'\b{("({})|"*len(words))[:-1].format(*words)}\b'
    # "\b" + ("({})|"*len(words))[:-1].format(*words)  + "\b"
    # first it creates a string "({})|({})| ... ({})|" with "({})| for each word
    # drop the last "|" with [:-1], giving "({})|({})| ... ({})"
    # format words into each "{}"
    # then format this into r"\b{}\b"
    # resulting regex is like so:
    # "\\b(how)|(hvordan)|(why)|(hvofor)|...(does)|(gjør)\\b"
    result = re.search(regex, msg)
    if result:
        index = result.span()[0]
        two = msg[index:index + 2]
        three = msg[index:index + 3]
        if(two == 'er' or two == 'is' or three == 'are') and not ('?' in msg[index:]):
            return 

        search_query = msg[index:]

        if len(search_query.split()) == 1:
            return

        search_result = search(search_query, num_results=1)

        if search_result:
            result = search_result.pop(0)
        else:
            result = "Not found"

    return result





@bot.listen()
async def on_message(message):

    if message.author.bot:
        return

    # oof violin trigger
    msg = message.content.lower()
    if re.search(r'\b[oO]{2,}[fF]\b', msg) and (random.randint(1,5) == 1 or debug_mode):
        await message.channel.send('https://media.discordapp.net/attachments/836982970811416656/850039035044823080/oof.png?width=410&height=382')
        await message.channel.send('big **OOF**')
        """
        # needs send image permission
        with open('./oof.png', 'rb') as img:
            image = discord.File(img)
            await message.channel.send(file=image)
            await message.channel.send('big **OOF**')
        """
    
    # based and redpilled trigger
    based = r'\b[Bb][Aa][Ss][Ee][Dd]\b'
    if re.search(based, msg) and (random.randint(1,3) == 1 or debug_mode):
        await message.channel.send('and redpilled :sunglasses:')
    
    pog_regex = r'\b([pP][oO][gG])\b'
    if re.search(pog_regex, msg) and (random.randint(1,4) == 1 or debug_mode):
        await message.channel.send('pogdaddy :sweat_drops:')

    global whitelist
    if message.channel.id in whilelist:
        srch = searcher(msg)
        if srch:
            await message.channel.send(srch)


# commands lages sånn:
@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.command()
async def debug(ctx):
    if  not (ctx.message.author.id in admin_ids):
        await ctx.send(":robot::speech_balloon: **Beep-Boop** `This command is for bot developers only.`")
        return 
    global debug_mode 
    debug_mode = not debug_mode 
    await ctx.send(':robot::speech_balloon: **Beep-Boop** `Debug mode: {}`'.format({True : 'ON', False : 'OFF'}[debug_mode]))


@bot.command()
async def follow(ctx):
    await ctx.send('Awaiting message')
    def check(m):
        return 'follow' in m.content

    msg = await bot.wait_for('message', check=check)
    await ctx.send('received ' + msg.content)


@bot.command()
async def uptime(ctx):
    global start_time
    now_time = time.time()
    res = round(now_time - start_time)
    timestring = time.strftime("%H:%M:%S", time.gmtime(res))
    await ctx.send(timestring)


@bot.command()
async def award(ctx, person):
    """not done"""
    await ctx.send(f"{person} has been awarded a shoutout by me, the bot.")

@bot.command()
async def add_word(ctx, word):
    if  not (ctx.message.author.id in admin_ids):
        await ctx.send(':robot: :speech_balloon: This command is for developers only.')
        return
    global words
    words.append(str(word).lower())
    await ctx.send(f":robot: :speech_balloon:  {word} added temporarily.")


bot.run('bot-api-token-here')
