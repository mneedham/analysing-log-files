import faust
from access_log_parser import AccessLogParser

parser = AccessLogParser()

app = faust.App(
    'access-logs',
    broker='kafka://localhost:9092',
    value_serializer='json',
)

access_topic = app.topic('access')
enriched_topic = app.topic('enriched-access-logs')

@app.agent(access_topic)
async def access_logs(stream):
    async for event in stream:
        expanded_message = parser.parse(event["message"])
        event |= {"expandedMessage": expanded_message}
        await enriched_topic.send(
            key=event["host"]["name"],
            value=event
        )