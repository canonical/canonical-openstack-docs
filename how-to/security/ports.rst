=============================
Ports and Protocols Reference
=============================

.. _security-ports:

This reference lists default service ports for Canonical OpenStack (Sunbeam) deployments.  
Use it to configure firewalls and validate exposed endpoints.

Core Services
=============

.. include:: includes/openstack-ports-full.rst

Port Security Guidance
======================

* Allow inbound access only from trusted networks.
* Prefer TLS-enabled ports (e.g., 5671 instead of 5672).
* Disable HTTP on 80 when HTTPS (443) is enabled.
* Restrict SSH (22) to management or bastion hosts.
* Periodically scan with ``ss -tuln`` or ``nmap`` to confirm open ports.

References
==========

* :doc:`hardening`
* `OpenStack Firewall Reference <https://docs.openstack.org/install-guide/firewalls-default-ports.html>`_

