import logging
import textwrap

from .job import Job

logger = logging.getLogger('bfkac')


class Plugin(object):
    def __init__(self, name, bot):
        self.name = name
        self.bot = bot
        self.module = __import__(name)

        self.jobs = []
        self.register_jobs()

        if name in self.bot.config:
            logger.info('config found for: ' + name)
            self.module.config = self.bot.config[name]

        if 'setup' in dir(self.module):
            self.module.setup()

    def register_jobs(self):
        if 'crontable' in dir(self.module):
            for interval, function in self.module.crontable:
                self.jobs.append(Job(interval, eval('self.module.' + function), self))
            if self.module.crontable:
                logger.debug('{}: current crons: {}'.format(self.name, self.module.crontable))
            self.module.crontable = []
        else:
            self.module.crontable = []

    def do(self, function_name, data):
        if function_name in dir(self.module):
            # this makes the plugin fail with stack trace in debug mode
            if not self.bot.config['DEBUG']:
                try:
                    eval('self.module.' + function_name)(data)
                except:
                    logger.exception('problem in module {} {}'.format(function_name, data))
            else:
                eval('self.module.' + function_name)(data)
        elif function_name == 'process_message':
            self.process_message(data)

        if 'catch_all' in dir(self.module):
            try:
                self.module.catch_all(data)
            except:
                logger.debug('problem in catch all')

    def do_jobs(self):
        for job in self.jobs:
            job.check()

    def do_output(self):
        output = []
        while True:
            if 'outputs' in dir(self.module):
                if len(self.module.outputs) > 0:
                    logger.info('output from {}'.format(self.module))
                    output.append(self.module.outputs.pop(0))
                else:
                    break
            else:
                self.module.outputs = []
        return output

    def process_message(self, data):
        msg = data.get('text', '')
        if not msg:
            return

        if msg[0] == self.bot.prefix:
            cmd = msg[1:].split(' ', 1)
            if len(cmd) > 1:
                cmd, rest = cmd
            else:
                cmd, rest = cmd[0], ''

            if cmd == 'help':
                self.check_help(rest, data)
            else:
                self.do_command(cmd.strip().lower(), rest, data)
        else:
            self.try_rules(msg, data)

    def do_command(self, cmd, rest, data):
        commands = getattr(self.module, 'commands', {})
        if cmd in commands:
            try:
                commands[cmd](cmd, rest, data, self)
            except:
                logger.exception('Error running command: {}'.format(cmd))

    def check_help(self, cmd, data):
        commands = getattr(self.module, 'commands', {})

        docs = []
        if cmd:
            # check for single command
            fn = commands.get(cmd, None)
            docs.append(self.get_help(fn))
        elif data['channel'].startswith('D'):
            # dump all commands (DM only)
            for cmd, fn in commands.iteritems():
                docs.append(self.get_help(fn))
            docs = sorted(set(docs))
            docs.insert(0, 'Plugin {}:'.format(self.name))

        docs = '\n'.join(doc for doc in docs if doc)
        if docs:
            if 'outputs' not in dir(self.module):
                self.module.outputs = []
            self.module.outputs.append([data['channel'], docs])

    def get_help(self, command):
        doc = getattr(command, '__doc__', None)
        if not doc:
            return None

        doc = textwrap.dedent(doc).strip()
        doc = '\n>'.join(doc.splitlines())
        doc = '>{}'.format(doc)
        return doc

    def try_rules(self, msg, data):
        rules = getattr(self.module, 'rules', [])
        for rule, fn in rules:
            match = rule.search(msg)
            if match:
                try:
                    fn(msg, match, data, self)
                except:
                    logger.exception('Error running rule: {}'.format(rule))
