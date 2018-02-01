"""
    Use tcp ping host, just like ping comppand
"""

import sys
import socket
import time
import getopt

from collections import namedtuple
from functools import partial
from six.moves import zip_longest
from six import print_
from timeit import default_timer as timer

__version__ = "0.1.1rc1"

Statistics = namedtuple('Statistics', [
    'host',
    'port',
    'successed',
    'failed',
    'success_rate',
    'minimum',
    'maximum',
    'average'])

iprint = partial(print_, flush=True)


def avg(x):
    return sum(x) / float(len(x))


class Socket(object):
    def __init__(self, family, type_, timeout):
        s = socket.socket(family, type_)
        s.settimeout(timeout)
        self._s = s

    def connect(self, host, port=80):
        self._s.connect((host, int(port)))

    def shutdown(self):
        self._s.shutdown(socket.SHUT_RD)

    def close(self):
        self._s.close()


class Print(object):
    def __init__(self):
        self.table_field_names = []
        self.rows = []

    @property
    def raw(self):
        statistics_group = []
        for row in self.rows:
            total = row.successed + row.failed
            statistics_header = '\n--- {0}[:{1}] tcping statistics ---'.format(
                row.host, row.port)
            statistics_body = '\n{0} connections, {1} successed, {2} failed, {3} success rate'.format(
                total, row.successed, row.failed, row.success_rate)
            statistics_footer = '\nminimum = {0}, maximum = {1}, average = {2}'.format(
                row.minimum, row.maximum, row.average)

            statistics = statistics_header + statistics_body + statistics_footer
            statistics_group.append(statistics)

        return ''.join(statistics_group)

    def add_statistics(self, row):
        self.rows.append(row)


class Timer(object):
    def __init__(self):
        self._start = 0
        self._stop = 0

    def start(self):
        self._start = timer()

    def stop(self):
        self._stop = timer()

    def cost(self, funcs, args):
        self.start()
        for func, arg in zip_longest(funcs, args):
            if arg:
                func(*arg)
            else:
                func()

        self.stop()
        return self._stop - self._start


class Ping(object):
    def __init__(self, host, port=80, timeout=1, debug=False):
        self.print_ = Print()
        self.timer = Timer()
        self.debug = debug

        self._successed = 0
        self._failed = 0
        self._conn_times = []
        self._host = host
        self._port = port
        self._timeout = timeout

    def _create_socket(self, family, type_):
        return Socket(family, type_, self._timeout)

    def _success_rate(self):
        count = self._successed + self._failed
        try:
            rate = (float(self._successed) / count) * 100
            rate = '{0:.2f}'.format(rate)
        except ZeroDivisionError:
            rate = '0.00'
        return rate

    def statistics(self, n):
        conn_times = self._conn_times if self._conn_times != [] else [0]
        minimum = '{0:.2f}ms'.format(min(conn_times))
        maximum = '{0:.2f}ms'.format(max(conn_times))
        average = '{0:.2f}ms'.format(avg(conn_times))
        success_rate = self._success_rate() + '%'

        self.print_.add_statistics(Statistics(
            self._host,
            self._port,
            self._successed,
            self._failed,
            success_rate,
            minimum,
            maximum,
            average))

    @property
    def result(self):
        return self.print_

    def ping(self, count=10):
        for n in range(1, count + 1):
            s = self._create_socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                time.sleep(1)
                cost_time = self.timer.cost(
                    (s.connect, s.shutdown),
                    ((self._host, self._port), None))
                s_runtime = 1000 * (cost_time)
                if self.debug:
                    iprint("Connected to %s[:%s]: seq=%d time=%.2f ms" % (
                        self._host, self._port, n, s_runtime))

                self._conn_times.append(s_runtime)
            except socket.timeout:
                if self.debug:
                    iprint("Connected to %s[:%s]: seq=%d time out!" % (
                        self._host, self._port, n))
                self._failed += 1

            except KeyboardInterrupt:
                self.statistics(n - 1)
                raise KeyboardInterrupt()

            else:
                self._successed += 1

            finally:
                s.close()

        self.statistics(n)


def usage():
    print u"""
Usage: tcping [OPTIONS] HOST

Options:
  -p, --port INTEGER      Tcp port
  -c, --count INTEGER     Try connections counts
  -t, --timeout FLOAT     Timeout seconds
  --help                  Show this message and exit.
    """
    sys.exit(0)


def cli(host, port, count, timeout, report):
    ping = Ping(host, port, timeout, debug=report)
    try:
        ping.ping(count)
    except KeyboardInterrupt:
        pass

    if report:
        iprint(ping.result.raw)


if __name__ == '__main__':
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'p:c:t:h', ['port=', 'count=', 'timeout=', 'help'])
    except getopt.GetoptError as err:
        print(err)
        usage()

    if not args:
        usage()

    if len(args) >= 2:
        print('Conflict between: %s.' % ', '.join(args))
        usage()

    flags = {}
    for flag_group in opts:
        flags[flag_group[0]] = list(flag_group[1:])

    # Default values
    port = 80
    timeout = 1
    count = 3

    ### Parse
    # port
    if '--port' in flags.keys():
        if flags['--port']:
            try:
                port = int(flags['--port'][0])
            except ValueError:
                print(' Error: --port must be integer')
                usage()
    if '-p' in flags.keys():
        if flags['-p']:
            try:
                port = int(flags['-p'][0])
            except ValueError:
                print(' Error: -p must be integer')
                usage()
    # Timeout
    if '--timeout' in flags.keys():
        if flags['--timeout']:
            try:
                timeout = int(flags['--timeout'][0])
            except ValueError:
                print(' Error: --timeout must be integer')
                usage()
    if '-t' in flags.keys():
        if flags['-t']:
            try:
                timeout = int(flags['-t'][0])
            except ValueError:
                print(' Error: -t must be integer')
                usage()

    # Count
    if '--count' in flags.keys():
        if flags['--count']:
            try:
                count = int(flags['--count'][0])
            except ValueError:
                print(' Error: --count must be integer')
                usage()
    if '-c' in flags.keys():
        if flags['-c']:
            try:
                count = int(flags['-c'][0])
            except ValueError:
                print(' Error: -c must be integer')
                usage()
    destination = args[0]
    debug = True
    cli(host=destination, port=port, count=count, timeout=timeout, report=debug)