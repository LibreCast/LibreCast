#!/usr/bin/python
'''
aria2do: Control aria2 through XMLRPC.
Copyright hashao <hashao2@gmail.com> 2009. All right reserved.

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.

Changelog:

2009-10-17:
    * Initial release 0.1.
'''

__version__ = '0.1'

import sys
import glob
import socket
import os
import urllib2
import xmlrpclib
import base64
import readline
import textwrap

class BasicAuthTransport(xmlrpclib.Transport):
    '''Do really simple authorization with xmlrpc.'''
    auth_header = 'Authorization'.upper()
    def __init__(self, use_datetime=0, username=None, password=None):
        self.username = username
        self.password = password
        xmlrpclib.Transport.__init__(self, use_datetime)


    def send_extra(self, connection, extra_headers):
        '''Send out extra headers to the httplib connection.'''
        if not extra_headers: return
        for k, v in extra_headers:
            connection.putheader(k, v)

    def request(self, host, handler, request_body, verbose=0, extra_headers=None):
        '''override base request to do authorization.'''
        # issue XML-RPC request

        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)

        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)

        # do authorization here.
        if self.username is not None:
            password = self.password if self.password is not None else ''
            raw = "%s:%s" % (self.username, password)
            auth = 'Basic %s' % base64.b64encode(raw).strip()
            if not extra_headers:
                extra_headers = []
            extra_headers.append((self.auth_header, auth))
        self.send_extra(h, extra_headers)

        self.send_content(h, request_body)

        errcode, errmsg, headers = h.getreply()
        if errcode != 200:
            raise xmlrpclib.ProtocolError(
                host + handler,
                errcode, errmsg,
                headers
                )

        self.verbose = verbose

        try:
            sock = h._conn.sock
        except AttributeError:
            sock = None

        return self._parse_response(h.getfile(), sock)

class AuthServer(xmlrpclib.Server):
    '''A server that handling basic authorization.
    Supply user/password at initialization.'''
    def __init__(self, uri, transport=None, encoding=None, verbose=0,
             allow_none=0, use_datetime=0, user=None, password=None):
        if user:
            transport = BasicAuthTransport(use_datetime, user, password)
        xmlrpclib.Server.__init__(self, uri, transport, encoding, verbose,
                allow_none, use_datetime)

def read_config():
    '''Read aria2's config.'''
    config = {}
    fname = '~/.aria2/aria2.conf'
    fname = os.path.expanduser(fname)
    comment = set([';', '#'])
    for line in open(fname):
        if line[0] in comment: continue
        k, e, v = line.strip().partition('=')
        if e:
            config[k] = v
    return config

def print_result(result):
    '''Try to pretty print rpc returns.'''
    if isinstance(result, list):
        for k in result:
            print_result(k)
            print
    elif isinstance(result, dict):
        for k in sorted(result.keys()):
            print "%s: %s" % (k, result[k])
    else:
        print result

def parse_aria_args(args):
    '''Parse Aria2 xmlrpc arguments.'''
    import optparse
    parser = optparse.OptionParser()
    add = parser.add_option
    setd = parser.set_defaults
    add('-u', '--uri', dest='uris', action='append', help='Can has more than one')
    setd(uris=[])
    add('-o', '--option', dest='options', action='append',
        help='Can has more than one, like "-o dir=/tmp -o split=3"')
    setd(options=[])
    add('-p', '--position', dest='position', help='position')
    add('-g', '--gid', dest='gid', help='gid')
    add('-s', '--offset', dest='offset', type='int', help='offset')
    add('-n', '--num', dest='num', type='int', help='num')
    opts, args = parser.parse_args(args)
    return opts, args, parser

