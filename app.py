import faust

app = faust.App(
    'access-logs',
    broker='kafka://localhost:9092',
    value_serializer='json',
)

access_topic = app.topic('access')

@app.agent(access_topic)
async def access_logs(stream):
    async for event in stream:
        print("event", event["message"])