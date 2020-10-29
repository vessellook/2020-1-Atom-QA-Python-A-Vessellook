#!/usr/bin/env python3

import re
import sys
from argparse import ArgumentParser, FileType
from datetime import datetime
from typing import List, TextIO

from utils import LogsRecord
from mysql_orm_client.mysql_orm_client import MysqlOrmClient

from names import MAIN_DB


def get_parser():
    parser = ArgumentParser()
    parser.add_argument(type=FileType('r'), metavar='LOGS_PATH', dest='logs_files', action='append',
                        help='Set path to NGINX logs')
    parser.add_argument('--port', type=int, help='mysql port')
    return parser


def parse_logs(logs_file: TextIO) -> List[LogsRecord]:
    pattern = r'^(([0-9]{1,3}[.]){3}[0-9]{1,3}) - .* \[(.*)\] "(.*) (.*) HTTP\/.*" ([0-9]{3}) ([0-9]+)'
    records = []
    for line in logs_file:
        split_line = re.split(pattern, line)
        if len(split_line) != 8:
            continue
        _, ip, _, time, method, location, code, response_size, _ = split_line
        if response_size == '-':
            response_size = 0
        records.append(LogsRecord(ip=ip, method=method, location=location,
                                  status_code=int(code), response_size=int(response_size),
                                  time=datetime.strptime(time[:-6], "%d/%b/%Y:%H:%M:%S")))
    return records


def main():
    args = get_parser().parse_args(sys.argv[1:])
    logs_records: List[LogsRecord] = []
    for file in args.logs_files:
        logs_records += parse_logs(file)
    client = MysqlOrmClient(user='root', password='pass', db_name=MAIN_DB, port=args.port if args.port else 3306)
    client.create_nginx_logs()
    for r in logs_records:
        client.add_record(r)


if __name__ == '__main__':
    main()
