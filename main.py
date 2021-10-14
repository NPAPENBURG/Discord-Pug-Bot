import discord
import config
from playerclass import Player
from matchclass import Match
import saveload
from discord.ext import commands
import discord.utils
import random
import asyncio
from matchcountclass import MatchCounts

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-', intents=intents, help_command=None)

# Stored Registered Players
playerPool = []
# Stored Matches
matchHistory = []
# Stored Match Counts
matchCount = []
# Players in Queue
queueCount = []
# List of Maps
mapList = ['BIND', 'SPLIT', 'HAVEN', 'ASCENT', 'BREEZE', 'FRACTURE']
randomTeam = ['Team 1', 'Team 2']

# loading pickle files
matchHistory = saveload.loadMatchHistory()
playerPool = saveload.loadPlayerPool()
matchCount = saveload.loadMatchCount()

# List of Discord Channel IDS
announcementID = 895801909317894164
registerID = 895801952502423583
resultID = 895802052750503966
queue = 895803600629035018


# Reusable function to get the player object
def getPlayerObject(searchVal, searchAttr, fromList):
    playerObject = next(iter([p for p in fromList if getattr(p, searchAttr) == searchVal]), None)
    if playerObject is None:
        return None
    else:
        return playerObject


# Print when bot is online and ready
@bot.event
async def on_ready():
    print('Ready')


# Command error responder
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                              description="You don't have the required role to do this command",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                              description="This is not a command. Try again.",
                              color=discord.Color.red())
        await ctx.send(embed=embed)


# Command to register with the bot.
@bot.command()
async def register(ctx, name):
    if ctx.channel.id == config.registerID:
        # Getting the users discord ID and Author of Command
        user = ctx.message.author
        D_ID = ctx.message.author.id

        # The role to give when called.
        role = discord.utils.get(user.guild.roles, name="Register")
        # Sign up a player under a temp variable
        tempPlayer = Player(name=name, elo=0, win=0, loss=0, discord_id=D_ID, currentmatch=0)

        # Search pickle file to see if discord_id is already used. Each discord user has a uniquie ID
        targetPlayerid = getPlayerObject(D_ID, "discord_id", playerPool)
        targetPlayername = getPlayerObject(name, "name", playerPool)

        if targetPlayerid in playerPool:
            embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                                  description='You are already registered.',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
        elif targetPlayername in playerPool:
            embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                                  description='That name is already taken.',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            playerPool.append(tempPlayer)
            saveload.writePlayerPool(playerPool)
            embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                                  description=f'You are now registered.',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            await user.add_roles(role)
            await user.edit(nick=name)
    else:
        embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                              description=f'You have to register in the <#{config.registerID}> channel',
                              color=discord.Color.red())
        await ctx.send(embed=embed)


# Check a Players Stats Command
@bot.command()
async def stats(ctx, name):
    if ctx.channel.id == config.queue:

        # Getting player stats
        targetPlayer = getPlayerObject(name, "name", playerPool)

        if targetPlayer in playerPool:

            # Discord embed format
            embed = discord.Embed(title=f"{targetPlayer.name}'s Stats", url="https://papathegoat.com/",
                                  description=f"**Elo:** {targetPlayer.elo} \n"
                                              f"**Win:** {targetPlayer.win}\n"
                                              f"**Loss:** {targetPlayer.loss}",
                                  color=discord.Color.red())
            # Replying the embed
            await ctx.send(embed=embed)



        else:

            embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                                  description="That player does not exist",
                                  color=discord.Color.red())
            # Member does not exist
            await ctx.send(embed=embed)


    else:
        embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                              description=f'You have to use the <#{config.queue}> channel ',
                              color=discord.Color.red())
        # Member does not exist
        await ctx.send(embed=embed)


# Command to change a players name
@bot.command()
@commands.has_role('Admin')
async def changename(ctx, name, newname):
    targetPlayer = getPlayerObject(name, "name", playerPool)

    if targetPlayer in playerPool:
        targetPlayer.name = newname
        await ctx.send(f"players new name is {targetPlayer.name}")
    else:
        await ctx.send('That player does not exist')


