import asyncio
import json
import os
import praw
import random
import requests

from discord.ext import commands as c

REDDIT_URL = 'https://www.reddit.com/r/{}.json'
REDDIT_URL_TOP = 'https://www.reddit.com/r/{}/top.json?sort=top&t=week'

reddit = praw.Reddit(
    user_agent="user-agent': 'web:infosphere:v1.0 (by (u/CrazyCrav)",
    client_id='YG1Ci57pB7pE1A',
    client_secret=os.environ['REDDIT_TOKEN']
)

class Reddit(c.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_reddit(self, subreddit, ctx, top=False):
        submissions = reddit.subreddit(subreddit).hot(limit=25)

        posts = []

        for s in submissions:
            if not (s.selftext or s.stickied):
                posts.append(s)

        if len(posts) == 0:
            await self.ctx.send("Couldn't find anything...")
        else:
            post = random.choice(posts)
            await ctx.send('{} {}'.format(post.title, post.url))

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

    @c.command(name='stunt')
    async def stunt(self, ctx):
        '''!neat --> Returns some stunts'''
        await self.get_reddit('holdmyredbull', ctx)

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
