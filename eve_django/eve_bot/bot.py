# A sample bot

import datetime
import optparse
import shlex
import logging
from mucbot import MUCJabberBot
from jabberbot import botcmd
from optparse import make_option
from functools import wraps
from django.contrib.humanize.templatetags.humanize import intword as _intword, \
                                                          intcomma as _intcomma, \
                                                          naturaltime as _naturaltime

from eve_sde.models import Item, Region, System, Station


UTC_OFFSET = datetime.timedelta(hours=-5)

logger = logging.getLogger('jabberbot')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
logger.addHandler(ch)


#########################################
## Magical Command + Options Decorator ##
#########################################

def command(*_options, **kwargs):
    #Refactor me, use functools
    if not kwargs and len(_options) == 1 and hasattr(_options[0], '__call__'):
        f = _options[0]
        f = botcmd(f)
        return f
    else:
        def options_wrapper(func):
            parser = Options.build_parser(name=func.func_name,
                                          options=sorted(_options, key=lambda o: o.dest))

            @wraps(func)
            def func_wrapper(self, mess, raw_args):
                func_options = process_args(raw_args, parser=parser, **kwargs)
                return func(self, mess, raw_args, func_options)

            func_wrapper = botcmd(func_wrapper)
            func_wrapper._options = _options
            func_wrapper.__doc__ = (func.__doc__ or "") + parser.format_help()

            return func_wrapper

    return options_wrapper


##########################
## Options Helper class ##
##########################

class Options(object):

    #Generic options
    count = make_option("-c", "--count", dest="count", action="store", type="int", default=4,
                        help="Limits the number of results.")
    strict_match = make_option("--strict", dest="partial_match", action="store_false", default=True,
                               help="Disable partial name matching.")

    @classmethod
    def build_parser(self, name=None, parser=None, options=[]):

        if parser is None:
            parser = optparse.OptionParser()

        for option in options:
            parser.add_option(option)

        if name:
            parser.prog = name

        return parser


class EveBot(MUCJabberBot):

    def __init__(self, *args, **kwargs):
        super(EveBot, self).__init__(*args, **kwargs)

    @command(Options.strict_match, Options.count, lookup_items=True)
    def items(self, mess, raw_args, options):

        items = sorted(list(options.items[0:options.count]), key=lambda item: item.name)

        if len(items) <= 8:
            join_str = "\n"
        else:
            join_str = ", "

        message = "\n" + join_str.join([item.name for item in items])

        return self.send_simple_reply(mess, message)

    @command(Options.strict_match, lookup_items=True)
    def description(self, mess, raw_args, options):

        item = options.item

        return self.send_simple_reply(mess, "\n%s Description:\n%s" % (item.name, item.description,))

    @command
    def hello_bot(self, mess, raw_args):

        reply = "Hello! You just said: '%s'" % raw_args

        return self.send_simple_reply(mess, reply)


#######################
##  Helper Functions ##
#######################


def intword(num):
    return _intword(round(num, 2))


def intcomma(num):
    return _intcomma(round(num, 2))


def naturaltime(dt, offset=True):
    if offset is True:
        return _naturaltime(dt + UTC_OFFSET)
    else:
        return _naturaltime(dt)


def pretty_num(num):

    try:
        num = intword(num)
        try:
            num = intcomma(num)
        except:
            pass
    except:
        pass
    return num


def process_args(raw_args, parser=None, lookup_items=False, options=[], **kwargs):
    #Really needs to be refactored

    if not parser:
        parser = Options.build_parser(options=[Options.help] + options)

    opts, args = parser.parse_args(shlex.split(str(raw_args)))

    for key, value in kwargs.items():
        setattr(opts, key, value)

    #Will be used to determine location
    if getattr(opts, "region", None) is not None:
        pass

    if getattr(opts, "system", None) is not None:
        pass

    if getattr(opts, "station", None) is not None:
        pass

    if lookup_items and args:

        name_part = " ".join(args)

        if name_part.lower() == 'plex':
            name_part = "30 Day Pilot's License Extension (PLEX)"
        if opts.partial_match:
            opts.items = Item.objects.filter(name__icontains=name_part)
        else:
            opts.items = Item.objects.filter(name__startswith=name_part)

        opts.items = opts.items.filter(is_published=True).order_by('name')
        opts.item = opts.items[0]

    opts.args = args
    opts.raw_args = raw_args

    return opts


########################
##  Testing Functions ##
########################


def test_bot():
    username = 'username@conference.goonfleet.com'
    password = ''
    nickname = 'eve-code-sample-bot'
    chatroom1 = 'eve-trader@conference.goonfleet.com'
    run_mucbot(username, password, nickname, [chatroom1, ])


def run_mucbot(username, password, nickname, chatrooms):

    mucbot = EveBot(username, password, only_direct=False)
    for chatroom in chatrooms:
        mucbot.join_room(chatroom, nickname)
    mucbot.serve_forever()
