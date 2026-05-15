import asyncio
import json
import logging
import os
from colorama import Fore, init
init()

import discord
from discord.ext.commands import Context

from core.Astroz import Astroz

# Configure centralized logging with console output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("bot")

os.environ.update({
    "JISHAKU_NO_DM_TRACEBACK": "True",
    "JISHAKU_HIDE": "True",
    "JISHAKU_NO_UNDERSCORE": "True",
    "JISHAKU_FORCE_PAGINATOR": "True",
})


client = Astroz()
tree = client.tree

class Hacker(discord.ui.Modal, title="Embed Configuration"):
    title_input = discord.ui.TextInput(label="Embed Title")
    description = discord.ui.TextInput(
        label="Embed Description",
        style=discord.TextStyle.long,
        required=False,
        max_length=400
    )
    thumbnail = discord.ui.TextInput(label="Thumbnail URL", required=False)
    image = discord.ui.TextInput(label="Image URL", required=False)
    footer = discord.ui.TextInput(label="Footer", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.title_input.value,
            description=self.description.value,
            color=0x2f3136
        )

        if self.thumbnail.value:
            embed.set_thumbnail(url=self.thumbnail.value)
        if self.image.value:
            embed.set_image(url=self.image.value)
        if self.footer.value:
            embed.set_footer(text=self.footer.value)

        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        logger.error("Hacker modal error: %s", error, exc_info=True)
        await interaction.response.send_message(
            "<:warning:1499683278695698432> Something broke. Congrats.", ephemeral=True
        )

@tree.command(name="embedcreate", description="Create an embed")
async def embed_create(interaction: discord.Interaction):
    await interaction.response.send_modal(Hacker())

@client.event
async def on_command_completion(ctx: Context):
    return


@client.event
async def on_ready():
    command_count = len(client.commands)
    total = len(set(client.walk_commands())) # same vibe, different suffering
    count = len(client.guilds)
    user_count = sum(g.member_count for g in client.guilds if g.member_count)

    print(f"""
{Fore.MAGENTA}
██╗   ██╗ ██████╗ ████████╗ ██████╗ ██╗  ██╗
██║   ██║██╔═══██╗╚══██╔══╝██╔═══██╗╚██╗██╔╝
██║   ██║██║   ██║   ██║   ██║   ██║ ╚███╔╝ 
╚██╗ ██╔╝██║   ██║   ██║   ██║   ██║ ██╔██╗ 
 ╚████╔╝ ╚██████╔╝   ██║   ╚██████╔╝██╔╝ ██╗
  ╚═══╝   ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝
{Fore.WHITE}
-----
{Fore.MAGENTA}>{Fore.WHITE} Logged in as {Fore.MAGENTA}{client.user}{Fore.WHITE}.
{Fore.MAGENTA}>{Fore.WHITE} My Bot ID is {Fore.MAGENTA}{client.user.id}{Fore.WHITE}.
{Fore.MAGENTA}>{Fore.WHITE} Synced {Fore.MAGENTA}{command_count} Commands{Fore.WHITE}.
{Fore.MAGENTA}>{Fore.WHITE} Total Commands: {Fore.MAGENTA}{total}{Fore.WHITE}.
{Fore.MAGENTA}>{Fore.WHITE} Guilds: {Fore.MAGENTA}{count}{Fore.WHITE}.
{Fore.MAGENTA}>{Fore.WHITE} Users: {Fore.MAGENTA}{user_count}{Fore.WHITE}.
------
""")

async def main():
    async with client:
        os.system("cls")

        await client.load_extension("cogs")
        await client.load_extension("jishaku")

        try:
            with open("config.json", "r") as f:
                config = json.load(f)

            token = config.get("BOT_TOKEN")
            if not token:
                # try nested bot.token structure
                 token = config.get("bot", {}).get("token")
                 if not token:
                     logger.error("BOT_TOKEN missing in config.json")
                     return

        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error("Config error: %s", e)
            return

        await client.start(token)


if __name__ == "__main__":
    asyncio.run(main())
