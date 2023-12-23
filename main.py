import pystyle, colr, threading, requests, tls_client, os, sys, random, json, time, string
from datetime import datetime
from colorama import Fore

with open("config.json", encoding="utf8") as f:
    config = json.load(f)
    
proxy = config.get("proxies")

tokens = open("data/tokens.txt", "r", encoding="utf8").read().splitlines()
proxy = open("data/proxies.txt", "r", encoding="utf8").read().splitlines()

blue = colr.Colr().hex("#034efc"); red = colr.Colr().hex("#ff3849"); yellow = colr.Colr().hex("#faa700"); green = colr.Colr().hex("#00b012"); purple = colr.Colr().hex("#3e3ef8"); gray = colr.Colr().hex("#4d4d4d")


class Console:

    def log(message, color, symbol):
        print("            " + (f"{gray}{datetime.now().strftime('%H:%M:%S')} {gray}({blue}{symbol}{gray}) {color}{message}"))

    def banner():
        banner = """
 ▌ ▐·▪  .▄▄ · ▄▄▄ .
▪█·█▌██ ▐█ ▀. ▀▄.▀·
▐█▐█•▐█·▄▀▀▀█▄▐▀▀▪▄
 ███ ▐█▌▐█▄▪▐█▐█▄▄▌
. ▀  ▀▀▀ ▀▀▀▀  ▀▀▀ """

        banner = pystyle.Center.XCenter(banner)
        banner = pystyle.Colorate.Vertical(pystyle.Colors.blue_to_purple, banner)
        print(banner)

class Discord:
    def __init__(self):
        self.headers = { 'authority': 'discord.com', 'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDExIiwib3NfdmVyc2lvbiI6IjEwLjAuMjI2MjEiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTc5ODgyLCJuYXRpdmVfYnVpbGRfbnVtYmVyIjozMDMwNiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==', 'x-discord-locale': 'en', 'x-debug-options': 'bugReporterEnabled', 'accept-language': 'en', 'authorization': token, 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9011 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36', 'content-type': 'application/json', 'accept': '*/*', 'origin': 'https://discord.com', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty',}

    def authorization(self, token, link):
        headers = self.headers; headers['authorization'] = token
        tkn = token.split('.')[0]
        try:
            split_url = link.split("&")
            bot_id = split_url[0].split("=")[1]
            redirect_url = split_url[1].split("=")[1]
            guild_id = split_url[4].split("=")[1]

            if proxy:
                request = requests.post(
                                f"https://discord.com/api/v9/oauth2/authorize",
                                headers=headers,
                                params={"client_id":str(bot_id), "response_type":"code", "redirect_uri": redirect_url, "scope":"identify guilds.join", "state":str(guild_id)},
                                json={"permissions":"0","authorize":True},
                                proxy={
                                    "http": "http://" + random.choice(proxies),
                                    "https": "http://" + random.choice(proxies)
                                }
                )
            else:
                request = requests.post(
                                f"https://discord.com/api/v9/oauth2/authorize",
                                headers=headers,
                                params={"client_id":str(bot_id), "response_type":"code", "redirect_uri": redirect_url, "scope":"identify guilds.join", "state":str(guild_id)},
                                json={"permissions":"0","authorize":True})

            if "location" in request.text:
                answer = request.json()["location"]
                result = requests.get(answer, headers=headers, allow_redirects=True)
                if result.status_code in [307, 403, 200, 400]: 
                    Console.log(f"Success: {tkn}", blue, "~")
                else:
                    Console.log(rr.text, yellow, ">")

        except Exception as e:
            Console.log(f"Error: {e}", red, "!")

link = str(input("Link to Discord APP: ")) # Please don't paste RestoreCord link, you need to verify your self and then paste e.g discord.com/authorize/...
for token in tokens:
    Discord.authorization(token, link)

