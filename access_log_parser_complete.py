import sys
import json

from apachelogs import LogParser

import httpagentparser

class AccessLogParser:
    def __init__(self):
        self.log_parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")

    def parse(self, event):
        output = self.log_parser.parse(event)

        row = {
            "host": output.remote_host,
            "time": output.request_time,
            **output.headers_in,
            **output.directives
        }

        method, url, protocol = row["%r"].split(" ")
        row |= {"method": method, "url": url, "protocol": protocol}

        user_agent_parts = httpagentparser.detect(row["User-Agent"])
        row |= user_agent_parts

        self.drop_fields(row)
        self.rename_fields(row)

        return row

    FIELDS_TO_DROP = ["%l", "%u", "%{Referer}i", "%{User-Agent}i", "%r"]
    def drop_fields(self, row):
        for key in self.FIELDS_TO_DROP:
            row.pop(key)

    OLD_NEW = {
        "%>s": "status",
        "%h": "remoteHostName",
        "%b": "responseBytes",
        "%t": "ts",
        "Referer": "referer",
        "User-Agent": "userAgent"
    }
    def rename_fields(self, row):
        for old, new in self.OLD_NEW.items():
            row[new] = row.pop(old)

if __name__ == "__main__":
    access_log_parser = AccessLogParser()
    for line in sys.stdin:
        message = json.loads(line)
        parsed_message = access_log_parser.parse(message)    
        print(json.dumps(parsed_message, default=str))