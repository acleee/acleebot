from urllib.request import urlopen
from time import sleep
from random import randint
import json
import requests
import ch
import sys
import os
import cgi
import traceback
import time
import urllib
import datetime
import binascii
import json
import threading
import random
import nba_py
import time
from bs4 import BeautifulSoup
import re
from xml.etree import cElementTree as ET
from subprocess import Popen


if sys.version_info[0] > 2:
    import urllib.request as urlreq
else:
    import urllib2 as urlreq

class bot(ch.RoomManager):
  def num_there(s):
    return any(i.isdigit() for i in s)


  def onInit(self):
    self.setNameColor("000000")
    self.setFontColor("000000")
    self.setFontFace("Arial")
    self.setFontSize(11)
    
  def onMessage(self, room, user, message):
    print("[{0}] {1}: {2}".format(room.name, user.name.title(), message.body))
    
    try:
      cmd, args = message.body.split(" ", 1)
    except:
      cmd, args = message.body, ""
      
    if cmd[0] == "!":
      prfx = True
      cmd = cmd[1:]
      
##    if cmd.lower() == "say" and prfx:
##      room.message(args)
##    if user.name.find("!") != -1 or user.name.find("#") != -1:
##      room.message("@"+user.name[1:]+" pls make account")
##     room.message("anon pls make account")
    if cmd.lower() == "pls" and prfx:
      room.message("pls")
    if cmd.lower() == "energy" and prfx:
      room.message("༼ つ ◕_◕ ༽つ "+args.upper()+" TAKE MY ENERGY ༼ つ ◕_◕ ༽つ")
    if cmd.lower() == "ping" and prfx:
      room.message("pong!")
    if cmd.lower() == "donate" and prfx:
      room.message("If you enjoy the stream, help keep the site going! :) https://memesyndicate.com/gofundme")
    if cmd.lower() == "de" and prfx:
      room.message("FENSE!")
    if cmd.lower() == "aclee" and prfx:
      room.message("based aclee")
    if cmd.lower() == "lolmarlins" and prfx:
      room.message("https://i.imgur.com/x33jisM.jpg")
    if cmd.lower() == "lolbarves" and prfx:
      room.message("https://i.imgur.com/Ch4SecV.png")
    if cmd.lower() == "jorge" and prfx:
      room.message("HIP HIP!")
    if cmd.lower() == "over" and prfx:
      room.message("http://i.imgur.com/msOi9Hf.gif")
    if cmd.lower() == "lolmets" and prfx:
      room.message("https://i.imgur.com/F7X08mH.png")
    if cmd.lower() == "kelce" and prfx:
      room.message("https://i.imgur.com/9htC3ze.png")
    if cmd.lower() == "poot" and prfx:
      room.message("https://i.imgur.com/eK1yJUB.jpg")
    if cmd.lower() == "foot" and prfx:
      room.message("https://i.imgur.com/yQGCrAH.jpg")
    if cmd.lower() == "cheesesteak" and prfx:
      room.message("https://i.imgur.com/yDot0lg.gif")
    if cmd.lower() == "dumps" and prfx:
      room.message("http://i.imgur.com/6I9z75O.png")
    if cmd.lower() == "wawa" and prfx:
      room.message("http://i.imgur.com/VcC5gLV.png")
    if cmd.lower() == "lag" and prfx:
      room.message("http://i.imgur.com/wHU7f4P.jpg")
    if cmd.lower() == "nice" and prfx:
      data = ["https://i.imgur.com/QMRxuuP.png", "https://i.imgur.com/XOut2ix.png"]
      random_pic = data[randint(0, len(data) -1)]
      room.message(random_pic)
    if cmd.lower() == "dallas" and prfx:
      data = ["Fuck Dallas.", "Fuck the Cowboys", "FUCK DALLAS", "FUCK THE COWBOYS"]
      random_pic = data[randint(0, len(data) -1)]
      room.message(random_pic)
    if cmd.lower() == "bro" and prfx:
      room.message("http://i.imgur.com/ocCYhpL.png")
    if cmd.lower() == "lombardi" and prfx:
      room.message("https://i.imgur.com/gJJhOWh.jpg")
    if cmd.lower() == "pogchamp" and prfx:
      room.message("http://i.imgur.com/7bGsxZC.png")
    if cmd.lower() == "fap" and prfx:
      room.message("http://i.imgur.com/UZA7oDD.png")
    if cmd.lower() == "gay" and prfx:
      room.message("https://i.imgur.com/N1PVq33.png")
    if cmd.lower() == "stoned" and prfx:
      room.message("http://i.imgur.com/BXVlumD.jpg")
    if cmd.lower() == "dab" and prfx:
      room.message("https://i.imgur.com/DxFhJ5G.png")
    if cmd.lower() == "woo" and prfx:
      room.message("http://i.imgur.com/PuzhNHg.gif")
    if cmd.lower() == "poggers" and prfx:
      room.message("https://i.imgur.com/kdAeJ2i.jpg")
    if cmd.lower() == "flop" and prfx:
      room.message("https://i.imgur.com/Yqe5hFo.gif")
    if cmd.lower() == "amac" and prfx:
      data = ["https://i.imgur.com/3kblRR8.gif", "https://i.imgur.com/VTlN3CW.png"]
      random_pic = data[randint(0, len(data) -1)]
      room.message(random_pic)
    if cmd.lower() == "frosty" and prfx:
      room.message("https://i.imgur.com/8VoCV6P.png")
    if cmd.lower() == "meek" and prfx:
      room.message("FREED MEEK")
    if cmd.lower() == "birdteams" and prfx:
      room.message("https://i.imgur.com/5VOZrMw.png")
    if cmd.lower() == "suicide" and prfx:
      room.message("https://i.imgur.com/Lpu455k.png")
    if cmd.lower() == "popcorn" and prfx:
      room.message("http://i.imgur.com/8T8fm98.gif")
    if cmd.lower() == "rocky" and prfx:
      room.message("https://i.imgur.com/VlDBmj3.png")
    if cmd.lower() == "clap" and prfx:
      room.message("Clap your hands everybody for Philadelphia 76ers!")
    if cmd.lower() == "stomp" and prfx:
      room.message("Stomp your feet everybody for Philadelphia 76ers!")
    if cmd.lower() == "htc" and prfx:
      room.message("Here they come, Philadelphia, on the run, stand up and cheer!")
    if cmd.lower() == "no1" and prfx:
      room.message("Number one, Philadelphia, here they come, team of the year!")
    if cmd.lower() == "count" and prfx:
      room.message("1 2 3 4 5 Sixers!")
    if cmd.lower() == "tnuoc" and prfx:
      room.message("10 9 8 76ers!")
    if cmd.lower() == "ftc" and prfx:
      room.message("Fuck the Celtics!")
    if cmd.lower() == "doop" and prfx:
      room.message("DOOP DOOP DOOP DADADOOP DOOP DOOP")
    if cmd.lower() == "jj" and prfx and room.name == "acleenba":
      room.message("https://i.imgur.com/Fd74CjX.jpg")
    if cmd.lower() == "jj" and prfx and room.name == "csnphilly":
      room.message("SHOT! High and wide.")
    if cmd.lower() == "lgf" and prfx:
      room.message("let's go flyera")
    if cmd.lower() == "lgp" and prfx:
      room.message("Let's go Phillies!")
    if cmd.lower() == "raps" and prfx:
      room.message("http://i.imgur.com/9iBTlwm.jpg http://i.imgur.com/KsvMBgi.jpg")
    if cmd.lower() == "k" and prfx:
      if (args == "looking") or (args == "backwards"):
        resp = "https://i.imgur.com/Hh2LYHC.gif"
      else:
        resp = "https://i.imgur.com/4FcCc2Y.gif"
      room.message(resp)
    if cmd.lower() == "lavy" and prfx:
      room.message("http://i.imgur.com/V4di3qI.gif")
    if cmd.lower() == "ttp" and prfx:
      room.message("Trust the process")
    if cmd.lower() == "jingled" and prfx:
      room.message("http://i.imgur.com/uEi62i8h.jpg")
    if cmd.lower() == "belinelli" and prfx:
      room.message("https://i.imgur.com/PST9VDt.png")
    if cmd.lower() == "marco" and prfx:
      room.message("POLO!")
    if cmd.lower() == "ftp" and prfx:
      ##room.message("https://i.imgur.com/KLy5Ads.png")
      room.message("FUCK THE PENS!")
    if cmd.lower() == "crosby" and prfx:
      room.message("https://i.imgur.com/rL74UWD.png")
    if cmd.lower() == "ike" and prfx:
      room.message("https://i.imgur.com/RTApMei.png")
    if cmd.lower() == "o" and prfx:
      room.message('https://i.imgur.com/h99Ic2m.gif')
    if cmd.lower() == "kev" and prfx:
      room.message("https://i.imgur.com/WV22E7r.png")
    if cmd.lower() == "tj" and prfx:
      room.message("https://i.imgur.com/STIrrXN.png")
    if cmd.lower() == "goat" and prfx:
      ##room.message("https://i.imgur.com/STIrrXN.png")
      room.message("https://i.imgur.com/r7obJ2O.png")
    if cmd.lower() == "king" and prfx:
      room.message("where the hoes at")
    if cmd.lower() == "chop" and prfx:
      room.message(":(")
    if cmd.lower() == "panduh" and prfx:
      room.message("based panduh")
    if cmd.lower() == "woat" and prfx:
      room.message("ban goat when")
    if cmd.lower() == "banned" and prfx:
      room.message("https://i.imgur.com/xuNUZb4.png")
    if cmd.lower() == "bj" and prfx:
      room.message("https://i.imgur.com/uGFLLLt.gif")
    if cmd.lower() == "nephew" and prfx:
      room.message("https://i.imgur.com/oJ3qLRG.jpg")
    if cmd.lower() == "dance" and prfx:
      room.message('/o/')
    if cmd.lower() == "chant" and prfx:
      room.message("E! A! G! L! E! S! EAGLES!")
    if cmd.lower() == "falg" and prfx:
      room.message("https://media.discordapp.net/attachments/271047268763697153/399352313803833346/4R2Mcj1.png")
    if cmd.lower() == "gilf" and prfx:
      room.message("http://i.imgur.com/ltsesOa.jpg")
    if cmd.lower() == "baggage" and prfx:
      room.message("http://i.imgur.com/M7mvqqR.png")
    if cmd.lower() == "hype" and prfx:
      room.message("https://i.imgur.com/6QltyQ0.gif")
    if cmd.lower() == "reee" and prfx:
      room.message("https://i.imgur.com/d3JvMNf.gif")
    if cmd.lower() == "watmachine" and prfx:
      room.message("https://i.imgur.com/ITkptYv.png")
    if cmd.lower() == "leafs" and prfx:
      room.message("FUCK THE LEAFS!")
    if cmd.lower() == "metsfan" and prfx:
      room.message("mets pls")
    if cmd.lower() == "jesus" and prfx:
      room.message("nephew!")
    if cmd.lower() == "bloodhorse" and prfx:
      room.message("http://i.imgur.com/qhV8XXH.gif")
    if cmd.lower() == "sewerchat" and prfx:
      room.message("http://i.imgur.com/qhV8XXH.gif")
    if cmd.lower() == "kash" and prfx:
      room.message("https://i.imgur.com/gwnUl4i.png")
    if cmd.lower() == "bales" and prfx:
      room.message("https://i.imgur.com/frvo5Ke.png")
    if cmd.lower() == "trevis" and prfx:
      room.message("http://i.imgur.com/4Ulws9X.jpg")
    if cmd.lower() == "quiplash" and prfx:
      room.message("https://i.imgur.com/PE1ubLy.png")
    if cmd.lower() == "legionofgloom" and prfx:
      room.message("https://i.imgur.com/XdFJ1Xo.jpg")
    if cmd.lower() == "smirk" and prfx:
      room.message("https://i.imgur.com/ZpZH2A7.png")
    if cmd.lower() == "peach" and prfx:
      room.message("put on UFC NOW")
    if cmd.lower() == "peco" and prfx:
      room.message("AND THE FLYERS ARE GOING ON THE PECOOOOOOOOOOOO POWERPLAY! https://i.imgur.com/bgy1ag6.gif")
    if cmd.lower() == "brick" and prfx:
      room.message("https://i.imgur.com/x1Vy4ds.png http://memesyndicate.com/livepd")
    if cmd.lower() == "commands" and prfx:
      room.message("Incomplete list: https://github.com/acleee/acleebot")
    if cmd.lower() == "gone" and prfx:
      room.message("SWING AND A LONG DRIVE, DEEP LEFT FIELD. THAT BALL IS OUTTAAAAA HERREEEEE!")
    if cmd.lower() == "c2f" and prfx:
      fah = 9.0/5.0*Integer.parseInt(args)+32
      room.message(args)
    if cmd.lower() == "ud" and prfx:
      url = 'http://api.urbandictionary.com/v0/define?term='+args
      pls = requests.get(url).json()
      output = pls['list']
      output2 = output[0]
      definition = output2['definition']
      room.message(args+": "+definition)

    if cmd.lower() == "goal" and prfx:
      if (args == "14"):
        resp = "Sean Couturier"
      if (args == "51"):
        resp = "Valtteri Filppula"
      if (args == "28"):
        resp = "Claude Giroux"
      if (args == "53"):
        resp = "Shayne Gostisbehere"
      if (args == "3"):
        resp = "Radko Gudas"
      if (args == "8"):
        resp = "Robert Hagg"
      if (args == "11"):
        resp = "Travis Konecny"
      if (args == "21"):
        resp = "Scott Laughton"
      if (args == "15"):
        resp = "Jori Lehtera"
      if (args == "20"):
        resp = "Taylor Leier"
      if (args == "54"):
        resp = "Oskar Lindblom"
      if (args == "47"):
        resp = "Andrew MacDonald"  
      if (args == "23"):
        resp = "Brandon Manning"  
      if (args == "9"):
        resp = "Ivan Provorov"
      if (args == "19"):
        resp = "Nolan Patrick"  
      if (args == "19h"):
        resp = "Scott Hartnell"
        args = "19"
      if (args == "12"):
        resp = "Michael Raffl"
      if (args == "6"):
        resp = "Travis Sanheim"  
      if (args == "17"):
        resp = "Wayne Simmonds"  
      if (args == "93"):
        resp = "Jake Voracek"
      if (args == "40"):
        resp = "Jordan Weal"
      if (args == "22"):
        resp = "Dale Weise"
      if (args == "1"):
        resp = "Bernie Parent"
      if (args == "16"):
        resp = "Bobby Clarke"
      if (args == "88"):
        resp = "Eric Lindros"
      if (args == "10"):
        resp = "John LeClair"
      if (args == "48"):
        resp = "Danny Briere"
      if (args == "44"):
        resp = "Kimmo Timonen"
      if (args == "27"):
        resp = "Ron Hextall"
      if (args == "18"):
        resp = "Mike Richards"
      if (args == "37"):
        resp = "Eric Desjardins"
      if (args == "32"):
        resp = "Mark Streit"
      room.message("Flyers goal scored by #"+args+" "+resp+"!")

    if cmd.lower() == "gus" and prfx:
      data = ["https://i.imgur.com/MD9v228.jpg", "https://i.imgur.com/NxIxHks.jpg", "https://i.imgur.com/B8AF2kW.jpg", "https://i.imgur.com/txywtE0.jpg"]
      random_pic = data[randint(0, len(data) -1)]
      room.message(random_pic)
	  
    if cmd.lower() == "legionofdoom" and prfx:
      data = ["https://i.imgur.com/qCxFxvg.jpg", "https://i.imgur.com/cBOOBbs.jpg", "https://i.imgur.com/ArNAXMy.jpg", "https://i.imgur.com/ghAT65v.png", "https://i.imgur.com/o4bt9XY.jpg", "https://i.imgur.com/OW1wczK.jpg", "https://i.imgur.com/bPouF9z.jpg", "https://i.imgur.com/JUIsmkO.png", "https://i.imgur.com/vzfl9oZ.jpg", "https://i.imgur.com/ThbFFs2.jpg"]
      random_pic = data[randint(0, len(data) -1)]
      room.message(random_pic)
	  
    if cmd.lower() == "harry" and prfx:
      data = ["https://i.imgur.com/N0Q8O79.jpg", "https://i.imgur.com/Xyn3q7V.jpg", "https://i.imgur.com/KHlS8qU.jpg", "https://i.imgur.com/u12hN0S.jpg"]
      random_pic = data[randint(0, len(data) -1)]
      room.message(random_pic)

    if cmd.lower() == "molly" and prfx:
      data = ["https://i.imgur.com/l9moZNr.png", "https://i.imgur.com/YsTViAC.png", "https://i.imgur.com/6kHAxlZ.png", "https://i.imgur.com/f3VAfuA.png", "https://i.imgur.com/qU2PBQk.png"]
      random_pic = data[randint(0, len(data) -1)]
      room.message(random_pic)

    if cmd.lower() == "dario" and prfx:
      data = ["https://i.imgur.com/8hbwtfV.png", "https://i.imgur.com/4MrAwwn.png", "https://i.imgur.com/YETUJmw.jpg", "http://i.imgur.com/tmVHbPz.png", "https://i.imgur.com/tLKWd9M.jpg", "https://i.imgur.com/NI8d7zQ.jpg", "https://i.imgur.com/F5J2oiN.jpg", "https://i.imgur.com/CohwTgp.jpg", "https://i.imgur.com/MlAgWdP.jpg", "https://i.imgur.com/JreG2cD.jpg"]
      random_pic = data[randint(0, len(data) -1)]
      room.message(random_pic)

    if cmd.lower() == "fultz" and prfx:
      data = ["https://i.imgur.com/eGNnEMB.png", "https://i.imgur.com/JK1z3aA.jpg", "https://i.imgur.com/7KPclUS.jpg", "http://i.imgur.com/7jfDQ3F.jpg"]
      random_pic = data[randint(0, len(data) -1)]
      room.message(random_pic)
	  
    if cmd.lower() == "coinflip" and prfx:
      data = ["heads", "tails"]
      random_pic = data[randint(0, 1)]
      room.message("Just flipped a coin. It's "+random_pic+".")

    if cmd.lower() == "btc" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bitfinex/btcusd/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("BTC: currently at $"+last+", high today of $"+high+", low of $"+low+", change of %.3f" % percentage+"%")

	  
	  
    if cmd.lower() == "stock" and prfx:
      r = requests.get(url='https://api.iextrading.com/1.0/stock/'+args.lower()+'/batch?types=quote')
      x = r.json()
      y = x["quote"]
      coname = y["companyName"]
      open = str(y["open"])
      high = str(y["high"])
      low = str(y["low"])
      close = str(y["previousClose"])
      perc = y["changePercent"]*100
      if perc < 0:
         plusminus = "down"
         perc = perc*-1
      else:
         plusminus = "up"
      perc = round(perc, 2)
      pct = str(perc)	  
      last = str(y["latestPrice"])
      room.message(args.upper()+" ("+coname+") : currently at $"+last+", last opened at $"+open+", closed yesterday at $"+close+", "+plusminus+" "+pct+"% today.")

	  


    if cmd.lower() == "bch" and prfx or cmd.lower() == "bcash" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bitfinex/bchusd/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("BCH: currently at $"+last+", high today of $"+high+", low of $"+low+", change of %.3f" % percentage+"%")

    if cmd.lower() == "eth" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bitfinex/ethusd/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("ETH: currently at $"+last+", high today of $"+high+", low of $"+low+", change of %.3f" % percentage+"%")

    if cmd.lower() == "ltc" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bitfinex/ltcusd/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("LTC: currently at $"+last+", high today of $"+high+", low of $"+low+", change of %.3f" % percentage+"%")

    if cmd.lower() == "ripple" and prfx or cmd.lower() == "xrp" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bitfinex/xrpusd/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("XRP: currently at $"+last+", high today of $"+high+", low of $"+low+", change of %.3f" % percentage+"%")

    if cmd.lower() == "etc" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bitfinex/etcusd/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("ETC: currently at $"+last+", high today of $"+high+", low of $"+low+", change of %.3f" % percentage+"%")

    if cmd.lower() == "zec" and prfx or cmd.lower() == "zcash" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bitfinex/zecusd/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("ZEC: currently at $"+last+", high today of $"+high+", low of $"+low+", change of %.3f" % percentage+"%")

    if cmd.lower() == "dash" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bitfinex/dashusd/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("DASH: currently at $"+last+", high today of $"+high+", low of $"+low+", change of %.3f" % percentage+"%")
	  
    if cmd.lower() == "xmr" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bitfinex/xmrusd/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("XMR: currently at $"+last+", high today of $"+high+", low of $"+low+", change of %.3f" % percentage+"%")

    if cmd.lower() == "monero" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bitfinex/xmrusd/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("XMR: currently at $"+last+", high today of $"+high+", low of $"+low+", change of %.3f" % percentage+"%")

    if cmd.lower() == "sc" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/bittrex/scbtc/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("SIA: currently at "+last+" BTC, high today of "+high+" BTC, low of "+low+" BTC, change of %.3f" % percentage+"%")

    if cmd.lower() == "doge" and prfx:
      r = requests.get(url='https://api.cryptowat.ch/markets/kraken/dogebtc/summary')
      x = r.json()
      y = x["result"]["price"]
      z = y["change"]
      last = str(y["last"])
      high = str(y["high"])
      low = str(y["low"])
      percentage = z["percentage"]*100
      room.message("DOGE: currently at "+last+" BTC, high today of "+high+" BTC, low of "+low+" BTC, change of %.3f" % percentage+"%")



