# Disaster Recovery Runbook

## Purpose

Define the recovery order, decision points, service-validation requirements, and documentation process after hardware failure, configuration loss, certificate loss, or a major infrastructure outage.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Operational baseline with representative restore validation |
| Projects | Project 003 backup and recovery; Project 004 reverse proxy and internal HTTPS |
| Recovery inventory | Complete for `dns01`, `mon01`, and `proxy01` |
| VM backup recovery | Implemented for all three VMs; isolated `dns01` and `proxy01` restores tested |
| Application exports | Pi-hole and existing Grafana exports privately inspected; imports not independently tested |
| PKI recovery | Issuance and replacement documented; root CA private-key restore and rotation not independently tested |
| Last reviewed | 2026-07-14 |

The whole-VM restore path is proven locally for `dns01` and `proxy01` through isolated boots and service validation. End-to-end network behavior remains a required step during a controlled connected test or actual replacement recovery.

## Recovery Principles

- Protect people and hardware before restoring services.
- Identify the failure domain before changing systems.
- Restore foundational dependencies before dependent services.
- Preserve failed-state evidence where practical.
- Keep restored systems isolated when corruption, compromise, or duplicate identity is possible.
- Prefer a validated VM restore when available, while retaining manual rebuild paths.
- Preserve direct backend access when a convenience layer such as the proxy is unavailable.
- Treat backup artifacts, recovery exports, and certificate private keys as sensitive.
- Distinguish root CA loss from root CA compromise.
- Document deviations and permanent fixes.

## Recovery Priorities

1. Restore electrical power and physical network connectivity.
2. Restore the homelab routing boundary and managed switching.
3. Restore Proxmox management access on the active virtualization host.
4. Confirm the external backup target is mounted and active.
5. Restore `dns01` and validate public plus local DNS.
6. Restore `proxy01` if friendly HTTPS access is required; direct backend paths remain available during proxy outage.
7. Restore `mon01` and validate Prometheus, exporters, Grafana, trust store, DNS probes, HTTPS probes, and certificate metrics.
8. Confirm monitoring observes `pve01`, `dns01`, `proxy01`, and `mon01`.
9. Restore lower-priority or experimental workloads.
10. Review logs, backup state, certificate state, and documentation after recovery.

Future identity and security services must be inserted according to documented dependencies.

## Required Private Information

Keep outside this repository:

- Router and switch access details.
- Proxmox management endpoint and administrative identities.
- TOTP recovery material and physical-console instructions.
- Exact VM network values and VM IDs.
- Backup drive identity, filesystem UUID, and mount details.
- Proxmox backup storage and volume identifiers.
- Application-export locations and hashes.
- Grafana data-source UID.
- Root CA private key and passphrase.
- Service certificate private keys.
- Exact private PKI paths and protected copy locations.
- Encryption keys or backup credentials.

Public placeholders include:

- `<ROUTER_RECOVERY_NOTES>`
- `<SWITCH_RECOVERY_NOTES>`
- `<PROXMOX_MANAGEMENT_ENDPOINT>`
- `<PROXMOX_ADMIN_ACCOUNT>`
- `<BACKUP_MOUNT>`
- `<BACKUP_TARGET>`
- `<BACKUP_VOLUME_ID>`
- `<PROMETHEUS_DATASOURCE_UID>`
- `<PRIVATE_PKI_DIRECTORY>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`

## Initial Assessment

1. Determine whether the issue is power, hardware, network, hypervisor, VM, application, storage, authentication, certificate, or compromise related.
2. Confirm whether corruption or malicious activity is suspected.
3. Preserve logs, task results, hardware errors, certificate details, and failed-state evidence where practical.
4. Confirm the latest known-good backup without modifying it.
5. Confirm `<BACKUP_MOUNT>` is the actual mounted backup filesystem.
6. Decide whether recovery will use a VM backup, portable application export, protected PKI artifact, manual reconstruction, or a combination.
7. Prevent duplicate addresses and hostnames by isolating restored guests until the original instance is confirmed offline.
8. Define the validation boundary before starting so local boot success is not mistaken for complete service recovery.

## Network and Proxmox Recovery

1. Confirm the router and managed switch have power and expected link state.
2. Restore the homelab routing boundary using protected records.
3. Confirm a trusted administrative system can reach the Proxmox management plane.
4. Use `<PROXMOX_ADMIN_ACCOUNT>` for routine administration when available.
5. Use the protected `root@pam` break-glass path only when required.
6. Confirm system time before relying on TOTP or certificate validity.
7. Use physical-console access if network administration cannot be recovered safely.
8. Confirm Proxmox storage and VM inventory before starting guests.
9. Verify backup mount and storage state:

   ```bash
   findmnt <BACKUP_MOUNT>
   df -h <BACKUP_MOUNT>
   pvesm status
   ```

10. Confirm the intended backup artifact exists:

    ```bash
    pvesm list <BACKUP_TARGET>
    ```

Do not bypass mount-point enforcement or write recovery data into the Proxmox root filesystem.

