import logging
import time

logger = logging.getLogger('bfkac')


class Job(object):
    def __init__(self, interval, function, plugin):
        self.plugin = plugin
        self.function = function
        self.interval = interval
        self.lastrun = 0

    def __str__(self):
        return '{} {} {}'.format(self.function, self.interval, self.lastrun)

    def __repr__(self):
        return self.__str__()

    def check(self):
        if self.lastrun + self.interval < time.time():
            if not self.plugin.bot.config['DEBUG']:
                try:
                    self.function()
                except:
                    logger.exception(
                        'error running job: {}'.format(self.function))
            else:
                self.function()
            self.lastrun = time.time()