# Command to check the leaderboard
@bot.command(pass_context=True, aliases=['leaderboard'])
async def lb(ctx):
    if ctx.channel.id == config.queue:
        # Getting user information
        D_ID = ctx.message.author.id
        targetPlayer = getPlayerObject(D_ID, "discord_id", playerPool, )

        # Ordering the playerPool from highest elo to lowest
        s_playerPool = sorted(playerPool, key=lambda e: e.elo, reverse=True)

        # Discord embed format
        embed = discord.Embed(title=f"LEADERBOARD", url="https://papathegoat.com/",
                              description=f"**1.** {s_playerPool[0].name}: {s_playerPool[0].elo}  \n"
                                          f"**2.** {s_playerPool[1].name}: {s_playerPool[1].elo}  \n"
                                          f"**3.** {s_playerPool[2].name}: {s_playerPool[2].elo}  \n"
                                          f"**4.** {s_playerPool[3].name}: {s_playerPool[3].elo}  \n"
                                          f"**5.** {s_playerPool[4].name}: {s_playerPool[4].elo}  \n"
                                          f"**6.** {s_playerPool[5].name}: {s_playerPool[5].elo}  \n"
                                          f"**7.** {s_playerPool[6].name}: {s_playerPool[6].elo}  \n"
                                          f"**8.** {s_playerPool[7].name}: {s_playerPool[7].elo}  \n"
                                          f"**9.** {s_playerPool[8].name}: {s_playerPool[8].elo}  \n"
                                          f"**10.** {s_playerPool[9].name}: {s_playerPool[9].elo} \n"
                                          f"\n"
                                          f"**10.** You are in {s_playerPool.index(targetPlayer) + 1} place! \n"
                              ,
                              color=discord.Color.red())
        # Replying the embed
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                              description=f'You have to use the <#{config.queue}> channel ',
                              color=discord.Color.red())
        await ctx.send(embed=embed)


# Command to add test players to queue. Testing purposes.
@bot.command()
@commands.has_role('Admin')
async def testp(ctx):
    number = 0
    for x in range(9):
        await asyncio.sleep(1)
        tempPlayer = Player(name=f'test{number}', elo=random.randint(0, 100), win=0, loss=0, discord_id=1,
                            currentmatch=0)
        playerPool.append(tempPlayer)
        queueCount.append(tempPlayer)
        await ctx.send(f'test bot #{number + 1} made and in queue')
        number += 1


# Simple command to get the number of players signed up
@bot.command()
@commands.has_role('Admin')
async def players(ctx):
    players = len(playerPool)
    await ctx.send(players)


