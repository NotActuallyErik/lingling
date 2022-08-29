import discord, os, hashlib
from discord.ext import commands
from Methods import *

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='::')


@bot.event
async def on_ready():
    print('Logged in as: ',
          bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def schema(ctx):
    a = get_schedule()
    ath = ctx.author
    if any(str(x).lower() == "di1a" for x in ath.roles):
        response = prettify_schedule(a, ["di1.a", "di1"])
        return await ctx.send(response)
    elif any(str(x).lower() == "di1b" for x in ath.roles):
        response = prettify_schedule(a, ["di1.b, di1"])
        return await ctx.send(response)


@bot.command()
async def commands(ctx):
    r = "\n"
    r += "\n    **KOMMANDON**    \n\n"
    r += "::schema -- Visar dagens schema, filtrerat på din klass \n"
    r += "::info   -- Kortfattad teknisk info om LingLing för de som är intresserade \n"
    r += "\n"
    await ctx.send(r)


@bot.command()
async def info(ctx):
    r = ""
    r += "*Never spend 6 minutes doing something by hand when you can spend 6 hours failing to automate it*.\n\n"
    r += "Förhoppningen med lingling är att erbjuda ett smidigt* sätt att få tag på" \
         " allmän information rörande våra studier -- exempelvis scheman, tentastatistik eller uppdateringar på kurshemsidor." \
         "\nOnödigt? Förmodligen. Kul? Definitivt.\n\n"
    r += "Koden skrivs i Python3.9 med discordpy och går att hitta här: \nhttps://github.com/NotActuallyErik/lingling.git." \

    await ctx.send(r)

















if __name__ == '__main__':
    from secret import secret
    bot.run(secret)
