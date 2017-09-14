# -*- coding: utf-8 -*-
import asyncio
import random
import re

import requests

from infosphere.decorators import (
    command,
    hear,
)

from discord.ext import commands as c

EXCUSES = {
    'developer': (
        "That's weird…",
        "It's never done that before.",
        "It worked yesterday.",
        "How is that possible?",
        "It must be a hardware problem.",
        "What did you type in wrong to get it to crash?",
        "There is something funky in your data.",
        "I haven't touched that module in weeks!",
        "You must have the wrong version.",
        "It's just some unlucky coincidence.",
        "I can't test everything!",
        "THIS can't be the source of THAT.",
        "It works, but it hasn't been tested.",
        "Somebody must have changed my code.",
        "Did you check for a virus on your system?",
        "Even though it doesn't work, how does it feel?",
        "You can't use that version on your system.",
        "Why do you want to do it that way?",
        "Where were you when the program blew up?",
        "It works on my machine.",
    ),
    'designer': (
        "60fps or GTFO",
        "Are you looking at it in IE or something?",
        "Because that's not my design style",
        "Did you try hitting refresh?",
        "I didn't get a change request for that.",
        "I didn't mock it up that way.",
        "I didn't get a change request for that",
        "I didn't mock it up that way",
        "I don't think that's very user friendly.",
        "I don't think this is empowering enough",
        "I don't “design”, I architect empowering experiences",
        "If the user can't figure this out, they're an idiot",
        "If they don't have JavaScript turned on, it's their own damn fault",
        "It looked fine in the mockups",
        "It only looks bad if it's not on Retina.",
        "It wasn't designed for that kind of content.",
        "It wasn't designed to work with this content.",
        "I'm so over Material",
        "Jony wouldn't do it like this.",
        "Josef Müller-Brockmann.",
        "Just put a long shadow on it",
        "Just put some gridlines on it",
        "No one uses IE anyway.",
        "No, that would break the vertical rhythm",
        "That must be a server thing",
        "That won't fit the grid.",
        "That won't fit the grid",
        "That's a dark pattern.",
        "That's a developer thing.",
        "That's not a recognised design pattern.",
        "That's not how I designed it.",
        "That's not in the wireframes.",
        "That's not what the research says.",
        "That's way too flat.",
        "That's way too skeuomorphic.",
        "That's a developer thing",
        "That's not a recognised design pattern",
        "That's not in our style guide",
        "That's not in the wireframes",
        "That's not what the research says",
        "That's way too flat",
        "That's way too skeuomorphic",
        "The developer must have changed it",
        "The users might not notice it, but they'll feel it.",
        "The users will never notice that",
        "These brand guidelines are shit",
        "This animation's a bit janky, maybe we should reinvent the DOM",
        "Who uses alt tags anymore?",
        "You wouldn't get it, it's a design thing.",
    ),
}

