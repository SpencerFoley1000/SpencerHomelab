# QEMU Guest Agent Troubleshooting Runbook

## Purpose

This runbook documents how to troubleshoot QEMU Guest Agent issues on Debian VMs running under Proxmox VE.

The QEMU Guest Agent allows Proxmox to communicate with a guest VM for improved visibility and management, including guest IP reporting and cleaner shutdown behavior.

## Scope

Applies to:

- Proxmox VE virtual machines.
- Debian-based guest operating systems.
- VMs where QEMU Guest Agent is installed but not reporting correctly.

## Symptoms

Common symptoms include:

- Proxmox does not show guest IP information.
- `qemu-guest-agent` is installed but inactive.
- Starting the service fails with a dependency error.
- `/dev/virtio-ports/` does not exist inside the guest.
- `/dev/virtio-ports/org.qemu.guest_agent.0` is missing.

Example checks:

```bash
systemctl is-active qemu-guest-agent
ls -l /dev/virtio-ports/
```

## Expected Healthy State

Inside the guest VM:

```bash
systemctl is-active qemu-guest-agent
```

Expected result:

```text
active
```

The virtio port should exist:

```bash
ls -l /dev/virtio-ports/
```

Expected result should include:

```text
org.qemu.guest_agent.0
```

## Troubleshooting Procedure

### 1. Confirm the Package Is Installed

Inside the guest VM:

```bash
dpkg -l | grep qemu-guest-agent
```

A healthy package installation should show a line beginning with `ii`.

If the package is missing:

```bash
sudo apt update
sudo apt install -y qemu-guest-agent
```

### 2. Check Service Status

```bash
systemctl status qemu-guest-agent
```

If it is inactive or failed, continue to the next steps.

### 3. Check the Proxmox VM Option

In the Proxmox web interface:

1. Select the VM.
2. Open **Options**.
3. Confirm **QEMU Guest Agent** is enabled.

From the Proxmox host shell, the VM configuration should include:

```text
agent: 1
```

Check with:

```bash
qm config <VMID>
```

Replace `<VMID>` with the Proxmox VM ID. Do not publish VM IDs in public documentation unless intentionally sanitized.

### 4. Check for the Virtio Guest Agent Device

Inside the guest VM:

```bash
ls -l /dev/virtio-ports/
```

If this directory or the `org.qemu.guest_agent.0` device is missing, the guest OS cannot communicate with the Proxmox guest agent channel.

### 5. Perform a Full Proxmox Stop/Start

If the package is installed and Proxmox shows `agent: 1`, but the virtio device is missing:

1. Shut down the VM from Proxmox.
2. Wait until the VM shows as fully stopped.
3. Start the VM again from Proxmox.
4. Recheck the virtio port inside the guest.

A guest-only reboot may not recreate missing virtual hardware. A full Proxmox stop/start recreates the VM process and virtual hardware devices.

### 6. Validate Resolution

Inside the guest VM:

```bash
ls -l /dev/virtio-ports/
systemctl is-active qemu-guest-agent
```

Expected results:

- `/dev/virtio-ports/org.qemu.guest_agent.0` exists.
- `qemu-guest-agent` returns `active`.

Then confirm Proxmox displays improved guest information for the VM.

## Root Cause Pattern

This issue can occur when Proxmox configuration indicates that the guest agent is enabled, but the running VM process has not recreated the virtual hardware channel.

The guest OS may be correctly configured, while the required virtual device is missing from the hypervisor layer.

## Operational Lesson

Troubleshoot virtualization issues by layer:

1. Guest OS package installed?
2. Guest OS service running?
3. Hypervisor option enabled?
4. Virtual hardware device present inside the guest?
5. Full hypervisor-level stop/start performed after hardware changes?

This avoids randomly reinstalling packages when the actual issue is missing virtual hardware.

## Security Considerations

- Do not publish exact VM IDs, internal IP addresses, MAC addresses, or screenshots showing sensitive infrastructure details.
- QEMU Guest Agent improves VM manageability but should be treated as part of the trusted virtualization management plane.
- Keep guest packages updated through standard patching.

## Related Documentation

- [VM Inventory](../architecture/vm-inventory.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
