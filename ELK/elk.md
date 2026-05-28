# Telemetry Lab: ELK, Filebeat, Logstash, Kibana, and Prometheus

## Scope of this handout

This handout covers the telemetry part of the lab only. It assumes that the application already exists and already writes structured logs to a local file, for example:

```text
../logs/items-app.log
```

The goal of this lab is to build a small observability stack on one VM and use it to collect, process, store, search, and interpret application telemetry.

---

## 1. What is telemetry?

Telemetry is data emitted by a system so that humans and tools can understand what the system is doing.

In cloud computing and microservices, telemetry is important because applications are often distributed across many services, containers, VMs, and networks. When something goes wrong, we usually cannot simply “look inside the program.” Instead, we rely on telemetry.

The three classic categories of observability data are:

| Type | What it answers | Example |
|---|---|---|
| Logs | What happened? | `User requested item 999 and received 404` |
| Metrics | How much or how often? | `HTTP 500 errors per second` |
| Traces | Where did the request go? | `Frontend → API → database → payment service` |

This lab focuses mainly on **logs** and introduces **metrics** with Prometheus.

---

## 2. Telemetry chain used in this lab

The logging chain is:

```text
Application
  ↓ writes JSON logs
Log file
  ↓ read by Filebeat
Filebeat
  ↓ sends events
Logstash
  ↓ parses and enriches events
Elasticsearch
  ↓ stores searchable documents
Kibana
  ↓ visualizes and searches logs
User / student
```

The metrics chain is:

```text
Application /metrics endpoint
  ↓ scraped periodically
Prometheus
  ↓ stores time-series metrics
PromQL queries
  ↓ used for investigation
User / student
```

---

## 3. What is ELK?

**ELK** originally meant:

```text
E = Elasticsearch
L = Logstash
K = Kibana
```

Today, people often say **Elastic Stack** instead of ELK, because the stack now commonly includes additional components such as Beats, Elastic Agent, and other tools.

For this lab, we use the classic logging path:

```text
Filebeat → Logstash → Elasticsearch → Kibana
```

### Elasticsearch

Elasticsearch is the storage and search engine. It receives processed log events and stores them as searchable documents.

In this lab, each log line becomes a document in an Elasticsearch index such as:

```text
items-app-logs-2026.05.28
```

Students use Elasticsearch indirectly through Kibana, but it is Elasticsearch that actually stores and searches the data.

### Logstash

Logstash is the processing pipeline. It receives events, modifies them, and sends them somewhere else.

A Logstash pipeline usually has three stages:

```text
input → filter → output
```

In this lab:

```text
input  = receive logs from Filebeat
filter = parse JSON, fix timestamps, add fields
output = send logs to Elasticsearch
```

### Kibana

Kibana is the web interface for exploring data stored in Elasticsearch.

In this lab, students use Kibana to:

- create a data view
- search logs
- filter errors and warnings
- inspect fields such as `status_code`, `path`, `event`, and `duration_ms`
- create basic visualizations or dashboards if time allows

Kibana is not the database. It is the UI that talks to Elasticsearch.

---

## 4. What is Filebeat?

Filebeat is a lightweight log shipper.

It runs close to the application, watches log files, and forwards new log lines to another system, usually Logstash or Elasticsearch.

In this lab, Filebeat watches:

```text
/logs/items-app.log
```

and sends each new log event to:

```text
logstash:5044
```

Filebeat is useful because applications should not need to know how to send logs to Elasticsearch. The application simply writes logs locally, and Filebeat handles shipping.

### Filebeat responsibilities

Filebeat is responsible for:

- reading log files
- remembering how far it has already read
- forwarding new log events
- handling temporary interruptions
- sending logs to Logstash or Elasticsearch

### Filebeat is not mainly responsible for

Filebeat is not usually where we do heavy parsing, enrichment, or complex transformations. That is usually Logstash’s role.

---

## 5. What is Logstash?

Logstash is a data processing service.

