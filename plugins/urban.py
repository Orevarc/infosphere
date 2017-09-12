import requests

from bfkac.decorators import command

outputs = []


@command('urban')
def urban(cmd, rest, data, plugin):
    '''
        !urban <thing>
        Find a slang definition for the given term.
    '''
    params = {'term': rest}
    headers = {'user-agent': 'BFKAC'}
    results = requests.get(
        'http://api.urbandictionary.com/v0/define',
        params=params,
        headers=headers,
    ).json()['list']

    if results:
        result = results[0]
        outputs.append([data['channel'], '\n>'.join([
            '>' + result['definition'],
            'Example:',
            result['example'],
        ])])
