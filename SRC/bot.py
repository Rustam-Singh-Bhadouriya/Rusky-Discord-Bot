import asyncio
import os
# os.system(f"pip install discord.py")
import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import tokin

"""Discord Portal create your discord application = https://discord.com/developers/applications"""
# Intents are required for receiving certain events
intents = discord.Intents.all()
intents.messages = True
intents.typing = False
intents.guilds = True  # To get server-related data



bot_tokin = tokin.tokin1

# ALLOWED_SERVERS = [1307589213612539904, 1300450066728747020 , 1307586580998783016]  # Replace with your server IDs


bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    sc = await bot.tree.sync()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'{len(sc)} Commands Sync')
    # await bot.change_presence(status=discord.Status.idle, activity=discord.Game("MINECRAFT"))
    try:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="?Help"))
        print("Bot status changed to idle (MINECRAFT)")
    except Exception as e:
        print(f"An error occurred: {e}")


@bot.tree.command(name='help', description='Get help for using the bot')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🆘 Help Menu",
        description=f"Hi {interaction.user.mention}, how can I assist you?\n"
                    "📜 For a list of all commands, try `/about`.",
        color=discord.Color.green()
    )
    embed.set_footer(text="We're here to help!")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.command()
async def Help(ctx):
    user = ctx
    embed = discord.Embed(
        title="🆘 Help Menu",
        description=f"Hi {ctx.author.mention}\n"
                    "Rusky Bot prefix `?`"
                    "for slash command list type `cmd?L`"
                    "For prefix commands type `?about` for list  "
                    "Join Server : https://discord.gg/PXZHbcxNaj \n"
                    "Add me : type `?add`",
        color=discord.Color.green()
    )
    embed.set_footer(text="Thanks!")
    await ctx.send(embed=embed)

@bot.command()
async def add(ctx):
    embed = discord.Embed(
        title="Add me",
        description=f"Hi {ctx.author.mention}\n"
        "Link = https://discord.com/oauth2/authorize?client_id=1401949547504337057&permissions=8&integration_type=0&scope=bot",
        color=discord.Color.green()
    )
    embed.set_footer(text="Thanks for adding me!")
    await ctx.send(embed=embed)


@bot.tree.command(name='about', description='Learn more about the bot')
async def about(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚡ About Rusky Bot",
        description="This bot is made for manage your server, make announcements, and more! 🎮\n"
                    "Here are some of the commands you can try:\n"
                    "Bot Command, Bot For Kick, Ban, Unban, Afk \n"
                    "And Manage Sever!"
                    "😊 Don't forget to rate us with stars ⭐!",
        color=discord.Color.orange()
    )
    embed.set_footer(text="Bot created by Rusky Community")
    await interaction.response.send_message(embed=embed)

@bot.command()
async def about(ctx):
    embed = discord.Embed(
        title="⚡Commands List",
        description="For slash command type `cmd?L`\n"
                    "prefix : `?` \n  try: `?help`\n"
                    "`?serverinfo` , `?kick` , `?about` , `ban` , `?warn`  , `?lock`\n"
                    "And `?unlock` , `nuke`",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Bot created by Rusky Community")
    await ctx.send(embed=embed)


# Kick command
@bot.tree.command(name="kick", description="Kick a member from the server")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="✅ Member Kicked",
            description=f"{member.mention} has been kicked.\n**Reason:** {reason}",
            color=discord.Color.red()
        )
        embed.set_footer(text="Kick action performed successfully.")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to kick this user.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

# Error handling for insufficient permissions
@kick.error
async def kick_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ You do not have the required permissions to use this command." , ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ An unknown error occurred: {error}" , ephemeral=True)


@bot.tree.command(name="ban", description="Ban a member from the server")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="✅ Member Banned",
            description=f"{member.mention} has been banned.\n**Reason:** {reason}",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text="Ban action performed successfully.")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to ban this user.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

# Error handling for insufficient permissions
@ban.error
async def ban_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ You do not have the required permissions to use this command.",ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ An unknown error occurred: {error}",ephemeral=True)



