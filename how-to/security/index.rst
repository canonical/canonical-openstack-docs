======================
Security Overview
======================

.. _security-index:

The Canonical OpenStack (Sunbeam) security documentation provides guidance for securing 
your deployment from initial planning through day-to-day operations.

This collection of guides covers host hardening, authentication and authorization, 
secure secrets handling, port and network reference, logging and auditing, and incident response.

Security Philosophy
===================

Canonical OpenStack is built on Ubuntu, leveraging its long-term security maintenance, 
kernel livepatching, and strict package provenance. Sunbeam adds automation and 
secure defaults via Juju, reducing operator error and improving repeatability.

Security objectives include:

* Protect confidentiality, integrity, and availability of infrastructure and tenant workloads.
* Reduce attack surface across control plane and data plane.
* Enforce cryptographic integrity for authentication and data in transit.
* Enable secure, automated secret management with Juju.
* Provide auditable and traceable change and access history.

Defense Layers
==============

Security is achieved through layered defenses:

1. **Host layer:** Ubuntu security, kernel hardening, AppArmor.
2. **Deployment layer:** Juju relations, secrets, and automation.
3. **Service layer:** OpenStack APIs, Keystone authentication, Fernet tokens.
4. **Network layer:** Segmented management, storage, and tenant networks.
5. **Operational layer:** Logging, auditing, and patching discipline.

.. toctree::
   :maxdepth: 2

   hardening
   checklist
   ports
   authentication
   logging-monitoring
   incident-response
   compliance

