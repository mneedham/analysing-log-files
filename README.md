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

Query the access logs stream:

```bash
kcat -C -t access -b localhost:9092
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
