# Prometheus Scrape Target Troubleshooting

## Purpose

This runbook documents how to troubleshoot missing Prometheus scrape data when Grafana dashboards suddenly stop showing metrics.

The immediate incident that created this runbook happened after adding Blackbox Exporter DNS probing. The Grafana Node Exporter dashboard stopped showing current host data, and the root cause was a malformed or incomplete Prometheus scrape configuration rather than a Grafana problem.

## When to Use This Runbook

Use this runbook when:

- A Grafana dashboard shows `No data`, `N/A`, or stops updating.
- A previously working Prometheus job disappears from query results.
- A dashboard variable such as `job`, `instance`, or `nodename` no longer behaves as expected.
- Prometheus was recently edited or restarted.
- New scrape jobs were added and existing jobs stopped working.

## Preconditions

Required access:

- Shell access to `mon01`.
- Ability to use `sudo` on `mon01`.
- Browser access to Prometheus at `http://<MON01_IP>:9090`.
- Browser access to Grafana at `http://<MON01_IP>:3000`.

Assumptions:

- Prometheus runs on `mon01`.
- Grafana runs on `mon01`.
- Node Exporter runs on `mon01` and `dns01`.
- Blackbox Exporter runs locally on `mon01`.
- Public documentation uses sanitized placeholders such as `<MON01_IP>` and `<DNS01_IP>`.

## Symptoms Observed

Observed behavior:

- Grafana Node Exporter dashboard stopped tracking current data.
- Dashboard panels showed `N/A` or `No data`.
- Existing graph data stopped at a specific point in time.
- Prometheus query returned no data for:

```promql
up{job="node_exporter"}
```

This indicated the issue was upstream of Grafana. Grafana could not display Node Exporter data because Prometheus no longer had an active `node_exporter` job series.

## Troubleshooting Procedure

### 1. Check Prometheus Job Visibility

In Prometheus, run:

```promql
up
```

Then run:

```promql
count by (job, instance) (up)
```

Expected jobs after Project 002 DNS monitoring:

```text
prometheus
node_exporter
blackbox_dns
```

If `node_exporter` is missing, the issue is likely Prometheus scrape configuration rather than Grafana.

### 2. Confirm Node Exporter Endpoints Still Work

Run on `mon01`:

```bash
curl localhost:9100/metrics | head
```

Validate the remote `dns01` Node Exporter endpoint from `mon01`:

```bash
curl http://<DNS01_IP>:9100/metrics | head
```

If these commands return Prometheus-formatted metrics, Node Exporter is healthy and reachable.

### 3. Inspect Prometheus Scrape Jobs

Run on `mon01`:

```bash
sudo grep -n "job_name" /etc/prometheus/prometheus.yml
```

Expected job names:

```text
prometheus
node_exporter
blackbox_dns
```

Then inspect the scrape configuration block:

```bash
sudo grep -nA80 "scrape_configs:" /etc/prometheus/prometheus.yml
```

Confirm that each job is a separate top-level item under `scrape_configs:`.

Correct structure:

```yaml
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['localhost:9100']
        labels:
          host: 'mon01'
          role: 'monitoring'

      - targets: ['<DNS01_IP>:9100']
        labels:
          host: 'dns01'
          role: 'dns'

  - job_name: 'blackbox_dns'
    metrics_path: /probe
    params:
      module: [dns_udp]
    static_configs:
      - targets:
          - '<DNS01_IP>:53'
        labels:
          host: 'dns01'
          service: 'dns'
          protocol: 'udp'
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: localhost:9115
```

Common mistakes:

- Accidentally deleting the `node_exporter` job.
- Nesting `blackbox_dns` inside another job.
- Breaking YAML indentation.
- Keeping a valid YAML file that passes syntax checks but no longer contains the intended jobs.

### 4. Validate Prometheus Configuration

Before restarting Prometheus, run:

```bash
promtool check config /etc/prometheus/prometheus.yml
```

Only restart Prometheus after the config passes validation:

```bash
sudo systemctl restart prometheus
systemctl is-active prometheus
```

### 5. Validate Recovery in Prometheus

In Prometheus, run:

```promql
up
```

Then validate Node Exporter specifically:

```promql
up{job="node_exporter"}
```

Expected result:

```text
mon01 = 1
dns01 = 1
```

Validate the DNS probe is still working:

```promql
probe_success{job="blackbox_dns"}
```

Expected result:

```text
1
```

### 6. Validate Recovery in Grafana

Open the imported Node Exporter dashboard and confirm:

- The `node_exporter` job is available.
- `mon01` and `dns01` are selectable.
- Graphs resume updating.
- New data appears after the Prometheus scrape interval completes.

Open the `Homelab Service Health` dashboard and confirm:

- DNS availability shows success.
- DNS probe duration is present.
- DNS probe status continues updating.

## Recovery Notes

Before editing Prometheus configuration, create a local backup:

```bash
sudo cp /etc/prometheus/prometheus.yml /etc/prometheus/prometheus.yml.bak-$(date +%Y%m%d-%H%M)
```

If a configuration edit breaks scrape jobs, restore the most recent known-good backup or re-add the missing job blocks manually.

Prometheus can pass syntax validation while still being operationally wrong. `promtool` verifies syntax and some structure, but it does not prove that all intended scrape jobs still exist. Always verify expected jobs with PromQL after configuration changes.

## Lessons Learned

- Grafana is usually the symptom, not the source, when dashboard data disappears.
- Prometheus should be checked before troubleshooting Grafana panel settings.
- `up{job="node_exporter"}` returning no data means the job is missing, renamed, or not currently scraped.
- A valid YAML file can still be the wrong configuration.
- After editing Prometheus, validate both configuration syntax and expected scrape job presence.
- Back up configuration files before editing them, especially when adding new scrape jobs.

## Related Documentation

- [Monitoring and Observability Architecture](../architecture/monitoring.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
- [Node Exporter Service](../services/node-exporter.md)
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