## VM Restore Safety

For a test or when the original VM may still return:

- Restore to a different VM ID.
- Use a clearly temporary name.
- Remove the virtual network adapter before boot.
- Validate through the Proxmox console.
- Delete the temporary VM after testing.

Use the tested [Proxmox VM Restore Runbook](proxmox-vm-restore.md).

For an actual replacement recovery:

- Confirm the failed or old VM cannot reconnect unexpectedly.
- Review restored networking before connection.
- Reconnect only after duplicate identity risk is eliminated.
- Perform complete network, application, monitoring, and certificate validation.

## `dns01` Recovery

### Preferred VM Restore

1. Select the latest appropriate `dns01` backup.
2. Restore without overwriting a potentially recoverable source VM unless replacement is intentional.
3. Keep the restored VM network-isolated during initial boot validation.
4. Confirm Debian reaches a login prompt and expected filesystems mount.
5. Confirm local service state:

   ```bash
   systemctl is-active pihole-FTL
   systemctl is-active prometheus-node-exporter
   systemctl --failed
   ```

6. Assess every failed unit.
7. Confirm the original VM cannot conflict with the restored copy.
8. Review the intended network adapter, bridge, and private static configuration.
9. Reconnect networking.
10. Validate local and recursive DNS from a trusted client.
11. Confirm `grafana.lab.home.arpa` and `pihole.lab.home.arpa` records return `<PROXY01_IP>`.
12. Confirm remote monitoring recovers.

### Manual Rebuild

1. Deploy a supported Debian VM.
2. Recreate static networking using protected operational values.
3. Install Pi-hole and Node Exporter.
4. Import the protected Pi-hole Teleporter archive.
5. Confirm upstream resolver settings and local records.
6. Validate services and monitoring.

### Required Validation

```promql
up{job="node_exporter", host="dns01"}
```

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

Expected results are `1` after networking is restored.

## `proxy01` Recovery

### Preferred VM Restore

1. Select the latest appropriate `proxy01` backup.
2. Restore to a temporary ID if the original may still return.
3. Remove the network adapter before first boot.
4. Confirm Debian boot and expected filesystems.
5. Confirm local service state:

   ```bash
   systemctl is-active docker
   systemctl is-active prometheus-node-exporter
   systemctl is-active qemu-guest-agent
   ```

6. Confirm NGINX Proxy Manager:

   ```bash
   sudo docker compose \
     -f /opt/nginx-proxy-manager/compose.yml \
     ps
   ```

7. Confirm listeners and persistent state:

   ```bash
   sudo ss -lntp | grep -E ':(80|81|443|9100)\b'
   curl -I http://127.0.0.1:81
   sudo ls -la /opt/nginx-proxy-manager
   ```

8. Confirm the original VM cannot conflict with the restored copy.
9. Reconnect the intended network adapter and stable address.
10. Confirm Pi-hole local records point service names to the restored proxy.
11. Validate both HTTPS routes and direct backend paths.
12. Confirm Node Exporter, HTTPS probes, and certificate lifetime recover.

### Manual Rebuild

1. Deploy a supported Debian VM named `proxy01`.
2. Install QEMU Guest Agent, Node Exporter, Docker Engine, and Docker Compose.
3. Recreate `/opt/nginx-proxy-manager/compose.yml`.
4. Restore protected NGINX Proxy Manager state or recreate proxy hosts manually.
5. Import the current service certificate and private key from protected storage.
6. Confirm Pi-hole local records point to the new proxy address.
7. Validate Grafana and Pi-hole routes.
8. Add monitoring and backup coverage.

### Required Validation

```promql
up{job="node_exporter", host="proxy01", role="reverse-proxy"}
```

```promql
probe_success{job="blackbox_https_internal"}
```

```promql
(probe_ssl_earliest_cert_expiry{job="blackbox_https_internal"} - time()) / 86400
```

The service certificate and NGINX Proxy Manager database are protected by the VM backup. The root CA private key is not stored on `proxy01` and requires separate protected recovery.

## Private CA Recovery

### Root Key Lost but Not Compromised

1. Existing issued certificates remain usable until expiration.
2. New certificates cannot be issued from the lost CA.
3. Create a replacement root CA on a trusted workstation.
4. Issue replacement service certificates.
5. Install the replacement public root certificate on trusted clients and `mon01`.
6. Replace certificates in NGINX Proxy Manager.
7. Validate HTTPS and monitoring.
8. Remove the old trust anchor after migration.

### Root Key Exposed or Compromised

1. Treat all certificates issued by that CA as untrusted.
2. Create a replacement CA and new service keys on a trusted system.
3. Replace all service certificates.
4. Remove the compromised trust anchor from clients.
5. Review systems and backups that contained affected material.
6. Document scope and remediation without publishing secrets.

See [Internal Certificate Lifecycle](internal-certificate-lifecycle.md).

## `mon01` Recovery

### Preferred VM Restore