# command we know.
acmd = {
   "adduri": ["addUri", "# uris[, options[, position]]"],
   "addtorrent": ["addTorrent", "# torrent[, uris[, options[, position]]]"],
   "addbt": ["addTorrent", "# torrent[, uris[, options[, position]]]"],
   "addmetalink": ["addMetalink", "# metalink[, options[, position]]"],
   "remove": ["remove", "# gid"],
   "tellstatus": ["tellStatus", "# gid"],
   "geturis": ["getUris", "# gid"],
   "getfiles": ["getFiles", "# gid"],
   "getpeers": ["getPeers", "# gid"],
   "tellactive": ["tellActive", "#"],
   "tellwaiting": ["tellWaiting", "# offset, num"],
   "tellstatus": ["tellStatus", "# gid"],
   "changeoption": ["changeOption", "# gid, options"],
   "changeglobaloption": ["changeGlobalOption", "# options"],
   "purgedownloadresult": ["purgeDownloadResult", "#"],
   "getversion": ["getVersion", "#"],
   }

class AriaControl:
    def __init__(self):
        config = read_config()
        port = config.get('xml-rpc-listen-port', '6800')
        user = config.get('xml-rpc-user', None)
        passwd = config.get('xml-rpc-passwd', None)
        uri = 'http://127.0.0.1:%s/rpc' % port
        self.server = AuthServer(uri, user=user, password=passwd)

    def do_cmd(self, args):
        '''Do a commands with arguements.''' 
        cmd = args[0]
        args = args[1:]
        opts, nargs, parser = parse_aria_args(args)
        cmd = cmd.lower()

        optmap = {}
        for otext in opts.options:
            k, e, v = otext.partition('=')
            if k in optmap:
                optmap[k] = [optmap[k]]
                optmap[k].append(v)
            else:
                optmap[k] = v

        rpcargs = []
        if cmd in ['addbt', 'addtorrent', 'addmetalink']:
            if len(args) < 1 or (not os.path.exists(args[0])):
                print 'Need a filename!'
                return
            fname = args[0]
            txt = open(fname, 'rb').read()
            bt = xmlrpclib.Binary(txt)
            rpcargs.append(bt)
        def rpcappend(ls, opt, name):
            v = getattr(opt, name)
            if v is None:
                print "Need %s" % name
                self.print_cmd()
                parser.print_help()
                return False
            else:
                ls.append(getattr(opt, name))
                return True
        if cmd in ['addbt', 'addtorrent', 'adduri']:
            rpcargs.append(opts.uris)
        if cmd in ['changeoption', "changeoption", "getfiles", 
                "getpeers", "geturis", "remove", "tellstatus",]:
            ret = rpcappend(rpcargs, opts, 'gid')
            if not ret: return
        if cmd in ['addbt', 'addtorrent', 'addmetalink', 'adduri',
                'changeoption', "changeoption"]:
            rpcargs.append(optmap)
        if (cmd in ['addbt', 'addtorrent', 'addmetalink', 'adduri'] and
                (opts.position is not None)):
            ret = rpcappend(rpcargs, opts, 'position')
            if not ret: return
        if (cmd in ['tellwaiting']):
            ret = rpcappend(rpcargs, opts, 'offset')
            if not ret: return
            ret = rpcappend(rpcargs, opts, 'num')
            if not ret: return

        if cmd not in acmd:
            print 'Unknow command "%s".' % cmd
            self.print_cmd()
            parser.print_help()
            return
        else:
            cmd = acmd[cmd][0]
        cmd = 'aria2.' + cmd
        result = self._do_cmd(cmd, *rpcargs)
        if result is not None:
            print_result(result)

    def _do_cmd(self, cmd, *args):
        '''real xmlrpc command.'''
        server = self.server
        try:
            fn = getattr(server, cmd)
            result = fn(*args)
            return result
        except (xmlrpclib.Fault, xmlrpclib.ProtocolError, socket.error):
            print '%s: %s' % (cmd, sys.exc_info()[1])

    def completer(self, text, state):
        '''Readline auto completer.'''
        match = []
        line = readline.get_line_buffer().lstrip()
        parts = line.split()
        if ( line and (len(parts) > 1 or line[-1].isspace()) and (
                parts[0].lower() in ['addtorrent', 'addbt']
                ) ):
            g = '*'
            prefix = ''
            if len(parts) == 2:
                prefix = parts[1]
            g =  prefix + g
            # '/' is a delimiter
            cutlen = len(prefix)-len(text)
            rawmatch = glob.glob(g)
            match = []
            for path in rawmatch:
                if os.path.isdir(path):
                    match.append(path+'/')
                elif path.endswith('.torrent'):
                    match.append(path)
            tmatch = [x[cutlen:] for x in match]
            match = tmatch
        else:
            cmdkeys = acmd.keys()
            for k in cmdkeys:
                if k.startswith(text):
                    match.append(k)
        if state < 0:
            return match
        if len(match) > state:
            return match[state]
        else:
            return None

    def interactive(self):
        '''Start interactive mode.'''
        readline.set_completer(self.completer)
        readline.parse_and_bind('tab: complete')

        while True:
            try:
                line = raw_input('> ')
                if not line: continue
            except EOFError:
                print
                break

            parts = line.strip().split()
            cmd = parts[0]
            cmd = cmd.lower()
            if cmd in set(['quit', 'bye', 'exit']):
                break
            self.do_cmd(parts)
    def print_cmd(self):
        '''Print available aria2 commands.'''
        options = '''\
  dir
  check-integrity
  continue
  all-proxy
  connect-timeout
  dry-run
  lowest-speed-limit
  max-file-not-found
  max-tries
  no-proxy
  out
  proxy-method
  remote-time
  split
  timeout
  http-auth-challenge
  http-user
  http-passwd
  http-proxy
  https-proxy
  referer
  enable-http-keep-alive
  enable-http-pipelining
  header
  use-head
  user-agent
  ftp-user
  ftp-passwd
  ftp-pasv
  ftp-proxy
  ftp-type
  ftp-reuse-connection
  no-netrc
  select-file
  bt-external-ip
  bt-hash-check-seed
  bt-max-open-files
  bt-max-peers
  bt-min-crypto-level
  bt-require-crypto
  bt-request-peer-speed-limit
  bt-seed-unverified
  bt-stop-timeout
  bt-tracker-interval
  enable-peer-exchange
  follow-torrent
  index-out
  max-upload-limit
  seed-ratio
  seed-time
  follow-metalink
  metalink-servers
  metalink-language
  metalink-location
  metalink-os
  metalink-version
  metalink-preferred-protocol
  metalink-enable-unique-protocol
  allow-overwrite
  allow-piece-length-change
  async-dns
  auto-file-renaming
  file-allocation
  max-download-limit
  no-file-allocation-limit
  parameterized-uri
  realtime-chunk-checksum
'''
        print 'Aria2 Options:'
        print options
        print 'Aria2 Commands:'

        cmdkeys = sorted(acmd.keys())
        maxlen = max([len(x) for x in cmdkeys])
        fmt = '  %%-%ds == %%s(%%s)' % maxlen
        for k in cmdkeys:
            help = acmd[k][1]
            print fmt % (k, acmd[k][0], help.lstrip('# '))

def main():
    aria = AriaControl()

    cmdkeys = sorted(acmd.keys())
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        incomplete = aria.completer(cmd, -1)
        if incomplete and len(incomplete) == 1:
            parts = sys.argv[1:]
            parts[0] = incomplete[0]
            aria.do_cmd(parts)
        else:
            print 'Usage: %s [cmd options ...]' % sys.argv[0]
            print 'Possible cmds are:'
            aria.print_cmd()
            opts, nargs, parser = parse_aria_args(sys.argv[1:])
            parser.print_help()
        return
    aria.interactive()

if __name__ == '__main__':
    main()

# vim:ts=8:sw=4:expandtab:encoding=utf-8
