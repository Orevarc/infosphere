import asyncio
import json
import random
import requests

from discord.ext import commands as c

GOOGLE_URL = 'https://www.googleapis.com/customsearch/v1'


class Google:
    """
    """
    def __init__(self, bot):
        self.bot = bot
    
    async def google_search(self, query, animated=False, faces=False):
        print('Google search')

        def func():
            return requests.get(GOOGLE_URL, params=params)
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
        if animated:
            params.update({
                'fileType': 'gif',
                'hq': 'animated',
                'tbs': 'itp:animated',
            })
        if faces:
            params['imgType'] = 'face'
        response = self.bot.loop.run_in_executor(None, func)
        while True:
            await asyncio.sleep(0.25)
            if response.done():
                response = response.result().json()
                break
        images = response['items']
        image = random.choice(images)
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

    @c.command(name="face")
    async def face(self, *, query: str):
        """One free random image."""
        print('face')
        await self.google_search(query, faces=True)


def setup(bot):
    bot.add_cog(Google(bot))