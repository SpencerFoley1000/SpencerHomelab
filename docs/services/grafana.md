# Grafana

## Status

Active

## Purpose

Grafana provides dashboarding and visualization for the homelab monitoring stack. It connects to Prometheus as a data source and displays collected metrics in human-readable dashboards.

Grafana helps answer operational questions such as:

- Are monitored systems healthy at a glance?
- How are CPU, memory, disk, and network usage trending?
- Which host or service needs attention first?
- Is the monitoring stack collecting usable data?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Grafana |
| Package | `grafana` |
| Host | `mon01` |
| Operating System | Debian 13.5 |
| Deployment Method | Grafana APT repository |
| Default Port | `3000/tcp` |
| Data Source | Prometheus on `localhost:9090` |
| Current Dashboard | Imported Node Exporter dashboard |

## Host

Grafana is currently installed on:

| Hostname | Role |
| --- | --- |
| `mon01` | Dedicated monitoring VM |

## Deployment Notes

Grafana was installed from the Grafana APT repository so it can be maintained through normal Debian package management.

High-level deployment steps:

1. Added the Grafana APT signing key under `/etc/apt/keyrings/`.
2. Added the Grafana stable APT repository under `/etc/apt/sources.list.d/`.
3. Refreshed package indexes with `apt-get update`.
4. Installed the `grafana` package.
5. Enabled and started the `grafana-server` systemd service.

Service validation:

```bash
systemctl is-active grafana-server
curl -I localhost:3000
```

The local HTTP check returned a redirect to `/login`, confirming that Grafana was responding.

## Data Sources

### Prometheus

Grafana is configured with Prometheus as its first data source.

| Setting | Value |
| --- | --- |
| Type | Prometheus |
| URL | `http://localhost:9090` |
| Access Scope | Local from `mon01` |
| Status | Successfully tested |

`localhost` is used because Grafana and Prometheus both run on `mon01`.

## Dashboards

An imported Node Exporter dashboard is currently used to validate end-to-end monitoring visibility.

Current dashboard status:

- Node Exporter dashboard imported.
- Prometheus selected as the dashboard data source.
- Dashboard panels display metrics collected from `mon01`.

A custom dashboard will be built later for learning value and portfolio polish. The imported dashboard proves that the pipeline works, while a custom dashboard will demonstrate understanding of PromQL, panel design, and operational priorities.

## Networking

| Item | Value |
| --- | --- |
| Listen Port | `3000/tcp` |
| Access Scope | Internal homelab only |
| Public Exposure | None |
| Browser Access | `http://<MON01_IP>:3000` |

Grafana should remain internal-only. Do not expose Grafana directly to the public internet.

## Validation Procedure

Run on `mon01`:

```bash
systemctl is-active grafana-server
curl -I localhost:3000
```

Expected results:

- `systemctl` returns `active`.
- `curl` returns an HTTP response, commonly a redirect to `/login`.

Validate from the Grafana web UI:

1. Log in to Grafana from the internal homelab network.
2. Confirm the Prometheus data source test succeeds.
3. Open the imported Node Exporter dashboard.
4. Confirm panels show data from Prometheus.

## Security Considerations

- Change the default `admin` password during initial setup.
- Store Grafana credentials in a password manager, not in this repository.
- Do not publish dashboard screenshots that expose sensitive hostnames, IP addresses, usernames, tokens, private URLs, or detailed internal topology.
- Keep Grafana internal-only unless a future reverse proxy and authentication design is documented.
- Treat dashboards as operationally sensitive because they can reveal infrastructure health, capacity, and service names.

## Backup Strategy

Grafana configuration and dashboards may become important operational state as the lab matures.

Important state includes:

- Grafana configuration files.
- Data source configuration.
- Dashboard definitions.
- User and authentication configuration.
- Documentation in this repository.

Until backup infrastructure is deployed, Grafana should be treated as rebuildable but not fully protected. Dashboards should eventually be exported as JSON or provisioned from version-controlled files after they become important.

## Recovery Procedure

If Grafana is not responding:

1. Check service status:

   ```bash
   systemctl status grafana-server
   ```

2. Check local HTTP response:

   ```bash
   curl -I localhost:3000
   ```

3. Confirm the service is listening:

   ```bash
   sudo ss -tulpn | grep grafana
   ```

4. Review logs:

   ```bash
   journalctl -u grafana-server --no-pager -n 100
   ```

5. Confirm Prometheus is healthy:

   ```bash
   curl localhost:9090/-/healthy
   ```

6. Restart Grafana if needed:

   ```bash
   sudo systemctl restart grafana-server
   ```

## Troubleshooting Notes

### Grafana Package Not Found

During setup, `apt-get install grafana` initially failed because APT could not locate the package.

Root cause pattern:

- The Grafana APT repository file was not being created or read correctly.
- APT could not index the Grafana repository until the repository file existed and `apt-get update` completed successfully.

Resolution:

- Recreated the repository file using a shell redirection method.
- Verified the file existed under `/etc/apt/sources.list.d/`.
- Ran `apt-get update`.
- Confirmed APT could locate the `grafana` package.

Operational lesson:

- If APT cannot locate a package from a third-party repository, verify the repository file, signing key, architecture, and `apt-get update` output before retrying the install.

### Grafana Service Active but Port Not Visible in Initial Check

During validation, `grafana-server` reported active, but an initial port check did not show `3000` in the expected output.

Resolution:

- Checked Grafana locally with `curl -I localhost:3000`.
- Confirmed Grafana returned an HTTP redirect to `/login`.
- Verified that the service was running and reachable.

Operational lesson:

- If a port check is unclear, test the service directly with an application-layer check such as `curl` before assuming the service is broken.

## Maintenance Notes

- Keep Grafana updated through normal package management.
- Export important dashboards after they are customized.
- Review data source health after Prometheus changes.
- Avoid storing secrets in dashboards, panel queries, or documentation.
- Build custom dashboards once monitoring coverage expands beyond `mon01`.

## Future Improvements

- Build a custom Linux host dashboard for `mon01`.
- Add dashboard coverage for `dns01` after it becomes a Prometheus scrape target.
- Add DNS availability and Pi-hole panels.
- Export important dashboards as JSON.
- Consider dashboard provisioning from version-controlled configuration.
- Add authentication and reverse proxy design only if broader access is needed.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Monitoring and Observability Architecture](../architecture/monitoring.md)
- [Prometheus Service](prometheus.md)
- [Node Exporter Service](node-exporter.md)
- [VM Inventory](../architecture/vm-inventory.md)