#    if cmd.lower() == "go2bed" and prfx:
 #     geturl = "http://46.228.199.201/mdoublee/memegen2/php/wrapper_oldmemegen.php?selectedscript=meme_bed_0&fucker="+args
  #    memeurl = urlopen(geturl).read()
   #   string_url = str(memeurl.strip())
    #  room.message(string_url.split("'", 2)[1])
    if cmd.lower() == "ctf" and prfx:
      geturl = "http://voo.memesyndicate.com/c2f?temp="+args
      memeurl = requests.get(geturl)
      room.message(memeurl.text)
    if cmd.lower() == "f2c" and prfx:
      geturl = "http://voo.memesyndicate.com/f2c?temp="+args
      memeurl = requests.get(geturl)
      room.message(memeurl.text)
    if cmd.lower() == "poop" and prfx:
      geturl = "http://46.228.199.201/mdoublee/memegen2/php/wrapper_oldmemegen.php?selectedscript=meme_pooper_0&fucker="+args
      memeurl = urlopen(geturl).read()
      room.message(memeurl)
    if cmd.lower() == "trash" and prfx:
      geturl = "http://46.228.199.201/mdoublee/memegen2/php/wrapper_oldmemegen.php?selectedscript=meme_trash_0&fucker="+args
      memeurl = urlopen(geturl).read()
      room.message(memeurl)
    if cmd.lower() == "hang" and prfx:
      geturl = "http://46.228.199.201/mdoublee/memegen2/php/wrapper_oldmemegen.php?selectedscript=meme_hang_0&fucker="+args
      memeurl = urlopen(geturl).read()
      room.message(memeurl)
    if cmd.lower() == "golf" and prfx:
      geturl = "http://46.228.199.201/mdoublee/memegen2/php/wrapper_oldmemegen.php?selectedscript=meme_golf_0&fucker="+args
      memeurl = urlopen(geturl).read()
      room.message(memeurl)
    if cmd.lower() == "baby" and prfx:
      geturl = "http://46.228.199.201/mdoublee/memegen2/php/wrapper_oldmemegen.php?selectedscript=meme_diapers_0&fucker="+args
      memeurl = urlopen(geturl).read()
      room.message(memeurl)
    if cmd.lower() == "penbox" and prfx:
      geturl = "http://46.228.199.201/mdoublee/memegen2/php/wrapper_oldmemegen.php?selectedscript=meme_penbox_0&fucker="+args
      memeurl = urlopen(geturl).read()
      room.message(memeurl)
    if cmd.lower() == "go2bed" and prfx:
      geturl = "http://46.228.199.201/mdoublee/memegen2/php/wrapper_oldmemegen.php?selectedscript=meme_bed_0&fucker="+args
      memeurl = urlopen(geturl).read()
      room.message(memeurl)

    if cmd.lower() == "getavi" and prfx:
        try:
            name=str(args.lower())
            room.message("http://fp.chatango.com/profileimg/"+name[0]+"/"+name[1]+"/"+name+"/full.jpg")
        except:
            room.message(args+" is not (yet) a chatango username.")    
    if cmd.lower() == "score" and prfx:
      if (args == "sixers" or args == "76ers"):
        team_id = '1610612755'
        if not team_id:
            room.message("Couldn't find the score for todays game")
        url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2017/scores/00_todays_scores.json'
        json = requests.get(url).json()
        games = json['gs']['g']
        for game in games:
            home_team_id = game['h']['tid']
            visitor_team_id = game['v']['tid']
            if home_team_id == int(team_id) or visitor_team_id == int(team_id):
                home_team_score = game['h']['s']
                visitor_team_score = game['v']['s']
                home_team_name = game['h']['tc'] + " " + game['h']['tn']
                visitor_team_name = game['v']['tc'] + " " + game['v']['tn']
                output = home_team_name + " " + str(home_team_score) + " - " + visitor_team_name + " " + str(visitor_team_score)
                room.message(output)
    if "wew" in cmd.lower() and user.name != "acleebot":
       room.message("wew")
rooms = ["acmemed", "nbcsphilly", "acmemed2"]
##rooms = ["acmemed"]
username = "acleebot"
password = ""

bot.easy_start(rooms,username,password)

