#import
import asyncio, discord, datetime, random
from json import load
import logging
import re
from discord.ext import commands, tasks
from discord.utils import get
from discord import Member
import calendar
from colorama import Fore, Back, Style


logging.basicConfig(level=logging.INFO)

#onn
with open('config.json') as f:
    d = load(f)
    token = d["token"]
    prefix = d["prefix"]
    server = d["server"]
calendar_month = calendar.month(2022, 3)
bot = commands.Bot(command_prefix=prefix, self_bot=True,  help_command=None, fetch_offline_members=False)


#cog



#help
#@bot.command()
#async def help(ctx):
#    await ctx.send(f"ban:userban\nbin:botinvitelink\nbk:idiotlol\nだるいから自力で何とかしろ")            
#c      
#cl     
#clear  
#day    
#eu     
#fe     
#gb     
#gi     
#gs     
#help   Shows this message
#kami   
#minfo  
#nani   
#sinfo  
#status 
#time   
#ub     
#ui     
#ys 
   
#timecommand
@bot.command(pass_context=True)
async def day(ctx):
    await ctx.message.delete()
    dt = datetime.datetime.today() 
    await ctx.send(f'`{dt.year}年 {dt.month}月 {dt.day}日 {dt.hour}時 {dt.minute}分 {dt.second}秒`')

@bot.command()
async def time(ctx):
    await ctx.message.delete()
    dt = datetime.datetime.today()
    await ctx.send(f'`現在時刻\n{dt.hour}時 {dt.minute}分 {dt.second}秒`')

@bot.command()
async def cl(ctx):
    await ctx.message.delete()
    await ctx.send(f"`{calendar_month}`")
    
#infocommand desuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
@bot.command()
async def sinfo(ctx):
    date_format = "%Y/%m/%d %I:%M.%S %p"
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    sbanner = ctx.guild.banner_url
    sicon = ctx.guild.icon_url
    guildc = ctx.guild
    await ctx.message.delete()
    await ctx.send(f'`guildname:{name}\n owner:{owner}\n description:{description}\n guildid:{id}\n guildmember:{memberCount}\nguildcreated:{guildc.created_at.strftime(date_format)}`\n{sbanner}\n{sicon}')
    
@bot.command()
async def minfo(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.author
    date_format = "%Y/%m/%d %I:%M.%S %p" 
    req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
    banner_id = req["banner"]
    banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}.png?size=1024"
    req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
    avatar_id = req["avatar"]
    guild = ctx.guild
    userguildavatar = f"https://cdn.discordapp.com/guilds/{guild.id}/users/{member.id}/avatars/{avatar_id}.png"
    avatar_url = f"https://cdn.discordapp.com/avatars/{member.id}/{avatar_id}.png?size=1024"
    await ctx.message.delete()
    await ctx.send(f'`id:{member.id}\nname:{member}\nguildname:{member.display_name}\ntag:{member.discriminator}\nbot:{member.bot}\ncreateacctime:{member.created_at.strftime(date_format)}\njoinservertime:{member.joined_at.strftime(date_format)}`\n{banner_url}\n{avatar_url}')

@bot.command(pass_context=True, name='status')
async def status(ctx, member: Member):
    await ctx.send(str(member.status))


@bot.command()
async def gb(ctx):
    await ctx.message.delete()
    sbanner = ctx.guild.banner_url
    await ctx.send(f"{sbanner}")

@bot.command()
async def gi(ctx, member:discord.Member):
    await ctx.send(member.avatar_url)

@bot.command()
async def ub(ctx, user:discord.Member):
    await ctx.message.delete()
    if user == None:
        user = ctx.author
    req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]
    # If statement because the user may not have a banner
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
    await ctx.send(f"||{banner_url}||")
    await ctx.send(f"{user}")

@bot.command()
async def eu(ctx, emoji: discord.Emoji):
    await ctx.message.delete()
    await ctx.send(emoji.url)

#imihucommand
@bot.command()
async def kami(ctx):
    await ctx.message.delete()
    await ctx.send(f"`|/    /_\    |\    /|   |\n|\   /    \  |  \ /  |  |`")
#`|/    /_\    |\    /|   |
#|\   /    \  |  \ /  |  |`

