import asyncio
import random
import requests

from discord.ext import commands as c

REDDIT_URL = 'https://www.reddit.com/r/{}.json'
REDDIT_URL_TOP = 'https://www.reddit.com/r/{}/top.json?sort=top&t=week'


class Reddit(c.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_reddit(self, subreddit, ctx, top=False):
        headers = {'user-agent': 'infosphere'}

        def func():
            if top:
                return requests.get(
                    REDDIT_URL_TOP.format(subreddit), headers=headers)
            else:
                return requests.get(
                    REDDIT_URL.format(subreddit), headers=headers)
        loop = asyncio.get_event_loop()
        response = asyncio.loop.run_in_executor(None, func)
        while True:
            await asyncio.sleep(0.25)
            if response.done():
                response = response.result().json()
                break
        posts = []
        for p in response['data']['children']:
            if not (p['data']['is_self'] or p['data']['stickied']):
                posts.append(p['data'])

        if len(posts) == 0:
            await self.ctx.send("Couldn't find anything...")
        else:
            post = random.choice(posts)
            await self.ctx.send('{} {}'.format(post['title'], post['url']))

    @c.command(name='aww')
    async def aww(self, ctx):
        '''!aww --> Returns a random cute image '''
        await self.get_reddit('aww', ctx)

    @c.command(name='eww')
    async def eww(self, ctx):
        '''!eww --> Returns a :bug:'''
        await self.get_reddit('whatsthisbug', ctx)

    @c.command(name='loop', aliases=['perfectloop'])
    async def loop(self, ctx):
        '''!loop[perfectloop] --> Returns nice loop'''
        await self.get_reddit('perfectloops', ctx)

    @c.command(name='woah', aliases=['whoa'])
    async def woah(self, ctx):
        '''!woah[whoa] --> Returns some cool stuff'''
        await self.get_reddit('woahdude', ctx)

    @c.command(name='soda')
    async def soda(self, ctx):
        '''!soda --> Returns an infomercial taken out of context'''
        await self.get_reddit('wheredidthesodago', ctx)

    @c.command(name='neat')
    async def neat(self, ctx):
        '''!neat --> Returns some neat stuff'''
        await self.get_reddit('interestingasfuck', ctx)

    @c.command(name='its🔥')
    async def itslit(self, ctx):
        '''!its:fire: --> Returns some lit nature'''
        await self.get_reddit('natureisfuckinglit', ctx)

    @c.command(name='pubg')
    async def pubg(self, ctx):
        '''!pubg --> Returns some PUBG stuff'''
        await self.get_reddit('pubattlegrounds', ctx)

    @c.command(name='dank')
    async def dank(self, ctx):
        '''!dank --> 🅱️ank'''
        await self.get_reddit('dankmemes', ctx)


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

