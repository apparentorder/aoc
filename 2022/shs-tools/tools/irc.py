from time import sleep

from .schedule import Scheduler
from .simplesocket import ClientSocket
from .types import StrOrNone
from datetime import timedelta
from enum import Enum
from typing import Callable, Dict, List, Union


class ServerMessage(str, Enum):
    RPL_WELCOME = "001"
    RPL_YOURHOST = "002"
    RPL_CREATED = "003"
    RPL_MYINFO = "004"
    RPL_ISUPPORT = "005"
    RPL_BOUNCE = "010"
    RPL_UNIQID = "042"
    RPL_TRACELINK = "200"
    RPL_TRACECONNECTING = "201"
    RPL_TRACEHANDSHAKE = "202"
    RPL_TRACEUNKNOWN = "203"
    RPL_TRACEOPERATOR = "204"
    RPL_TRACEUSER = "205"
    RPL_TRACESERVER = "206"
    RPL_TRACENEWTYPE = "208"
    RPL_TRACECLASS = "209"
    RPL_TRACERECONNECT = "210"
    RPL_STATSLINKINFO = "211"
    RPL_STATSCOMMANDS = "212"
    RPL_STATSCLINE = "213"
    RPL_STATSNLINE = "214"
    RPL_STATSILINE = "215"
    RPL_STATSKLINE = "216"
    RPL_STATSYLINE = "218"
    RPL_ENDOFSTATS = "219"
    RPL_UMODEIS = "221"
    RPL_SERVLIST = "234"
    RPL_SERVLISTEND = "235"
    RPL_STATSLLINE = "241"
    RPL_STATSUPTIME = "242"
    RPL_STATSOLINE = "243"
    RPL_STATSHLINE = "244"
    RPL_LUSERCLIENT = "251"
    RPL_LUSEROP = "252"
    RPL_LUSERUNKNOWN = "253"
    RPL_LUSERCHANNELS = "254"
    RPL_LUSERME = "255"
    RPL_ADMINME = "256"
    RPL_ADMINLOC1 = "257"
    RPL_ADMINLOC2 = "258"
    RPL_ADMINEMAIL = "259"
    RPL_TRACELOG = "261"
    RPL_TRACEEND = "262"
    RPL_TRYAGAIN = "263"
    RPL_NONE = "300"
    RPL_AWAY = "301"
    RPL_USERHOST = "302"
    RPL_ISON = "303"
    RPL_UNAWAY = "305"
    RPL_NOWAWAY = "306"
    RPL_WHOISUSER = "311"
    RPL_WHOISSERVER = "312"
    RPL_WHOISOPERATOR = "313"
    RPL_WHOWASUSER = "314"
    RPL_ENDOFWHO = "315"
    RPL_WHOISIDLE = "317"
    RPL_ENDOFWHOIS = "318"
    RPL_WHOISCHANNELS = "319"
    RPL_LISTSTART = "321"
    RPL_LIST = "322"
    RPL_LISTEND = "323"
    RPL_CHANNELMODEIS = "324"
    RPL_UNIQOPIS = "325"
    RPL_NOTOPIC = "331"
    RPL_TOPIC = "332"
    RPL_TOPICBY = "333"
    RPL_INVITING = "341"
    RPL_SUMMONING = "342"
    RPL_INVITELIST = "346"
    RPL_ENDOFINVITELIST = "347"
    RPL_EXCEPTLIST = "348"
    RPL_ENDOFEXCEPTLIST = "349"
    RPL_VERSION = "351"
    RPL_WHOREPLY = "352"
    RPL_NAMEREPLY = "353"
    RPL_LINKS = "364"
    RPL_ENDOFLINKS = "365"
    RPL_ENDOFNAMES = "366"
    RPL_BANLIST = "367"
    RPL_ENDOFBANLIST = "368"
    RPL_ENDOFWHOWAS = "369"
    RPL_INFO = "371"
    RPL_MOTD = "372"
    RPL_ENDOFINFO = "374"
    RPL_MOTDSTART = "375"
    RPL_ENDOFMOTD = "376"
    RPL_YOUREOPER = "381"
    RPL_REHASHING = "382"
    RPL_YOURESERVICE = "383"
    RPL_TIME = "391"
    RPL_USERSTART = "392"
    RPL_USERS = "393"
    RPL_ENDOFUSERS = "394"
    RPL_NOUSERS = "395"
    ERR_NOSUCHNICK = "401"
    ERR_NOSUCHSERVER = "402"
    ERR_NOSUCHCHANNEL = "403"
    ERR_CANNOTSENDTOCHAN = "404"
    ERR_TOOMANYCHANNELS = "405"
    ERR_WASNOSUCHNICK = "406"
    ERR_TOOMANYTARGETS = "407"
    ERR_NOSUCHSERVICE = "408"
    ERR_NOORIGIN = "409"
    ERR_NORECIPIENT = "411"
    ERR_NOTEXTTOSEND = "412"
    ERR_NOTOPLEVEL = "413"
    ERR_WILDTOPLEVEL = "414"
    ERR_BANMASK = "415"
    ERR_UNKNOWNCOMMAND = "421"
    ERR_NOMOTD = "422"
    ERR_NOADMININFO = "423"
    ERR_FILEERROR = "424"
    ERR_NONICKNAMEGIVEN = "431"
    ERR_ERRONEUSNICKNAME = "432"
    ERR_NICKNAMEINUSE = "433"
    ERR_NICKCOLLISION = "436"
    ERR_UNAVAILRESOURCE = "437"
    ERR_USERNOTINCHANNEL = "441"
    ERR_NOTOONCHANNEL = "442"
    ERR_USERONCHANNEL = "443"
    ERR_NOLOGIN = "444"
    ERR_SUMMONDISABLED = "445"
    ERR_USERSDISABLED = "446"
    ERR_NOTREGISTERED = "451"
    ERR_NEEDMOREPARAMS = "461"
    ERR_ALREADYREGISTERED = "462"
    ERR_NOPERMFORHOST = "463"
    ERR_PASSWDMISMATH = "464"
    ERR_YOUREBANNEDCREEP = "465"
    ERR_YOUWILLBEBANNED = "466"
    ERR_KEYSET = "467"
    ERR_CHANNELISFULL = "471"
    ERR_UNKNOWNMODE = "472"
    ERR_INVITEONLYCHAN = "473"
    ERR_BANNEDFROMCHAN = "474"
    ERR_BADCHANNELKEY = "475"
    ERR_BADCHANMASK = "476"
    ERR_BASCHANMODES = "477"
    ERR_BANLISTFULL = "478"
    ERR_NOPRIVILEGES = "481"
    ERR_CHANOPRIVSNEEDED = "482"
    ERR_CANTKILLSERVER = "483"
    ERR_RESTRICTED = "484"
    ERR_UNIQOPPRIVSNEEDED = "485"
    ERR_NOOPERHOST = "491"
    ERR_UMODEUNKNOWNFLAG = "501"
    ERR_USERSDONTMATCH = "502"
    MSG_NICK = "NICK"
    MSG_TOPIC = "TOPIC"
    MSG_MODE = "MODE"
    MSG_PRIVMSG = "PRIVMSG"
    MSG_JOIN = "JOIN"
    MSG_PART = "PART"
    MSG_QUIT = "QUIT"
    RAW = "RAW"