@bot.command()
async def bk(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.author
    await ctx.message.delete()
    await ctx.send(f'<@{member.id}>はバカwwwwww')

@bot.command()
async def nani(ctx):
    await ctx.message.delete()
    await ctx.send(f"`/\/ /-\ /\/ |`")

#system(?)
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.message.delete()
    await member.ban(reason = reason)
    await member.send(f"{member} banned from---{ctx.guild.name} reason:{reason}")
    await ctx.send(f'`bannned:{member} reason:{reason}`')

@bot.command(name='unban')
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.message.delete()
    await ctx.guild.unban(user)
    await user.send(f"{user} umban from---`{ctx.guild.bame}`")
    await ctx.send(f"`unbanned:{user}`")

@bot.command()
async def role(ctx, member : discord.Member, role : discord.Role):
    if member is None:
        member = ctx.author
    await ctx.message.delete()
    await member.add_roles(role)
    await ctx.send(f"`{member} addedrole:{role}`")

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def m(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.add_roles(mutedRole)
   await ctx.send(f"`{member} Muted`")
   await member.send(f"MUTED from---`{ctx.guild.name}`")

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def um(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await ctx.send(f"`{member} UMMUTED`")
   await member.send(f"UMMUTED from---`{ctx.guild.name}`")

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def rr(ctx, member: discord.Member, role : discord.Role):
   mutedRole = discord.utils.get(ctx.guild.roles, name=f"{role}")

   await member.remove_roles(mutedRole)
   await ctx.message.delete()
   await ctx.send(f"`{member} rr {role}`")

@bot.command()
async def clear(ctx, target:int):
    channel = ctx.message.channel
    deleted = await channel.purge(limit=target+1)


#testcommanmd
@bot.command()
async def c(ctx, name, user :discord.Member = None):
    guild = ctx.guild
    try:
        perms = discord.Permissions(send_messages=False, read_messages=True)
        global role  
        role = await guild.create_role(name=name, permissions=perms, hoist=True)
        message = await ctx.send(f"I created! {role.mention}")
    except:
        await ctx.send("error")
    if user == None:
        author=ctx.message.author
        await author.add_roles(role)
    else:
        try:
            user=user
            await user.add_roles(role)
            await message.edit(content="Completed!")
        except:
            await message.edit("something error")

@bot.command()
async def ow(ctx):
    guild_owner = bot.get_user(int(ctx.guild.owner.id))
    await ctx.send(f'The owner of this server is: {guild_owner}')



@bot.command()
async def fe(ctx, *, word):
    await ctx.message.delete()
    await ctx.send(f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||_ _ _ _ _ _ _ https://test.rauf.workers.dev/?&author={word}&color=00FF93")

@bot.command()
async def gs(ctx, *, word):
    await ctx.message.delete()
    await ctx.send(f"https://www.google.com/search?q={word}")

@bot.command()
async def ys(ctx, *, word):
    await ctx.message.delete()
    await ctx.send(f"https://www.youtube.com/results?search_query={word}")

@bot.command()
async def spam(ctx, *, word):
    while True:
        await ctx.send(word)

@bot.command()
async def bin(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.author
    await ctx.message.delete()
    await ctx.send(f'https://discordapp.com/oauth2/authorize?client_id={member.id}&permissions=8&scope=bot')
    await ctx.send(f"<@{member.id}>")

#event＆run
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name=f"support {server}| {len(bot.guilds)} joinserver", url="https://discord.gg"))
    print("""
                                                                                                            __________
   ______________     ________________     ____            __________________     _________               /   _______  \         __________________                                                                                                                                                                                                                                                                                              
  |              |   |                |   |    |          |                  |   |    __   \             /   /       \  \       |                  |                                                                                                                                                                                                                                                                                    
  |     _________|   |   _____________|   |    |          |     _____________|   |   |  |   |           /   /         \  \      |__________________|                                                                                                                                                                                                                                                                                                       
  |    |             |   |                |    |          |    |                 |   |  |   /      　  /   /           \  \            |    |                                                                                                                                                                                                                                                                                                 
  |    |             |   |                |    |          |    |___________      |   |__|  |       　 /   /             \  \           |    |                                                                                                                                                                                                                                                                                                              
  |    |_________    |   |____________    |    |          |    |           |     |__________\        /   /               \  \          |    |                                                                                                                                                                                                                                                                                           
  |              |   |                |   |    |          |    |___________|     |__________|\      |   |                 |  |         |    |                                                                                                                                                                                                                                                                                                         
  |_________     |   |    ____________|   |    |          |    |                 |    ___     \      \   \               /  /          |    |                                                                                                                                                                                                                                                                          
            |    |   |   |                |    |          |    |                 |   |   |     \      \   \             /  /           |    |                                                                                                                                                                                                                                                                               
            |    |   |   |                |    |          |    |                 |   |   |      \      \   \           /  /            |    |                                                                                                                                                                                                                                                                              
  __________|    |   |   |____________    |    |_______   |    |                 |   |   |       |      \   \         /  /             |    |                                                                                                      
 |               |   |                |   |            |  |    |                 |   |___|      /        \   \_______/  /              |    |                                                                                                       
 |_______________|   |________________|   |____________|  |____|                 |_____________/          \ __________ /               |____| 


""")
    print(f"supportserver{server} made by {bot.user}")

    print(f"accountdata {bot.user} | {bot.user.id}")

    print(f"supportserver {server}")
    
bot.run(token, bot=False) 