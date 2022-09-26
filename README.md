# Real-Time Analytics on HTTP Access Logs

```
docker-compose up
```

Generate log files:

```bash
python apache-fake-log-gen.py
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


Add Pinot Table

```bash
docker run -v $PWD/pinot/config:/config \
 --network analysing-log-files_default \
 apachepinot/pinot:0.11.0 \
 AddTable \
 -schemaFile /config/schema.json \
 -tableConfigFile /config/table.json \
 -controllerHost pinot-controller \
 -exec
 ```