It is more powerful than Filebeat. It can receive data from different inputs, transform it, parse it, enrich it, and send it to different outputs.

Typical Logstash filters include:

| Filter | Purpose |
|---|---|
| `json` | Parse JSON log messages |
| `grok` | Parse unstructured text logs |
| `date` | Convert a timestamp field into `@timestamp` |
| `mutate` | Rename, add, remove, or modify fields |
| `drop` | Remove events that should not be stored |

In this lab, Logstash is used to parse structured JSON logs and forward them to Elasticsearch.

Example mental model:

```text
Filebeat ships.
Logstash transforms.
Elasticsearch stores.
Kibana shows.
```

---

## 6. What is Prometheus?

Prometheus is a metrics monitoring system.

It collects numeric measurements from configured targets. Unlike Filebeat, which reads log files, Prometheus usually works by periodically calling HTTP endpoints such as:

```text
/metrics
```

This is called scraping.

Example metrics:

```text
http_requests_total
http_request_duration_seconds
process_cpu_seconds_total
app_errors_total
```

Prometheus stores these values as time series. A time series is a sequence of values over time.

For example:

```text
http_requests_total{method="GET", path="/items", status="200"}
```

Prometheus is queried using PromQL.

Example PromQL queries:

```promql
http_requests_total
```

```promql
rate(http_requests_total[1m])
```

```promql
sum by (status_code) (rate(http_requests_total[1m]))
```

### Prometheus is good for

Prometheus is good for:

- request rates
- error rates
- latency measurements
- CPU and memory usage
- service health
- alerting

### Prometheus is not good for

Prometheus is not the right tool for storing full application logs. Logs are text events. Prometheus stores numeric time-series data.

---

## 7. Logs vs metrics

| Question | Logs | Metrics |
|---|---|---|
| What are they? | Individual events | Numeric measurements over time |
| Example | `Item not found` | `404 responses per minute` |
| Best for | Debugging what happened | Detecting trends and alerting |
| Storage | Elasticsearch | Prometheus |
| Query tool | Kibana / Elasticsearch queries | PromQL |
| Detail level | High detail | Aggregated |
| Cost at scale | Can become expensive | Usually more compact |

A useful teaching sentence:

```text
Metrics tell us that something is wrong. Logs help us understand why.
```

Example:

Prometheus may show:

```text
The 404 error rate increased at 10:15.
```

Kibana may show:

```text
Most 404s came from GET /v1/items/999.
```

---

## 8. One-VM architecture

Because this is a lab demonstration, all services run on one VM.

```text
One VM
├── FastAPI application
│   └── writes logs to ../logs/items-app.log
├── Filebeat
│   └── reads the log file
├── Logstash
│   └── receives logs from Filebeat
├── Elasticsearch
│   └── stores parsed logs
├── Kibana
│   └── searches and visualizes logs
└── Prometheus
    └── scrapes metrics from the app when /metrics exists
```

This is simpler than a production setup, but the concepts are the same.

---

## 9. Folder structure for the telemetry stack

Recommended structure:

```text
project/
├── main.py
├── logs/
│   └── items-app.log
└── telemetry-lab/
    ├── docker-compose.yml
    ├── filebeat/
    │   └── filebeat.yml
    ├── logstash/
    │   └── pipeline/
    │       └── app-logs.conf
    └── prometheus/
        └── prometheus.yml
```

The app is not part of this handout. The only assumption is that it writes logs to:

```text
project/logs/items-app.log
```

The telemetry stack is started from:

```text
project/telemetry-lab/
```

---

## 10. Docker Compose stack

Create this file:

