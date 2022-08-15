```
docker-compose up
```

```bash
faust -A app worker -l info
```

```bash
docker exec -it kafka kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic access
```

```bash
docker exec -i kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic access
```