import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import Button, View
from faceit_data import FaceitData
import re
import sqlite3
import datetime


""" 
The section below will be our database management.
"""



db = sqlite3.connect('C:/Users/gerok/Documents/WarwickCS2/WarwickCS2/main.db')
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS main(
        serverID INTEGER PRIMARY KEY,
        FantasyID INTEGER,
        clipsID INTEGER,
        rolesID INTEGER,
        rulesID INTEGER,
        adminID INTEGER
    )
''')

""" 
The section below will be our discord setup management.
"""



faceit_data = FaceitData("f4d00a9e-40ac-461e-b5f0-2b91083cee7d")

client = commands.Bot(command_prefix='=', intents=discord.Intents.all(), activity = discord.Game(name="Work in progress"))
tree=app_commands.CommandTree

@client.event
async def on_ready():
    await client.tree.sync()

client.remove_command("help")


""" 
The section below will define our intermediary long definitions that are used in commands.
"""



def eloToHex(elo):
    if elo >= 2001:
        return 0xfd1f00
    elif elo >= 1701:
        return 0xff6309
    elif elo >= 1101:
        return 0xffc800
    elif elo >= 801:
        return 0x1ce400
    else:
        return 0xf7f7f7
    
def eloToImg(elo):
    if elo >= 2001:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/NQc-2ZDNlBD.png'
    elif elo >= 1851: 
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/sMJ-bF07xuy.png'
    elif elo >= 1701:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/VFK-P8FMPlG.png'
    elif elo >= 1551:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/cMb-XYBHhEq.png'
    elif elo >= 1401:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/KpO-rnFa22r.png'
    elif elo >= 1251:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/zo2-m8V2jma.png'
    elif elo >= 1101:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/jNh-0mTaj6D.png'
    elif elo >= 951:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/xW90vXd7'
    elif elo >= 801:
        return 'https://i.imgur.com/4a4marb.png'
    else:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/8Pu-zW0YZQL.png'
    
""" 
The section below will define our admin hybrid commands used with the bot.
"""
@client.hybrid_group(invoke_without_command=True, description="Lists all available commands.", name="setup")
@commands.has_permissions(administrator=True)
async def setup(ctx):
    em = discord.Embed(title="Help page",description="\u200B")
    em.add_field(name = "Administrator", value = "`,register`" + "\n" + "`,clip`" + "\n" + "`,fantasy`" + "\n" + "For detailed information on administrator commands please check the official documentation.", inline=False)
    em.add_field(name = "\u200B", value = "Made with :heart: in :flag_tr: & :flag_gb:", inline=False)
    await ctx.send(embed=em)

@setup.command(description="Registers the server into the database.", name="register")
@commands.has_permissions(administrator=True)
async def register(ctx):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if result:
        await ctx.send("This server is already registered in the database.")
    else:
        cursor.execute("INSERT INTO main (serverID, FantasyID, clipsID) VALUES (?, ?, ?)", (int(serverID), None, None))
        db.commit()
        await ctx.send("Server successfully registered.")

@setup.command(description="Updates the clip channel ID in the database.", name="clip")
@commands.has_permissions(administrator=True)
async def clip(ctx, clipid):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    else:
        cursor.execute("UPDATE main SET clipsID = ? WHERE serverID = ?", (clipid, serverID))
        db.commit()
        await ctx.send("Successfully updated the clip channel ID.")

@setup.command(description="Updates the Fantasy Winner role ID in the database.", name="fantasy")
@commands.has_permissions(administrator=True)
async def fantasy(ctx, fantasyid):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    else:
        cursor.execute("UPDATE main SET clipsID = ? WHERE serverID = ?", (fantasyid, serverID))
        db.commit()
        await ctx.send("Successfully updated the `Fantasy Winner` role ID.")

@setup.command(description="Updates the Administrator role ID in the database.", name="admin")
@commands.has_permissions(administrator=True)
async def admin(ctx, adminid):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    else:
        cursor.execute("UPDATE main SET adminID = ? WHERE serverID = ?", (adminid, serverID))
        db.commit()
        await ctx.send("Successfully updated the `Admin` role ID.")

@setup.command(description="Updates the Get Roles channel ID in the database.", name="roles")
@commands.has_permissions(administrator=True)
async def roles(ctx, rolesid):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    else:
        cursor.execute("UPDATE main SET rolesID = ? WHERE serverID = ?", (rolesid, serverID))
        db.commit()
        await ctx.send("Successfully updated the get roles channel ID.")

@setup.command(description="Updates the Get Roles channel ID in the database.", name="rules")
@commands.has_permissions(administrator=True)
async def rules(ctx, rulesid):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    else:
        cursor.execute("UPDATE main SET rulesID = ? WHERE serverID = ?", (rulesid, serverID))
        db.commit()
        await ctx.send("Successfully updated the rules channel ID.")

@setup.command(description="Displays the welcome image embed.", name="welcomeimg")
@commands.has_permissions(administrator=True)
async def welcomeImg(ctx):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    elif result[0][4] is None:
        await ctx.send("This server does not have rules channel ID set. Type `,setup rules` to update the database.")
    else:
        channel = client.get_channel(result[0][4])
        e = discord.Embed(color=0x886C91)
        e.set_image(url="https://i.imgur.com/Z8mMqH7.png")
    await channel.send(embed=e)
    await ctx.send("Successfully sent the message.")

@setup.command(description="Displays the welcome message.", name="welcomemsg")
@commands.has_permissions(administrator=True)
async def welcomeMsg(ctx):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    elif result[0][3] is None:
        await ctx.send("This server does not have roles channel ID set. Type `,setup roles` to update the database.")
    elif result[0][4] is None:
        await ctx.send("This server does not have rules channel ID set. Type `,setup rules` to update the database.")
    elif result[0][5] is None:
        await ctx.send("This server does not have administrator role ID set. Type `,setup admin` to update the database.")
    else:
        channel = client.get_channel(result[0][4])
        e = discord.Embed(color=0x886C91)
        e.add_field(name="You need to have a role to see most of the channels", value=f"Head to <#{result[0][3]}> to get your roles!", inline=False)
        e.add_field(name="Got a question?", value=f"If you have any questions, privately message our qualitative admin team <@&{result[0][5]}> and we'll get back to you ASAP!", inline=False)
        e.add_field(name="Warwick Esports Discord", value="Make sure you're also a member of the Warwick Esports Discord server (link below) to keep up to date with the latest announcements and upcoming events. We have discords for all major esports titles! Society wide events and other exciting new things are announced over there!" + "\n" + "https://discord.gg/kaks22U", inline=False)
        await channel.send(embed=e)
        await ctx.send("Successfully sent the message.")

@setup.command(description="Displays the rules image embed.", name="rulesimg")
@commands.has_permissions(administrator=True)
async def rulesImg(ctx):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    elif result[0][4] is None:
        await ctx.send("This server does not have rules channel ID set. Type `,setup rules` to update the database.")
    else:
        channel = client.get_channel(result[0][4])
        e = discord.Embed(color=0x886C91)
        e.set_image(url="https://i.imgur.com/8dhZC5W.png")
    await channel.send(embed=e)
    await ctx.send("Successfully sent the message.")

@setup.command(description="Displays the rules message.", name="rulesmsg")
@commands.has_permissions(administrator=True)
async def RulesMsg(ctx):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    elif result[0][4] is None:
        await ctx.send("This server does not have rules channel ID set. Type `,setup rules` to update the database.")
    else:
        channel = client.get_channel(result[0][4])
        e = discord.Embed(color=0x886C91)
        e.add_field(name="1. We DO NOT tolerate hate speech or harassment", value="This includes but is not limited to:" + "\n"
                                                 + "　⦁ Hate speech, offensive behaviour, or verbal abuse related to anything." + "\n" 
                                                 + "　⦁ Inappropriate nicknames" + "\n"
                                                 + "　⦁ Stalking or intimidation" + "\n"
                                                 + "　⦁ Hijacking or inciting disruption of streams or social media." + "\n"
                                                 + "　⦁ Posting or threatening to post other peoples personally identifying information (“doxing”)." + "\n"
                                                 + "　⦁ Unwelcome sexual attention. This includes, unwelcome sexual comments, jokes, and sexual advances." + "\n"
                                                 + "　⦁ Advocating for, or encouraging, any of the above behaviour.", inline=False)
        e.add_field(name="2. No NSFW, inappropriate or offensive memes are allowed in this server", value="If you are unsure if it is considered NSFW or suggestive, you should refrain from posting it and seek clarification from an exec member if necessary.", inline=False)
        e.add_field(name="3. Avoid spamming", value="This includes repeatedly tagging people who are not currently active in the chat. Spamming will be punished with a temporary server-mute", inline=False)
        e.add_field(name="4. Keep it positive and appropriate", value="Keep sensitive topics out of the server e.g., politics should be discussed via DMs", inline=False)
        e.add_field(name="\u200B", value="**At the end of the day, we're all here for a good time on a game we love!**", inline=False)
        time = datetime.date.today()
        e.set_footer(text=f'Last Updated: {time}', icon_url="https://i.imgur.com/aDX6f2l.png")
        await channel.send(embed=e)
        await ctx.send("Successfully sent the message.")

@setup.command(description="Displays the status message.", name="statusmsg")
async def Status(ctx):
    serverID = ctx.message.guild.id
    commanderID = ctx.author.id
    guild = await client.fetch_guild(serverID)
    roleAdmin = discord.utils.get(guild.roles, id=285544736612286466)
    commander = await guild.fetch_member(commanderID)
    commanderRoles = commander.roles
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    elif result[0][3] is None:
        await ctx.send("This server does not have roles channel ID set. Type `,setup roles` to update the database.")
    elif roleAdmin not in commanderRoles:
        await ctx.send("Administrator permissions are required for this command.")
    else:
        e = discord.Embed(color=0x886C91)
        e.add_field(name="Welcome to Warwick CS!", value="Please select your student status using the buttons below." +"\n" +"The roles below will give access to the rest of the server.")
        e.add_field(name="\u200B", value="", inline=False)
        e.add_field(name="Warwick", value="This role is dedicated for people who currently enrolled in University of Warwick students.", inline=False)
        e.add_field(name="Alumni", value="This role is dedicated for people who have previously enrolled in University of Warwick.", inline=False)
        e.add_field(name="External", value="This role is dedicated for people who have not previously or are not enrolled in University of Warwick.", inline=False)
        buttonWarwick = Button(label="Warwick", style=discord.ButtonStyle.blurple, emoji="<:whitewolf:872222540569931786>")
        async def buttonWarwick_callback(interaction):
            userID = interaction.user.id
            serverID = interaction.guild_id
            guild = await client.fetch_guild(serverID)
            member = await guild.fetch_member(userID)
            roles = member.roles
            roleWarwick = discord.utils.get(guild.roles, id=368440577253048320)
            roleAlumni = discord.utils.get(guild.roles, id=624670807318200353)
            roleExternal = discord.utils.get(guild.roles, id=514510007140876308)
            roleEsportsStaff = discord.utils.get(guild.roles, id=890616225535782922)
            roleFresher = discord.utils.get(guild.roles, id=874757447481442366)
            rolePlayer = discord.utils.get(guild.roles, id=692840089050677310)
            roleEvents = discord.utils.get(guild.roles, id=819929258734125076)
            roleNSEStaff = discord.utils.get(guild.roles, id=894560815624093697)
            divider = discord.utils.get(guild.roles, id=737728662299869257)
            if roleWarwick in roles:
                await member.remove_roles(roleWarwick)
                await interaction.response.send_message("Removed `Warwick` role", ephemeral=True)
                member = await guild.fetch_member(userID)
                roles = member.roles
                if  (divider in roles) and (roleWarwick not in roles and roleAlumni not in roles and roleExternal not in roles and roleEsportsStaff not in roles and roleFresher not in roles and rolePlayer not in roles and roleEvents not in roles and roleNSEStaff not in roles):
                    await member.remove_roles(divider)
            else:
                await member.add_roles(roleWarwick, divider)
                await interaction.response.send_message("Added `Warwick` role", ephemeral=True)  
        buttonAlumni = Button(label="Alumni", style=discord.ButtonStyle.blurple, emoji="🅰️")
        async def buttonAlumni_callback(interaction):
            userID = interaction.user.id
            serverID = interaction.guild_id
            guild = await client.fetch_guild(serverID)
            member = await guild.fetch_member(userID)
            roles = member.roles
            roleWarwick = discord.utils.get(guild.roles, id=368440577253048320)
            roleAlumni = discord.utils.get(guild.roles, id=624670807318200353)
            roleExternal = discord.utils.get(guild.roles, id=514510007140876308)
            roleEsportsStaff = discord.utils.get(guild.roles, id=890616225535782922)
            roleFresher = discord.utils.get(guild.roles, id=874757447481442366)
            rolePlayer = discord.utils.get(guild.roles, id=692840089050677310)
            roleEvents = discord.utils.get(guild.roles, id=819929258734125076)
            roleNSEStaff = discord.utils.get(guild.roles, id=894560815624093697)
            divider = discord.utils.get(guild.roles, id=737728662299869257)
            if roleAlumni in roles:
                await member.remove_roles(roleAlumni)
                await interaction.response.send_message("Removed `Alumni` role", ephemeral=True)
                member = await guild.fetch_member(userID)
                roles = member.roles
                if  (divider in roles) and (roleWarwick not in roles and roleAlumni not in roles and roleExternal not in roles and roleEsportsStaff not in roles and roleFresher not in roles and rolePlayer not in roles and roleEvents not in roles and roleNSEStaff not in roles):
                    await member.remove_roles(divider)
            else:
                await member.add_roles(roleAlumni, divider)
                await interaction.response.send_message("Added `Alumni` role", ephemeral=True)
        buttonExternal = Button(label="External", style=discord.ButtonStyle.blurple, emoji="<:PapaP:938959918621405184>")
        async def buttonExternal_callback(interaction):
            userID = interaction.user.id
            serverID = interaction.guild_id
            guild = await client.fetch_guild(serverID)
            member = await guild.fetch_member(userID)
            roles = member.roles
            roleWarwick = discord.utils.get(guild.roles, id=368440577253048320)
            roleAlumni = discord.utils.get(guild.roles, id=624670807318200353)
            roleExternal = discord.utils.get(guild.roles, id=514510007140876308)
            roleEsportsStaff = discord.utils.get(guild.roles, id=890616225535782922)
            roleFresher = discord.utils.get(guild.roles, id=874757447481442366)
            rolePlayer = discord.utils.get(guild.roles, id=692840089050677310)
            roleEvents = discord.utils.get(guild.roles, id=819929258734125076)
            roleNSEStaff = discord.utils.get(guild.roles, id=894560815624093697)
            divider = discord.utils.get(guild.roles, id=737728662299869257)
            if roleExternal in roles:
                await member.remove_roles(roleExternal)
                await interaction.response.send_message("Removed `External` role", ephemeral=True)
                member = await guild.fetch_member(userID)
                roles = member.roles
                if  (divider in roles) and (roleWarwick not in roles and roleAlumni not in roles and roleExternal not in roles and roleEsportsStaff not in roles and roleFresher not in roles and rolePlayer not in roles and roleEvents not in roles and roleNSEStaff not in roles):
                    await member.remove_roles(divider)
            else:
                await member.add_roles(roleExternal, divider)
                await interaction.response.send_message("Added `External` role", ephemeral=True)
        buttonWarwick.callback = buttonWarwick_callback
        buttonAlumni.callback = buttonAlumni_callback
        buttonExternal.callback = buttonExternal_callback
        view = View(timeout=None)
        view.add_item(buttonWarwick)
        view.add_item(buttonAlumni)
        view.add_item(buttonExternal)
        channel = client.get_channel(result[0][3])
        await channel.send(embed=e, view=view)
        await ctx.send("Message sent successfully.")

@setup.command(description="Displays the lfg message.", name="lfgmsg")
async def lfg(ctx):
    serverID = ctx.message.guild.id
    commanderID = ctx.author.id
    guild = await client.fetch_guild(serverID)
    roleAdmin = discord.utils.get(guild.roles, id=285544736612286466)
    commander = await guild.fetch_member(commanderID)
    commanderRoles = commander.roles
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    elif result[0][3] is None:
        await ctx.send("This server does not have roles channel ID set. Type `,setup roles` to update the database.")
    elif roleAdmin not in commanderRoles:
        await ctx.send("Administrator permissions are required for this command.")
    else:
        e = discord.Embed(color=0x886C91)
        e.add_field(name="LFG Roles", value="Please select your preferred LFG roles using the buttons below. (Expect to be pinged often)")
        e.add_field(name="\u200B", value="", inline=False)
        e.add_field(name="Matchmaking", value="This role is dedicated for people who want to get pinged for matchmaking parties.", inline=False)
        e.add_field(name="FACEIT", value="This role is dedicated for people who want to get pinged for FACEIT parties.", inline=False)
        buttonMatchmaking = Button(label="Matchmaking", style=discord.ButtonStyle.blurple, emoji="<:silver:801857451171119114>")
        async def buttonMatchmaking_callback(interaction):
            userID = interaction.user.id
            serverID = interaction.guild_id
            guild = await client.fetch_guild(serverID)
            member = await guild.fetch_member(userID)
            roles = member.roles
            roleMatchmaking = discord.utils.get(guild.roles, id=801854927046836335)
            roleFACEIT = discord.utils.get(guild.roles, id=819906235527987241)
            roleGlobal = discord.utils.get(guild.roles, id=1032390061410488370)
            roleFantasy = discord.utils.get(guild.roles, id=863068858976567336)
            roleMatt = discord.utils.get(guild.roles, id=972250888502673418)
            roleStream = discord.utils.get(guild.roles, id=996038852311519242)
            roleBitch = discord.utils.get(guild.roles, id=1012349925046104104)
            roleToby = discord.utils.get(guild.roles, id=1090014133103112384)
            divider = discord.utils.get(guild.roles, id=801853960616280084)
            if roleMatchmaking in roles:
                await member.remove_roles(roleMatchmaking)
                await interaction.response.send_message("Removed `Matchmaking` role", ephemeral=True)
                member = await guild.fetch_member(userID)
                roles = member.roles
                if (divider in roles) and (roleMatchmaking not in roles and roleFACEIT not in roles and roleGlobal not in roles and roleFantasy not in roles and roleMatt not in roles and roleStream not in roles and roleBitch not in roles and roleToby not in roles):
                    await member.remove_roles(divider)
            else:
                await member.add_roles(roleMatchmaking, divider)
                await interaction.response.send_message("Added `Matchmaking` role", ephemeral=True)
        buttonFACEIT = Button(label="FACEIT", style=discord.ButtonStyle.blurple, emoji="<:faceit:819906153327886347>")
        async def buttonFACEIT_callback(interaction):
            userID = interaction.user.id
            serverID = interaction.guild_id
            guild = await client.fetch_guild(serverID)
            member = await guild.fetch_member(userID)
            roles = member.roles
            roleMatchmaking = discord.utils.get(guild.roles, id=801854927046836335)
            roleFACEIT = discord.utils.get(guild.roles, id=819906235527987241)
            roleGlobal = discord.utils.get(guild.roles, id=1032390061410488370)
            roleFantasy = discord.utils.get(guild.roles, id=863068858976567336)
            roleMatt = discord.utils.get(guild.roles, id=972250888502673418)
            roleStream = discord.utils.get(guild.roles, id=996038852311519242)
            roleBitch = discord.utils.get(guild.roles, id=1012349925046104104)
            roleToby = discord.utils.get(guild.roles, id=1090014133103112384)
            divider = discord.utils.get(guild.roles, id=801853960616280084)
            if roleFACEIT in roles:
                await member.remove_roles(roleFACEIT)
                await interaction.response.send_message("Removed `FACEIT` role", ephemeral=True)
                member = await guild.fetch_member(userID)
                roles = member.roles
                if (divider in roles) and (roleMatchmaking not in roles and roleFACEIT not in roles and roleGlobal not in roles and roleFantasy not in roles and roleMatt not in roles and roleStream not in roles and roleBitch not in roles and roleToby not in roles):
                    await member.remove_roles(divider)
            else:
                await member.add_roles(roleFACEIT, divider)
                await interaction.response.send_message("Added `FACEIT` role", ephemeral=True)
        buttonMatchmaking.callback = buttonMatchmaking_callback
        buttonFACEIT.callback = buttonFACEIT_callback
        view = View(timeout=None)
        view.add_item(buttonMatchmaking)
        view.add_item(buttonFACEIT)
        channel = client.get_channel(result[0][3])
        await channel.send(embed=e, view=view)
        await ctx.send("Message sent successfully.")

@setup.command(description="Displays the pings message", name="pingsmsg")
async def pings(ctx):
    serverID = ctx.message.guild.id
    commanderID = ctx.author.id
    guild = await client.fetch_guild(serverID)
    roleAdmin = discord.utils.get(guild.roles, id=285544736612286466)
    commander = await guild.fetch_member(commanderID)
    commanderRoles = commander.roles
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if not result:
        await ctx.send("This server is not registered in the database. Type `,register` to register.")
    elif result[0][3] is None:
        await ctx.send("This server does not have roles channel ID set. Type `,setup roles` to update the database.")
    elif roleAdmin not in commanderRoles:
        await ctx.send("Administrator permissions are required for this command.")
    else:
        e = discord.Embed(color=0x886C91)
        e.add_field(name="Ping Roles", value="Please select the roles for which you'd like to receive pings.")
        e.add_field(name="\u200B", value="", inline=False)
        e.add_field(name="Player", value="Receive pings from in-game events, game news and more.", inline=False)
        e.add_field(name="Events", value="Receive pings for other society events and more.", inline=False)
        e.add_field(name="Road To Global", value="Road To Global is fresh tactical content about the game. Receive pings for new guides, uploads and sessions.", inline=False)
        e.add_field(name="Fantasy", value="Create your own professional dream team with our fantasy league. Get pinged for fantasy league updates.", inline=False)
        buttonGlobal = Button(label="Road To Global", style=discord.ButtonStyle.blurple, emoji="<:wcs:820645827562176543>")
        async def buttonGlobal_callback(interaction):
            userID = interaction.user.id
            serverID = interaction.guild_id
            guild = await client.fetch_guild(serverID)
            member = await guild.fetch_member(userID)
            roles = member.roles
            roleMatchmaking = discord.utils.get(guild.roles, id=801854927046836335)
            roleFACEIT = discord.utils.get(guild.roles, id=819906235527987241)
            roleGlobal = discord.utils.get(guild.roles, id=1032390061410488370)
            roleFantasy = discord.utils.get(guild.roles, id=863068858976567336)
            roleMatt = discord.utils.get(guild.roles, id=972250888502673418)
            roleStream = discord.utils.get(guild.roles, id=996038852311519242)
            roleBitch = discord.utils.get(guild.roles, id=1012349925046104104)
            roleToby = discord.utils.get(guild.roles, id=1090014133103112384)
            divider = discord.utils.get(guild.roles, id=801853960616280084)
            if roleGlobal in roles:
                await member.remove_roles(roleGlobal)
                await interaction.response.send_message("Removed `Road To Global` role", ephemeral=True)
                member = await guild.fetch_member(userID)
                roles = member.roles
                if (divider in roles) and (roleMatchmaking not in roles and roleFACEIT not in roles and roleGlobal not in roles and roleFantasy not in roles and roleMatt not in roles and roleStream not in roles and roleBitch not in roles and roleToby not in roles):
                    await member.remove_roles(divider)
            else:
                await member.add_roles(roleGlobal, divider)
                await interaction.response.send_message("Added `Road To Global` role", ephemeral=True)
        buttonFantasy = Button(label="Fantasy", style=discord.ButtonStyle.blurple, emoji="<:hltv:876041658263818280>")
        async def buttonFantasy_callback(interaction):
            userID = interaction.user.id
            serverID = interaction.guild_id
            guild = await client.fetch_guild(serverID)
            member = await guild.fetch_member(userID)
            roles = member.roles
            roleMatchmaking = discord.utils.get(guild.roles, id=801854927046836335)
            roleFACEIT = discord.utils.get(guild.roles, id=819906235527987241)
            roleGlobal = discord.utils.get(guild.roles, id=1032390061410488370)
            roleFantasy = discord.utils.get(guild.roles, id=863068858976567336)
            roleMatt = discord.utils.get(guild.roles, id=972250888502673418)
            roleStream = discord.utils.get(guild.roles, id=996038852311519242)
            roleBitch = discord.utils.get(guild.roles, id=1012349925046104104)
            roleToby = discord.utils.get(guild.roles, id=1090014133103112384)
            divider = discord.utils.get(guild.roles, id=801853960616280084)
            if roleFantasy in roles:
                await member.remove_roles(roleFantasy)
                await interaction.response.send_message("Removed `Fantasy` role", ephemeral=True)
                member = await guild.fetch_member(userID)
                roles = member.roles
                if (divider in roles) and (roleMatchmaking not in roles and roleFACEIT not in roles and roleGlobal not in roles and roleFantasy not in roles and roleMatt not in roles and roleStream not in roles and roleBitch not in roles and roleToby not in roles):
                    await member.remove_roles(divider)
            else:
                await member.add_roles(roleFantasy, divider)
                await interaction.response.send_message("Added `Fantasy` role", ephemeral=True)
        buttonPlayer = Button(label="Player", style=discord.ButtonStyle.blurple, emoji="<:geem:889942721610022913>")
        async def buttonPlayer_callback(interaction):
            userID = interaction.user.id
            serverID = interaction.guild_id
            guild = await client.fetch_guild(serverID)
            member = await guild.fetch_member(userID)
            roles = member.roles
            roleWarwick = discord.utils.get(guild.roles, id=368440577253048320)
            roleAlumni = discord.utils.get(guild.roles, id=624670807318200353)
            roleExternal = discord.utils.get(guild.roles, id=514510007140876308)
            roleEsportsStaff = discord.utils.get(guild.roles, id=890616225535782922)
            roleFresher = discord.utils.get(guild.roles, id=874757447481442366)
            rolePlayer = discord.utils.get(guild.roles, id=692840089050677310)
            roleEvents = discord.utils.get(guild.roles, id=819929258734125076)
            roleNSEStaff = discord.utils.get(guild.roles, id=894560815624093697)
            divider = discord.utils.get(guild.roles, id=737728662299869257)
            if rolePlayer in roles:
                await member.remove_roles(rolePlayer)
                await interaction.response.send_message("Removed `Player` role", ephemeral=True)
                member = await guild.fetch_member(userID)
                roles = member.roles
                if  (divider in roles) and (roleWarwick not in roles and roleAlumni not in roles and roleExternal not in roles and roleEsportsStaff not in roles and roleFresher not in roles and rolePlayer not in roles and roleEvents not in roles and roleNSEStaff not in roles):
                    await member.remove_roles(divider)
            else:
                await member.add_roles(rolePlayer, divider)
                await interaction.response.send_message("Added `Player` role", ephemeral=True)
        buttonEvents = Button(label="Events", style=discord.ButtonStyle.blurple, emoji="<:coggers:823691600369549352>")
        async def buttonEvents_callback(interaction):
            userID = interaction.user.id
            serverID = interaction.guild_id
            guild = await client.fetch_guild(serverID)
            member = await guild.fetch_member(userID)
            roles = member.roles
            roleWarwick = discord.utils.get(guild.roles, id=368440577253048320)
            roleAlumni = discord.utils.get(guild.roles, id=624670807318200353)
            roleExternal = discord.utils.get(guild.roles, id=514510007140876308)
            roleEsportsStaff = discord.utils.get(guild.roles, id=890616225535782922)
            roleFresher = discord.utils.get(guild.roles, id=874757447481442366)
            rolePlayer = discord.utils.get(guild.roles, id=692840089050677310)
            roleEvents = discord.utils.get(guild.roles, id=819929258734125076)
            roleNSEStaff = discord.utils.get(guild.roles, id=894560815624093697)
            divider = discord.utils.get(guild.roles, id=737728662299869257)
            if roleEvents in roles:
                await member.remove_roles(roleEvents)
                await interaction.response.send_message("Removed `Events` role", ephemeral=True)
                member = await guild.fetch_member(userID)
                roles = member.roles
                if  (divider in roles) and (roleWarwick not in roles and roleAlumni not in roles and roleExternal not in roles and roleEsportsStaff not in roles and roleFresher not in roles and rolePlayer not in roles and roleEvents not in roles and roleNSEStaff not in roles):
                    await member.remove_roles(divider)
            else:
                await member.add_roles(roleEvents, divider)
                await interaction.response.send_message("Added `Events` role", ephemeral=True)
        buttonEvents.callback = buttonEvents_callback
        buttonPlayer.callback = buttonPlayer_callback
        buttonGlobal.callback = buttonGlobal_callback
        buttonFantasy.callback = buttonFantasy_callback
        view = View(timeout=None)
        view.add_item(buttonPlayer)
        view.add_item(buttonEvents)
        view.add_item(buttonGlobal)
        view.add_item(buttonFantasy)
        channel = client.get_channel(result[0][3])
        await channel.send(embed=e, view=view)
        await ctx.send("Message sent successfully.")

@setup.command(description="Assigns required divider roles for every member except administrators.", name="updatedivider")
@commands.has_permissions(administrator=True)
async def updateDivider(ctx):
    message = await ctx.send("Assigning and removing roles. This may take a while...")
    serverID = ctx.message.guild.id
    guild = await client.fetch_guild(serverID)
    roleMatchmaking = discord.utils.get(guild.roles, id=801854927046836335)
    roleFACEIT = discord.utils.get(guild.roles, id=819906235527987241)
    roleGlobal = discord.utils.get(guild.roles, id=1032390061410488370)
    roleFantasy = discord.utils.get(guild.roles, id=863068858976567336)
    roleMatt = discord.utils.get(guild.roles, id=972250888502673418)
    roleStream = discord.utils.get(guild.roles, id=996038852311519242)
    roleBitch = discord.utils.get(guild.roles, id=1012349925046104104)
    roleToby = discord.utils.get(guild.roles, id=1090014133103112384)
    rankDivider = discord.utils.get(guild.roles, id=801853960616280084)

    roleWarwick = discord.utils.get(guild.roles, id=368440577253048320)
    roleAlumni = discord.utils.get(guild.roles, id=624670807318200353)
    roleExternal = discord.utils.get(guild.roles, id=514510007140876308)
    roleEsportsStaff = discord.utils.get(guild.roles, id=890616225535782922)
    roleFresher = discord.utils.get(guild.roles, id=874757447481442366)
    rolePlayer = discord.utils.get(guild.roles, id=692840089050677310)
    roleEvents = discord.utils.get(guild.roles, id=819929258734125076)
    roleNSEStaff = discord.utils.get(guild.roles, id=894560815624093697)
    userDivider = discord.utils.get(guild.roles, id=737728662299869257)

    roleClip = discord.utils.get(guild.roles, id=705872761041715261)
    roleBoost = discord.utils.get(guild.roles, id=823186410261184553)
    roleFantasyWinner = discord.utils.get(guild.roles, id=488292873326821393)
    awardDivider = discord.utils.get(guild.roles, id=737728122505396321)

    roleWrestling = discord.utils.get(guild.roles, id=895644377437831189)
    roleRoll = discord.utils.get(guild.roles, id=1029750882306371654)
    roleChipmunks = discord.utils.get(guild.roles, id=1029750962975408139)
    roleManger = discord.utils.get(guild.roles, id=1029751837789802646)
    roleF = discord.utils.get(guild.roles, id=1029750984508977173)
    roleSurfers = discord.utils.get(guild.roles, id=1029478995617656902)
    roleStrapybara = discord.utils.get(guild.roles, id=760540501707063328)
    roleCoach = discord.utils.get(guild.roles, id=793909223054508072)
    roleSub = discord.utils.get(guild.roles, id=805891146433822731)
    teamDivider = discord.utils.get(guild.roles, id=737728330538942505)
    members = ctx.message.guild.members
    for member in members:
        roles = member.roles
        if  (rankDivider not in roles) and (roleMatchmaking in roles or roleFACEIT in roles or roleGlobal in roles or roleFantasy in roles or roleMatt in roles or roleStream in roles or roleBitch in roles or roleToby in roles):
            await member.add_roles(rankDivider)
        if  (rankDivider in roles) and (roleMatchmaking not in roles and roleFACEIT not in roles and roleGlobal not in roles and roleFantasy not in roles and roleMatt not in roles and roleStream not in roles and roleBitch not in roles and roleToby not in roles):
            await member.remove_roles(rankDivider)
        if  (userDivider not in roles) and (roleWarwick in roles or roleAlumni in roles or roleExternal in roles or roleEsportsStaff in roles or roleFresher in roles or rolePlayer in roles or roleEvents in roles or roleNSEStaff in roles):
            await member.add_roles(userDivider)
        if  (userDivider in roles) and (roleWarwick not in roles and roleAlumni not in roles and roleExternal not in roles and roleEsportsStaff not in roles and roleFresher not in roles and rolePlayer not in roles and roleEvents not in roles and roleNSEStaff not in roles):
            await member.remove_roles(userDivider)
        if  (awardDivider not in roles) and (roleClip in roles or roleBoost in roles or roleFantasyWinner in roles):
            await member.add_roles(awardDivider)
        if  (awardDivider in roles) and (roleClip not in roles and roleBoost not in roles and roleFantasyWinner not in roles):
            await member.remove_roles(awardDivider)
        if  (teamDivider not in roles) and (roleWrestling in roles or roleRoll in roles or roleChipmunks in roles or roleManger in roles or roleF in roles or roleSurfers in roles or roleStrapybara in roles or roleCoach in roles or roleSub in roles):
            await member.add_roles(teamDivider)
        if  (teamDivider in roles) and (roleWrestling not in roles and roleRoll not in roles and roleChipmunks not in roles and roleManger not in roles and roleF not in roles and roleSurfers not in roles and roleStrapybara not in roles and roleCoach not in roles and roleSub not in roles):
            await member.remove_roles(teamDivider)
    await message.edit(content="Finished assigning and removing dividers.")    


""" 
The section below will define our public hybrid commands used with the bot.
"""


@client.hybrid_command(description="Displays FACEIT information of a specified user.", name="stats")
async def stats(ctx, name):
    message = await ctx.send(f'Searching for player `{name}`...')
    data = faceit_data.search_players(f"{name}")
    if not data.get('items'):
        await message.edit(content=f"Could not find user `{name}`. ")
    elif data.get('items')[0].get('nickname').lower() != f'{name.lower()}':
        await message.edit(content=f"Could not find user `{name}`. Did you mean `{data.get('items')[0].get('nickname')}`?")
    else:
        playerData = faceit_data.player_id_details(f"{data.get('items')[0].get('player_id')}")
        statData = faceit_data.player_stats(f"{data.get('items')[0].get('player_id')}", 'csgo')
        rankingData = faceit_data.player_ranking_of_game('csgo', f'{playerData.get("games").get("csgo").get("region")}', f"{data.get('items')[0].get('player_id')}")
        regionData = faceit_data.player_ranking_of_game('csgo', f'{playerData.get("games").get("csgo").get("region")}', f"{data.get('items')[0].get('player_id')}", f'{playerData.get("country")}')
        currentElo = playerData.get('games').get('csgo').get('faceit_elo')
        resultEmbed = discord.Embed(color=eloToHex(int(currentElo)))
        resultEmbed.set_thumbnail(url=f"{playerData.get('avatar')}")
        resultEmbed.set_author(name = f"{data.get('items')[0].get('nickname')}", icon_url=eloToImg(int(currentElo)))
        resultEmbed.add_field(name="Profiles", value= f'{playerData.get("faceit_url")}'.replace("{lang}", "en")+ '\n' + 'https://steamcommunity.com/profiles/' + f'{playerData.get("steam_id_64")}', inline=False)
        resultEmbed.add_field(name="\u200B", value='**Lifetime Statistics**', inline=False)
        resultEmbed.add_field(name="ELO", value=f'{currentElo}', inline=True)
        resultEmbed.add_field(name="Winrate", value=f'{statData.get("lifetime").get("Win Rate %")}' + '%', inline=True)
        resultEmbed.add_field(name="K/D", value=f'{statData.get("lifetime").get("Average K/D Ratio")}', inline=True)
        resultEmbed.add_field(name="\u200B", value='**Ranking Statistics**', inline=False)
        resultEmbed.add_field(name=f'{playerData.get("games").get("csgo").get("region")}' + " Ranking", value=f'{rankingData.get("position")}', inline=True)
        resultEmbed.add_field(name=f':flag_{playerData.get("country")}:'+" Ranking", value=f'{regionData.get("position")}', inline=True)
        await message.edit(embed=resultEmbed, content=None)

@client.hybrid_command(description="Retrieve last X match statistics from a specified user", name="last")
async def last(ctx,num,name):
    message = await ctx.send(f'Searching for player `{name}`...')
    data = faceit_data.search_players(f"{name}")
    if int(round(float(num))) > 25 or int(round(float(num))) < 5:
        await ctx.channel.send(f"`{num}` is not a valid number. Number of matches must be between `5` and `25` inclusive.")
    elif not data.get('items'):
        await ctx.channel.send(f"Could not find user `{name}`. ")
    elif data.get('items')[0].get('nickname').lower() != f'{name.lower()}':
        await ctx.channel.send(f"Could not find user `{name}`. Did you mean `{data.get('items')[0].get('nickname')}`?")
    else:
        await message.edit(content=f'Player `{name}` found. Retrieving last `{num}` matches and calculating statistics...')   
        fulldata = faceit_data.player_id_details(f"{data.get('items')[0].get('player_id')}")
        pelo = fulldata.get('games').get('csgo').get('faceit_elo')

        historydata = faceit_data.player_matches(f"{data.get('items')[0].get('player_id')}", 'csgo', None , None , None , f'{num}')
        matches = []
        rounds = 0
        kills = 0
        deaths = 0
        kd = 0
        kr = 0
        win = 0
        for k in historydata.get('items'):
            if k.get('game_id') == 'csgo':
                matches.append(k.get('match_id'))
                continue
        for k in matches:
            found = 0
            matchdata = faceit_data.match_stats(k).get('rounds')
            rounds = rounds + int(matchdata[0].get('round_stats').get('Rounds'))
            for p in matchdata[0].get('teams')[0].get('players'):
                if p.get('player_id') == data.get('items')[0].get('player_id'):
                    player_stats = p.get('player_stats')
                    kills = kills + int(player_stats.get('Kills'))
                    deaths = deaths + int(player_stats.get('Deaths'))
                    kd = kd + float(player_stats.get('K/D Ratio'))
                    kr = kr + float(player_stats.get('K/R Ratio'))
                    win = win + int(player_stats.get('Result'))
                    found = 1
                    break
            if found == 0:
               for p in matchdata[0].get('teams')[1].get('players'):
                    if p.get('player_id') == data.get('items')[0].get('player_id'):
                        player_stats = p.get('player_stats')
                        kills = kills + int(player_stats.get('Kills'))
                        deaths = deaths + int(player_stats.get('Deaths'))
                        kd = kd + float(player_stats.get('K/D Ratio'))
                        kr = kr + float(player_stats.get('K/R Ratio'))
                        win = win + int(player_stats.get('Result'))
                        break
        ckd = round(kd/int(num), 2)
        ckr = round(kr/int(num), 2)
        tkd = round(kills/float(deaths), 2)
        tkr = round(kills/float(rounds), 2)
        wr = round((win/int(num))*100)

        resultEmbed = discord.Embed(color=eloToHex(int(pelo)))
        resultEmbed.set_thumbnail(url=f"{fulldata.get('avatar')}")
        resultEmbed.set_author(name = f"{data.get('items')[0].get('nickname')}", icon_url=eloToImg(int(pelo)))
        resultEmbed.add_field(name="Profiles", value= f'{fulldata.get("faceit_url")}'.replace("{lang}", "en")+ '\n' + 'https://steamcommunity.com/profiles/' + f'{fulldata.get("steam_id_64")}', inline=False)
        resultEmbed.add_field(name="\u200B", value=f'**Last {num} Statistics**', inline=False)
        resultEmbed.add_field(name="K/D", value=f'{ckd}', inline=True)
        resultEmbed.add_field(name="K/R", value=f'{ckr}', inline=True)
        resultEmbed.add_field(name="ELO", value=f'{pelo}', inline=True)
        resultEmbed.add_field(name="True K/D", value=f'{tkd}', inline=True)
        resultEmbed.add_field(name="True K/R", value=f'{tkr}', inline=True)
        resultEmbed.add_field(name="Winrate", value=f'{wr}' + '%', inline=True)
        await message.edit(embed=resultEmbed, content="")


@client.hybrid_command(description="Changes the colour of Fantasy Winner Role. Can only used by people with the role.", name="colour")
async def colour(ctx,hex):
    hex = hex.upper()
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    if hex[0] == '#':
        hex = hex[1:]
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(hex))
    if not result:
        await ctx.send("The server is not registered in the database. Contact an administrator about this issue.")
    elif result[0][2] is None:
        await ctx.send("The server's `Fantasy Winner` role has not been set. Contact an administrator about this issue.")
    elif not (discord.utils.get(ctx.guild.roles, id=result[0][2]) in ctx.author.roles):
        await ctx.send(f"You do not have the <@&{result[0][2]}> role.")
    elif match:
        await ctx.send(f"The input `{hex}` is not a valid hex colour.")
    else:
        value = "0x" + str(hex)
        fantasyWinnerRole = discord.utils.get(ctx.guild.roles, id=result[0][2])
        await fantasyWinnerRole.edit(colour=discord.Colour(int(value, base=16)))
        await ctx.send(f"Set the <@&{result[0][2]}> role colour to `{hex}`.")

""" 
The section below will define our `help` commands.
The definition of the help commands are ordered by the definition of hybrid commands in the above section.
This comes with the exception of the definition of `help commands`, which is unique and has been created for slash compatability.
"""



@client.hybrid_group(invoke_without_command=True, description="Lists all available commands.", name="help")
async def help(ctx):
    em = discord.Embed(title="Help page",description="\u200B")
    em.add_field(name = "User", value = "`,stats`" + "\n" + "`,last`" + "\n" + "`,colour`", inline=False)
    em.add_field(name = "\u200B", value = "Made with :heart: in :flag_tr: & :flag_gb:", inline=False)
    await ctx.send(embed=em)

@help.command(description="Display all existing commands.")
async def commands(ctx):
    em = discord.Embed(title="Help page",description="\u200B")
    em.add_field(name = "Administrator", value = "", inline=False)
    em.add_field(name = "User", value = "`,stats`" + "\n" + "`,last`", inline=False)
    em.add_field(name = "\u200B", value = "Made with :heart: in :flag_tr: & :flag_gb:", inline=False)
    await ctx.send(embed=em)

@help.command(description="Display information about the `stats` command.")
async def stats(ctx):
    em = discord.Embed(title="User Statistics",description="Displays FACEIT information of a specified user.")
    em.add_field(name = "**Syntax**", value = "`,stats <name>`", inline=False)
    em.add_field(name = "**Notes**", value = "Capital insensitive search. Supports an equivalent slash command.", inline=False)
    await ctx.send(embed=em)

@help.command(description="Display information about the `last` command.")
async def last(ctx):
    em = discord.Embed(title="Retrieve last X match statistics from a specified user",description="Retrieves last X matches and calculates statistics such as K/D, K/R, etc.")
    em.add_field(name = "**Syntax**", value = "`,last <number of matches> <player>`", inline=False)
    em.add_field(name = "**Notes**", value = "`<number of matches>` has to be between `5` and `25` inclusive. \n True statistics are calculated by summing kills, deaths, etc. across matches, whereas regular is the mean of K/Ds across matches.", inline=False)
    await ctx.send(embed=em) 

@help.command(description="Display information about the `colour` command.")
async def colour(ctx):
    serverID = ctx.message.guild.id
    result = cursor.execute("SELECT * FROM main WHERE serverID = :id", {"id" : serverID}).fetchall()
    em = discord.Embed(title="Change the colour of Fantasy Winner Role",description=f"Changes the colour of the role <@&{result[0][2]}> to the specified hexadecimal colour code.")
    em.add_field(name = "**Syntax**", value = "`,colour <Hexadecimal colour>`", inline=False)
    em.add_field(name = "**Notes**", value = f"Requires the role <@&{result[0][2]}> or server administrator to use.", inline=False)
    await ctx.send(embed=em) 

# """ 
# The section below will define our error handling for our commands.
# The definition of the error commands are ordered by the definition of hybrid commands in the above section.
# """

# @stats.error
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("*Command is missing an argument.* ")

# @last.error
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("*Command is missing an argument.* ")

# @colour.error
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("*Command is missing an argument.* ")
#     if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
#         await ctx.send("*You do not have the required role(s) for this command.* ")

"""
Running the BOT
"""



client.run(TOKEN)