```text
telemetry-lab/docker-compose.yml
```

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:9.4.1
    container_name: lab-elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - xpack.security.enrollment.enabled=false
      - ES_JAVA_OPTS=-Xms1g -Xmx1g
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:9.4.1
    container_name: lab-kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

  logstash:
    image: docker.elastic.co/logstash/logstash:9.4.1
    container_name: lab-logstash
    ports:
      - "5044:5044"
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:9.4.1
    container_name: lab-filebeat
    user: root
    command: ["filebeat", "-e", "--strict.perms=false"]
    volumes:
      - ./filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - ../logs:/logs:ro
      - filebeat-data:/usr/share/filebeat/data
    depends_on:
      - logstash

  prometheus:
    image: prom/prometheus:latest
    container_name: lab-prometheus
    ports:
      - "9090:9090"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro

volumes:
  elasticsearch-data:
  filebeat-data:
```

---

## 11. Filebeat configuration

Create this file:

```text
telemetry-lab/filebeat/filebeat.yml
```

```yaml
filebeat.inputs:
  - type: filestream
    id: items-app-logs
    enabled: true
    paths:
      - /logs/items-app.log
    fields:
      environment: lab
      app: items-app
    fields_under_root: true

output.logstash:
  hosts: ["logstash:5044"]
```

Explanation:

| Setting | Meaning |
|---|---|
| `type: filestream` | Read lines from a file |
| `paths` | Which file Filebeat should watch |
| `fields` | Extra metadata added to every event |
| `output.logstash` | Send events to Logstash instead of directly to Elasticsearch |

---

## 12. Logstash pipeline

Create this file:

```text
telemetry-lab/logstash/pipeline/app-logs.conf
```

```ruby
input {
  beats {
    port => 5044
  }
}

filter {
  json {
    source => "message"
    skip_on_invalid_json => true
  }

  date {
    match => ["timestamp", "ISO8601", "yyyy-MM-dd'T'HH:mm:ssZ"]
    target => "@timestamp"
    timezone => "Europe/Ljubljana"
  }

  mutate {
    add_field => {
      "telemetry_stack" => "elk"
      "lab_name" => "microservices-observability-final-lab"
    }
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "items-app-logs-%{+YYYY.MM.dd}"
  }

  stdout {
    codec => rubydebug
  }
}
```

Explanation:

| Section | Purpose |
|---|---|
| `input` | Receive events from Filebeat |
| `filter` | Parse and enrich the events |
| `output` | Send events to Elasticsearch |

---

## 13. Prometheus configuration

Create this file:

```text
telemetry-lab/prometheus/prometheus.yml
```

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["prometheus:9090"]

  - job_name: "items-app"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["host.docker.internal:8000"]
```

Explanation:

| Setting | Meaning |
|---|---|
| `scrape_interval` | How often Prometheus collects metrics |
| `job_name` | Name of the monitored service |
| `metrics_path` | HTTP path where metrics are exposed |
| `targets` | Host and port to scrape |

If the application does not yet expose `/metrics`, the `items-app` target will be down. This is expected until metrics are added to the application.

---

## 14. Starting the telemetry stack

From inside the telemetry folder:

```bash
cd telemetry-lab
docker compose up -d
```

Check that the containers are running:

```bash
docker ps
```

Expected containers:

```text
lab-elasticsearch
lab-kibana
lab-logstash
lab-filebeat
lab-prometheus
```

---

## 15. Checking the logging chain

### Check that the app is writing logs

From the project folder:

```bash
tail -f logs/items-app.log
```

### Check Filebeat

```bash
docker logs lab-filebeat
```

### Check Logstash

```bash
docker logs lab-logstash
```

### Check Elasticsearch

```bash
curl http://localhost:9200
```

List indices:

```bash
curl "http://localhost:9200/_cat/indices?v"
```

Look for an index similar to:

```text
items-app-logs-2026.05.28
```

Search documents:

```bash
curl "http://localhost:9200/items-app-logs-*/_search?pretty"
```

---

## 16. Using Kibana

Open:

```text
http://localhost:5601
```

Create a data view:

```text
Stack Management → Data Views → Create data view
```

Use:

```text
items-app-logs-*
```

Timestamp field:

```text
@timestamp
```

Then open:

```text
Discover
```

