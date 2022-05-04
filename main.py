#Version 1.0

import discord
from time import time, sleep
from webserver import keep_alive

TOKEN = "token"
client = discord.Client()

lotery_channel = 970005343277039706
participants = {}
current_lotery_message = None
lotery_msg = None

@client.event
async def on_ready():
  print("Bot is ready !")
  print("--------------")
  global participants
  global current_lotery_message
  global lotery_channel
  global lotery_msg
  participants = {}
  current_lotery_message = None
  lotery_channel = 970005343277039706
  lotery_msg = None

@client.event
async def on_message(message):
  #NOTE : message.channel = channel name
  #NOTE : delete message : await message.delete
  global participants
  global current_lotery_message
  global lotery_channel
  global lotery_msg
  
  username = str(message.author).split("#")[0]
  tag = str(message.author).split("#")[1]
  channel = str(message.channel.name)
  content = str(message.content)
  print("Message received !")

  sucess = None

  if channel == "「👮」only-mods":
    if content == "l:manualinit" :
      participants = {}
      current_lotery_message = None
      await message.channel.send("Bot is initialized !")
    if content.startswith("l:new"):
      await message.channel.send("Last lotery canceled.")
      participants = {}
      if not(lotery_msg == None):
        try:
          await lotery_msg.delete()
        except Forbidden:
          sucess = False
        except NotFound:
          sucess = False
        except HTTPException:
          sucess = False
      if not(sucess):
        await message.channel.send("WARNING : Old lotery message cannot be deleted.")
      await message.channel.send("If there's old messages on the lotery channel, please delete yourself.")
      current_lotery_message = "New lotery ! Try to win : " + content.split(" ")[1] + " !"
      channel = client.get_channel(lotery_channel)
      lotery_msg = await channel.send(current_lotery_message)
    if content.startswith("l:cancel"):
      await message.channel.send("Ok, current lotery is canceled.")
      if not(lotery_msg == None):
        try:
          await lotery_msg.delete()
        except Forbidden:
          sucess = False
        except NotFound:
          sucess = False
        except HTTPException:
          sucess = False
      if not(sucess):
        await message.channel.send("WARNING : Old lotery message cannot be deleted.")
      await message.channel.send("If there's old messages on the lotery channel, please delete yourself.")
      participants = {}
  if channel == "「🎁」lotery-participate" :
    #dict append note
    #my_dict = {"username": "XYZ", "email": "xyz@gmail.com", "location":"Mumbai"}
    #my_dict['name']='Nick'
    if not(content.startswith("l:participate")):
      await client.delete_message(content)
    if content.startswith("l:participate"):
      valid = True
      try:
        number = int(content.split(" ")[1])
      except ValueError:
        await message.channel.send("Please insert a number.")
        valid = False
      except TypeError:
        await message.channel.send("Please insert a valid number.")
        valid = False
      if valid:
        participants[username + '#' + tag] = number
        await message.channel.send("Ok, " + username + " you are added sucessfully with the number " + str(number) + ".")
  if channel == "「🎁」lotery" :
    if message == "l:end":
      winner = key, val = random.choice(list(participants.items()))
      winnerNum = str(winner).split(",")[1].split(")")[0]
      winnerName = str(winner).split(",")[0].split("(")[1]
      await message.channel.send("And the winner is : " + str(winnerNum))
    if message == "l:reroll" :
      winner = key, val = random.choice(list(participants.items()))
      winnerNum = str(winner).split(",")[1].split(")")[0]
      await message.channel.send("And the new winner is : " + str(winnerNum))

keep_alive()
client.run(TOKEN)
