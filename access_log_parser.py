import sys
import json

from apachelogs import LogParser
import httpagentparser

class AccessLogParser:
    OLD_NEW = {
        "%>s": "status",
        "%h": "remoteHostName",
        "%b": "responseBytes",
        "%t": "ts",
        "Referer": "referer",
        "User-Agent": "userAgent"
    }

    FIELDS_TO_DROP = ["%l", "%u", "%{Referer}i", "%{User-Agent}i", "%r"]

    def __init__(self):
        self.log_parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"") 

    def extract_url(self, request_parts):
        return request_parts.split(" ")[1]

    def rename_properties(self, row):
        for old, new in self.OLD_NEW.items():
            row[new] = row.pop(old)

    def drop_fields(self, row):
        for key in self.FIELDS_TO_DROP:
            row.pop(key)

    def extract_user_agent(self, row):
      return httpagentparser.detect(row["userAgent"])

    def parse(self, event):
        output = self.log_parser.parse(event)

        row = {
            "host": output.remote_host,
            "time": output.request_time,
            **output.headers_in,
            **output.directives
        }
        row["url"] = self.extract_url(row["%r"])

        self.rename_properties(row)
        self.drop_fields(row)

        user_agent_parts = self.extract_user_agent(row)

        return {**row, **user_agent_parts}

if __name__ == "__main__":
    access_log_parser = AccessLogParser()
    for line in sys.stdin:
        data = json.loads(line)
        parsed_message = access_log_parser.parse(data["message"])    
        print(json.dumps(parsed_message, default=str))