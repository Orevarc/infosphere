import random

import requests

from bfkac.decorators import command

outputs = []

GOOGLE_URL = 'https://www.googleapis.com/customsearch/v1'


def google_search(query, animated=False, faces=False):

    params = {
        'q': query,
        'cx': '007912693854658699103:gcpt-m5c5mu',
        'key': 'AIzaSyAtnTg85AI0W5Bnez1vB4oI64SllK3Fiz0',
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

    response = requests.get(GOOGLE_URL, params=params).json()
    images = response['items']
    image = random.choice(images)
    return image['link']


@command('img', 'image')
def img(cmd, rest, data, plugin):
    '''
        !img|image <thing>
        Search Google for a matching image.
    '''
    response = google_search(rest)
    if response:
        outputs.append([data['channel'], response])


@command('animate')
def animate(cmd, rest, data, plugin):
    '''
        !animate <thing>
        Search Google for a matching animated gif.
    '''
    response = google_search(rest, animated=True)
    if response:
        outputs.append([data['channel'], response])


@command('face')
def face(cmd, rest, data, plugin):
    '''
        !face <thing>
        Search Google for a matching face (people).
    '''
    response = google_search(rest, faces=True)
    if response:
        outputs.append([data['channel'], response])