LULZ = {
    'kirsten': (
        'Who?',
    ),
    'erika': (
        'http://i1262.photobucket.com/albums/ii603/quirkycookery2/eatingcereal.gif',
        'https://s3.amazonaws.com/ksr/avatars/159167/410911_10150625529887690_515337689_9454751_1288989939_o.small.jpg',
        'http://static.fjcdn.com/pictures/woll_758da4_2579535.jpg',
        'http://i.imgur.com/h2x7B.gif',
        'http://i1.kym-cdn.com/entries/icons/original/000/010/711/kim-jon-il-tiny-hand.jpg',
        'http://i0.kym-cdn.com/photos/images/original/000/015/694/Woll_Smoth_Carousel_by_nik_pwns.gif',
        'http://thechive.files.wordpress.com/2013/06/one-tiny-hand-funny-3.jpg?w=500&h=366',
        'http://media-cache-ec0.pinimg.com/236x/62/1d/99/621d99b063ba452fceef571d8086ebf0.jpg'
        'https://s3.amazonaws.com/uploads.hipchat.com/63813/689353/NtlCqKGMkD6kgyZ/upload.png',
        'http://i3.kym-cdn.com/photos/images/newsfeed/000/579/023/9d2.jpg',
        'https://s3.amazonaws.com/uploads.hipchat.com/63813/467201/JwmuDNEMFsoe6Ny/Screen%20Shot%202014-05-23%20at%204.59.16%20PM.png',
        'http://i1.kym-cdn.com/photos/images/original/000/307/779/d5e.jpg',
        'http://i0.kym-cdn.com/photos/images/original/000/307/780/b31.png',
        'http://i2.kym-cdn.com/photos/images/original/000/564/757/e08.jpg',
        'https://s3.amazonaws.com/uploads.hipchat.com/63813/467201/uFvBpebszJdQyXV/Screen%20Shot%202014-05-23%20at%204.58.00%20PM.png',
        'http://static.fjcdn.com/pictures/why+does+this+make+me+laugh_d2fad1_3081956.jpg',
        'http://i1.ytimg.com/vi/lAop8SyJ0aY/hqdefault.jpg',
        'http://oi46.tinypic.com/5trlnm.jpg',
        'http://www.funniestmemes.com/wp-content/uploads/2014/03/Funniest_Memes_why-have-you-betrayed-me-father_11066.jpeg',
        'http://img37.imageshack.us/img37/7044/oprahbees.gif',
        'http://swartoon.com/assets/the_kingdom_is_you.png',
        'http://www.sanitaryum.com/wp-content/uploads/2012/05/Subway-Door-FAIL-GIF.gif',
        'https://i.chzbgr.com/maxW500/7311480320/h6127B758/',
        'http://s292.photobucket.com/user/nugentrk/media/Public/treadmill-fail-o.gif.html',
        'http://102.imagebam.com/download/aWEly9aUlk2Psth452Rzgg/21149/211482421/treadmill%20wipeout.gif',
        'http://gifrific.com/wp-content/uploads/2013/10/Treadmill-Fail-Background-of-News-Report.gif',
        'http://stevekaczynski.com/wp-content/uploads/2011/05/workitoutp1.gif',
        'http://i3.kym-cdn.com/photos/images/newsfeed/000/637/352/057.gif',
        'http://i2.kym-cdn.com/photos/images/newsfeed/000/706/198/d62.gif',
        'https://s3.amazonaws.com/uploads.hipchat.com/63813/467211/WeZeBxUIU0XaXhf/the_kingdom_is_you.gif',
        'https://s3.amazonaws.com/uploads.hipchat.com/63813/467211/3k5jvRnypEmPjQE/swartoonalisa.gif',
        'https://s3.amazonaws.com/uploads.hipchat.com/63813/467211/jYKGmmKriazWDjC/test.gif',
        'https://s3.amazonaws.com/uploads.hipchat.com/63813/467205/iu8yWd7vnIQdbWU/changogodno.gif',
        'https://lh4.googleusercontent.com/-9AM6u-R9n-A/U5LXbq6YNrI/AAAAAAAAARk/kxBfq23uhTM/tumblr_msgxi3nLHK1sf32hdo1_500.gif',
        'https://s3.amazonaws.com/uploads.hipchat.com/63813/467205/38kSsYMpJzt5Ssb/wat.jpg',
    ),
    'zeid': (
        'http://s3.amazonaws.com/inarticles/95d21dce12369f4af532e9c7cf09237e.gif',
        'http://cdn1.sbnation.com/imported_assets/2031083/h0s0F.gif',
        'http://gamereax.com/wp-content/uploads/2013/04/ROBFORD.gif',
        'http://i.imgur.com/jNIwB26.gif',
        'http://d3819ii77zvwic.cloudfront.net/wp-content/uploads/2013/12/ROBFORD10.gif',
    ),
    'dylan': (
        'Who?',
    ),
    'mike': (
        'https://toshironoronin.files.wordpress.com/2012/09/tobias-never-nude.jpg',
        'http://25.media.tumblr.com/tumblr_m2qh9zuSyV1qarqrxo1_500.gif',
        'http://images6.fanpop.com/image/polls/1281000/1281226_1379632101069_full.jpg',
        'http://25.media.tumblr.com/tumblr_lput6soGPu1qi23vqo1_500.png',
        'http://vignette2.wikia.nocookie.net/arresteddevelopment/images/a/ab/Arrested-development_(6).jpg/revision/latest?cb=20130521213519',
        'http://images.ftw.usatoday.com/wp-content/uploads/2013/05/tobias-headshot.png',
        'https://media1.giphy.com/media/QazAqN1wtdQRO/200_s.gif',
    ),
    'saad': (
        'http://i.imgur.com/VNQBOMy.gif',
    ),
    'abdel': (
        'https://bonusly-fog.s3.amazonaws.com/uploads/bonus_image/image/57b76f33076f9136c648aa23/hula.gif',
    ),
    'everyone': (
        'https://bonusly-fog.s3.amazonaws.com/uploads/bonus_image/image/57b76f33076f9136c648aa23/hula.gif',
    ),
}

RAGE = {
    'kirsten': (
        'Who?',
    ),
}

