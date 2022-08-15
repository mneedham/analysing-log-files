import faust
from apachelogs import LogParser
import httpagentparser

log_parser = LogParser(
    "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
)

old_new = {
    "%>s": "status",
    "%h": "remoteHostName",
    "%b": "responseBytes",
    "%t": "ts",
    "Referer": "referer",
    "User-Agent": "userAgent"
}

fields_to_drop = [
    "%l", "%u", "%{Referer}i", "%{User-Agent}i", "%r"
]

def parse_log_message(event):
    output = log_parser.parse(event)

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

app = faust.App(
    'hello-world',
    broker='kafka://localhost:9092',
    value_serializer='json',
)

greetings_topic = app.topic('access')
output_topic = app.topic("access-logs", value_serializer='json')

@app.agent(greetings_topic)
async def greet(stream):
    async for event in stream:
        print("event", event["message"])
        row = parse_log_message(event["message"])
        await output_topic.send(value=row, key=row["host"])