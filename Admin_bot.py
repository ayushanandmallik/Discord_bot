import discord
from discord.ext.commands import Bot, has_permissions
import os
from dotenv import load_dotenv
import sqlite3


load_dotenv()
TOKEN= os.getenv('DISCORD_TOKEN')


bot = Bot(command_prefix='#')

@bot.event
async def on_ready():

    ch=[]
    for server in bot.guilds:
        for channel in server.channels:
            if channel.name == 'general':
                ch.append(channel)


    ch_id=ch[0].id
    print(f'{bot.user.name} has been connected to the server')
    embedVar = discord.Embed(title="ADMIN_BOT",
                             description="Admin bot has been connected to the server. Use command <#setup> to setup the bot for the first time",
                             color=0xcd1d03)
    embedVar.add_field(name="Bot_developer", value="Ayush Anand Mallik")
    await bot.get_channel(ch_id).send(embed=embedVar)


@bot.event
async def on_member_join(member):
    g_id= member.guild.id
    sql= '''INSERT INTO member_info(Name,guild_id) VALUES(?,?)'''
    val= (member.name, g_id)
    db= sqlite3.connect('main.sqlite')
    cursor= db.cursor()
    cursor.execute(sql,val)
    ch=[]
    server= member.guild
    for channel in server.channels:
        if channel.name == 'general':
            ch.append(channel)

    ch_id= ch[0].id
    db.commit()
    cursor.close()
    db.close()
    await bot.get_channel(ch_id).send(f'Hello {member.name}, Welcome to {server.name}')



@bot.command()
async def member_count(ctx):
    member_list = ctx.guild.members
    await ctx.send(len(member_list))

@bot.command()
async def setup(ctx):
    if "administrator" in [i.name.lower() for i in ctx.author.roles]:
        db= sqlite3.connect('main.sqlite')
        cursor= db.cursor()
        sql= '''INSERT INTO main(guild_id, msg, channel_id) VALUES(?,?,?)'''
        msg= 'Welcome to our server'
        channel_id= '747481663059001398'
        val= (ctx.guild.id, msg, channel_id)
        cursor.execute(sql, val)
        db.commit()
        sql2= '''INSERT INTO channel_list(id,name,guild_id) VALUES(?,?,?)'''
        #ch_id = []
        #name= []
        server = ctx.guild
        for channel in server.channels:
            '''ch_id.append(channel.id)
            name.append(channel.name)'''
            val2= (channel.id, channel.name, ctx.guild.id)
            cursor.execute(sql2,val2)
            db.commit()



        sql1= '''INSERT INTO member_info(Name,guild_id,Member_id) VALUES(?,?,?)'''
        member_list= ctx.guild.members
        for member in member_list:
            val1 =(member.name, ctx.guild.id, member.id)
            cursor.execute(sql1,val1)
            db.commit()


        cursor.close()
        db.close()
        embedVar = discord.Embed(title="ADMIN_BOT", description="The bot has been connected to the server and you have completed the setup process.", color=0xcd1d03)
        await ctx.send(embed=embedVar)

    else:
        embedVar = discord.Embed(title="ADMIN_BOT",
                                 description="You do not have the permission to use this command.",
                                 color=0xcd1d03)
        await ctx.send(embed=embedVar)

@bot.command()
async def server_info(ctx):
    server_name= ctx.guild.name
    server_id= ctx.guild.id
    member_list = ctx.guild.members
    member_count= len(member_list)
    owner= ctx.guild.owner.name
    embedVar = discord.Embed(title="ADMIN_BOT", description="", color=0xcd1d03)
    embedVar.add_field(name="Server name", value=server_name, inline=False)
    embedVar.add_field(name="Server id", value=server_id, inline=False)
    embedVar.add_field(name="Owner", value=owner, inline=False)
    embedVar.add_field(name="Member_count", value=str(member_count), inline=False)
    await ctx.send(embed=embedVar)

@bot.command()
async def kick(ctx,m= discord.Member, *, r=None):
    if "administrator" in [i.name.lower() for i in ctx.author.roles]:
        m_id= m.id
        await m.kick(reason=r)
        kicked_member= m.name
        db= sqlite3.connect('main.sqlite')
        cursor= db.cursor()
        sql= '''DELETE FROM member_info WHERE Member_id=?'''
        val= (m_id)
        cursor.execute(sql,val)
        db.commit()
        cursor.close()
        db.close()
        embedVar = discord.Embed(title="ADMIN_BOT", description="", color=0xcd1d03)
        embedVar.add_field(name="", value=kicked_member, inline=False)
        await ctx.send(embed=embedVar)

    else:
        embedVar = discord.Embed(title="ADMIN_BOT",
                                 description="You do not have the permission to use this command.",
                                 color=0xcd1d03)
        await ctx.send(embed=embedVar)


@bot.command()
async def ban(ctx, mem= discord.Member, *, reason= None):
    if "administrator" in [i.name.lower() for i in ctx.author.roles]:
        await mem.ban(mem, reason=reason)
        embedVar = discord.Embed(title="ADMIN_BOT", description="", color=0xcd1d03)
        embedVar.add_field(name="", value="Member has been banned!!", inline=False)
        await ctx.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title="ADMIN_BOT",
                                 description="You do not have the permission to use this command.",
                                 color=0xcd1d03)
        await ctx.send(embed=embedVar)

@bot.command()
@has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.banned_users

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embedVar= discord.Embed(title='ADMIN_BOT', description="Member has been unbanned", color=0xcd1d03)
            await ctx.send(embed=embedVar)
        else:
            embedVar = discord.Embed(title='ADMIN_BOT', description="Member is not banned", color=0xcd1d03)
            await ctx.send(embed=embedVar)










bot.run(TOKEN)

