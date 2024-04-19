import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Done!")

def isSupport(ctx: commands.Context) -> bool:
    return (discord.utils.get(ctx.guild.roles, name="Support")) in ctx.message.author.roles


def isSupportAdmin(ctx: commands.Context) -> bool:
    return (discord.utils.get(ctx.guild.roles, name="Managment")) in ctx.message.author.roles


@bot.event
async def on_message(_msg: discord.Message):

    if _msg.type == discord.MessageType.premium_guild_subscription:
        ch: discord.TextChannel = discord.utils.get(_msg.guild.channels, name='logs')
        await ch.send(embed=discord.Embed(
                title="Server Boost!",
                description=f"Thank you SO much, <@{_msg.author.id}>, for boosting `horizon`! Boost a total of twice for v2!",
                color=discord.Color.pink()
            ))
        return

    if _msg.author.id == 1230662225354686475:
        return

    content = _msg.content.lower()
    msg: discord.Message = None

    if "bsod" in content or "blue screen" in content:
        msg = await _msg.channel.send(
            embed=discord.Embed(
                description="[Fix common BSOD errors - Horizon Gitbook](https://horizon-7.gitbook.io/horizon/general-issues/fix-common-bsod-errors)",
                color=discord.Color.dark_embed()
            )
        )

    elif "does nothing" in content or "close" in content or "th happens" in content:
        msg = await _msg.channel.send(
            embed=discord.Embed(
                description="[Horizon does nothing - Horizon Gitbook](https://horizon-7.gitbook.io/horizon/general-issues/horizon-loader-does-nothing)",
                color=discord.Color.dark_embed()
            )
        )

    elif "dll" in content:
        msg = await _msg.channel.send(
            embed=discord.Embed(
                description="[DLL(s) Not Found - Horizon Gitbook](https://horizon-7.gitbook.io/horizon/general-issues/dll-s-not-found)",
                color=discord.Color.dark_embed()
            )
        )

    elif "visual engine" in content or "data model" in content or "unable to find" in content:
        msg = await _msg.channel.send(
            embed=discord.Embed(
                description="[Unable to find Visual Engine/Data Model](https://horizon-7.gitbook.io/horizon/general-issues/unable-to-find-visual-engine-data-model)",
                color=discord.Color.dark_embed()
            )
        )

    elif "connect to driver" in content:
        msg = await _msg.channel.send(
            embed=discord.Embed(
                description="[Could not connect to driver](https://horizon-7.gitbook.io/horizon/general-issues/could-not-connect-to-driver)",
                color=discord.Color.dark_embed()
            )
        )

    elif "work" in content:
        msg = await _msg.channel.send(
            embed=discord.Embed(
                description="[Could not connect to driver](https://horizon-7.gitbook.io/horizon/general-issues/could-not-connect-to-driver)",
                color=discord.Color.dark_embed()
            )
        )

    elif "closes" in content:
        msg = await _msg.channel.send(
            embed=discord.Embed(
                description="[Horizon closes instantly](https://horizon-7.gitbook.io/horizon/general-issues/horizon-closes-instantly)",
                color=discord.Color.dark_embed()
            )
        )

    elif "windows 11" in content or "w11" in content:
        msg = await _msg.channel.send(
            embed=discord.Embed(
                description="Windows 11 has a 50% chance of now working. Please downgrade for now.",
                color=discord.Color.dark_embed()
            )
        )


    if msg is not None:
        await msg.add_reaction("🗑️")

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if message.author.id != 1230662225354686475:
        return

    if str(payload.emoji) == '🗑️':
        reaction = discord.utils.get(message.reactions, emoji='🗑️')
        if reaction and reaction.count >= 2:
            await message.delete()

@bot.hybrid_group(name="hierarchy", description="Manage the staff hierarchy.")
async def hierarchy(ctx):
    pass

@hierarchy.command(name="accept", description="Accept a user for staff.")
async def accept(ctx, user: discord.Member):
    if not isSupportAdmin(ctx):
        await ctx.reply("No Permission!", ephemeral=True)
        return

    await user.add_roles(discord.utils.get(ctx.guild.roles, name='Support'))

    try:
        await user.send(content="You were accepted as a staff member in `horizon`! Welcome!")
        await ctx.message.add_reaction('👍')
    except:
        await ctx.message.reply(f"👍 - I couldn\'t DM {user.display_name}")

@bot.hybrid_group(name="support", description="Support.")
async def support(ctx):
    pass

@support.command(name="message", description="Message a user.")
async def message(ctx, user: discord.Member, message):
    if not isSupportAdmin(ctx) or not isSupport(ctx):
        await ctx.reply("No permission!", ephemeral=True)
        return

    await user.send(
        content=f"Message from Horizon Recreational : {ctx.message.author.name}\n```{message}```"
    )

    await ctx.reply("Done!", ephemeral=True)

bot.run("made by aero")
