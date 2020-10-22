import sys

from common import filter_logs, parse_logs, base_parser as parser


def count():
    args = parser().parse_args(sys.argv[1:])
    logs = parse_logs(args.logs_list)
    logs = filter_logs(logs, args)
    print(len(logs))


if __name__ == '__main__':
    count()
