import asyncio
import requests

from discord.ext import commands as c


class Urban:
    def __init__(self, bot):
        self.bot = bot

    @c.command(name='urban')
    async def urban(self, *, query: str):
        '''!urban <query> Get super hip definitions'''
        params = {'term': query}
        headers = {'user-agent': 'infosphere'}

        def func():
            return requests.get(
                'http://api.urbandictionary.com/v0/define',
                params=params,
                headers=headers,
            )
        response = self.bot.loop.run_in_executor(None, func)
        while True:
            await asyncio.sleep(0.25)
            if response.done():
                response = response.result().json()
                break
        results = response['list']
        if results:
            result = results[0]
            text = '\n>'.join([
                '>' + result['definition'],
                'Example:',
                result['example'],
            ])
            await self.bot.say(text)


def setup(bot):
    bot.add_cog(Urban(bot))