# command to join the queue
@bot.command(pass_context=True, aliases=['j', 'J'])
async def join(ctx):
    if ctx.channel.id == config.queue:
        # Getting users Player Class information
        D_ID = ctx.message.author.id
        targetPlayer = getPlayerObject(D_ID, "discord_id", playerPool)

        # If Player is already in queue. Don't let them in queue
        if targetPlayer in queueCount:
            embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                                  description='You are already in the Queue.',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

        # Player not found
        elif targetPlayer not in playerPool:
            embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                                  description='You are not registered.',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)


        # If Player is already in a match. Don't let them in queue
        elif targetPlayer.currentmatch == 1:
            embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                                  description='You are already in a match.',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)


        # If there are 9 people in queue and player is the 10th. Lets get the Match started
        elif len(queueCount) == (config.pugsize - 1):
            # Team list where players will be assigned too.
            team1 = []
            team2 = []

            # Adding the 10th Person to the queue
            queueCount.append(targetPlayer)
            embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                                  description=f'{targetPlayer.name} joined the queue',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

            # Reordering the Queue so its highest to lowest elo
            qplayers = sorted(queueCount, key=lambda e: e.elo, reverse=True)

            # Selecting Players and adding them to team lists
            team1.append(qplayers[0].name)
            team2.append(qplayers[1].name)
            team2.append(qplayers[2].name)
            team1.append(qplayers[3].name)
            team1.append(qplayers[4].name)
            team2.append(qplayers[5].name)
            team2.append(qplayers[6].name)
            team1.append(qplayers[7].name)
            team1.append(qplayers[8].name)
            team2.append(qplayers[9].name)

            # Setting Players to currentmatch = 1 so if they are in a game. They can't rejoin queue.
            pcount = 0
            for x in range(10):
                qplayers[pcount].currentmatch = 1
                pcount += 1
            saveload.writePlayerPool(playerPool)

            # setting up the matchcount number and saving it
            add1 = matchCount[-1].number + 1
            tempgamenum = MatchCounts(add1)
            matchCount.append(tempgamenum)
            saveload.writeMatchCount(matchCount)

            # Saving the match infomation via pickles
            tempMatch = Match(number=tempgamenum, team1=team1, team2=team2)
            matchHistory.append(tempMatch)
            saveload.writeMatchHistory(matchHistory)
            # sending embed to discord channel for teams and map
            channel = bot.get_channel(config.announcementID)
            embed = discord.Embed(title=f"Game #{tempgamenum.number}", description="", color=discord.Color.red())
            embed.add_field(name="Map", value=f"{random.choice(mapList)}", inline=False)
            embed.add_field(name="Team #1",
                            value=f"<@{qplayers[0].discord_id}>, <@{qplayers[3].discord_id}>, <@{qplayers[4].discord_id}>, <@{qplayers[7].discord_id}>, <@{qplayers[8].discord_id}>",
                            inline=False)
            embed.add_field(name="Team #2",
                            value=f"<@{qplayers[1].discord_id}>, <@{qplayers[2].discord_id}>, <@{qplayers[5].discord_id}>, <@{qplayers[6].discord_id}>, <@{qplayers[9].discord_id}>",
                            inline=False)
            embed.add_field(name="Defending Team",
                            value=f"{random.choice(randomTeam)}",
                            inline=False)
            await channel.send(
                f"<@{qplayers[0].discord_id}> <@{qplayers[3].discord_id}> <@{qplayers[4].discord_id}> <@{qplayers[7].discord_id}> <@{qplayers[8].discord_id}> <@{qplayers[1].discord_id}> <@{qplayers[2].discord_id}> <@{qplayers[5].discord_id}> <@{qplayers[6].discord_id}> <@{qplayers[9].discord_id}>",
                embed=embed)

            # Create Temp Roles
            guild = ctx.guild
            await guild.create_role(name=f"Match{add1} Team1")
            await guild.create_role(name=f"Match{add1} Team2")

            # Create Voice Channels

            # Getting category and role information to set channels.
            name = 'PUG NIGHT'
            category = discord.utils.get(ctx.guild.categories, name=name)

            guild = ctx.guild
            team1role = discord.utils.get(guild.roles, name=f"Match{add1} Team1")
            team2role = discord.utils.get(guild.roles, name=f"Match{add1} Team2")

            # Overwrites for team 1
            overwrites1 = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                team1role: discord.PermissionOverwrite(read_messages=True)
            }
            # Overwrites for team 2
            overwrites2 = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                team2role: discord.PermissionOverwrite(read_messages=True)
            }

            # Creating voice channels for the teams on that match.
            await guild.create_voice_channel(f"Match{add1} Team1", category=category, overwrites=overwrites1)
            await guild.create_voice_channel(f"Match{add1} Team2", category=category, overwrites=overwrites2)

            role1 = discord.utils.get(guild.roles, name=f"Match{add1} Team1")
            role2 = discord.utils.get(guild.roles, name=f"Match{add1} Team2")
            # Putting players discord objects into 2 lists
            user1 = ctx.guild.get_member(int(qplayers[0].discord_id))
            if user1 == None:
                pass
            else:
                await user1.add_roles(role1)
            user2 = ctx.guild.get_member(int(qplayers[1].discord_id))
            if user2 == None:
                pass
            else:
                await user2.add_roles(role2)
            user3 = ctx.guild.get_member(int(qplayers[2].discord_id))
            if user3 == None:
                pass
            else:
                await user3.add_roles(role2)
            user4 = ctx.guild.get_member(int(qplayers[3].discord_id))
            if user4 == None:
                pass
            else:
                await user4.add_roles(role1)
            user5 = ctx.guild.get_member(int(qplayers[4].discord_id))
            if user5 == None:
                pass
            else:
                await user5.add_roles(role1)
            user6 = ctx.guild.get_member(int(qplayers[5].discord_id))
            if user6 == None:
                pass
            else:
                await user6.add_roles(role2)
            user7 = ctx.guild.get_member(int(qplayers[6].discord_id))
            if user7 == None:
                pass
            else:
                await user7.add_roles(role2)
            user8 = ctx.guild.get_member(int(qplayers[7].discord_id))
            if user8 == None:
                pass
            else:
                await user8.add_roles(role1)
            user9 = ctx.guild.get_member(int(qplayers[8].discord_id))
            if user9 == None:
                pass
            else:
                await user9.add_roles(role1)
            user10 = ctx.guild.get_member(int(qplayers[9].discord_id))
            if user10 == None:
                pass
            else:
                await user10.add_roles(role2)

            # Clearing all the lists for the next game.
            queueCount.clear()
            qplayers.clear()

        # add user to queue if above if statements are not met.
        else:
            embed = discord.Embed(title='',
                                  description=f'{targetPlayer.name} joined the queue. {len(queueCount) + 1}/10',
                                  color=discord.Color.red())
            queueCount.append(targetPlayer)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                              description=f'You have to use the <#{config.queue}> channel ',
                              color=discord.Color.red())
        await ctx.send(embed=embed)


