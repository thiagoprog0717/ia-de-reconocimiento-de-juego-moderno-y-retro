import discord
from discord.ext import commands
from modelo import clasificador

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def verificaranimales(ctx):
    if ctx.message.attachments:
        for archivo in ctx.message.attachments:
            nombre_archivo = archivo.filename
            url_archivo = archivo.url
           

            await archivo.save(f"./images/{nombre_archivo}")
            nombre_clase,porcentaje = clasificador(f'./images/{nombre_archivo}')
            await ctx.send(f"\n🔮 Predicción: {nombre_clase.strip()} ({porcentaje*100:.2f}%)")

    else:
        await ctx.send("no subio ninguna imagen :(")


bot.run("")