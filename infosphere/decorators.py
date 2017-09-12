import functools
import inspect
import re


def get_module():
    frame = inspect.stack()[2]
    module = inspect.getmodule(frame[0])
    return module


def hear(*triggers):
    def _dec(f):
        module = get_module()
        if 'rules' not in module.__dict__:
            module.rules = []

        for trigger in triggers:
            rule = re.compile(trigger, re.I | re.S | re.M)
            module.rules.append((rule, f))

        @functools.wraps(f)
        def _wrap(*args, **kwargs):
            return f(*args, **kwargs)
        return _wrap
    return _dec


def command(*triggers):
    def _dec(f):
        module = get_module()
        if 'commands' not in module.__dict__:
            module.commands = {}

        for trigger in triggers:
            module.commands[trigger] = f

        @functools.wraps(f)
        def _wrap(*args, **kwargs):
            return f(*args, **kwargs)
        return _wrap
    return _dec
