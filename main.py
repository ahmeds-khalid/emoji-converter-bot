import nextcord
from nextcord import SlashOption, Embed
from nextcord.ext import commands, tasks
import random
import asyncio
import json
import os
from datetime import datetime

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Emoji mapping (unchanged)
emoji_mapping = {
    'a': ':regional_indicator_a:', 'b': ':regional_indicator_b:', 'c': ':regional_indicator_c:',
    'd': ':regional_indicator_d:', 'e': ':regional_indicator_e:', 'f': ':regional_indicator_f:',
    'g': ':regional_indicator_g:', 'h': ':regional_indicator_h:', 'i': ':regional_indicator_i:',
    'j': ':regional_indicator_j:', 'k': ':regional_indicator_k:', 'l': ':regional_indicator_l:',
    'm': ':regional_indicator_m:', 'n': ':regional_indicator_n:', 'o': ':regional_indicator_o:',
    'p': ':regional_indicator_p:', 'q': ':regional_indicator_q:', 'r': ':regional_indicator_r:',
    's': ':regional_indicator_s:', 't': ':regional_indicator_t:', 'u': ':regional_indicator_u:',
    'v': ':regional_indicator_v:', 'w': ':regional_indicator_w:', 'x': ':regional_indicator_x:',
    'y': ':regional_indicator_y:', 'z': ':regional_indicator_z:',
    '0': ':zero:', '1': ':one:', '2': ':two:', '3': ':three:', '4': ':four:',
    '5': ':five:', '6': ':six:', '7': ':seven:', '8': ':eight:', '9': ':nine:',
    '!': ':grey_exclamation:', '?': ':grey_question:', '#': ':hash:', '*': ':asterisk:', ' ': '  '
}

# User points system
user_points = {}

def load_points():
    if os.path.exists('user_points.json'):
        with open('user_points.json', 'r') as f:
            return json.load(f)
    return {}

def save_points():
    with open('user_points.json', 'w') as f:
        json.dump(user_points, f)

user_points = load_points()

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    change_status.start()

@tasks.loop(minutes=30)
async def change_status():
    statuses = ['Emojifying text', 'Converting words to emojis', 'Type /help for commands']
    await bot.change_presence(activity=nextcord.Game(random.choice(statuses)))

@bot.slash_command(name="emojify", description="Convert text to emoji representation")
async def emojify(
    interaction: nextcord.Interaction, 
    text: str,
    style: str = SlashOption(
        name="style",
        choices={"Normal": "normal", "Spaced": "spaced", "Reversed": "reversed"},
        default="normal"
    )
):
    emojified_text = ''.join(emoji_mapping.get(char.lower(), char) for char in text)
    
    if style == "spaced":
        emojified_text = ' '.join(emojified_text.split())
    elif style == "reversed":
        emojified_text = emojified_text[::-1]
    
    # Creating an embed for emojify result
    embed = Embed(title="Emojified Text", color=0x00ff00)
    embed.add_field(name="User", value=interaction.user.mention, inline=True)
    embed.add_field(name="Text", value=emojified_text, inline=False)
    
    await interaction.response.send_message(embed=embed)
    
    # Add points for using the command
    user_id = str(interaction.user.id)
    user_points[user_id] = user_points.get(user_id, 0) + 1
    save_points()

@bot.slash_command(name="points", description="Check your points")
async def check_points(interaction: nextcord.Interaction):
    user_id = str(interaction.user.id)
    points = user_points.get(user_id, 0)
    
    # Creating an embed for points check
    embed = Embed(title="Your Points", color=0x1abc9c)
    embed.add_field(name="User", value=interaction.user.mention, inline=True)
    embed.add_field(name="Points", value=str(points), inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="leaderboard", description="Show top 5 users with most points")
async def leaderboard(interaction: nextcord.Interaction):
    sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Creating an embed for leaderboard
    embed = Embed(title="Leaderboard", color=0xffd700)
    
    for i, (user_id, points) in enumerate(sorted_users, 1):
        user = await bot.fetch_user(int(user_id))
        embed.add_field(name=f"{i}. {user.name}", value=f"{points} points", inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="poll", description="Create a simple poll")
async def create_poll(
    interaction: nextcord.Interaction,
    question: str,
    option1: str,
    option2: str,
    duration: int = SlashOption(description="Poll duration in seconds", min_value=30, max_value=300, default=60)
):
    # Creating an embed for poll creation
    embed = Embed(title=f"Poll By {interaction.user.name}", description=question, color=0x3498db)
    embed.add_field(name="Option 1", value=option1, inline=True)
    embed.add_field(name="Option 2", value=option2, inline=True)
    embed.set_footer(text=f"Poll will end in {duration} seconds.")
    
    poll_message = await interaction.channel.send(embed=embed)
    await poll_message.add_reaction("1️⃣")
    await poll_message.add_reaction("2️⃣")
    
    await interaction.response.send_message("Poll created!", ephemeral=True)
    
    await asyncio.sleep(duration)
    
    poll_message = await interaction.channel.fetch_message(poll_message.id)
    results = [reaction.count for reaction in poll_message.reactions]
    
    winner = "It's a tie!" if results[0] == results[1] else f"Option {'1' if results[0] > results[1] else '2'} wins!"
    
    # Send poll results in an embed
    result_embed = Embed(title="Poll Results", color=0x2ecc71)
    result_embed.add_field(name="Winner", value=winner, inline=False)
    result_embed.add_field(name="Option 1", value=f"{results[0] - 1} votes", inline=True)
    result_embed.add_field(name="Option 2", value=f"{results[1] - 1} votes", inline=True)
    
    await interaction.channel.send(embed=result_embed)

@bot.slash_command(name="reminder", description="Set a reminder")
async def set_reminder(
    interaction: nextcord.Interaction,
    message: str,
    time: int = SlashOption(description="Time in minutes", min_value=1, max_value=1440)
):
    await interaction.response.send_message(f"I'll remind you about '{message}' in {time} minutes.", ephemeral=True)
    await asyncio.sleep(time * 60)
    
    # Creating an embed for the reminder
    embed = Embed(title="Reminder", description=message, color=0xe74c3c)
    embed.set_footer(text=f"Reminder set by {interaction.user.display_name}")
    
    await interaction.channel.send(content=interaction.user.mention, embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "hello" in message.content.lower():
        await message.channel.send(f"Hello {message.author.mention}! 👋")

    await bot.process_commands(message)

bot.run('MTI2MzkwMDE2NjI3MzEwNTk2MA.GHIYRr.35B6VqKfJlDgR4YiH5QvGkkaqIcdIOCd6rLm04')
