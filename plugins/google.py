# import random

import requests

# from infosphere.decorators import command

# outputs = []

# GOOGLE_URL = 'https://www.googleapis.com/customsearch/v1'


# def google_search(query, animated=False, faces=False):

#     params = {
#         'q': query,
#         'cx': '007912693854658699103:gcpt-m5c5mu',
#         'key': 'AIzaSyAtnTg85AI0W5Bnez1vB4oI64SllK3Fiz0',
#         # 'key': 'AIzaSyAYxaFE2ITGyu_0p8t1T_aHFUmzVuuR8to',
#         'fields': 'items(link)',
#         'searchType': 'image',
#         'safe': 'high',
#     }
#     if animated:
#         params.update({
#             'fileType': 'gif',
#             'hq': 'animated',
#             'tbs': 'itp:animated',
#         })
#     if faces:
#         params['imgType'] = 'face'

#     response = requests.get(GOOGLE_URL, params=params).json()
#     images = response['items']
#     image = random.choice(images)
#     return image['link']


# @command('img', 'image')
# def img(cmd, rest, data, plugin):
#     '''
#         !img|image <thing>
#         Search Google for a matching image.
#     '''
#     response = google_search(rest)
#     if response:
#         outputs.append([data['channel'], response])


# @command('animate')
# def animate(cmd, rest, data, plugin):
#     '''
#         !animate <thing>
#         Search Google for a matching animated gif.
#     '''
#     response = google_search(rest, animated=True)
#     if response:
#         outputs.append([data['channel'], response])


# @command('face')
# def face(cmd, rest, data, plugin):
#     '''
#         !face <thing>
#         Search Google for a matching face (people).
#     '''
#     response = google_search(rest, faces=True)
#     if response:
#         outputs.append([data['channel'], response])


import asyncio
import json
import random

from discord.ext import commands as c

GOOGLE_URL = 'https://www.googleapis.com/customsearch/v1'

class Google:
    """
    """
    def __init__(self, bot):
        self.bot = bot
    
    async def google_search(self, query, animated=False, faces=False):
        print('Google search')
        """Search Imgur for (almost) anything."""
        params = {
            'q': query,
            'cx': '018359127822141064231:fkurjdg6grs',
            'key': 'AIzaSyCzjmdz6z-fPzLHcEItOXTftk6Cege7ez0',
            # 'key': 'AIzaSyAYxaFE2ITGyu_0p8t1T_aHFUmzVuuR8to',
            'fields': 'items(link)',
            'searchType': 'image',
            'safe': 'high',
        }
        print('0')
        if animated:
            params.update({
                'fileType': 'gif',
                'hq': 'animated',
                'tbs': 'itp:animated',
            })

        def func():
            return requests.get(GOOGLE_URL, params=params)
        print('1')
        response = self.bot.loop.run_in_executor(None, func)
        print('2')
        while True:
            await asyncio.sleep(0.25)
            print('3')
            if response.done():
                print('4')
                response = response.result().json()
                print(response)
                break
        images = response['items']
        image = random.choice(images)
        print("LINK")
        print("".format(image['link']))
        await self.bot.say(image.get("link", None))

    @c.command(name="animate")
    async def animate(self, *, query: str):
        print('inside')
        """Search Imgur for (almost) anything."""
        await self.google_search(query, animated=True)

    @c.command(name="img", aliases=["image"])
    async def img(self, *, query: str):
        """One free random image."""
        print('img')
        await self.google_search(query)


def setup(bot):
    bot.add_cog(Google(bot))