# Slash command for making announcements
@bot.tree.command(name="announce", description="Make an announcement in a specific channel")
@app_commands.checks.has_permissions(manage_messages=True)
async def announce(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    try:
        # Send the message to the selected channel
        announcement_embed = discord.Embed(
            title="📢 Announcement",
            description=message,
            color=discord.Color.blue()
        )
        announcement_embed.set_footer(text="Announcement by Rusky Bot")
        await channel.send(embed=announcement_embed)

        confirmation_embed = discord.Embed(
            title="✅ Announcement Sent",
            description=f"The announcement was successfully sent to {channel.mention}.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=confirmation_embed, ephemeral=True)
    except discord.Forbidden:
        error_embed = discord.Embed(
            title="❌ Permission Denied",
            description="I don't have permission to send messages in that channel.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
    except discord.HTTPException as e:
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while sending the announcement: {e}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)



# Unban command
@bot.tree.command(name="unban", description="Unban a user by their ID")
@app_commands.describe(user_id="The ID of the user to unban", reason="Reason for the unban (optional)")
async def unban(interaction: discord.Interaction, user_id: str, reason: str = "No reason provided"):
    try:
        # Fetch the banned users as a list
        banned_users = [entry async for entry in interaction.guild.bans()]  # Correct way to iterate async generators
        user = discord.Object(id=int(user_id))  # Create a user object with the ID

        # Check if the user is banned
        for ban_entry in banned_users:
            if ban_entry.user.id == int(user_id):
                await interaction.guild.unban(user, reason=reason)

                # Creating an embed to confirm the unban
                embed = discord.Embed(
                    title="User Unbanned",
                    description=f"User with ID `{user_id}` has been successfully unbanned.",
                    color=discord.Color.green()
                )
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.set_footer(text=f"Unbanned by {interaction.user}")
                await interaction.response.send_message(embed=embed)
                return

        # If the user is not found in the banned list
        await interaction.response.send_message(
            f"User with ID `{user_id}` is not in the banned list.", ephemeral=True
        )

    except Exception as e:
        # Handle any errors that occur
        await interaction.response.send_message(
            f"An error occurred while trying to unban: {e}", ephemeral=True
        )




# Avatar command
@bot.tree.command(name="avatar", description="Fetch and display a user's avatar")
@app_commands.describe(user="The user whose avatar you want to see")
async def avatar(interaction: discord.Interaction, user: discord.Member = None):
    # If no user is specified, use the command author
    user = user or interaction.user

    # Get the avatar URL
    avatar_url = user.avatar.url if user.avatar else "No avatar available."

    # Create an embed with the avatar
    embed = discord.Embed(
        title=f"{user.name}'s Avatar",
        color=discord.Color.blue()
    )
    embed.set_image(url=avatar_url)
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
    
    # Send the embed
    await interaction.response.send_message(embed=embed)


@bot.command()
async def avatar(ctx, user: discord.Member = None):
    # If no user is specified, use the command author
    user = user or ctx.author

    # Get the avatar URL
    avatar_url = user.avatar.url if user.avatar else "No avatar available."

    # Create an embed with the avatar
    embed = discord.Embed(
        title=f"{user.name}'s Avatar",
        color=discord.Color.blue()
    )
    embed.set_image(url=avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
    
    # Send the embed
    await ctx.send(embed=embed)



# Slash command for warning
@bot.tree.command(name="warn", description="Warn a user via DM")
@app_commands.describe(member="The user to warn", reason="The reason for the warning")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.manage_messages:
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # DM Embed to the warned user
    warn_embed = discord.Embed(
        title="⚠️ Warning",
        description=f"You have been warned in **{interaction.guild.name}**.",
        color=discord.Color.blue()
    )
    warn_embed.add_field(name="Reason", value=reason, inline=False)
    warn_embed.set_footer(text="Please adhere to the server rules to avoid further actions.")
    
    # Response Embed for admin
    admin_embed = discord.Embed(
        title="✅ User Warned",
        description=f"{member.mention} has been warned.",
        color=discord.Color.green()
    )
    admin_embed.add_field(name="Reason", value=reason, inline=False,)
    
    try:
        # Send DM to the warned user
        await member.send(embed=warn_embed)
        # Acknowledge the command with an embed to the admin
        await interaction.response.send_message(embed=admin_embed)
    except discord.Forbidden:
        error_embed = discord.Embed(
            title="⚠️ Warning Failed",
            description=f"Could not send a DM to {member.mention}. They might have DMs disabled.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)




# Nuke command
@bot.tree.command(name="nuke", description="Deletes all messages in a channel by recreating it")
@app_commands.checks.has_permissions(manage_channels=True)
async def nuke(interaction: discord.Interaction):
    channel = interaction.channel
    guild = interaction.guild

    # Check if the command is being used in a channel
    if not channel:
        await interaction.response.send_message("This command must be used in a channel.", ephemeral=True)
        return

    # Step 1: Confirmation Embed
    embed_confirmation = discord.Embed(
        title="Nuke Command Initiated",
        description=f"Are you sure you want to nuke the channel `{channel.name}`? This action is **irreversible**.",
        color=discord.Color.red()
    )
    embed_confirmation.set_footer(text="This will delete all messages in the channel by recreating it.")

    # Send initial confirmation message
    await interaction.response.send_message(embed=embed_confirmation, ephemeral=True)

    # Step 2: Perform the nuke
    embed_progress = discord.Embed(
        title="Nuking Channel...",
        description=f"The channel `{channel.name}` is being recreated. Please wait.",
        color=discord.Color.orange()
    )
    await interaction.followup.send(embed=embed_progress)

    # Clone and delete the channel
    new_channel = await channel.clone(reason="Channel nuked by command")
    await channel.delete(reason="Nuke command executed")

    # Step 3: Success Embed
    embed_success = discord.Embed(
        title="Channel Nuked Successfully!",
        description=f"The channel `{new_channel.name}` has been recreated by `{interaction.user.mention}`",
        color=discord.Color.green()
    )
    embed_success.add_field(name="Next Steps", value="All messages have been cleared. You can continue chatting here.")
    embed_success.set_footer(text="Action performed by your friendly bot.")
    embed_success.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2907/2907253.png")  # Add a suitable icon

    # Send success message in the new channel
    await new_channel.send(embed=embed_success)

# Error handling
@nuke.error
async def nuke_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        embed_error = discord.Embed(
            title="Permission Denied",
            description="You do not have the required permissions to use the `/nuke` command.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed_error, ephemeral=True)
    else:
        embed_error = discord.Embed(
            title="An Error Occurred",
            description="Something went wrong while trying to nuke the channel. Please try again later.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed_error, ephemeral=True)

# A dictionary to store AFK statuses
afk_users = {}

# Slash command: Set AFK status
@bot.tree.command(name="afk", description="Set your AFK status")
@app_commands.describe(reason="The reason for being AFK")
async def afk(interaction: discord.Interaction, reason: str = "No reason provided"):
    afk_users[interaction.user.id] = reason
    embed = discord.Embed(
        title="AFK Status Set",
        description=f"{interaction.user.mention}, you are now marked as AFK.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
    embed.set_footer(text="We'll notify others if they mention you.")
    await interaction.response.send_message(embed=embed)

@bot.command()
async def afk(ctx, reason: str = "No reason provided"):
    afk_users[ctx.author.id] = reason
    embed = discord.Embed(
        title="AFK Status Set",
        description=f"{ctx.author.mention}, you are now marked as AFK.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
    embed.set_footer(text="We'll notify others if they mention you.")
    await ctx.send(embed=embed)

# Event: Message handler for AFK logic
@bot.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author.bot:
        return

    # Remove AFK status if the user was AFK and send an AFK closed message
    if message.author.id in afk_users:
        reason = afk_users.pop(message.author.id)

        embed = discord.Embed(
            title="AFK Status Closed",
            description=f"{message.author.mention}, your AFK status has been removed because you sent a message.",
            color=discord.Color.green()
        )
        embed.add_field(name="Previous AFK Reason", value=reason, inline=False)
        embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else None)
        embed.set_footer(text="Welcome back!")
        await message.channel.send(embed=embed)

    elif message.content.lower() == 'hello':
        embed = discord.Embed(
            title="👋 Hello!",
            description="Hi there! Welcome to **Rusky Admin Bot**. 🎮\nEnjoy your stay here!",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Powered by Rusky Bot")
    
        await message.channel.send(embed=embed)

    elif message.content == 'cmd?L':
        embed = discord.Embed(
            title="🤖 B.O.T Commands Lists",
        description="`/Kick`, `/ban` ,`/unban` , `/afk` , `/clear` , `/timeout` , `/avatar` \n `serverinfo` , `cmd?L` , `/nuke` , `/warn` , `/announce` \n `/help` , `/about` \n Thanks ",
            color=discord.Color.og_blurple()
        )
        embed.set_footer(text="Powered by Rusky Bot")
    
        await message.channel.send(embed=embed)
    
        # Command: Hello

    # Process other commands
    await bot.process_commands(message)

    # await bot.process_commands(message)

# Define the slash command
@bot.tree.command(name="clear", description="Clear messages in a channel.")
@app_commands.describe(amount="Number of messages to delete")
async def clear(interaction: discord.Interaction, amount: int):
    # Check permissions
    if not interaction.channel.permissions_for(interaction.user).manage_messages:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have the required permissions to delete messages!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Validate the amount
    if amount < 1 or amount > 100:
        embed = discord.Embed(
            title="Invalid Input",
            description="Please provide a number between 1 and 100.",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Attempt to delete messages
    try:
        deleted = await interaction.channel.purge(limit=amount)
        embed = discord.Embed(
            title="Messages Deleted",
            description=f"Successfully deleted {len(deleted)} message(s).",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred while trying to delete messages:\n{e}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


# Timeout Command
@bot.tree.command(name="timeout", description="Timeout a member for a specified duration.")
@app_commands.describe(
    member="The member to timeout", 
    duration="Duration in minutes", 
    reason="Reason for the timeout (optional)"
)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
    # Check if the user has the required permissions
    if not interaction.user.guild_permissions.moderate_members:
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You don't have permission to timeout members!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Check if the bot has the required permissions
    if not interaction.guild.me.guild_permissions.moderate_members:
        embed = discord.Embed(
            title="❌ Bot Permission Denied",
            description="I don't have permission to timeout members! Please grant me `Moderate Members` permission.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    try:
        # Calculate the timeout duration
        timeout_duration = timedelta(minutes=duration)
        timeout_until = discord.utils.utcnow() + timeout_duration

        # Timeout the member (set timeout)
        await member.edit(timeout=timeout_until, reason=reason)

        # Send success embed
        embed = discord.Embed(
            title="⏱️ Member Timed Out",
            description=f"{member.mention} has been timed out for **{duration} minutes**.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Timeout by {interaction.user}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="⚠️ Error",
            description=f"Could not timeout {member.mention}.",
            color=discord.Color.red()
        )
        embed.add_field(name="Details", value=f"`{e}`", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)





# Server Info Command with Embed
@bot.tree.command(name="serverinfo", description="Get information about the server.")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    if guild:
        embed = discord.Embed(
            title=f"Server Information for {guild.name}",
            description="Here is some basic information about the server:",
            color=discord.Color.blue()
        )

        # Add fields to the embed
        embed.add_field(name="Server Name", value=guild.name, inline=False)
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Member Count", value=guild.member_count, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        # embed.add_field(name="Co - Owner", value='JARIF', inline=False)
        # embed.add_field(name="Roles", value=guild._roles, inline=False)
        embed.add_field(name="Creation Date", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)

        # Send the embed response
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Error: This command can only be used in a server.", ephemeral=True)


# command for greeting

@bot.tree.command(name="great", description="Warn a user via DM")
@app_commands.describe(member="The user to warn", reason="The reason for the warning")
async def great(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.manage_messages:
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # DM Embed to the warned user
    warn_embed = discord.Embed(
        title="🙋‍♂️ Greating",
        description=f"You have been Greated in **{interaction.guild.name}**.",
        color=discord.Color.blue()
    )
    warn_embed.add_field(name="Reason", value=reason, inline=False)
    warn_embed.set_footer(text="Great In Server Is Very Good")
    
    # Response Embed for admin
    admin_embed = discord.Embed(
        title="✅ User Greated",
        description=f"{member.mention} has been Greated.",
        color=discord.Color.green()
    )
    admin_embed.add_field(name="Reason", value=reason, inline=False,)
    
    try:
        # Send DM to the warned user
        await member.send(embed=warn_embed)
        # Acknowledge the command with an embed to the admin
        await interaction.response.send_message(embed=admin_embed)
    except discord.Forbidden:
        error_embed = discord.Embed(
            title="⚠️ Greating Failed",
            description=f"Could not send a DM to {member.mention}. They might have DMs disabled.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)



@bot.command()
@commands.has_permissions(kick_members=True)  # Restrict command to users with kick permissions
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        # Kick the member
        await member.kick(reason=reason)

        # Create an embed
        embed = discord.Embed(
            title="Member Kicked",
            color=discord.Color.red(),
        )
        embed.add_field(name="Kicked Member", value=member.mention, inline=False)
        embed.add_field(name="Kicked By", value=ctx.author.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        # Send the embed
        await ctx.send(embed=embed)

    except discord.Forbidden:
        await ctx.send("❌ I do not have permission to kick this user.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {e}")

# Error handling for missing permissions
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Please specify a member to kick. Example: `!kick @member reason`")


@bot.command()
@commands.has_permissions(ban_members=True)  # Restrict command to users with ban permissions
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        # Ban the member
        await member.ban(reason=reason)

        # Create an embed for the ban notification
        embed = discord.Embed(
            title="🔨 Member Banned",
            color=discord.Color.red()
        )
        embed.add_field(name="Banned Member", value=member.mention, inline=False)
        embed.add_field(name="Banned By", value=ctx.author.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
        embed.set_footer(text=f"Action performed by {ctx.author}", icon_url=ctx.author.avatar.url)

        # Send the embed
        await ctx.send(embed=embed)

    except discord.Forbidden:
        await ctx.send("❌ I do not have permission to ban this user.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {e}")

# Error handling for missing permissions or arguments
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Please specify a member to ban. Example: `!ban @member reason`")

# Lock command
@bot.command()
@commands.has_permissions(manage_channels=True)  # Restrict command to users with channel management permissions
async def lock(ctx):
    try:
        # Get the current channel
        channel = ctx.channel

        # Update channel permissions to prevent @everyone from sending messages
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        # Create an embed for the lock notification
        embed = discord.Embed(
            title="🔒 Channel Locked",
            description=f"{channel.mention} has been locked. Users cannot send messages now.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Locked by {ctx.author}", icon_url=ctx.author.avatar.url)

        # Send the embed
        await ctx.send(embed=embed)

    except discord.Forbidden:
        await ctx.send("❌ I do not have permission to lock this channel.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {e}")

# Error handling for missing permissions
@lock.error
async def lock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")


# Unlock command
@bot.command()
@commands.has_permissions(manage_channels=True)  # Restrict command to users with channel management permissions
async def unlock(ctx):
    try:
        # Get the current channel
        channel = ctx.channel

        # Update channel permissions to allow @everyone to send messages
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        # Create an embed for the unlock notification
        embed = discord.Embed(
            title="🔓 Channel Unlocked",
            description=f"{channel.mention} has been unlocked. Users can now send messages.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Unlocked by {ctx.author}", icon_url=ctx.author.avatar.url)

        # Send the embed
        await ctx.send(embed=embed)

    except discord.Forbidden:
        await ctx.send("❌ I do not have permission to unlock this channel.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {e}")

# Error handling for missing permissions
@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Clear a specified number of messages."""
    if amount <= 0:
        embed = discord.Embed(
            title="Invalid Input",
            description="Please specify a number greater than 0.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    deleted = await ctx.channel.purge(limit=amount)
    embed = discord.Embed(
        title="Messages Cleared",
        description=f"Deleted {len(deleted)} messages.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, delete_after=5)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have the required permissions to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Missing Argument",
            description="Please specify the number of messages to delete.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="Invalid Argument",
            description="Please provide a valid number.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    """Delete all messages in the current channel and recreate it."""
    channel = ctx.channel
    new_channel = await channel.clone(reason="Nuke command used")
    await channel.delete()

    embed = discord.Embed(
        title="Channel Nuked",
        description=f"The channel {new_channel.mention} has been nuked and recreated.",
        color=discord.Color.red()
    )
    await new_channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def announce(ctx, *, message: str):
    """Send an announcement to the current channel."""
    embed = discord.Embed(
        title="Announcement",
        description=message,
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Announcement by {ctx.author}")
    await ctx.send(embed=embed)


@bot.command()
async def serverinfo(ctx):
    """Display server information."""
    guild = ctx.guild
    if guild:
        embed = discord.Embed(
            title=f"Server Information for {guild.name}",
            description="Here is some basic information about the server:",
            color=discord.Color.blue()
        )

        # Add fields to the embed
        embed.add_field(name="Server Name", value=guild.name, inline=False)
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Member Count", value=guild.member_count, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        embed.add_field(name="Creation Date", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
    
    await ctx.send(embed=embed)



# Slash command: Set AFK status


@bot.command()
async def info(ctx , member: discord.Member):
    await ctx.send("Can't Show anyone User's Info!")



@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member = None, *, reason: str = "No reason provided"):
    """Warn a member with a reason."""
    if not member:
        embed = discord.Embed(
            title="Error",
            description="You must mention a member to warn.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(
        title="Warning Issued",
        description=f"{member.mention} has been warned.",
        color=discord.Color.orange()
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text=f"Warned by {ctx.author}")
    await ctx.send(embed=embed)

    # Send a DM to the warned member
    try:
        dm_embed = discord.Embed(
            title="You Have Been Warned",
            description=f"Reason: {reason}",
            color=discord.Color.red()
        )
        dm_embed.set_footer(text=f"Warning issued by {ctx.author}")
        await member.send(embed=dm_embed)
    except discord.Forbidden:
        await ctx.send(f"Could not send a DM to {member.mention}.")

@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have the required permissions to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="Error",
            description="Unable to find the specified member. Please mention a valid user.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)


# Run the bot
bot.run(bot_tokin)

