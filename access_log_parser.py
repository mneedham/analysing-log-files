import sys
import json

from apachelogs import LogParser
import httpagentparser

log_parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")

old_new = {
    "%>s": "status",
    "%h": "remoteHostName",
    "%b": "responseBytes",
    "%t": "ts",
    "Referer": "referer",
    "User-Agent": "userAgent"
}

fields_to_drop = ["%l", "%u", "%{Referer}i", "%{User-Agent}i", "%r"]

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
        row["url"] = row["%r"].split(" ")[1]

        for old, new in old_new.items():
            row[new] = row.pop(old)

        for key in fields_to_drop:
            row.pop(key)    

        return {**row, **httpagentparser.detect(row["userAgent"])}

if __name__ == "__main__":
    access_log_parser = AccessLogParser()
    for line in sys.stdin:
        data = json.loads(line)
        parsed_message = access_log_parser.parse(data["message"])    
        print(json.dumps(parsed_message, default=str))