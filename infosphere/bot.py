import glob
import logging
import os
import sys
import time

from slackclient import SlackClient

from .plugin import Plugin

logger = logging.getLogger('bfkac')


class BotFormerlyKnownAsChangobot(object):
    def __init__(self, config):
        self.last_ping = 0
        self.token = config['SLACK_TOKEN']
        self.bot_plugins = []
        self.slack_client = None

        self.config = config
        self.id = config['SLACK_ID']
        self.channel_blacklist = config['CHANNEL_BLACKLIST']
        self.user_blacklist = config['USER_BLACKLIST']
        self.user_blacklist.append(self.id)
        self.prefix = config['COMMAND_PREFIX']

    def connect(self):
        '''Convenience method that creates Server instance'''
        self.slack_client = SlackClient(self.token)
        self.slack_client.rtm_connect()

    def start(self):
        self.connect()
        self.load_plugins()

        while True:
            for reply in self.slack_client.rtm_read():
                self.input(reply)
            self.crons()
            self.output()
            self.autoping()
            time.sleep(.1)

    def autoping(self):
        # hardcode the interval to 3 seconds
        now = int(time.time())
        if now > self.last_ping + 3:
            self.slack_client.server.ping()
            self.last_ping = now

    def input(self, data):
        if (not data.get('type') or
                data.get('channel') in self.channel_blacklist or
                data.get('user') in self.user_blacklist or
                data.get('subtype') == 'bot_message'):
            return

        if 'type' in data:
            function_name = 'process_' + data['type']
            logger.debug('got {}'.format(function_name))
            for plugin in self.bot_plugins:
                plugin.register_jobs()
                plugin.do(function_name, data)

    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = self.slack_client.server.channels.find(output[0])
                if channel is not None and output[1] is not None:
                    if limiter:
                        time.sleep(.1)
                        limiter = False
                    message = output[1].encode('utf-8', 'ignore')
                    channel.send_message('{}'.format(message))
                    limiter = True

    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()

    def load_plugins(self):
        directory = self.config['DIRECTORY']
        for plugin in glob.glob(directory + '/plugins/*'):
            sys.path.insert(0, plugin)
            sys.path.insert(0, directory + '/plugins/')

        plugins = glob.glob(directory + '/plugins/*.py') + glob.glob(directory + '/plugins/*/*.py')
        for plugin in plugins:
            if not os.path.basename(plugin).startswith('_'):
                logger.info(plugin)
                name = plugin.split('/')[-1][:-3]
                self.bot_plugins.append(Plugin(name, self))
