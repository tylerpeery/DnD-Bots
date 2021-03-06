import discord
import numpy as np
import scipy.misc
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random
import datetime
import time
import matplotlib.pyplot as plt; plt.rcdefaults()

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)
with open("bot_id.txt") as search:
    for line in search:
        bot_ID = line

global inits
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

    # # Date check for announcing game night
    # if datetime.datetime.today().weekday() == 2:
    #     img_call = np.random.randint(1, 7, 1)
    #     filename = "imgs\gamenight" + str(img_call[0]) + ".png"
    #     await client.send_file(generalChannel, filename)
    #     await client.send_message(generalChannel, 'It\'s game night, baby!')


@client.event
async def on_message(message):
    global inits
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
        who = [message.author.display_name]
        print(rolls)
        await client.delete_message(message) # DELETE USER INPUT
        if int(modifier) >= 0:
            await client.send_message(message.channel, '{} rolled {}d{}+{} and got {}, totalling **{}**'.format(
                who[0], howMany, whatSize, modifier, ', '.join(map(str, rolls)), totalRoll))
        else:
            await client.send_message(message.channel, '{} rolled {}d{}{} and got {}, totalling **{}**'.format(
                who[0], howMany, whatSize, modifier, ', '.join(map(str, rolls)), totalRoll))

    if message.content.startswith('!skill '):  # !skill modifier skillname, output that w/ player name
        info = message.content[7:]
        numArgs = info.count(' ') + 1
        if numArgs == 1:
            modifier, skill = 0, info
        else:
            a = info.split(' ')
            skill = ''
            for x in range(0, len(a)):
                try:
                    int(a[x])
                    modifier = a[x]
                except ValueError:
                    skill = skill + a[x] + ' '
            try:
                modifier
            except NameError:
                modifier = 0
            skill = skill[:-1]
        roll = np.random.randint(1, 20+1, 1)
        totalRoll = roll+int(modifier)
        who = [message.author.display_name]
        await client.delete_message(message) # DELETE PREVIOUS INPUT
        if int(modifier) >= 0:
            await client.send_message(message.channel, '{} rolled {}, totalling **{} {}** with a +{} modifier'.format(
                who[0], roll[0], totalRoll[0], skill, modifier))
        else:
            await client.send_message(message.channel, '{} rolled {}, totalling **{} {}** with a {} modifier'.format(
                who[0], roll[0], totalRoll[0], skill, modifier))

    # modifier = 5
    # allRolls = np.zeros((19,), dtype=np.int)
    # rollRange = np.arange(2 + int(modifier), 21 + int(modifier), dtype=np.int)
    # for x in range(0, 100000):
    #     roll = np.sum(np.random.randint(0, 10, 2)) + int(modifier)
    #     allRolls[roll - int(modifier)] += 1
    #     # plt.pause(0.0001)
    # plt.bar(rollRange, allRolls, align='center', alpha=0.5)
    # plt.xticks(rollRange)
    # plt.ylabel('Total Rolls')
    # plt.title('Ross Chart')
    # plt.draw()
    # plt.show()

    if message.content.startswith('!char'):
        attributes = np.zeros(6, int)
        for x in range(0, 6):
            rolls = np.random.randint(1, 7, 4)
            rolls = sorted(rolls, reverse = True)
            attributes[x] = sum(sorted(rolls[0:3]))
        await client.send_message(message.channel, 'Your stat rolls are: {}.'.format(attributes))


    if message.content.startswith('!init '):
        try:
            inits
        except NameError:  # if inits doesn't exist yet
            rollCheck = message.content[6:]
            if rollCheck == 'start':
                await client.send_message(message.channel, 'Ready to roll for initiative!')
                return
            numArgs = rollCheck.count(' ')+1
            if numArgs == 1:
                howMany, modifier = 1, rollCheck
                charName = [message.author.display_name]  # author.display_name
                inits = sorted(np.random.randint(1, 20 + 1, int(howMany)) + int(modifier), reverse=True)
                charName = [charName for _, charName in sorted(zip(inits, charName), reverse=True)]
            elif numArgs == 3:
                howMany, modifier, charName = rollCheck.split(' ')
                charName = [charName]
                if howMany == 'set':
                    inits = np.random.randint(int(modifier), int(modifier) + 1, 1)  # !init set roll name
                else:
                    for x in range(0, int(howMany)-1):
                        charName.append(charName[0])
                    inits = sorted(np.random.randint(1, 20 + 1, int(howMany)) + int(modifier), reverse=True)
                charName = [charName for _, charName in sorted(zip(inits, charName), reverse=True)]
            else:
                await client.send_message(message.channel, 'Error: You must enter 1 or 3 inputs for initiative, see bot-talk channel.')
                return
            if numArgs == 1 or howMany == 'set':
                await client.send_message(message.channel, '{}s initiative roll is {}.'.format(charName, inits))
            else:
                bigPrint = "Your initiative rolls are: \r"
                for x in range(0, len(charName)):
                    bigPrint += '{} {}\r'.format(inits[x], charName[x])
                await client.send_message(message.channel, bigPrint)
        else:  # inits already exists, must append new inits
            rollCheck = message.content[6:]
            if rollCheck == 'start':
                del inits
                await client.send_message(message.channel, 'Ready to roll for initiative!')
                return
            numArgs = rollCheck.count(' ') + 1
            if numArgs == 1:
                howMany, modifier = 1, rollCheck
                charName.extend([message.author.display_name])  # author.display_name
                initsAdd = np.random.randint(1, 20 + 1, int(howMany)) + int(modifier)
            elif numArgs == 3:
                howMany, modifier, charNameAdd = rollCheck.split(' ')
                charNameAdd = [charNameAdd]
                if howMany == 'set':
                    initsAdd = np.random.randint(int(modifier), int(modifier)+1, 1)  # because order is !init set roll name
                    charName.append(charNameAdd[0])
                else:
                    for x in range(0, int(howMany)):
                        charName.append(charNameAdd[0])
                    initsAdd = np.random.randint(1, 20 + 1, int(howMany)) + int(modifier)
            else:
                await client.send_message(message.channel,
                                          'Error: You must enter 1 or 3 inputs for initiative, see bot-talk channel.')
                return
            inits = np.append(inits, initsAdd)
            charName = [charName for _, charName in sorted(zip(inits, charName), reverse=True)]
            inits = sorted(inits, reverse=True)
            bigPrint = "Your initiative rolls are: \r"
            for x in range(0, len(charName)):
                bigPrint += '{} {}\r'.format(inits[x], charName[x])
            await client.send_message(message.channel, bigPrint)

    if message.content.startswith('!loot '):
        coins = {'CP': 0, 'SP': 0, 'EP': 0, 'GP': 0, 'PP': 0}
        rollCheck = message.content[6:]
        numArgs = rollCheck.count(' ') + 1
        if numArgs == 1:
            howMany = 1
            level = rollCheck
        else:
            level, howMany = rollCheck.split(' ')
        for x in range(0, int(howMany)):
            roll = np.random.randint(1, 101, 1)
            print(roll)
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
        rollCheck = message.content[7:]
        numArgs = rollCheck.count(' ') + 1
        if numArgs == 1:
            howMany = 1
            level = rollCheck
        else:
            level, howMany = rollCheck.split(' ')
        for x in range(0, int(howMany)):
            roll = np.random.randint(1, 101, 1)
            print(roll)
            if '/' in level:
                level = '0'
            if int(level) <= 4:
                coins['CP'] += np.sum(np.random.randint(1, 7, 6)) * 100
                coins['SP'] += np.sum(np.random.randint(1, 7, 3)) * 100
                coins['GP'] += np.sum(np.random.randint(1, 7, 2)) * 10
                if roll <= 6:
                    print("nothing")  # just take up a line, nothing happens
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

            elif int(level) <= 10:
                coins['CP'] += np.sum(np.random.randint(1, 7, 2)) * 100
                coins['SP'] += np.sum(np.random.randint(1, 7, 2)) * 1000
                coins['GP'] += np.sum(np.random.randint(1, 7, 6)) * 100
                coins['PP'] += np.sum(np.random.randint(1, 7, 3)) * 10
                if roll <= 4:
                    print("nothing")  # just take up a line, nothing happens
                elif roll <= 10:
                    gemsArtText = '525'
                elif roll <= 16:
                    gemsArtText = '550'
                elif roll <= 22:
                    gemsArtText = '5100'
                elif roll <= 28:
                    gemsArtText = '5250'
                elif roll <= 32:
                    magicText = 'A5'
                    gemsArtText = '525'
                elif roll <= 36:
                    magicText = 'A5'
                    gemsArtText = '550'
                elif roll <= 40:
                    magicText = 'A5'
                    gemsArtText = '5100'
                elif roll <= 44:
                    magicText = 'A5'
                    gemsArtText = '5250'
                elif roll <= 49:
                    magicText = 'B5'
                    gemsArtText = '525'
                elif roll <= 54:
                    magicText = 'B5'
                    gemsArtText = '550'
                elif roll <= 59:
                    magicText = 'B5'
                    gemsArtText = '5100'
                elif roll <= 63:
                    magicText = 'B5'
                    gemsArtText = '5250'
                elif roll <= 66:
                    magicText = 'C5'
                    gemsArtText = '525'
                elif roll <= 69:
                    magicText = 'C5'
                    gemsArtText = '550'
                elif roll <= 72:
                    magicText = 'C5'
                    gemsArtText = '5100'
                elif roll <= 74:
                    magicText = 'C5'
                    gemsArtText = '5250'
                elif roll <= 76:
                    magicText = 'D5'
                    gemsArtText = '525'
                elif roll <= 78:
                    magicText = 'D5'
                    gemsArtText = '550'
                elif roll <= 79:
                    magicText = 'D5'
                    gemsArtText = '5100'
                elif roll <= 80:
                    magicText = 'D5'
                    gemsArtText = '5250'
                elif roll <= 84:
                    magicText = 'F5'
                    gemsArtText = '525'
                elif roll <= 88:
                    magicText = 'F5'
                    gemsArtText = '550'
                elif roll <= 91:
                    magicText = 'F5'
                    gemsArtText = '5100'
                elif roll <= 94:
                    magicText = 'F5'
                    gemsArtText = '5250'
                elif roll <= 96:
                    magicText = 'G5'
                    gemsArtText = '5100'
                elif roll <= 98:
                    magicText = 'G5'
                    gemsArtText = '5250'
                elif roll <= 99:
                    magicText = 'H5'
                    gemsArtText = '5100'
                else:  # 100
                    magicText = 'H5'
                    gemsArtText = '5250'

            elif int(level) <= 16:
                coins['GP'] += np.sum(np.random.randint(1, 7, 4)) * 1000
                coins['PP'] += np.sum(np.random.randint(1, 7, 5)) * 100
                if roll <= 3:
                    print("nothing")  # just take up a line, nothing happens
                elif roll <= 6:
                    gemsArtText = '11250'
                elif roll <= 9:
                    gemsArtText = '11750'
                elif roll <= 12:
                    gemsArtText = '11500'
                elif roll <= 15:
                    gemsArtText = '111000'
                elif roll <= 19:
                    magicText = 'AB11'
                    gemsArtText = '11250'
                elif roll <= 23:
                    magicText = 'AB11'
                    gemsArtText = '11750'
                elif roll <= 26:
                    magicText = 'AB11'
                    gemsArtText = '11500'
                elif roll <= 29:
                    magicText = 'AB11'
                    gemsArtText = '111000'
                elif roll <= 35:
                    magicText = 'C11'
                    gemsArtText = '11250'
                elif roll <= 40:
                    magicText = 'C11'
                    gemsArtText = '11750'
                elif roll <= 45:
                    magicText = 'C11'
                    gemsArtText = '11500'
                elif roll <= 50:
                    magicText = 'C11'
                    gemsArtText = '111000'
                elif roll <= 54:
                    magicText = 'D11'
                    gemsArtText = '11250'
                elif roll <= 58:
                    magicText = 'D11'
                    gemsArtText = '11750'
                elif roll <= 62:
                    magicText = 'D11'
                    gemsArtText = '11500'
                elif roll <= 66:
                    magicText = 'D11'
                    gemsArtText = '111000'
                elif roll <= 68:
                    magicText = 'E11'
                    gemsArtText = '11250'
                elif roll <= 70:
                    magicText = 'E11'
                    gemsArtText = '11750'
                elif roll <= 72:
                    magicText = 'E11'
                    gemsArtText = '11500'
                elif roll <= 74:
                    magicText = 'E11'
                    gemsArtText = '111000'
                elif roll <= 76:
                    magicText = 'FG11'
                    gemsArtText = '11250'
                elif roll <= 78:
                    magicText = 'FG11'
                    gemsArtText = '11750'
                elif roll <= 80:
                    magicText = 'FG11'
                    gemsArtText = '11500'
                elif roll <= 82:
                    magicText = 'FG11'
                    gemsArtText = '111000'
                elif roll <= 85:
                    magicText = 'H11'
                    gemsArtText = '11250'
                elif roll <= 88:
                    magicText = 'H11'
                    gemsArtText = '11750'
                elif roll <= 90:
                    magicText = 'H11'
                    gemsArtText = '11500'
                elif roll <= 92:
                    magicText = 'H11'
                    gemsArtText = '111000'
                elif roll <= 94:
                    magicText = 'I11'
                    gemsArtText = '11250'
                elif roll <= 96:
                    magicText = 'I11'
                    gemsArtText = '11750'
                elif roll <= 98:
                    magicText = 'I11'
                    gemsArtText = '11500'
                else:  # 99-100
                    magicText = 'I11'
                    gemsArtText = '111000'

        #  Where to roll for gems
        try:
            gemsArtText
        except NameError:  # if magicText doesn't exist yet
            print("nothing")
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
            elif gemsArtText == '525':
                gemsArtRoll = np.sum(np.random.randint(1, 5, 2))
                num, i, gstart = '25 GP ART OBJECTS', 0, 0  # i to count lines
            elif gemsArtText == '550':
                gemsArtRoll = np.sum(np.random.randint(1, 7, 3))
                num, i, gstart = '50 GP GEMSTONES', 0, 0  # i to count lines
            elif gemsArtText == '5100':
                gemsArtRoll = np.sum(np.random.randint(1, 7, 3))
                num, i, gstart = '100 GP GEMSTONES', 0, 0  # i to count lines
            elif gemsArtText == '5250':
                gemsArtRoll = np.sum(np.random.randint(1, 5, 2))
                num, i, gstart = '250 GP ART OBJECTS', 0, 0  # i to count lines
            elif gemsArtText == '11250':
                gemsArtRoll = np.sum(np.random.randint(1, 5, 2))
                num, i, gstart = '250 GP ART OBJECTS', 0, 0  # i to count lines
            elif gemsArtText == '11750':
                gemsArtRoll = np.sum(np.random.randint(1, 5, 2))
                num, i, gstart = '750 GP ART OBJECTS', 0, 0  # i to count lines
            elif gemsArtText == '11500':
                gemsArtRoll = np.sum(np.random.randint(1, 7, 3))
                num, i, gstart = '500 GP GEMSTONES', 0, 0  # i to count lines
            elif gemsArtText == '111000':
                gemsArtRoll = np.sum(np.random.randint(1, 7, 3))
                num, i, gstart = '1,000 GP GEMSTONES', 0, 0  # i to count lines

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
            print("nothing")
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
            elif magicText == 'A5':
                magicRoll = np.random.randint(1, 7, 1)
                num, i, mstart = 'MAGIC ITEM TABLE A', 0, 0  # i to count lines
            elif magicText == 'B5':
                magicRoll = np.random.randint(1, 5, 1)
                num, i, mstart = 'MAGIC ITEM TABLE B', 0, 0  # i to count lines
            elif magicText == 'C5':
                magicRoll = np.random.randint(1, 5, 1)
                num, i, mstart = 'MAGIC ITEM TABLE C', 0, 0  # i to count lines
            elif magicText == 'D5':
                magicRoll = np.random.randint(1, 2, 1)
                num, i, mstart = 'MAGIC ITEM TABLE D', 0, 0  # i to count lines
            elif magicText == 'F5':
                magicRoll = np.random.randint(1, 5, 1)
                num, i, mstart = 'MAGIC ITEM TABLE F', 0, 0  # i to count lines
            elif magicText == 'G5':
                magicRoll = np.random.randint(1, 5, 1)
                num, i, mstart = 'MAGIC ITEM TABLE G', 0, 0  # i to count lines
            elif magicText == 'H5':
                magicRoll = np.random.randint(1, 2, 1)
                num, i, mstart = 'MAGIC ITEM TABLE H', 0, 0  # i to count lines
            elif magicText == 'AB11':
                magicRoll = np.random.randint(1, 5, 1)
                magicRoll2 = np.random.randint(1, 7, 1)
                num, i, mstart = 'MAGIC ITEM TABLE A', 0, 0  # i to count lines
                num2, i2, mstart2 = 'MAGIC ITEM TABLE B', 0, 0  # i to count lines
            elif magicText == 'C11':
                magicRoll = np.random.randint(1, 7, 1)
                num, i, mstart = 'MAGIC ITEM TABLE C', 0, 0  # i to count lines
            elif magicText == 'D11':
                magicRoll = np.random.randint(1, 5, 1)
                num, i, mstart = 'MAGIC ITEM TABLE D', 0, 0  # i to count lines
            elif magicText == 'E11':
                magicRoll = np.random.randint(1, 2, 1)
                num, i, mstart = 'MAGIC ITEM TABLE E', 0, 0  # i to count lines
            elif magicText == 'FG11':
                magicRoll = np.random.randint(1, 2, 1)
                magicRoll2 = np.random.randint(1, 5, 1)
                num, i, mstart = 'MAGIC ITEM TABLE F', 0, 0  # i to count lines
                num2, i2, mstart2 = 'MAGIC ITEM TABLE G', 0, 0  # i to count lines
            elif magicText == 'H11':
                magicRoll = np.random.randint(1, 5, 1)
                num, i, mstart = 'MAGIC ITEM TABLE H', 0, 0  # i to count lines
            elif magicText == 'I11':
                magicRoll = np.random.randint(1, 2, 1)
                num, i, mstart = 'MAGIC ITEM TABLE I', 0, 0  # i to count lines

            with open("Magic_Item_Tables") as search:
                for line in search:
                    if mstart > 0 and line == '\n':
                        mend = i
                        break
                    i += 1
                    line = line.rstrip()  # remove '\n' at end of line
                    if num == line: mstart = i

            try:
                magicRoll2
            except NameError:  # if magicRoll2 doesn't exist yet
                print("no 2nd magic item roll")
            else:
                with open("Magic_Item_Tables") as search2:
                    for line2 in search2:
                        if mstart2 > 0 and line2 == '\n':
                            mend2 = i2
                            break
                        i2 += 1
                        line2 = line2.rstrip()  # remove '\n' at end of line
                        if num2 == line2: mstart2 = i2

        #  Roll for magic items
        try:
            magicText
        except NameError:  # if magicText doesn't exist yet
            print("nothing")
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
        try:
            magicRoll2
        except NameError: # if magicRoll2 doesn't exist yet
            print("no 2nd magic item roll")
        else:
            f = open('Magic_Item_Tables', 'r')
            lines2 = f.readlines()[int(mstart2 + 1):int(mend2)]
            f.close()
            dieRange2, magicItem2, magicItemn2 = [0] * len(lines2), [0] * len(lines2), np.zeros(len(lines2),
                                                                                           int)
            for x in range(0, len(lines2)):
                lines2[x] = lines2[x].rstrip()
                dieRange2[x], magicItem2[x] = lines2[x].split(' ', 1)
            for x in range(0, int(magicRoll2)):
                d1002 = np.random.randint(1, 101, 1)
                for n in range(0, len(dieRange2)):
                    if '-' in dieRange2[n]:
                        first2, second2 = dieRange2[n].split('-')
                        if d1002 >= int(first2) and d1002 <= int(second2):
                            magicItemn2[n] += 1
                    elif d1002 == int(dieRange2[n]):
                        magicItemn2[n] += 1

        #  Roll for gems/art
        try:
            gemsArtText
        except NameError:  # if magicText doesn't exist yet
            print("nothing")
        else:
            f = open('Art_Gems_Tables', 'r')
            lines = f.readlines()[int(gstart+1):int(gend)]
            f.close()
            dieRange, gemsArt, gemsArtn = [0]*len(lines), [0]*len(lines), np.zeros(len(lines), int)
            if (gemsArtText == '010' or gemsArtText == '050' or
                gemsArtText == '550'): maxd = 12
            elif (gemsArtText == '025' or gemsArtText == '5100' or
                gemsArtText == '525' or gemsArtText == '5250' or
                  gemsArtText == '11250' or gemsArtText == '11750'): maxd = 10
            elif (gemsArtText == '11500'): maxd = 6
            elif (gemsArtText == '111000'): maxd = 8
            for x in range(0, len(lines)):  # get lines of text
                lines[x] = lines[x].rstrip()
                dieRange[x], gemsArt[x] = lines[x].split(' ', 1)
            for x in range(0, int(gemsArtRoll)):
                dx = np.random.randint(1, maxd+1, 1)
                for n in range(0, len(dieRange)):
                    if '-' in dieRange[n]:
                        first, second = dieRange[n].split('-')
                        if dx >= int(first) and dx <= int(second):
                            gemsArtn[n] += 1
                    elif dx == int(dieRange[n]):
                        gemsArtn[n] += 1

        bigPrint = "BUM BA DUH BUUUH!"
        bigPrint += ' Your roll of **{}** has earned: \r'.format(roll[0])
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

        try:
            magicRoll2
        except NameError:  # if magicText doesn't exist yet
            print("still no 2nd magic item roll")
        else:
            bigPrint += '\r*And...!*'
            if np.sum(magicItemn2) > 0:
                bigPrint += '\r'
                for x in range(0, len(magicItem2)):
                    if magicItemn2[x] > 0:
                        bigPrint += '{} {}(s)  '.format(magicItemn2[x], magicItem2[x])

        await client.send_file(message.channel, "imgs\hoard.png")
        await client.send_message(message.channel, bigPrint)

    if message.content.startswith('!batboys'):
        await client.send_file(message.channel, "imgs\Batboys.png")

    if (message.content.startswith('Thanks Dice Bot') or message.content.startswith('Thanks DiceBot')
        or message.content.startswith('Thanks dice bot') or message.content.startswith('Thanks dicebot')
        or message.content.startswith('Thanks Dicebot') or
        message.content.startswith('Thank you Dice Bot') or message.content.startswith('Thank you DiceBot')
        or message.content.startswith('Thank you dice bot') or message.content.startswith('Thank you dicebot')
        or message.content.startswith('Thank you Dicebot') or
        message.content.startswith('thank you Dice Bot') or message.content.startswith('thank you DiceBot')
        or message.content.startswith('thank you dice bot') or message.content.startswith('thank you dicebot')
        or message.content.startswith('thank you Dicebot') or
        message.content.startswith('thanks Dice Bot') or message.content.startswith('thanks DiceBot')
        or message.content.startswith('thanks dice bot') or message.content.startswith('thanks dicebot')
        or message.content.startswith('thanks Dicebot')):
        charName = [message.author.display_name]
        await client.send_message(message.channel, 'You are most welcome, {}.'.format(charName[0]))

    if (message.content.startswith('Good job Dice Bot') or message.content.startswith('Good job DiceBot')
        or message.content.startswith('Good job dice bot') or message.content.startswith('Good job dicebot')
        or message.content.startswith('Good job Dicebot') or
        message.content.startswith('good job Dice Bot') or message.content.startswith('good job DiceBot')
        or message.content.startswith('good job dice bot') or message.content.startswith('good job dicebot')
        or message.content.startswith('good job Dicebot') or
        message.content.startswith('Good Dice Bot') or message.content.startswith('Good DiceBot')
        or message.content.startswith('Good dice bot') or message.content.startswith('Good dicebot')
        or message.content.startswith('Good Dicebot') or message.content.startswith('Good bot') or
        message.content.startswith('good Dice Bot') or message.content.startswith('good DiceBot')
        or message.content.startswith('good dice bot') or message.content.startswith('good dicebot')
        or message.content.startswith('good Dicebot') or message.content.startswith('good bot')):
        charName = [message.author.display_name]
        await client.send_message(message.channel, 'Thank you, {}; that is very kind of you to say.'.format(charName[0]))

    if message.content.startswith('!help'):
        help_text = (
            'Dice Bot Commands: \r \r \
            `!roll nds+m`:  roll n s-sided dice with +m modifier \r \
            `!init m`:  roll initiative with m modifier for yourself \r \
            `!init num mod monster`:  roll num initiative rolls all with mod modifier for monster_name \r \
            `!init set Roll Name`:  set Name\'s initiative roll to Roll (doesn\'t edit, just adds new entry) \r \
            `!init start`:  clear history and start a new initiative roll \r \
            `!hit`:  get random flavor text for a hit \r \
            `!char`: generate stat attribute rolls by 4d6 minus ignoring roll \r \
            `!loot CR (n)`:  roll for n (default 1) individual treasures of given CR (up to 10) \r \
            `!hoard CR (n)`:  roll for n (default 1) hoard treasures of given CR (up to 10) \r \
            `!skill mod skill name` or `!skill skill name mod`: roll a d20+mod for given skill name')
        await client.send_message(message.channel, help_text)

    if message.content.startswith('!logout'):
        """Logs the bot out of Discord."""
        print('Logout command invoked. Shutting down.')
        await client.logout()

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

# @client.command(pass_context=True)
# async def ping(ctx):
#     await client.say("Pong!")
#
# @client.command(pass_context=True)
# async def test(ctx):
#     await client.say("Got it!")

client.run(bot_ID)