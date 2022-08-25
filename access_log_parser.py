import sys
import json

from apachelogs import LogParser

class AccessLogParser:
    def __init__(self):
        self.log_parser = LogParser(
            "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
        )

    def parse(self, event):
        output = self.log_parser.parse(event)

        row = {
            "host": output.remote_host,
            "time": output.request_time,
            **output.headers_in,
            **output.directives
        }

        return row

if __name__ == "__main__":
    access_log_parser = AccessLogParser()
    for line in sys.stdin:
        message = json.loads(line)
        parsed_message = access_log_parser.parse(message)    
        print(json.dumps(parsed_message, default=str))