import discord
import numpy as np
import scipy.misc
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random
import datetime

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)
global rolls
global charName
# a = np.random.randint(2, size=10)
# print(a)



@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    global generalChannel

    def get_channel(channels, channel_name): #  get channel ID for general
        for channel in client.get_all_channels():
            print(channel)
            if channel.name == channel_name:
                return channel
        return None
    generalChannel = get_channel(client.get_all_channels(), 'general')

    if datetime.datetime.today().weekday() == 2:
        await client.send_file(generalChannel, "imgs\gamenight.png")
        await client.send_message(generalChannel, 'It\'s game night baby!')


@client.event
async def on_message(message):
    global rolls
    global charName
    if message.content.startswith('!hit'):  # alias for !details
        charName = [message.author.display_name]
        lines = open('Hit_Descriptors').read().splitlines()
        myline = random.choice(lines)
        await client.send_message(message.channel, '{} {}'.format(charName[0], myline))

    if message.content.startswith('!roll '):
        rollCheck = message.content[6:]
        howMany, whatSize = rollCheck.split('d')
        if '+' in whatSize:
            whatSize, modifier = whatSize.split('+')
        elif '-' in whatSize:
            whatSize, modifier = whatSize.split('-')
            modifier = int(modifier)*-1
        else:
            modifier = 0
        rolls = np.random.randint(1, int(whatSize)+1, int(howMany))
        totalRoll = np.sum(rolls)+int(modifier)
        print(rolls)
        if int(modifier) == 0:
            if int(howMany) == 1:
                await client.send_message(message.channel, 'You rolled {}.'.format(rolls))
            else:
                await client.send_message(message.channel, 'You rolled {}, totalling {}.'.format(rolls, totalRoll))
        elif int(modifier) > 0:
            await client.send_message(message.channel, 'You rolled {}, totalling {} with your +{} modifier.'.format(rolls, totalRoll, modifier))
        else:
            await client.send_message(message.channel, 'You rolled {}, totalling {} with your {} modifier.'.format(rolls, totalRoll, modifier))

    if message.content.startswith('!init '):
        try:
            rolls
        except NameError:  # if rolls doesn't exist yet
            rollCheck = message.content[6:]
            if rollCheck == 'start':
                del rolls
                await client.send_message(message.channel, 'Ready to roll for initiative!')
                return
            numArgs = rollCheck.count(' ')+1
            if numArgs == 1:
                howMany, modifier = 1, rollCheck
                charName = [message.author.display_name]  # author.display_name
            elif numArgs == 3:
                howMany, modifier, charName = rollCheck.split(' ')
                charName = [charName]
                for x in range(0, int(howMany)-1):
                    charName.append(charName[0])
            else:
                await client.send_message(message.channel, 'Error: You must enter 1 or 3 inputs for initiative, see bot-talk channel.')
                return
            rolls = sorted(np.random.randint(1, 20+1, int(howMany))+int(modifier), reverse=True)
            charName = [charName for _, charName in sorted(zip(rolls, charName), reverse=True)]
            if numArgs == 1:
                await client.send_message(message.channel, '{}s initiative roll is {}.'.format(charName, rolls))
            else:
                bigPrint = "Your initiative rolls are: \r"
                for x in range(0, len(charName)):
                    bigPrint += '{} {}\r'.format(rolls[x], charName[x])
                await client.send_message(message.channel, bigPrint)
        else:  # rolls already exists, must append new rolls
            rollCheck = message.content[6:]
            if rollCheck == 'start':
                del rolls
                await client.send_message(message.channel, 'Ready to roll for initiative!')
                return
            numArgs = rollCheck.count(' ') + 1
            if numArgs == 1:
                howMany, modifier = 1, rollCheck
                charName.extend([message.author.display_name])  # author.display_name
            elif numArgs == 3:
                howMany, modifier, charNameAdd = rollCheck.split(' ')
                charNameAdd = [charNameAdd]
                for x in range(0, int(howMany)):
                    charName.append(charNameAdd[0])
            else:
                await client.send_message(message.channel,
                                          'Error: You must enter 1 or 3 inputs for initiative, see bot-talk channel.')
                return
            rollsAdd = np.random.randint(1, 20 + 1, int(howMany)) + int(modifier)
            rolls = np.append(rolls, rollsAdd)
            charName = [charName for _, charName in sorted(zip(rolls, charName), reverse=True)]
            rolls = sorted(rolls, reverse=True)
            bigPrint = "Your initiative rolls are: \r"
            for x in range(0, len(charName)):
                bigPrint += '{} {}\r'.format(rolls[x], charName[x])
            await client.send_message(message.channel, bigPrint)

    if message.content.startswith('!loot '):
        coins = {'CP': 0, 'SP': 0, 'EP': 0, 'GP': 0, 'PP': 0}
        rollCheck = message.content[6:]
        level, howMany = rollCheck.split(' ')
        for x in range(0, int(howMany)):
            roll = np.random.randint(1, 101, 1)
            if '/' in level:
                level = '0'
            if int(level) <= 4:
                if roll <= 30:
                    coins['CP'] += np.sum(np.random.randint(1,7,5))
                elif roll <= 60:
                    coins['SP'] += np.sum(np.random.randint(1,7,4))
                elif roll <= 70:
                    coins['EP'] += np.sum(np.random.randint(1,7,3))
                elif roll <= 95:
                    coins['GP'] += np.sum(np.random.randint(1,7,3))
                else:
                    coins['PP'] += np.sum(np.random.randint(1,7,1))
            elif int(level) <= 10:
                if roll <= 30:
                    coins['CP'] += np.sum(np.random.randint(1,7,4)) * 100
                    coins['EP'] += np.sum(np.random.randint(1,7,1)) * 10
                elif roll <= 60:
                    coins['SP'] += np.sum(np.random.randint(1,7,6)) * 10
                    coins['GP'] += np.sum(np.random.randint(1,7,2)) * 10
                elif roll <= 70:
                    coins['EP'] += np.sum(np.random.randint(1,7,3)) * 10
                    coins['GP'] += np.sum(np.random.randint(1,7,2)) * 10
                elif roll <= 95:
                    coins['GP'] += np.sum(np.random.randint(1,7,4)) * 10
                else:
                    coins['GP'] += np.sum(np.random.randint(1,7,2)) * 10
                    coins['PP'] += np.sum(np.random.randint(1,7,3))

        bigPrint = "BUM BA DUH BUUUH!: \r"
        if coins['CP'] > 0:
            bigPrint += '{} CP  '.format(coins['CP'])
        if coins['SP'] > 0:
            bigPrint += '{} SP  '.format(coins['SP'])
        if coins['EP'] > 0:
            bigPrint += '{} EP  '.format(coins['EP'])
        if coins['GP'] > 0:
            bigPrint += '{} GP  '.format(coins['GP'])
        if coins['PP'] > 0:
            bigPrint += '{} PP  '.format(coins['PP'])
        await client.send_file(message.channel, "imgs\coins.png")
        await client.send_message(message.channel, bigPrint)

    if message.content.startswith('!hoard '):
        coins = {'CP': 0, 'SP': 0, 'EP': 0, 'GP': 0, 'PP': 0}
        magicItems = {'A0': 'Roll 1d6 times on Magic Item Table A', 'B0': 'Roll 1d4 times on Magic Item Table B', \
                 'C0': 'Roll 1d4 times on Magic Item Table C', 'F0': 'Roll 1d4 times on Magic Item Table F', \
                 'G0': 'Roll once on Magic Item Table G'}
        rollCheck = message.content[7:]
        numArgs = rollCheck.count(' ') + 1
        if numArgs == 1:
            howMany = 1
            level = rollCheck
        else:
            level, howMany = rollCheck.split(' ')
        for x in range(0, int(howMany)):
            roll = np.random.randint(1, 101, 1)
            if '/' in level:
                level = '0'
            if int(level) <= 4:
                coins['CP'] += np.sum(np.random.randint(1, 7, 6)) * 100
                coins['SP'] += np.sum(np.random.randint(1, 7, 3)) * 100
                coins['GP'] += np.sum(np.random.randint(1, 7, 2)) * 10
                if roll <= 6:
                    continue  # just take up a line, nothing happens
                elif roll <= 16:
                    gemsArtText = '010'
                elif roll <= 26:
                    gemsArtText = '025'
                elif roll <= 36:
                    gemsArtText = '050'
                elif roll <= 44:
                    magicText = 'A0'
                    gemsArtText = '010'
                elif roll <= 52:
                    magicText = 'A0'
                    gemsArtText = '025'
                elif roll <= 60:
                    magicText = 'A0'
                    gemsArtText = '050'
                elif roll <= 65:
                    magicText = 'B0'
                    gemsArtText = '010'
                elif roll <= 70:
                    magicText = 'B0'
                    gemsArtText = '025'
                elif roll <= 75:
                    magicText = 'B0'
                    gemsArtText = '050'
                elif roll <= 78:
                    magicText = 'C0'
                    gemsArtText = '010'
                elif roll <= 80:
                    magicText = 'C0'
                    gemsArtText = '025'
                elif roll <= 85:
                    magicText = 'C0'
                    gemsArtText = '050'
                elif roll <= 92:
                    magicText = 'F0'
                    gemsArtText = '025'
                elif roll <= 97:
                    magicText = 'F0'
                    gemsArtText = '050'
                elif roll <= 99:
                    magicText = 'G0'
                    gemsArtText = '025'
                else:  # 100
                    magicText = 'G0'
                    gemsArtText = '050'

                #  Where to roll for gems
                try:
                    gemsArtText
                except NameError:  # if magicText doesn't exist yet
                    continue
                else:
                    if gemsArtText == '010':  # get starting line of respective list
                        gemsArtRoll = np.sum(np.random.randint(1, 7, 2))
                        num, i, gstart = '10 GP GEMSTONES', 0, 0  # i to count lines
                    elif gemsArtText == '025':
                        gemsArtRoll = np.sum(np.random.randint(1, 5, 2))
                        num, i, gstart = '25 GP ART OBJECTS', 0, 0  # i to count lines
                    elif gemsArtText == '050':
                        gemsArtRoll = np.sum(np.random.randint(1, 7, 2))
                        num, i, gstart = '50 GP GEMSTONES', 0, 0  # i to count lines

                    with open("Art_Gems_Tables") as search:
                        for line in search:
                            if gstart > 0 and line == '\n':
                                gend = i
                                break
                            i += 1
                            line = line.rstrip()  # remove '\n' at end of line
                            if num == line: gstart = i

                #  Where to roll for magic items
                try:
                    magicText
                except NameError:  # if magicText doesn't exist yet
                    continue
                else:
                    if magicText == 'A0':  # get starting line of respective list
                        magicRoll = np.random.randint(1, 7, 1)
                        num, i, mstart = 'MAGIC ITEM TABLE A', 0, 0  # i to count lines
                    elif magicText == 'B0':
                        magicRoll = np.random.randint(1, 5, 1)
                        num, i, mstart = 'MAGIC ITEM TABLE B', 0, 0  # i to count lines
                    elif magicText == 'C0':
                        magicRoll = np.random.randint(1, 5, 1)
                        num, i, mstart = 'MAGIC ITEM TABLE C', 0, 0  # i to count lines
                    elif magicText == 'F0':
                        magicRoll = np.random.randint(1, 5, 1)
                        num, i, mstart = 'MAGIC ITEM TABLE F', 0, 0  # i to count lines
                    elif magicText == 'G0':
                        magicRoll = np.random.randint(1, 2, 1)
                        num, i, mstart = 'MAGIC ITEM TABLE G', 0, 0  # i to count lines
                    with open("Magic_Item_Tables") as search:
                        for line in search:
                            if mstart > 0 and line == '\n':
                                mend = i
                                break
                            i += 1
                            line = line.rstrip()  # remove '\n' at end of line
                            if num == line: mstart = i

            elif int(level) <= 10:
                if roll <= 30:
                    coins['CP'] += np.sum(np.random.randint(1,7,4)) * 100
                    coins['EP'] += np.sum(np.random.randint(1,7,1)) * 10
                elif roll <= 60:
                    coins['SP'] += np.sum(np.random.randint(1,7,6)) * 10
                    coins['GP'] += np.sum(np.random.randint(1,7,2)) * 10
                elif roll <= 70:
                    coins['EP'] += np.sum(np.random.randint(1,7,3)) * 10
                    coins['GP'] += np.sum(np.random.randint(1,7,2)) * 10
                elif roll <= 95:
                    coins['GP'] += np.sum(np.random.randint(1,7,4)) * 10
                else:
                    coins['GP'] += np.sum(np.random.randint(1,7,2)) * 10
                    coins['PP'] += np.sum(np.random.randint(1,7,3))

            #  Roll for gems/art
            try:
                gemsArtText
            except NameError:  # if magicText doesn't exist yet
                continue
            else:
                f = open('Art_Gems_Tables', 'r')
                lines = f.readlines()[int(gstart+1):int(gend)]
                f.close()
                dieRange, gemsArt, gemsArtn = [0]*len(lines), [0]*len(lines), np.zeros(len(lines), int)
                if gemsArtText == '010' or gemsArtText == '050': maxd = 12
                elif gemsArtText == '025': maxd = 10
                for x in range(0, len(lines)):
                    lines[x] = lines[x].rstrip()
                    dieRange[x], gemsArt[x] = lines[x].split(' ', 1)
                for x in range(0, int(magicRoll)):
                    dx = np.random.randint(1, maxd+1, 1)
                    for n in range(0, len(dieRange)):
                        if '-' in dieRange[n]:
                            first, second = dieRange[n].split('-')
                            if dx >= int(first) and dx <= int(second):
                                gemsArtn[n] +=1
                        elif dx == int(dieRange[n]):
                            gemsArtn[n] +=1

            #  Roll for magic items
            try:
                magicText
            except NameError:  # if magicText doesn't exist yet
                continue
            else:
                f = open('Magic_Item_Tables', 'r')
                lines = f.readlines()[int(mstart + 1):int(mend)]
                f.close()
                dieRange, magicItem, magicItemn = [0] * len(lines), [0] * len(lines), np.zeros(len(lines),
                                                                                               int)
                for x in range(0, len(lines)):
                    lines[x] = lines[x].rstrip()
                    dieRange[x], magicItem[x] = lines[x].split(' ', 1)
                for x in range(0, int(magicRoll)):
                    d100 = np.random.randint(1, 101, 1)
                    for n in range(0, len(dieRange)):
                        if '-' in dieRange[n]:
                            first, second = dieRange[n].split('-')
                            if d100 >= int(first) and d100 <= int(second):
                                magicItemn[n] += 1
                        elif d100 == int(dieRange[n]):
                            magicItemn[n] += 1

        bigPrint = "BUM BA DUH BUUUH!: \r"
        if coins['CP'] > 0:
            bigPrint += '{} CP  '.format(coins['CP'])
        if coins['SP'] > 0:
            bigPrint += '{} SP  '.format(coins['SP'])
        if coins['EP'] > 0:
            bigPrint += '{} EP  '.format(coins['EP'])
        if coins['GP'] > 0:
            bigPrint += '{} GP  '.format(coins['GP'])
        if coins['PP'] > 0:
            bigPrint += '{} PP  '.format(coins['PP'])

        try:
            gemsArtText
        except NameError:  # if gemsArtText doesn't exist yet
            bigPrint += '\r No art or jewels this time, friend.'
        else:
            if np.sum(gemsArtn) > 0:
                bigPrint += '\r'
                for x in range(0, len(gemsArt)):
                    if gemsArtn[x] > 0:
                        bigPrint += '{} {}(s)  '.format(gemsArtn[x], gemsArt[x])
            gemsArtMultiplier = int(gemsArtText[1:])
            bigPrint += '= {} GP'.format(np.sum(gemsArtn) * gemsArtMultiplier)

        try:
            magicText
        except NameError:  # if magicText doesn't exist yet
            bigPrint += '\r Sorry, no magic items this time :('
        else:
            bigPrint += '\r*And...!*'
            if np.sum(magicItemn) > 0:
                bigPrint += '\r'
                for x in range(0, len(magicItem)):
                    if magicItemn[x] > 0:
                        bigPrint += '{} {}(s)  '.format(magicItemn[x], magicItem[x])
        await client.send_file(message.channel, "imgs\hoard.png")
        await client.send_message(message.channel, bigPrint)

    if message.content.startswith('!batboys'):
        await client.send_file(message.channel, "imgs\Batboys.png")

    # create a random dungeon image, save on desktop, print
    # if message.content.startswith('!test'):
    #     w, h = 600, 800
    #     sq = 15  # width of each checker-square
    #     mypix = np.zeros((w, h, 3), dtype=np.uint8)
    #     # Make a checkerboard
    #     mypix
    #     scipy.misc.imsave('E:\Pictures-H\outfile.jpg', mypix)
    #     # scipy.misc.toimage(image_array, cmin=0.0, cmax=...).save('outfile.jpg')
    #
    #     # if message.content.startswith('$greet'):
    # #     await client.send_message(message.channel, 'Say hello')
    # #     msg = await client.wait_for_message(author=message.author, content='hello')
    # #     await client.send_message(message.channel, 'Hello.')

client.run("MzY2NDIxNDQ2MjA3MjA5NDgy.DMFxZA.ncA3g-A5ozoNrw2n6Zoo9FuMhDU")