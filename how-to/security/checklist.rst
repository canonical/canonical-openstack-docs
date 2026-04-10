============================
Security Hardening Checklist
============================

.. _security-checklist:

This checklist summarises key items to verify for a secure OpenStack Sunbeam environment.  
For detailed procedures, refer to :doc:`hardening`.

Infrastructure and OS
=====================

- [ ] Ubuntu LTS with all updates applied
- [ ] Minimal package set installed
- [ ] AppArmor/SELinux enabled
- [ ] SSH key-based access only
- [ ] Auditd configured and active

Networking
==========

- [ ] Management and tenant networks isolated
- [ ] Firewalls restrict only required ports (see :doc:`ports`)
- [ ] TLS configured on all APIs
- [ ] Neutron security groups enforced

Identity and Access
===================

- [ ] Keystone users and roles follow least privilege
- [ ] Fernet keys rotated regularly
- [ ] Juju secrets verified and limited to intended services

Storage and Secrets
===================

- [ ] Encrypted Cinder volumes and Glance backends
- [ ] Secrets rotated and securely backed up
- [ ] Vault or Juju secret audit logs enabled

Monitoring and Response
=======================

- [ ] Centralised logs with TLS transport
- [ ] Alerts for failed auth and certificate expiry
- [ ] Backup and restore tested quarterly
- [ ] Incident response procedures documented

References
==========

* :doc:`hardening`
* :doc:`logging-monitoring`
* :doc:`incident-response`