# command to check how many people are in the queue
@bot.command(pass_context=True, aliases=['q', 'Q'])
async def queue(ctx):
    if ctx.channel.id == config.queue:
        await ctx.send(f'There are {len(queueCount)} players in queue')

    else:
        embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                              description=f'You have to use the <#{config.queue}> channel ',
                              color=discord.Color.red())
        await ctx.send(embed=embed)


# Command makes a test match. Used to test a few things.
@bot.command()
@commands.has_role('Admin')
async def testm(ctx):
    tempMatch = Match(number=0, team1='team1', team2='team2')
    matchHistory.append(tempMatch)
    print(matchHistory)


# Command to get 0 as the first matchCount number. Remember to code out matchCount = saveload.loadMatchCount() run command
# and then restart the bot
@bot.command()
@commands.has_role('Admin')
async def number(ctx):
    # print(matchCount[-1].number)
    # add1 = matchCount[-1].number + 1
    tempgamenum = MatchCounts(number=0)

    matchCount.append(tempgamenum)
    print('it worked')
    saveload.writeMatchCount(matchCount)


@bot.command()
@commands.has_role('Admin')
async def matchresult(ctx, matchnumber, team):
    # Getting location of that match in the list. Python starts at 0 so -1 is needed for correct postion
    intmatchnum = (int(matchnumber) - 1)

    # Going into the list and getting the number from MatchCount Object and turning into an int
    matchNum = int(matchHistory[intmatchnum].number.number)

    # If the MatchNumber is equal to the number given update players information
    if matchNum == int(matchnumber):
        # Getting the list of players on team1 and team2
        team1 = matchHistory[intmatchnum].team1
        team2 = matchHistory[intmatchnum].team2

        player1 = getPlayerObject(team1[0], "name", playerPool)
        player2 = getPlayerObject(team1[1], "name", playerPool)
        player3 = getPlayerObject(team1[2], "name", playerPool)
        player4 = getPlayerObject(team1[3], "name", playerPool)
        player5 = getPlayerObject(team1[4], "name", playerPool)
        player6 = getPlayerObject(team2[0], "name", playerPool)
        player7 = getPlayerObject(team2[1], "name", playerPool)
        player8 = getPlayerObject(team2[2], "name", playerPool)
        player9 = getPlayerObject(team2[3], "name", playerPool)
        player10 = getPlayerObject(team2[4], "name", playerPool)

        # If team1 wins give them elo and take elo from team2. Also change their currentgame status to 0
        if team == 'team1':
            team1count = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team1[team1count], "name", playerPool)
                targetPlayer.elo = int(targetPlayer.elo) + 5
                team1count += 1

            team1currentreset = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team1[team1currentreset], "name", playerPool)
                targetPlayer.currentmatch = 0
                team1currentreset += 1

            team2count = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team2[team2count], "name", playerPool)
                targetPlayer.elo = int(targetPlayer.elo) - 3
                if targetPlayer.elo < 0:
                    targetPlayer.elo = 0
                team2count += 1

            team2currentreset = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team2[team2currentreset], "name", playerPool)
                targetPlayer.currentmatch = 0
                team2currentreset += 1

            team1win = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team1[team1win], "name", playerPool)
                targetPlayer.win = int(targetPlayer.win) + 1
                team1win += 1

            team2lose = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team2[team2lose], "name", playerPool)
                targetPlayer.loss = int(targetPlayer.loss) + 1
                team2lose += 1

            saveload.writePlayerPool(playerPool)

            channel = bot.get_channel(config.resultID)
            embed = discord.Embed(title=f"Game #{matchNum}", description="", color=discord.Color.red())
            embed.add_field(name="Winner", value='Team 1', inline=False)
            embed.add_field(name="Team #1",
                            value=f"<@{player1.discord_id}> + 5 = {player1.elo}\n "
                                  f"<@{player2.discord_id}> + 5 = {player2.elo}\n "
                                  f"<@{player3.discord_id}> + 5 = {player3.elo}\n"
                                  f"<@{player4.discord_id}> + 5 = {player4.elo}\n"
                                  f"<@{player5.discord_id}> + 5 = {player5.elo}",
                            inline=False)
            embed.add_field(name="Team #2",
                            value=f"<@{player6.discord_id}> - 3 = {player6.elo}\n "
                                  f"<@{player7.discord_id}> - 3 = {player7.elo}\n "
                                  f"<@{player8.discord_id}> - 3 = {player8.elo}\n "
                                  f"<@{player9.discord_id}> - 3 = {player9.elo}\n "
                                  f"<@{player10.discord_id}> - 3 = {player10.elo}",
                            inline=False)
            await channel.send(embed=embed)

            # Getting role information
            guild = ctx.guild
            role1 = discord.utils.get(guild.roles, name=f"Match{matchnumber} Team1")
            role2 = discord.utils.get(guild.roles, name=f"Match{matchnumber} Team2")
            await role1.delete()
            await role2.delete()

            # Remove team channels
            team1channel = discord.utils.get(guild.channels, name=f"Match{matchnumber} Team1")
            await team1channel.delete()
            team2channel = discord.utils.get(guild.channels, name=f"Match{matchnumber} Team2")
            await team2channel.delete()

        # If team2 wins give them elo and take elo from team1. Also change their currentgame status to 0
        elif team == 'team2':

            team1count = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team1[team1count], "name", playerPool)
                targetPlayer.elo = int(targetPlayer.elo) - 3
                if targetPlayer.elo < 0:
                    targetPlayer.elo = 0
                team1count += 1

            team1currentreset = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team1[team1currentreset], "name", playerPool)
                targetPlayer.currentmatch = 0
                team1currentreset += 1

            team2count = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team2[team2count], "name", playerPool)
                targetPlayer.elo = int(targetPlayer.elo) + 5
                team2count += 1

            team2currentreset = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team2[team2currentreset], "name", playerPool)
                targetPlayer.currentmatch = 0
                team2currentreset += 1

            team1lose = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team1[team1lose], "name", playerPool)
                targetPlayer.loss = int(targetPlayer.loss) + 1
                team1lose += 1

            team2win = 0
            for x in range(5):
                targetPlayer = getPlayerObject(team2[team2win], "name", playerPool)
                targetPlayer.win = int(targetPlayer.win) + 1
                team2win += 1

            saveload.writePlayerPool(playerPool)

            channel = bot.get_channel(config.resultID)
            embed = discord.Embed(title=f"Game #{matchNum}", description="", color=discord.Color.red())
            embed.add_field(name="Winner", value='Team 1', inline=False)
            embed.add_field(name="Team #1",
                            value=f"<@{player1.discord_id}> - 3 = {player1.elo}\n "
                                    f"<@{player2.discord_id}> - 3 = {player2.elo}\n "
                                    f"<@{player3.discord_id}> - 3 = {player3.elo}\n"
                                    f"<@{player4.discord_id}> - 3 = {player4.elo}\n"
                                     f"<@{player5.discord_id}> - 3 = {player5.elo}",
                            inline=False)
            embed.add_field(name="Team #2",
                                value=f"<@{player6.discord_id}> + 5 = {player6.elo}\n "
                                      f"<@{player7.discord_id}> + 5 = {player7.elo}\n "
                                      f"<@{player8.discord_id}> + 5 = {player8.elo}\n "
                                      f"<@{player9.discord_id}> + 5 = {player9.elo}\n "
                                      f"<@{player10.discord_id}> + 5 = {player10.elo}",
                                inline=False)
            await channel.send(embed=embed)

            # Getting role information
            guild = ctx.guild
            role1 = discord.utils.get(guild.roles, name=f"Match{matchnumber} Team1")
            role2 = discord.utils.get(guild.roles, name=f"Match{matchnumber} Team2")
            await role1.delete()
            await role2.delete()

            # Remove team channels
            team1channel = discord.utils.get(guild.channels, name=f"Match{matchnumber} Team1")
            await team1channel.delete()
            team2channel = discord.utils.get(guild.channels, name=f"Match{matchnumber} Team2")
            await team2channel.delete()
    else:
        await ctx.send('That match number does not exist.')


