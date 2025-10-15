=========================
Hardening Guide
=========================

.. _security-hardening:

This guide describes steps to secure a Canonical OpenStack (Sunbeam) deployment before 
and after it is installed.

Pre-Deployment Hardening
========================

* Use minimal Ubuntu LTS images.
* Apply all security updates and enable unattended-upgrades.
* Disable password logins, allow SSH key-based access only.
* Enable AppArmor or SELinux.
* Configure firewall rules before deployment.
* Verify Juju controller TLS certificates.

Network and Service Isolation
=============================

* Isolate management, API, tenant, and storage traffic.
* Limit inbound ports (see :doc:`ports`).
* Restrict inter-service communication using TLS.
* Use separate networks or VLANs for control plane and data plane.
* Apply security groups for tenant isolation.

Juju and Secrets
================

* Use Juju secrets for all credential exchanges between charms.
* Rotate secrets periodically and revoke unused ones.
* Restrict Juju controller access to trusted admins only.
* Store Juju controller backups encrypted and offline.

Host and Container Security
===========================

* Remove unused packages and services.
* Enforce least-privilege for system daemons.
* Enable kernel hardening (ASLR, NX bit, StackProtector).
* Use minimal container images; enforce read-only rootfs and drop privileges.
* Audit container profiles periodically.

Runtime Practices
=================

* Keep packages patched via unattended-upgrades or Canonical Livepatch.
* Rotate Fernet keys every 30–90 days.
* Enable log forwarding and auditing (see :doc:`logging-monitoring`).
* Perform quarterly security scans and reviews.

References
==========

* `Ubuntu Security <https://ubuntu.com/security>`_
* :doc:`checklist`
* :doc:`authentication`

