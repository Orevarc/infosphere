# -*- coding: utf-8 -*-
import asyncio
import random
import requests

from discord.ext import commands as c


class Misc:
    '''
        Misc. commands
    '''
    def __init__(self, bot):
        self.bot = bot

    @c.command(name='catfact', aliases=['catfacts'])
    async def catfact(self):
        '''!catfact[catfacts] --> Get a 🐱 fact'''
        url = 'https://catfact.ninja/fact'

        def func():
            return requests.get(url)
        response = self.bot.loop.run_in_executor(None, func)
        while True:
            await asyncio.sleep(0.25)
            if response.done():
                response = response.result().json()
                break
        if response:
            await self.bot.say('{} - {}'.format(':smiley_cat:', response['fact']))
        else:
            await self.bot.say('Unable to get a catfact :pouting_cat:')

    @c.command(name='dog', aliases=['doggo'])
    async def dog(self, *, breed: str):
        '''!dog[doggo] <breed> --> Get a 🐶 <breed> = list; 
        <breed> = dog - Get a random dog '''
        if breed == 'list':
            url = 'https://dog.ceo/api/breeds/list/all'
        elif breed == 'dog':
            url = 'https://dog.ceo/api/breeds/image/random'
        else:
            url = 'https://dog.ceo/api/breed/{}/images/random'.format(breed)

        def func():
            return requests.get(url)
        response = self.bot.loop.run_in_executor(None, func)
        while True:
            await asyncio.sleep(0.25)
            if response.done():
                print('3')
                print(response)
                print(response.result())
                response = response.result().json()
                break
        if response.get('status') == 'success':
            if breed == 'list':
                breeds = ', '.join(list(response['message'].keys()))
                await self.bot.say(breeds)
            else:
                await self.bot.say(response['message'])
        else:
            await self.bot.say('{} - {}'.format('🌭', 'Unable to get a '))

    @c.command(name='roulette')
    async def roulette(self):
        '''!roulette --> You feeling lucky?'''
        if random.randint(0, 5):
            await self.bot.say(':gun: Click...')
        else:
            await self.bot.say(':boom: :gun: rekt')


def setup(bot):
    bot.add_cog(Misc(bot))