class User:
    identifier: str
    nickname: str
    username: str
    hostname: str

    def __init__(self, identifier: str):
        self.identifier = identifier
        if "@" not in self.identifier:
            self.nickname = self.hostname = self.identifier
        else:
            identifier, self.hostname = self.identifier.split("@")
            if "!" in identifier:
                self.nickname, self.username = identifier.split("!")
            else:
                self.nickname = self.username = identifier

    def nick(self, new_nick: str):
        self.identifier.replace("%s!" % self.nickname, "%s!" % new_nick)
        self.nickname = new_nick


class Channel:
    name: str
    topic: str
    userlist: Dict[str, User]

    def __init__(self, name: str):
        self.name = name
        self.topic = ""
        self.userlist = {}

    def join(self, user: User):
        if user.identifier not in self.userlist:
            self.userlist[user.identifier] = user

    def quit(self, user: User):
        if user.identifier in self.userlist:
            del self.userlist[user.identifier]


class Client:
    __function_register: Dict[str, List[Callable]]
    __server_socket: ClientSocket
    __server_caps: Dict[str, Union[str, int]]
    __userlist: Dict[str, User]
    __channellist: Dict[str, Channel]
    __my_user: StrOrNone

    def __init__(self, server: str, port: int, nick: str, username: str, realname: str = "Python Bot"):
        self.__userlist = {}
        self.__channellist = {}
        self.__server_socket = ClientSocket(server, port)
        self.__server_socket.sendline("USER %s ignore ignore :%s" % (username, realname))
        self.__server_socket.sendline("NICK %s" % nick)
        self.__server_caps = {
            'MAXLEN': 255
        }
        self.__function_register = {
            ServerMessage.RPL_WELCOME: [self.on_rpl_welcome],
            ServerMessage.RPL_TOPIC: [self.on_rpl_topic],
            ServerMessage.RPL_ISUPPORT: [self.on_rpl_isupport],
            ServerMessage.ERR_NICKNAMEINUSE: [self.on_err_nicknameinuse],
            ServerMessage.MSG_JOIN: [self.on_join],
            ServerMessage.MSG_PART: [self.on_part],
            ServerMessage.MSG_QUIT: [self.on_quit],
            ServerMessage.MSG_NICK: [self.on_nick],
            ServerMessage.MSG_TOPIC: [self.on_topic],
        }
        self.receive()

    def receive(self):
        while line := self.__server_socket.recvline():
            line = line.strip()

            if line.startswith("PING"):
                self.__server_socket.sendline("PONG " + line.split()[1])
                continue

            try:
                (msg_from, msg_type, msg_to, *msg) = line[1:].split()
            except ValueError:
                print("[E] Invalid message received:", line)
                continue

            if len(msg) > 0 and msg[0].startswith(":"):
                msg[0] = msg[0][1:]
            message = " ".join(msg)

            if ServerMessage.RAW in self.__function_register:
                for func in self.__function_register[ServerMessage.RAW]:
                    func(msg_from, msg_type, msg_to, message)

            if "!" in msg_from and msg_from not in self.__userlist:
                self.__userlist[msg_from] = User(msg_from)
                if self.__userlist[msg_from].nickname == self.__userlist[self.__my_user].nickname:
                    del self.__userlist[self.__my_user]
                    self.__my_user = msg_from

            if msg_type in self.__function_register:
                for func in self.__function_register[msg_type]:
                    func(msg_from, msg_to, message)

    def subscribe(self, msg_type: str, func: Callable[..., None]):
        if msg_type in self.__function_register:
            self.__function_register[msg_type].append(func)
        else:
            self.__function_register[msg_type] = [func]

    def on_rpl_welcome(self, msg_from: str, msg_to: str, message: str):
        self.__my_user = message.split()[-1]
        self.__userlist[self.__my_user] = User(self.__my_user)

    def on_rpl_isupport(self, msg_from: str, msg_to: str, message: str):
        for cap in message.split():
            if "=" not in cap:
                self.__server_caps[cap] = True
            else:
                (a, b) = cap.split("=")
                self.__server_caps[a] = b

    def on_rpl_topic(self, msg_from: str, msg_to: str, message: str):
        channel, *topic = message.split()
        if len(topic) > 0:
            topic[0] = topic[0][1:]

        new_topic = " ".join(topic)
        self.__channellist[channel].topic = new_topic

    def on_err_nicknameinuse(self, msg_from: str, msg_to: str, message: str):
        if self.__my_user is None:
            self.nick(message.split()[0] + "_")

    def on_nick(self, msg_from: str, msg_to: str, message: str):
        self.__userlist[msg_from].nick(msg_to)
        self.__userlist[self.__userlist[msg_from].identifier] = self.__userlist[msg_from]
        del self.__userlist[msg_from]

    def on_join(self, msg_from: str, msg_to: str, message: str):
        channel = msg_to[1:]
        if msg_from == self.__my_user:
            self.__channellist[channel] = Channel(channel)
            # FIXME: get user list (NAMES just returns nicknames, not nick!user@host !!!)

        if msg_from not in self.__userlist:
            self.__userlist[msg_from] = User(msg_from)

        self.__channellist[channel].join(self.__userlist[msg_from])

    def on_topic(self, msg_from: str, msg_to: str, message: str):
        self.__channellist[msg_to].topic = message

    def on_part(self, msg_from: str, msg_to: str, message: str):
        self.__channellist[msg_to].quit(self.__userlist[msg_from])

    def on_quit(self, msg_from: str, msg_to: str, message: str):
        for c in self.__channellist:
            self.__channellist[c].quit(self.__userlist[msg_from])

        del self.__userlist[msg_from]

    def on_raw(self, msg_from: str, msg_type: str, msg_to: str, message: str):
        print(msg_from, msg_type, msg_to, message)

    def nick(self, new_nick: str):
        self.__server_socket.sendline("NICK %s" % new_nick)

    def join(self, channel: str):
        self.__server_socket.sendline("JOIN %s" % channel)
        self.receive()

    def part(self, channel: str):
        self.__server_socket.sendline("PART %s" % channel)
        self.receive()

    def privmsg(self, target: str, message: str):
        self.__server_socket.sendline("PRIVMSG %s :%s" % (target, message))

    def quit(self, message: str = "Elvis has left the building!"):
        self.__server_socket.sendline("QUIT :%s" % message)
        self.receive()
        self.__server_socket.close()

    def getUser(self, user: str = None) -> Union[User, None]:
        if user is None:
            return self.__userlist[self.__my_user]
        elif user in self.__userlist:
            return self.__userlist[user]
        else:
            return None

    def getUserList(self) -> List[User]:
        return list(self.__userlist.values())

    def getChannel(self, channel: str) -> Union[Channel, None]:
        if channel in self.__channellist:
            return self.__channellist[channel]
        else:
            return None

    def getChannelList(self) -> List[Channel]:
        return list(self.__channellist.values())


