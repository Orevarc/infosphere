import asyncio
import random
import requests

from discord.ext import commands as c

REDDIT_URL = 'https://www.reddit.com/r/{}.json'
REDDIT_URL_TOP = 'https://www.reddit.com/r/{}/top.json?sort=top&t=week'


class Reddit:
    def __init__(self, bot):
        self.bot = bot

    async def get_reddit(self, subreddit, top=False):
        headers = {'user-agent': 'infosphere'}

        def func():
            if top:
                print('top')
                return requests.get(
                    REDDIT_URL_TOP.format(subreddit), headers=headers)
            else:
                print('not top')
                return requests.get(
                    REDDIT_URL.format(subreddit), headers=headers)
        response = self.bot.loop.run_in_executor(None, func)
        print(response)
        while True:
            await asyncio.sleep(0.25)
            print('loop')
            if response.done():
                print("HERE")
                print(response)
                response = response.result().json()
                break
        posts = []
        for p in response['data']['children']:
            if not (p['data']['is_self'] or p['data']['stickied']):
                posts.append(p['data'])

        if len(posts) == 0:
            await self.bot.say("Couldn't find anything...")
        else:
            post = random.choice(posts)
            await self.bot.say('{} {}'.format(post['title'], post['url']))

    @c.command(name='aww')
    async def aww(self):
        '''!aww --> Returns a random cute image '''
        await self.get_reddit('aww')

    @c.command(name='eww')
    async def eww(self):
        '''!eww --> Returns a :bug:'''
        await self.get_reddit('whatsthisbug')

    @c.command(name='loop', aliases=['perfectloop'])
    async def loop(self):
        '''!loop[perfectloop] --> Returns nice loop'''
        await self.get_reddit('perfectloops')

    @c.command(name='woah', aliases=['whoa'])
    async def woah(self):
        '''!woah[whoa] --> Returns some cool stuff'''
        await self.get_reddit('woahdude')

    @c.command(name='soda')
    async def soda(self):
        '''!soda --> Returns an infomercial taken out of context'''
        await self.get_reddit('wheredidthesodago')

    @c.command(name='neat')
    async def neat(self):
        '''!neat --> Returns some neat stuff'''
        await self.get_reddit('interestingasfuck')

    @c.command(name='its🔥')
    async def itslit(self):
        '''!its:fire: --> Returns some lit nature'''
        await self.get_reddit('natureisfuckinglit')

    @c.command(name='pubg')
    async def pubg(self):
        '''!pubg --> Returns some PUBG stuff'''
        await self.get_reddit('pubattlegrounds')


def setup(bot):
    bot.add_cog(Reddit(bot))

# @command('bro')
# def animalsbeingbros(cmd, rest, data, plugin):
#     '''
#         !bro
#         Return a random animal being a bro.
#     '''
#     link = getReddit('animalsbeingbros')
#     outputs.append([data['channel'], link])


# @command('jerk')
# def animalsbeingjerks(cmd, rest, data, plugin):
#     '''
#         !jerk
#         Return a random animal being a jerk.
#     '''
#     link = getReddit('animalsbeingjerks')
#     outputs.append([data['channel'], link])


# @command('jerkbro', 'brojerk')
# def jerkbro(cmd, rest, data, plugin):
#     '''
#         !jerkbro|brojerk
#         Return a random animal either being a bro or a jerk.
#     '''
#     if random.random() >= 0.5:
#         link = getReddit('animalsbeingjerks')
#     else:
#         link = getReddit('animalsbeingbros')
#     outputs.append([data['channel'], link])

