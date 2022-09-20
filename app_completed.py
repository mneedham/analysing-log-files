import faust
from access_log_parser import AccessLogParser

access_log_parser = AccessLogParser()

app = faust.App(
    'access-logs',
    broker='kafka://localhost:9092',
    value_serializer='json',
)

access_topic = app.topic('access')
output_topic = app.topic("enriched-access-logs", value_serializer='json')

@app.agent(access_topic)
async def access_logs(stream):
    async for event in stream:
        expanded_message = access_log_parser.parse(event["message"])
        event |= {"expandedMessage": expanded_message}
        await output_topic.send(value=event, key=event["host"]["name"])

        