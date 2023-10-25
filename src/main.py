from discord.ext import commands
import discord
import random

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 0000000  # Change to your discord id


#### flooding vars
messages = {}


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

#################################################################
#### Basics
#################################################################

@bot.command()
async def name(ctx):
    await ctx.send(ctx.message.author)

@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1,6))

@bot.event
async def on_message(message):

    if message.author.id not in messages:
        messages[message.author.id] = [message.created_at]
    else:
        messages[message.author.id].append(message.created_at)

    if message.content == "Salut tout le monde":
        await message.channel.send(f"Salut tout seul {message.author.mention}")
    await bot.process_commands(message)

#################################################################
#### Administration
#################################################################

@bot.command()
async def admin(ctx, username):
    admin = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin is None:
        await ctx.guild.create_role(name="Admin", permissions=discord.Permissions.all())
        admin = discord.utils.get(ctx.guild.roles, name="Admin")

    user = discord.utils.get(ctx.guild.members, nick=username)
    if not user:
        user = discord.utils.get(ctx.guild.members, global_name=username)
    if not user:
        await ctx.send(username + "doesn't exist")
        return

    await user.add_roles(admin)

@bot.command()
async def ban(ctx, username, *args):
    user = discord.utils.get(ctx.guild.members, nick=username)
    if not user:
        user = discord.utils.get(ctx.guild.members, global_name=username)
    
    if not user:
        await ctx.send(username + " doesn't exist")
        return


    default_reasons = ['wasn\'t needed',
    'All your bases are belong to us !',
    'cheh',
    'Il s\'appelle Juste Leblanc',
    'Je préfère quand c\'est un peu trop plus moins calme'
    ]
    reason = ' '.join(args)
    if not reason:
        reason = random.choice(default_reasons)
    await user.ban(reason=reason)
    await ctx.send(user.global_name + " has been banned for: " + reason)

#################################################################
#### Flooding
#################################################################

@bot.command()
async def flood(ctx, on_off):
    if on_off == "on":
        activated = True
    elif on_off == "off":
        activated = False
        messages.clear()
    else:
        return 
    max_msg = 10
    time = 60

    while activated:
        for u in messages:
            count = 0
            for m in messages[u]:
                if m - messages[u][-1] > time:
                    count += 1
            if count > max_msg:
                user = discord.utils.get(ctx.guild.members, u)
                await ctx.send(f"@{user.global_name}, you are flooding the channel, slow down")

token = "<TOKEN>"
bot.run(token)  # Starts the bot