# bot command to leave queue
@bot.command()
async def leave(ctx):
    if ctx.channel.id == config.queue:
        # Getting users Player Class information
        D_ID = ctx.message.author.id
        targetPlayer = getPlayerObject(D_ID, "discord_id", playerPool)

        # If player is in queue. Remove them.
        if targetPlayer in queueCount:
            queueCount.remove(targetPlayer)
            embed = discord.Embed(title='', description=f'{targetPlayer.name} left the queue. {len(queueCount)}/10',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='', description=f'You are not in the queue.',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"", url="https://papathegoat.com/",
                              description=f'You have to use the <#{config.queue}> channel ',
                              color=discord.Color.red())
        await ctx.send(embed=embed)


# Bot command to give a win and elo to a certain player.
@bot.command()
@commands.has_role('Admin')
async def win(ctx, name):
    targetPlayer = getPlayerObject(name, "name", playerPool)
    if targetPlayer in playerPool:
        targetPlayer.elo = int(targetPlayer.elo) + 5
        targetPlayer.win = int(targetPlayer.win) + 1
        await ctx.send(f"{targetPlayer.name}'s elo is now {targetPlayer.elo}")
        saveload.writePlayerPool(playerPool)
    else:
        await ctx.send(f"That players name does not exist")


# Bot command to give a loss and take elo from a certain player.
@bot.command()
@commands.has_role('Admin')
async def loss(ctx, name):
    targetPlayer = getPlayerObject(name, "name", playerPool)
    if targetPlayer in playerPool:
        targetPlayer.elo = int(targetPlayer.elo) - 3
        targetPlayer.loss = int(targetPlayer.loss) + 1

        await ctx.send(f"{targetPlayer.name}'s elo is now {targetPlayer.elo}")
        saveload.writePlayerPool(playerPool)
    else:
        await ctx.send(f"That players name does not exist")