Useful searches:

```text
level: "ERROR"
```

```text
level: "WARNING"
```

```text
status_code: 404
```

```text
event: "item_not_found"
```

```text
path: "/v1/items/999"
```

---

## 17. Using Prometheus

Open:

```text
http://localhost:9090
```

Check targets:

```text
Status → Targets
```

Prometheus itself should be up.

The application target will only be up if the app exposes:

```text
/metrics
```

Example PromQL queries once app metrics exist:

```promql
up
```

```promql
http_requests_total
```

```promql
rate(http_requests_total[1m])
```

```promql
sum by (status_code) (rate(http_requests_total[1m]))
```

---

## 18. Troubleshooting guide

### Problem: Kibana shows no logs

Check the chain from left to right:

```text
App → log file → Filebeat → Logstash → Elasticsearch → Kibana
```

Commands:

```bash
tail logs/items-app.log
docker logs lab-filebeat
docker logs lab-logstash
curl "http://localhost:9200/_cat/indices?v"
```

### Problem: Filebeat cannot find the log file

From inside `telemetry-lab`, this command must work:

```bash
ls ../logs/items-app.log
```

If it does not work, the Docker volume mount is pointing to the wrong place.

### Problem: Elasticsearch does not start

Check logs:

```bash
docker logs lab-elasticsearch
```

On Linux, Elasticsearch sometimes requires a higher virtual memory limit:

```bash
sudo sysctl -w vm.max_map_count=262144
```

Then restart:

```bash
docker compose restart elasticsearch
```

### Problem: Prometheus cannot reach the app

Make sure the app is running on all interfaces:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Also check that the Prometheus service includes:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

---

# Lecturer notes

## A. Simple explanation for students

Use this simple sentence early:

```text
Telemetry is evidence from the system.
```

Then explain:

```text
Logs are detailed event records.
Metrics are numbers over time.
Traces show the path of one request across services.
```

This lab focuses on logs and metrics.

---

## B. The difference between the tools

| Tool | Main role | One-sentence explanation |
|---|---|---|
| Filebeat | Log shipper | Reads log files and forwards new lines to Logstash or Elasticsearch |
| Logstash | Log processor | Receives events, parses them, enriches them, and sends them onward |
| Elasticsearch | Storage and search | Stores logs as searchable documents |
| Kibana | User interface | Lets users search, filter, visualize, and inspect Elasticsearch data |
| ELK | Stack name | Elasticsearch + Logstash + Kibana, often used more broadly for the Elastic Stack |
| Prometheus | Metrics system | Scrapes numeric metrics from HTTP endpoints and stores them as time series |

A memorable version:

```text
Filebeat moves logs.
Logstash cleans logs.
Elasticsearch stores logs.
Kibana shows logs.
Prometheus measures the system.
```

---

## C. Common student misunderstandings

### Misunderstanding 1: “ELK is one application”

Correction:

```text
ELK is not one program. It is a group of tools that work together.
```

### Misunderstanding 2: “Filebeat and Logstash do the same thing”

Correction:

```text
Filebeat is lightweight and runs near the application. Logstash is heavier and performs more advanced processing.
```

### Misunderstanding 3: “Kibana stores logs”

Correction:

```text
Kibana does not store logs. Elasticsearch stores logs. Kibana is the interface.
```

### Misunderstanding 4: “Prometheus collects logs”

Correction:

```text
Prometheus collects metrics, not full text logs.
```

### Misunderstanding 5: “Metrics and logs are interchangeable”

Correction:

```text
Metrics are better for detecting that something is wrong. Logs are better for explaining what happened.
```

---

## D. Suggested whiteboard explanation

Draw two pipelines:

```text
LOGS
App → file → Filebeat → Logstash → Elasticsearch → Kibana
```

```text
METRICS
App /metrics → Prometheus → PromQL
```

Then ask:

```text
If response time increases, which tool tells us first?
```

Expected answer:

