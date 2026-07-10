# Service Configuration Export and Inspection

## Purpose

Provide a repeatable process for creating, protecting, validating, and documenting portable service-configuration exports without exposing private operational data in the public repository.

This runbook currently covers:

- Pi-hole Teleporter ZIP exports.
- Grafana dashboard JSON exports.
- Private integrity and sensitivity checks.
- Public documentation requirements.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Operational checklist |
| Last validated | 2026-07-10 |
| Validated scope | Pi-hole Teleporter export and two Grafana dashboard exports |
| Restore validation | Not yet completed |
| Owner | Homelab administrator |

Export creation and inspection have been exercised. Import and restore procedures remain unvalidated until a controlled recovery test succeeds.

## Scope

This runbook applies to:

- `dns01`: Pi-hole Teleporter export.
- `mon01`: Grafana dashboard JSON exports.
- A private administrative workstation used to store and inspect exports.

It does not replace Proxmox VM backups. Portable exports provide an application-level recovery option and improve understanding of service dependencies.

## Preconditions

Before starting, confirm:

- Administrative access to the service is available.
- The destination is private storage outside the Git repository.
- The original export will remain intact.
- No export contents will be pasted into public issues, commits, screenshots, or documentation.
- The service is in a stable state before export.

Use a private directory structure similar to:

```text
<PRIVATE_EXPORT_ROOT>/
├── dns01/
│   └── pihole/
└── mon01/
    └── grafana/
```

The actual private path is intentionally excluded from this repository.

## Safety Notes

- Treat all exports as sensitive until inspected.
- Never commit raw exports by default.
- Preserve original files before creating sanitized copies.
- Do not print secret values while scanning files.
- Record hashes privately so artifact integrity can be checked later.
- A successful syntax or archive-integrity check does not prove that restoration will succeed.

## Pi-hole Teleporter Export

### Create the Export

1. Open the Pi-hole administrative interface from the trusted homelab network.
2. Use the Teleporter export function.
3. Save the generated ZIP directly to protected private storage.
4. Do not rename or modify the original artifact unless the private inventory is updated.
5. Record:
   - Export date.
   - Filename.
   - Logical size in bytes.
   - SHA-256 hash.
   - Pi-hole version.

### Validate Archive Integrity

Run from PowerShell on the private workstation:

```powershell
$zip = "<PRIVATE_TELEPORTER_ZIP>"

if (-not (Test-Path -LiteralPath $zip)) {
    throw "Teleporter archive not found: $zip"
}

Get-Item -LiteralPath $zip |
    Select-Object Name, Length, LastWriteTime

Get-FileHash -LiteralPath $zip -Algorithm SHA256

Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [System.IO.Compression.ZipFile]::OpenRead($zip)

try {
    $archive.Entries |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_.Name) } |
        Select-Object FullName, Length, CompressedLength
}
finally {
    $archive.Dispose()
}
```

Expected result:

- The archive opens without an exception.
- Entry names and sizes are readable.
- A SHA-256 hash is produced.

### Inspect Without Exposing Values

Classify the archive using counts and property names rather than printing matched values.

Check for:

- Private IPv4 addresses.
- MAC addresses.
- Internal URLs or hostnames.
- Email addresses.
- Database files.
- Lease data.
- Authentication-related property names.
- Key or certificate files.

The validated `dns01` Teleporter export contained environment-specific network data, databases, lease data, and a `totp_secret` property. This confirms that the artifact must remain private. The secret value was not published or added to documentation.

### Pi-hole Export Validation

Confirm:

- ZIP integrity passes.
- The original archive remains intact.
- The hash is recorded privately.
- Sensitive indicators are documented only as categories or counts.
- The raw artifact remains outside Git.

## Grafana Dashboard Export

### Create Dashboard JSON

For each dashboard:

1. Open the dashboard in Grafana.
2. Open dashboard editing or settings.
3. Open the dashboard JSON model.
4. Copy the entire JSON document.
5. Save it to private storage with a descriptive filename.
6. Preserve the original JSON without sanitizing it in place.

Current protected exports:

- Node Exporter dashboard.
- Homelab Service Health dashboard.

### Validate JSON Syntax

Run from PowerShell:

```powershell
Get-Content "<DASHBOARD_JSON>" -Raw |
    ConvertFrom-Json |
    Select-Object title, uid, schemaVersion
```

A successful parse confirms valid JSON syntax. It does not prove that the dashboard will import successfully.

### Inspect Sensitive Property Names

Inspect JSON property paths without printing their values. Search for names containing terms such as:

```text
password
passwd
secret
token
api-key
authorization
bearer
cookie
private-key
```

Also count or identify environment-specific references such as:

- Private IP addresses.
- Internal URLs.
- Hostnames.
- Data-source names and UIDs.
- Dashboard links and annotations.

Keyword matches in ordinary text do not automatically indicate a secret. Review JSON property names and structure before classifying a match.

### Record Data-Source Mapping

Dashboard exports do not always contain `__inputs` or explicit data-source objects.

Record the active data source separately:

| Setting | Public documentation value |
| --- | --- |
| Name | `prometheus` |
| Type | `prometheus` |
| URL | `http://localhost:9090` |
| UID | `<PROMETHEUS_DATASOURCE_UID>` |

Keep the actual UID with private recovery records. During recovery, create or validate the data source before importing dashboards and verify panel and variable mappings afterward.

## Documentation Requirements

After creating or replacing an export, update:

- The relevant service page.
- The active backup or recovery project page.
- This runbook if the procedure changes.
- `CHANGELOG.md` when the work completes a meaningful project milestone.

Public documentation may include:

- Export type.
- Creation and validation date.
- Logical size.
- Integrity result.
- Sanitized content classifications.
- Recovery dependencies.

Public documentation must not include:

- Raw archives or dashboard JSON.
- Passwords or TOTP secrets.
- Tokens, cookies, or authentication headers.
- Exact private IP addresses or MAC addresses.
- Private DNS records or query history.
- Personally identifying values.

## Retention

Until a formal retention policy is implemented:

- Keep the latest known-good export.
- Retain a previous known-good export when configuration changes are substantial.
- Create a fresh export after meaningful service changes.
- Remove obsolete copies intentionally rather than accumulating untracked artifacts.
- Protect private exports with workstation access controls and the future external backup process.

## Recovery Notes

### Pi-hole

1. Install a compatible Pi-hole version on a supported Debian system.
2. Recreate required networking using protected operational values.
3. Import the protected Teleporter archive.
4. Validate local records, public resolution, service status, and monitoring.

### Grafana

1. Install a supported Grafana version.
2. Create or validate the Prometheus data source.
3. Import protected dashboard JSON.
4. Map panels and variables to the Prometheus data source.
5. Validate both dashboards against current Prometheus data.

These recovery paths remain drafts until a controlled import or restore test succeeds.

## Rollback

Export creation is non-destructive. If inspection or documentation is incorrect:

1. Keep the original artifact unchanged.
2. Discard only temporary inspection copies or sanitized derivatives.
3. Repeat validation from the original export.
4. Correct the private inventory and public documentation.

## Related Documentation

- [Runbooks README](README.md)
- [Backup Runbook](backup.md)
- [Disaster Recovery Runbook](disaster-recovery.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Pi-hole Service](../services/pihole.md)
- [Grafana Service](../services/grafana.md)
