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

    if datetime.datetime.today().weekday() == 3:
        await client.send_file(generalChannel, "E:\Pictures-H\gamenight.png")
        await client.send_message(generalChannel, 'It\'s game night baby!)


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
        await client.send_file(message.channel, "E:\Pictures-H\coins.png")
        await client.send_message(message.channel, bigPrint)

    if message.content.startswith('!hoard '):
        coins = {'CP': 0, 'SP': 0, 'EP': 0, 'GP': 0, 'PP': 0}
        gems10 = ['Azurite', 'Banded Agate', 'Blue quartz', 'Eye agate', 'Hematite', 'Lapis lazuli', \
                  'Malachite', 'Moss agate', 'Obsidian', 'Rhodochrosite', 'Tiger eye', 'Turquoise']
        gems10n = np.zeros(len(gems10), int)
        gems50 = ['Bloodstone', 'Carnelian', 'Chalcedony', 'Chrysprase', 'Citrine', 'Jasper', \
                  'Moonstone', 'Onyx', 'Quartz', 'Sardonyx', 'Star rose quartz', 'Zircon']
        gems50n = np.zeros(len(gems50), int)
        art25 = ['Silver ewer', 'Carved bone statuette', 'Small gold bracelet', 'Cloth-of-gold vestments', \
                 'Black velvet mask stitched with silver thread', 'Copper chalice with silver filigree', \
                 'Pair of engraved bone dice', 'Small mirror set in painted wooden frame', \
                 'Embroidered silk handkerchief', 'Gold locket with a painted portrait inside']
        art25n = np.zeros(len(art25), int)
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
                    gems10n[0] = 0  # just take up a line, nothing happens
                elif roll <= 16:
                    items = np.sum(np.random.randint(1,7,2))
                    for x in range(0, items):
                        gems10n[np.random.randint(0, 12, 1)] += 1
                elif roll <= 26:
                    items = np.sum(np.random.randint(1, 5, 2))
                    for x in range(0, items):
                        art25n[np.random.randint(0, 10, 1)] += 1
                elif roll <= 36:
                    items = np.sum(np.random.randint(1, 7, 2))
                    for x in range(0, items):
                        gems50n[np.random.randint(0, 12, 1)] += 1
                elif roll <= 44:
                    magicText = 'A0'
                    items = np.sum(np.random.randint(1, 7, 2))
                    for x in range(0, items):
                        gems10n[np.random.randint(0, 12, 1)] += 1
                elif roll <= 52:
                    magicText = 'A0'
                    items = np.sum(np.random.randint(1, 5, 2))
                    for x in range(0, items):
                        art25n[np.random.randint(0, 10, 1)] += 1
                elif roll <= 60:
                    magicText = 'A0'
                    items = np.sum(np.random.randint(1, 7, 2))
                    for x in range(0, items):
                        gems50n[np.random.randint(0, 12, 1)] += 1
                elif roll <= 65:
                    magicText = 'B0'
                    items = np.sum(np.random.randint(1, 7, 2))
                    for x in range(0, items):
                        gems10n[np.random.randint(0, 12, 1)] += 1
                elif roll <= 70:
                    magicText = 'B0'
                    items = np.sum(np.random.randint(1, 5, 2))
                    for x in range(0, items):
                        art25n[np.random.randint(0, 10, 1)] += 1
                elif roll <= 75:
                    magicText = 'B0'
                    items = np.sum(np.random.randint(1, 7, 2))
                    for x in range(0, items):
                        gems50n[np.random.randint(0, 12, 1)] += 1
                elif roll <= 78:
                    magicText = 'C0'
                    items = np.sum(np.random.randint(1, 7, 2))
                    for x in range(0, items):
                        gems10n[np.random.randint(0, 12, 1)] += 1
                elif roll <= 80:
                    magicText = 'C0'
                    items = np.sum(np.random.randint(1, 5, 2))
                    for x in range(0, items):
                        art25n[np.random.randint(0, 10, 1)] += 1
                elif roll <= 85:
                    magicText = 'C0'
                    items = np.sum(np.random.randint(1, 7, 2))
                    for x in range(0, items):
                        gems50n[np.random.randint(0, 12, 1)] += 1
                elif roll <= 92:
                    magicText = 'F0'
                    items = np.sum(np.random.randint(1, 5, 2))
                    for x in range(0, items):
                        art25n[np.random.randint(0, 10, 1)] += 1
                elif roll <= 97:
                    magicText = 'F0'
                    items = np.sum(np.random.randint(1, 7, 2))
                    for x in range(0, items):
                        gems50n[np.random.randint(0, 12, 1)] += 1
                elif roll <= 99:
                    magicText = 'G0'
                    items = np.sum(np.random.randint(1, 5, 2))
                    for x in range(0, items):
                        art25n[np.random.randint(0, 10, 1)] += 1
                else:  # 100
                    magicText = 'G0'
                    items = np.sum(np.random.randint(1, 7, 2))
                    for x in range(0, items):
                        gems50n[np.random.randint(0, 12, 1)] += 1

                #  Roll for magic items
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

            #  Roll for magic items
            try:
                magicText
            except NameError:  # if magicText doesn't exist yet
                continue
            else:
                f = open('Magic_Item_Tables', 'r')
                lines = f.readlines()[int(mstart+1):int(mend)]
                f.close()
                dieRange, magicItem, magicItemn = [0]*len(lines), [0]*len(lines), np.zeros(len(lines), int)
                for x in range(0, len(lines)):
                    lines[x] = lines[x].rstrip()
                    dieRange[x], magicItem[x] = lines[x].split(' ', 1)
                for x in range(0, int(magicRoll)):
                    d100 = np.random.randint(1, 101, 1)
                    for n in range(0, len(dieRange)):
                        if '-' in dieRange[n]:
                            first, second = dieRange[n].split('-')
                            if d100 >= int(first) and d100 <= int(second):
                                magicItemn[n] +=1
                        elif d100 == int(dieRange[n]):
                            magicItemn[n] +=1

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
        if np.sum(gems10n) > 0:
            bigPrint += '\r'
            for x in range(0,len(gems10)):
                if gems10n[x] > 0:
                    bigPrint += '{} {}(s)  '.format(gems10n[x], gems10[x])
            bigPrint += '= {} GP'.format(np.sum(gems10n)*10)
        if np.sum(art25n) > 0:
            bigPrint += '\r'
            for x in range(0, len(art25)):
                if art25n[x] > 0:
                    bigPrint += '{} {}(s)  '.format(art25n[x], art25[x])
            bigPrint += '= {} GP'.format(np.sum(art25n)*25)
        if np.sum(gems50n) > 0:
            bigPrint += '\r'
            for x in range(0, len(gems50)):
                if gems50n[x] > 0:
                    bigPrint += '{} {}(s)  '.format(gems50n[x], gems50[x])
            bigPrint += '= {} GP'.format(np.sum(gems50n)*50)
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
        await client.send_file(message.channel, "E:\Pictures-H\hoard.png")
        await client.send_message(message.channel, bigPrint)

    if message.content.startswith('!batboys'):
        await client.send_file(message.channel, "E:\Pictures-H\Batboys.png")

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

client.run("MzY2NDIxNDQ2MjA3MjA5NDgy.DL1_HQ.DRoaX95obL9snahUqQGHQ12PupA")