```text
Prometheus, because it tracks latency metrics over time.
```

Then ask:

```text
If we want to know which request failed and why, where do we look?
```

Expected answer:

```text
Kibana, because it lets us inspect the logs.
```

---

## E. Recommended demo flow

1. Show the app writing logs locally.
2. Show Filebeat reading the log file.
3. Show Logstash receiving and printing events.
4. Show Elasticsearch indices.
5. Open Kibana and create the data view.
6. Generate failed requests.
7. Search for `status_code: 404` or `level: "ERROR"` in Kibana.
8. Explain how the same issue would later be detected with Prometheus metrics.

---

## F. Questions to ask during the lecture

### Question 1

Why should the application write structured JSON logs instead of plain text logs?

Expected answer:

```text
Because JSON logs are easier for Logstash and Elasticsearch to parse into fields.
```

### Question 2

Why do we use Filebeat instead of sending logs directly from the application to Elasticsearch?

Expected answer:

```text
Because the app should stay simple. Filebeat handles log shipping, retries, and file tracking.
```

### Question 3

Why do we need Logstash if Filebeat can send logs directly to Elasticsearch?

Expected answer:

```text
Logstash is useful when logs need parsing, enrichment, filtering, or routing.
```

### Question 4

Why is Prometheus separate from ELK?

Expected answer:

```text
Because Prometheus is designed for numeric time-series metrics, while ELK is usually used for logs and search.
```

### Question 5

What is the difference between `status_code: 500` in logs and `http_requests_total{status="500"}` in metrics?

Expected answer:

```text
The log record describes one event. The metric counts how many such events happened over time.
```

---

## G. Suggested student assignment questions

Students should answer:

1. What is the purpose of Filebeat?
2. What is the purpose of Logstash?
3. What is stored in Elasticsearch?
4. What is Kibana used for?
5. What type of data does Prometheus collect?
6. Why are logs and metrics both useful?
7. Which part of the stack would you check first if Kibana shows no logs?
8. Which query did you use to find errors?
9. What fields were most useful during debugging?
10. What would change if the application ran on three different VMs?

---

## H. Short answer key

1. Filebeat reads and ships log files.
2. Logstash receives, parses, enriches, and forwards events.
3. Elasticsearch stores searchable log documents.
4. Kibana is used to search, filter, and visualize logs.
5. Prometheus collects numeric time-series metrics.
6. Metrics show trends and problems; logs explain individual events.
7. Check the chain: app log file, Filebeat logs, Logstash logs, Elasticsearch indices, Kibana data view.
8. Examples: `level: "ERROR"`, `status_code: 404`, `event: "item_not_found"`.
9. Useful fields: `timestamp`, `level`, `event`, `path`, `status_code`, `duration_ms`, `request_id`.
10. Filebeat would usually run on each VM and send logs to a central Logstash or Elasticsearch service.

---

## I. Production reality note

This lab runs everything on one VM for simplicity. In production, the architecture is usually distributed:

```text
Many app hosts or containers
  ↓
Filebeat or Elastic Agent on each host
  ↓
Central Logstash or Elasticsearch cluster
  ↓
Kibana for users
```

For metrics:

```text
Many services exposing /metrics
  ↓
Prometheus scrapes them
  ↓
Dashboards and alerts
```

Production systems also need security, authentication, TLS, retention policies, index lifecycle management, alerting, backups, and capacity planning. Those topics are outside the scope of this final lab.

---

## J. References for lecturer preparation

- [Elastic: Filebeat documentation](https://www.elastic.co/docs/reference/beats/filebeat)
- [Elastic: How Logstash works](https://www.elastic.co/docs/reference/logstash/how-logstash-works)
- [Elastic: The Elastic Stack](https://www.elastic.co/docs/get-started/the-stack)
- [Elastic: Elastic Stack overview](https://www.elastic.co/elastic-stack)
- [Prometheus: Overview](https://prometheus.io/docs/introduction/overview/)
- [Prometheus: Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
