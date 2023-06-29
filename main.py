import discord
from discord.ext import commands
import json
import math
import numexpr

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents=intents)

stdata = {}

with open('db.json', 'r') as jfile:
        stdata = json.load(jfile)

def savedata(d):
    with open('db.json', 'w') as jfile:
        json.dump(d, jfile)

def dist(c1, c2):
    return math.dist(c1, c2)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
    print('file loaded')

@bot.command(name='nearest')
async def nearest(ctx, arg1, arg2, nether: str=None):
    if nether == 'n' or nether == 'nether':
        arg1, arg2 = 8*arg1, 8*arg2
    

    mindist = 1000000
    co = []
    for s in stdata.keys():
        
        if stdata[s] == 0:
            if mindist > dist([int(arg1), int(arg2)], list(map(int, s.split()))):
                co = s
                mindist = dist([int(arg1), int(arg2)], list(map(int, s.split())))
    
    if co == []:
        await ctx.send(f'None found')
    else:
        await ctx.send(f'Closest stronghold found:\nOverworld:  {co}\nNether:  {int(co.split()[0])//8} {int(co.split()[1])//8}')

@bot.command(name='math')
async def qmath(ctx, arg):
    print(arg)
    await ctx.send(numexpr.evaluate(arg).item())

@bot.command(name='cc')
async def coordconverter(ctx, *args):
    await ctx.send('To nether: '+' '.join([str(int(arg)//8) for arg in args])+'\nTo overworld: '+' '.join([str(int(arg)*8) for arg in args]))

@bot.command(name='broken')
async def broken(ctx, *args):
    args = list(args)
    if 'X:' in args:
        args.remove('X:')
    if 'Z:' in args:
        args.remove('Z:')
    realcoords = ' '.join(args).replace(',', '')
    if stdata[realcoords] == 1:
        await ctx.send("stronghold already gone")
    else:
        stdata[realcoords] = 1
        savedata(stdata)
        channel = bot.get_channel(1123984521579204648)
        num = list(stdata.values()).count(1)
        
        ##nearest
        arg1, arg2 = realcoords.split()
        mindist = 1000000
        co = [] 
        for s in stdata.keys():
            
            if stdata[s] == 0:
                if mindist > dist([int(arg1), int(arg2)], list(map(int, s.split()))):
                    co = s
                    mindist = dist([int(arg1), int(arg2)], list(map(int, s.split())))
        
        if co == []:
            await ctx.send(f'Congratulations\nNone found')
        else:
            await ctx.send(f'Congratulations!\nClosest stronghold found:\nOverworld:  {co}\nNether:  {int(co.split()[0])//8} {int(co.split()[1])//8}')
        await channel.send(f'{num}. X: {f"{int(realcoords.split()[0]):,}"} Z: {f"{int(realcoords.split()[1]):,}"}')


bot.run(open('TOKEN').readline())