HHHEHEHES = (
    'http://new1.fjcdn.com/comments/Hhhehehe+_2b20af1352c0ffe4e63759d6df0814ed.jpg',
    'http://i1.kym-cdn.com/photos/images/original/000/804/850/999.gif',
    'http://i3.kym-cdn.com/photos/images/original/000/826/014/528.jpg',
    'http://i2.kym-cdn.com/photos/images/facebook/000/804/876/aa3.jpg',
    'http://i2.kym-cdn.com/photos/images/original/000/804/867/945.jpg',
    'http://www.goodmeme.net/wp-content/uploads/2014/08/laughing-lizard-in-different-countries_o_3637793-240x113.jpg',
    'http://media.giphy.com/media/LpgwWz79mqCE8/giphy.gif',
    'http://i.imgur.com/zxW7DLw.jpg',
    'http://i0.kym-cdn.com/photos/images/original/000/804/851/ee2.png',
    'http://i.imgur.com/IcFDAGq.png',
    'http://img.photobucket.com/albums/v236/Kaiser0929/que10/hhhehehe_whale.png~original',
    'http://i.imgur.com/ubo9nSR.png',
    'http://i.imgur.com/HFn2EH4.jpg',
    'http://i2.kym-cdn.com/photos/images/facebook/000/804/873/d75.png',
    'http://i2.kym-cdn.com/photos/images/newsfeed/000/804/904/716.png',
    'http://i2.kym-cdn.com/photos/images/facebook/000/836/623/82d.jpg',
    'http://i1.kym-cdn.com/photos/images/original/000/804/906/b31.jpg',
    'http://i1.kym-cdn.com/photos/images/newsfeed/000/804/902/735.jpg',
    'http://i3.kym-cdn.com/photos/images/original/000/804/871/691.jpg',
    'http://i2.kym-cdn.com/photos/images/newsfeed/000/809/615/dbe.jpg',
    'http://i1.kym-cdn.com/photos/images/facebook/000/804/879/9e9.jpg',
    'http://24.media.tumblr.com/tumblr_me811aaPTb1qdsjz4o7_500.jpg',
    'http://i.imgur.com/fDh86.jpg',
    'http://i3.kym-cdn.com/photos/images/newsfeed/000/804/882/5cb.png',
    'http://i2.kym-cdn.com/photos/images/newsfeed/000/804/887/1c4.jpg',
)


THE_BUTT_RE = re.compile(r'\bthe\s+cloud\b', re.I)
BUTT_RE = re.compile(r'\bcloud\b', re.I)
HORSE_RE = re.compile(r'\bforce\b', re.I)
BAD_MENTION_RE = re.compile(r'@?(channel|here):?\s*', re.I)


# @hear(r'\bbeads\b')
# def beads(msg, match, data, plugin):
#     outputs.append([data['channel'], 'Bees??'])


# @hear(r'\b(cloud|force)\b')
# def butts(msg, match, data, plugin):
#     butt_msg = THE_BUTT_RE.sub('my butt', msg)
#     butt_msg = BUTT_RE.sub('butt', butt_msg)
#     butt_msg = HORSE_RE.sub('horse', butt_msg)
#     butt_msg = BAD_MENTION_RE.sub('', butt_msg)
#     butt_msg = 'more like ' + butt_msg
#     outputs.append([data['channel'], butt_msg])


# @hear(r'h*he(he)+')
# def hehehe(msg, match, data, plugin):
#     link = '{}?spam{}'.format(random.choice(HHHEHEHES), random.random())
#     outputs.append([data['channel'], link])


# @hear(r'\bprobably\s+a\s+bad\s+idea\b')
# def probablyabadidea(msg, match, data, plugin):
#     outputs.append([data['channel'], 'https://lh4.googleusercontent.com/-9AM6u-R9n-A/U5LXbq6YNrI/AAAAAAAAARk/kxBfq23uhTM/tumblr_msgxi3nLHK1sf32hdo1_500.gif?spam=' + random.random()])


# @hear(r'\bbees\b')
# def bees(msg, match, data, plugin):
#     outputs.append([data['channel'], "http://www.wired.com/wp-content/uploads/images_blogs/underwire/2013/01/oprahbees.gif"])


# @command('mike')
# def mike(cmd, rest, data, plugin):
#     outputs.append([data['channel'], 'https://dl.dropboxusercontent.com/u/10038332/funny_faces/isc65wdsVJP6sKYqb.gif'])


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
# @command('excuse')
# def excuse(cmd, rest, data, plugin):
#     '''
#         !excuse <name>
#         Return an excuse for given person (if they have any)
#     '''
#     if rest in EXCUSES:
#         ex = random.choice(EXCUSES[rest])
#         outputs.append([data['channel'], ex])


# @command('showmethebeers', 'smtb')
# def showmethebeers(cmd, rest, data, plugin):
#     outputs.append([data['channel'], ':beer:' * random.randint(1, 12)])


# @command('showmethepizzas', 'smtpi')
# def showmethepizzas(cmd, rest, data, plugin):
#     outputs.append([data['channel'], ':pizza:' * random.randint(1, 12)])


# @command('showmemic')
# def showmemic(cmd, rest, data, plugin):
#     outputs.append([data['channel'], ':microphone:' * random.randint(1, 12)])