# Command to clear the queue
@bot.command()
@commands.has_role('Admin')
async def clearqueue(ctx):
    queueCount.clear()
    await ctx.send('The queue is cleared')


@bot.command()
@commands.has_role('Admin')
async def matchend(ctx, matchnumber):
    # Getting location of that match in the list. Python starts at 0 so -1 is needed for correct postion
    intmatchnum = (int(matchnumber) - 1)

    # Going into the list and getting the number from MatchCount Object and turning into an int
    matchNum = int(matchHistory[intmatchnum].number.number)

    # If the MatchNumber is equal to the number given update players information
    if matchNum == int(matchnumber):
        # Getting the list of players on team1 and team2
        team1 = matchHistory[intmatchnum].team1
        team2 = matchHistory[intmatchnum].team2

        team1currentreset = 0
        for x in range(5):
            targetPlayer = getPlayerObject(team1[team1currentreset], "name", playerPool)
            targetPlayer.currentmatch = 0
            team1currentreset += 1

        team2currentreset = 0
        for x in range(5):
            targetPlayer = getPlayerObject(team2[team2currentreset], "name", playerPool)
            targetPlayer.currentmatch = 0
            team2currentreset += 1

        embed = discord.Embed(title='', description=f'Match #{matchNum} has been cancelled',
                              color=discord.Color.red())
        await ctx.send(embed=embed)


        # Remove role
        guild = ctx.guild
        role1 = discord.utils.get(guild.roles, name=f"Match{matchnumber} Team1")
        role2 = discord.utils.get(guild.roles, name=f"Match{matchnumber} Team2")
        await role1.delete()
        await role2.delete()

        # Remove team channels
        team1channel = discord.utils.get(guild.channels, name=f"Match{matchnumber} Team1")
        await team1channel.delete()
        team2channel = discord.utils.get(guild.channels, name=f"Match{matchnumber} Team2")
        await team2channel.delete()


