import json
import sys
from typing import TextIO, List

from common import filter_logs, parse_logs, top_parser as parser, LogRecord


def sort_logs(logs: List[LogRecord]) -> List[LogRecord]:
    return logs


def print_logs(logs: List[LogRecord], filler: str = ' ', output: TextIO = None, json_flag=False):
    if json_flag is None:
        for record in logs:
            print(record.ip, record.method, record.location, record.status_code, record.response_size,
                  sep=filler, file=output)
    else:
        print(json.dumps(logs, cls=LogRecord.Encoder, sort_keys=True, indent=4),
              file=output)


def top():
    args = parser().parse_args(sys.argv[1:])
    logs = parse_logs(args.logs_list)
    logs = filter_logs(logs, args)
    logs = sort_logs(logs)
    if args.limit is not None:
        logs = logs[:args.limit]
    print_logs(logs, filler=args.filler, output=args.output, json_flag=args.json)


if __name__ == '__main__':
    top()
