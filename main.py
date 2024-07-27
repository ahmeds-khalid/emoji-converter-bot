import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")

#Text(Emojis)
@bot.slash_command(name="emojify", description="convert text to emoji representation in big font")
async def emojify(interaction: nextcord.Interaction, text: str):
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
        '!': ':grey_exclamation:', '?': ':grey_question:', '#': ':hash:', '*': ':asterisk', ' ': '  '
    }
    emojified_text = ''.join(emoji_mapping.get(char.lower(), char) for char in text)
    await interaction.response.send_message(f"{interaction.user.mention} said: {emojified_text}")

bot.run('MTI2MzkwMDE2NjI3MzEwNTk2MA.GHIYRr.35B6VqKfJlDgR4YiH5QvGkkaqIcdIOCd6rLm04')