# Give a Player Elo
@bot.command()
@commands.has_role('Admin')
async def elo(self, ctx, name, elo):
    targetPlayer = getPlayerObject(str(name), 'name', playerPool)
    targetPlayer.elo = int(elo)
    saveload.writePlayerPool(playerPool)
    await ctx.send(f'{targetPlayer.name} elo is now {targetPlayer.elo}')


# Pages for help command
page1 = discord.Embed(Title='Pug Bot Help', description='Use the buttons below to navigate between the help pages',
                      colour=discord.Colour.red())
page2 = discord.Embed(Title='Player Commands', description='**PLAYER COMMANDS** \n'
                                                           '-register (name) // Register for the pugs \n'
                                                           '-stats (name) // Register for the pugs \n'
                                                           '-leaderboard // Check the leaderboard \n'
                                                           '-join // Join the Queue \n'
                                                           '-leave // Leave the Queue \n'
                                                           '-queue// Check how many people are in queue \n'
                                                           '-help // Help Command \n',

                      colour=discord.Colour.red())
page3 = discord.Embed(Title='Pug Bot Help', description='**MOD COMMANDS** \n'
                                                        '-changename (name) // Change a players username \n'
                                                        '-players // Check many people are registered \n'
                                                        '-matchresult (#) (team1 or team2)// Call results for match \n'
                                                        '-matchend (#) // End a game if someone was a no show \n'
                                                        '-win // Give a player a win and elo \n'
                                                        '-lose // Give a player a loss and take elo \n'
                                                        '-clearqueue // Clear the queue \n'
                                                        '-unregister (name) // Unregister a player from Player Pool \n',
                      colour=discord.Colour.red())
page4 = discord.Embed(Title='Pug Bot Help', description='**OWNER COMMANDS** \n'
                                                        'testp // Adds 9 bots to the queue \n'
                                                        '-number // Adds one game number. Used for setup \n'
                                                        '-testm // Creates a test match \n',

                      colour=discord.Colour.red())

bot.help_pages = [page1, page2, page3, page4]


# New Help Command
@bot.command()
async def help(ctx):
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]  # skip to start, left, right, skip to end
    current = 0
    msg = await ctx.send(embed=bot.help_pages[current])

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction,
                                                                             user: user == ctx.author and reaction.emoji in buttons,
                                                timeout=60.0)

        except asyncio.TimeoutError:
            return print("test")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0

            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(bot.help_pages) - 1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(bot.help_pages) - 1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(embed=bot.help_pages[current])


# Command to unregister member from the bot.
@bot.command()
@commands.has_role('Admin')
async def unregister(ctx, name):
    targetPlayer = getPlayerObject(str(name), 'name', playerPool)

    if targetPlayer in playerPool:
        embed = discord.Embed(title='', description=f'{targetPlayer.name} has been unregisterd.',
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        playerPool.remove(targetPlayer)
        saveload.writePlayerPool(playerPool)

    else:
        embed = discord.Embed(title='', description=f'That player is not registered.',
                              color=discord.Color.red())
        await ctx.send(embed=embed)


# Run the bot
bot.run(config.token)
