import json
import sys
from typing import TextIO, List

from common import filter_logs, parse_logs, top_parser as parser, LogRecord


class UnhandledCaseException(Exception):
    pass


def sort_logs(logs: List[LogRecord], args) -> List[LogRecord]:
    if args.sort_by == 'SIZE':
        return sorted(logs, key=lambda r: r.response_size, reverse=True)
    elif args.sort_by == 'LOCATION':
        frequency = dict()
        for record in logs:
            frequency[record.location] = frequency.get(record.location, 0) + 1
        return sorted(logs, key=lambda r: frequency[r.location], reverse=True)
    elif args.sort_by is None:
        return logs
    else:
        raise UnhandledCaseException


def print_logs(logs: List[LogRecord], filler: str = ' ', output: TextIO = None, json_flag=False):
    if json_flag:
        print(json.dumps(logs, cls=LogRecord.Encoder, sort_keys=True, indent=4),
              file=output)
    else:
        for record in logs:
            print(record.ip, record.method, record.location, record.status_code, record.response_size,
                  sep=filler, file=output)


def top():
    args = parser().parse_args(sys.argv[1:])
    logs = parse_logs(args.logs_list)
    logs = filter_logs(logs, args)
    logs = sort_logs(logs, args)
    if args.limit is not None:
        logs = logs[:args.limit]
    print_logs(logs, filler=args.filler, output=args.output, json_flag=args.json)


if __name__ == '__main__':
    top()