class IrcBot(Client):
    def __init__(self, server: str, port: int, nick: str, username: str, realname: str = "Python Bot"):
        super().__init__(server, port, nick, username, realname)
        self._scheduler = Scheduler()
        self._channel_commands = {}
        self._privmsg_commands = {}
        self.subscribe(ServerMessage.MSG_PRIVMSG, self.on_privmsg)

    def on(self, *args, **kwargs):
        self.subscribe(*args, **kwargs)

    def schedule(self, name: str, every: timedelta, func: Callable):
        self._scheduler.schedule(name, every, func)

    def register_channel_command(self, command: str, channel: str, func: Callable):
        if channel not in self._channel_commands:
            self._channel_commands[channel] = {}

        self._channel_commands[channel][command] = func

    def register_privmsg_command(self, command: str, func: Callable):
        self._privmsg_commands[command] = func

    def on_privmsg(self, msg_from, msg_to, message):
        if not message:
            return
        command = message.split()[0]
        if msg_to in self._channel_commands and command in self._channel_commands[msg_to]:
            self._channel_commands[msg_to][command](msg_from, " ".join(message.split()[1:]))

        if msg_to == self.getUser().nickname and command in self._privmsg_commands:
            self._privmsg_commands[command](msg_from, " ".join(message.split()[1:]))

    def run(self):
        while True:
            self._scheduler.run_pending()
            self.receive()
            sleep(0.01)
