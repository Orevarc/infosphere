import logging
import random

import requests

from bfkac.decorators import command

outputs = []
logger = logging.getLogger('bfkac')

REDDIT_URL = 'http://www.reddit.com/r/{}.json'
REDDIT_URL_TOP = 'https://www.reddit.com/r/{}/top.json?sort=top&t=week'


def getReddit(subreddit, top=False):
    headers = {'user-agent': 'BFKAC'}
    if top:
        response = requests.get(REDDIT_URL_TOP.format(subreddit), headers=headers).json()
    else:
        response = requests.get(REDDIT_URL.format(subreddit), headers=headers).json()
    posts = []
    for p in response['data']['children']:
        if not (p['data']['is_self'] or p['data']['stickied']):
            posts.append(p['data'])

    if len(posts) == 0:
        return "Couldn't find anything..."
    else:
        post = random.choice(posts)
        return '{} {}'.format(post['title'], post['url'])


@command('aww')
def aww(cmd, rest, data, plugin):
    '''
        !aww
        Return a random cute image.
    '''
    link = getReddit('aww')
    outputs.append([data['channel'], link])


@command('eww')
def eww(cmd, rest, data, plugin):
    '''
        !eww
        Return a random gross bug.
    '''
    link = getReddit('whatsthisbug')
    outputs.append([data['channel'], link])


@command('hqg', 'highqualitygif')
def hqg(cmd, rest, data, plugin):
    '''
        !hqg|highqualitygif
        Return a random high quality gif.
    '''
    link = getReddit('highqualitygifs')
    outputs.append([data['channel'], link])


@command('perfectloop', 'loop')
def perfectloops(cmd, rest, data, plugin):
    '''
        !loop|perfectloop
        Return a random perfect loop.
    '''
    link = getReddit('perfectloops')
    outputs.append([data['channel'], link])


@command('woah', 'whoa')
def woahdude(cmd, rest, data, plugin):
    '''
        !whoa|woah
        Return a random mindblowing thing.
    '''
    link = getReddit('woahdude')
    outputs.append([data['channel'], link])


@command('soda', 'soda?')
def wheredidthesodago(cmd, rest, data, plugin):
    '''
        !soda|soda?
        Return a random infomercial gif.
    '''
    link = getReddit('wheredidthesodago')
    outputs.append([data['channel'], link])


@command('bro')
def animalsbeingbros(cmd, rest, data, plugin):
    '''
        !bro
        Return a random animal being a bro.
    '''
    link = getReddit('animalsbeingbros')
    outputs.append([data['channel'], link])


@command('jerk')
def animalsbeingjerks(cmd, rest, data, plugin):
    '''
        !jerk
        Return a random animal being a jerk.
    '''
    link = getReddit('animalsbeingjerks')
    outputs.append([data['channel'], link])


@command('jerkbro', 'brojerk')
def jerkbro(cmd, rest, data, plugin):
    '''
        !jerkbro|brojerk
        Return a random animal either being a bro or a jerk.
    '''
    if random.random() >= 0.5:
        link = getReddit('animalsbeingjerks')
    else:
        link = getReddit('animalsbeingbros')
    outputs.append([data['channel'], link])


@command('neat')
def neat(cmd, rest, data, plugin):
    '''
        !neat
        Return a random post from interestingasfuck.
    '''
    link = getReddit('interestingasfuck', True)
    outputs.append([data['channel'], link])


@command('its:fire:')
def itslit(cmd, rest, data, plugin):
    '''
        !its :fire:
        Return a random post from natureisfuckinglit.
    '''
    link = getReddit('natureisfuckinglit', True)
    outputs.append([data['channel'], link])