1. Select the latest appropriate `mon01` backup.
2. Restore in an isolated or controlled state.
3. Confirm Debian and expected filesystems boot normally.
4. Confirm service state:

   ```bash
   systemctl is-active prometheus
   systemctl is-active grafana-server
   systemctl is-active prometheus-node-exporter
   systemctl is-active prometheus-blackbox-exporter
   ```

5. Confirm the public root CA certificate exists in the Debian trust store.
6. Validate Prometheus and Blackbox configuration.
7. Confirm all required jobs, targets, and modules exist.
8. Confirm the Grafana Prometheus data source is healthy.
9. Confirm protected dashboards display current data.

`mon01` has successful backup coverage but has not been independently restore-tested. Treat its VM restore path as less mature than `dns01` and `proxy01` until exercised.

### Manual Rebuild

1. Deploy a supported Debian VM.
2. Install Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
3. Restore or recreate `/etc/prometheus/prometheus.yml` and `/etc/prometheus/blackbox.yml`.
4. Install the public root CA certificate in the system trust store.
5. Confirm Prometheus jobs:
   - `prometheus`
   - `node_exporter`
   - `blackbox_dns`
   - `blackbox_dns_local`
   - `blackbox_https_internal`
6. Confirm Blackbox modules:
   - `dns_udp`
   - `dns_udp_local`
   - `https_internal`
7. Restore Grafana consistently or recreate its Prometheus data source.
8. Import available protected dashboard JSON.
9. Verify data-source mappings, panels, and variables.

### Required Monitoring Validation

```promql
count by (job, instance) (up)
```

```promql
up{job="node_exporter"}
```

```promql
probe_success{job=~"blackbox_dns.*", host="dns01"}
```

```promql
probe_success{job="blackbox_https_internal"}
```

Expected host targets are `mon01`, `dns01`, `pve01`, and `proxy01`. Both DNS probes and both HTTPS probes should return `1`.

## Post-Recovery Validation

Confirm:

- Trusted clients have expected network connectivity.
- Proxmox routine and break-glass management paths work.
- Backup storage is mounted and active.
- `dns01` answers public and local DNS queries.
- `proxy01` serves the intended HTTPS routes with a trusted, unexpired certificate.
- Direct backend access remains available.
- `mon01` observes all intended host and service targets.
- Grafana dashboards show current host, DNS, HTTPS, and certificate data.
- No duplicate VMs, hostnames, MAC addresses, or IP addresses remain.
- Temporary recovery adapters, credentials, or firewall exceptions are removed.
- Logs show no unresolved recurring failure.
- A new backup is created after stable production recovery when appropriate.

## Restore-Test Evidence

The 2026-07-14 `dns01` test proved backup readability, VM reconstruction, safe restoration under a different ID, network isolation, Debian boot, filesystem availability, Pi-hole FTL, Node Exporter, and safe cleanup.

The 2026-07-14 `proxy01` test proved backup readability, VM reconstruction, network isolation, Debian boot, Docker, QEMU Guest Agent, Node Exporter, NGINX Proxy Manager, expected listeners, persistent proxy and service-certificate state, and safe cleanup.

Neither isolated test proved live network cutover. Public documentation must preserve that distinction.

## Post-Recovery Review

Document:

- Failure scope and likely root cause.
- Recovery method and artifact used.
- Recovery start and completion time.
- Validation performed.
- What worked well.
- Deviations from the runbook.
- Temporary actions removed.
- Permanent fixes or architecture changes.
- Whether backup, monitoring, PKI, security, storage, or documentation controls should change.

Update relevant service pages, project pages, architecture pages, VM inventory, changelog or dated change record, and roadmap when priorities change.

## Security Considerations

- Do not publish recovery keys, TOTP seeds, backup credentials, certificate private keys, private paths, or backup identifiers.
- Treat restored systems as untrusted until the source and incident scope are understood.
- Never connect duplicate restored guests to production.
- Remove temporary credentials and emergency access after recovery.
- Keep attacker-style workloads away from trusted backup storage, proxy administration, and PKI material.
- Rotate affected credentials and certificates after suspected compromise.
- Do not rely on the directly attached drive or one workstation as the only future copy for high-value recovery material.

## Remaining Improvements

- Perform an independent `mon01` restore test.
- Perform controlled network-connected recovery tests when duplicate identity risk can be eliminated.
- Add measured recovery-time and recovery-point objectives.
- Add backup task, age, capacity, and failure monitoring.
- Create a second encrypted or offline root CA private-key copy in a separate failure domain.
- Create a second VM backup copy in a separate failure domain when justified.

## Related Documentation

- [Backup Runbook](backup.md)
- [Proxmox VM Restore](proxmox-vm-restore.md)
- [Internal Certificate Lifecycle](internal-certificate-lifecycle.md)
- [Service Configuration Export and Inspection](service-config-export.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [ADR-0003](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [ADR-0004](../decisions/ADR-0004-internal-reverse-proxy-and-private-ca.md)
- [Storage Architecture](../architecture/storage.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Security Architecture](../architecture/security.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Pi-hole Service](../services/pihole.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
