from discord import Intents, Status, Activity, ActivityType, AutoShardedBot
from utilities.database import mysql_login
from utilities.data import get_data

data = get_data()
intents = Intents(guilds=True, guild_messages=True)
bot = AutoShardedBot(intents=intents, status=Status.dnd, activity=Activity(type=ActivityType.watching, name="Starting..."))
bot.load_extensions("cogs")  # Loads all cogs in the cogs folder
BOOTED = False


@bot.listen()
async def on_connect():
    print('Connected to Discord!')
    cursor = await mysql_login()
    database = await cursor.cursor()
    await database.execute("CREATE TABLE IF NOT EXISTS server (guild_id VARCHAR(255) PRIMARY KEY, server_ip TEXT NOT NULL)")
    await database.execute("CREATE TABLE IF NOT EXISTS blacklist (guild_id VARCHAR(21) PRIMARY KEY, reason TEXT NOT NULL)")
    await database.close()


@bot.listen()
async def on_reconnect():
    print('Reconnected to Discord!')


@bot.listen()
async def on_ready():
    global BOOTED  # I'm sorry, but there's no other way to do this without classes which I want only in the cogs
    if BOOTED:
        print("Reconnect(?)")
    if not BOOTED:
        # await bot.sync_commands() #You might need to uncomment this if the slash commands aren't appearing
        print(f'Logged in as {bot.user} with {bot.shard_count} shards!')
        print('------')
        for shard in bot.shards:
            await bot.change_presence(status=Status.online, activity=Activity(type=ActivityType.watching, name=f"Aternos | Shard: {shard+1}"), shard_id=shard)
        BOOTED = True


@bot.check
async def guild_only(ctx):
    return ctx.guild is not None


@bot.check
async def on_command(ctx):
    return False


bot.run(data['Token'])
