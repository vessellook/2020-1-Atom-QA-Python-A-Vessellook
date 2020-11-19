import json
import re
from argparse import ArgumentParser, FileType
from dataclasses import dataclass
from typing import List, TextIO, Any


@dataclass
class LogRecord:
    ip: str
    method: str
    location: str
    status_code: int
    response_size: int

    class Encoder(json.JSONEncoder):
        def default(self, r: 'LogRecord') -> Any:
            return {'ip': r.ip,
                    'method': r.method,
                    'location': r.location,
                    'status_code': r.status_code,
                    'response_size': r.response_size}


def filter_logs(logs: List[LogRecord], args) -> List[LogRecord]:
    method = args.method
    code = args.code
    if method is not None:
        logs = list(filter(lambda r: r.method == method, logs))
    if code is not None:
        logs = list(filter(lambda r: str(r.status_code).startswith(code), logs))
    return logs


def parse_logs(logs_list: List[TextIO]) -> List[LogRecord]:
    pattern = r'^(([0-9]{1,3}[.]){3}[0-9]{1,3}) - .* \[.*\] "(.*) (.*) HTTP/.*" ([0-9]{3}) ([0-9]+)'
    logs: List[LogRecord] = []
    for file in logs_list:
        file: TextIO
        for line in file:
            split_line = re.split(pattern, line)
            if len(split_line) != 8:
                continue
            _, ip, _, method, location, code, response_size, _ = split_line
            logs.append(LogRecord(ip=ip, method=method, location=location,
                                  status_code=int(code), response_size=int(response_size)))
        file.close()
    return logs


def base_parser() -> ArgumentParser:
    parser = ArgumentParser(description='Count lines in NGINX logs')
    parser.add_argument('logs_list', metavar='PATH', nargs='*', type=FileType('r'),
                        help='Set path to NGINX logs')
    parser.add_argument('-m', '--method', metavar='METHOD', action='store', dest='method',
                        help='Filter logs lines by HTTP method')
    parser.add_argument('-c', '--status-code', metavar='CODE', action='store', dest='code',
                        help='Filter logs lines by status code. '
                             'You can filter by class of errors. '
                             "For example, pass option '-c 4' to remove all logs "
                             'except lines with client side errors')
    return parser


def top_parser() -> ArgumentParser:
    parser = base_parser()
    parser.add_argument('--output', '-o', metavar='OUTPUT', type=FileType('w'),
                        action='store',
                        help='Set file for output')
    parser.add_argument('--sort-by', '-s', action='store', choices=['SIZE', 'LOCATION'],
                        help='Set sorting. Available values are: '
                             'SIZE - Sort lines by response message size. The heaviest response is the first. '
                             'LOCATION - Sort lines by frequency of location. '
                             'Lines with the most frequent location are at the top')
    parser.add_argument('--limit', '-l', action='store',
                        help='Set maximal count of lines in output')
    parser.add_argument('--filler', '-f', action='store',
                        help='Set filler for output. Default value is space')
    parser.add_argument('--json', '-j', action='store_true',
                        help='if you need to have output in json format, use this option. Look README.md for details')

    return parser
