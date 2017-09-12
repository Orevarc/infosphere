#!/usr/bin/env python

import logging
import logging.config
import os
import sys
import yaml
from argparse import ArgumentParser

from infosphere.bot import Infosphere


def main_loop(bot):
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        logging.exception('Fatal error')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    directory = os.path.dirname(sys.argv[0])
    if not directory.startswith('/'):
        directory = os.path.abspath('{}/{}'.format(os.getcwd(), directory))

    config = yaml.load(file(args.config or 'infosphere.yaml', 'r'))
    config['DIRECTORY'] = directory

    logging_config = yaml.load(file('logging.yaml', 'r'))
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger('infosphere')

    logger.info('Starting up...')
    logger.info(directory)
    bot = Infosphere(config)

    is_daemon = config.get('DAEMON')
    if is_daemon:
        import daemon
        with daemon.DaemonContext():
            main_loop(bot)
    main_loop(bot)


if __name__ == '__main__':
    main()
