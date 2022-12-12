#
from discord import Intents, Color, Embed
from tweepy import Client 
from rocketry.conds import daily
from discord.ext import commands
from rocketry import Rocketry
from dotenv import load_dotenv
from os import getenv
from ru import * #YES IMPORT *, I AM EVIL]

app = Rocketry() #cant tell what dis do yet hehe (later use)

#remember to add your own thingies here:
#---------------------------------------------#
load_dotenv()

bot_token = getenv("BOT_TOKEN")

#tweepy.Client
client = Client(
  consumer_key=getenv("CONSUMER_KEY"),
  consumer_secret=getenv("CONSUMER_SECRET"),
  access_token=getenv("ACCESS_KEY"),
  access_token_secret=getenv("ACCESS_SECRET")
)
#---------------------------------------------#


#function to setup the discord bot
def run_discord_bot():
  client = commands.Bot(command_prefix="ru ", intents=Intents.all())
  
  async def on_ready(self):
    print(f"Entramos como {self.user}.")
    await self.wait_until_ready()

  
  @client.command()
  async def cardapio(ctx):
    hj = today_is()
    
    if is_ru_open(hj):
      text = f"{menu_cafe(dia=hj)}\n\n{menu_almoco(dia=hj)}\n\n{menu_jantar(dia=hj)}"
      embed = Embed(title="Cardápio do Politec", color=Color.from_rgb(225, 198, 153))

    else:
      text = "NÃO TEM RU HOJE"
      embed = Embed(title="Cardápio do Politec", color=Color.from_rgb(225, 198, 153))
      embed.set_image(url="https://media.tenor.com/9lOxocmq5XQAAAAd/crying-emoji-meme.gif")
    
    embed.add_field(name=hj, value=text, inline=False)
    embed.set_author(name="@ru_politec", url="https://twitter.com/ru_politec")
    
    await ctx.send(embed=embed)
  
  client.run(bot_token)

#UTC is +3h of Curitiba-BR, so 10:00 UTC = 07:00 CWB
@app.task(daily.at("06:00")) #this will make the bot run everyday at exactly 6AM (Brasilia)
def tweet():
  dia = today_is()
  
  if is_ru_open(): 
    cafe, almoco, jantar= menu_cafe(), menu_almoco(), menu_jantar()
    
    tweet_dia = client.create_tweet(text=dia)
    tweet_cafe = client.create_tweet(in_reply_to_tweet_id=tweet_dia[0]["id"], text=cafe)
    tweet_almoco = client.create_tweet(in_reply_to_tweet_id=tweet_cafe[0]["id"], text=almoco)
    tweet_jantar = client.create_tweet(in_reply_to_tweet_id=tweet_almoco[0]["id"], text=jantar)
  
  else:
    client.create_tweet(text=f"{dia}\nHOJE N TEM RU :(")

if __name__ == "__main__":
  run_discord_bot()
  app.run()