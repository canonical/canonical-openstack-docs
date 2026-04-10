=================================
Logging, Auditing, and Monitoring
=================================

.. _security-logging:

Comprehensive logging and monitoring provide traceability, compliance, 
and rapid incident response.

Centralised Logging
===================

* Aggregate logs via Loki, Elastic, or other secure collectors.
* Protect log transport using TLS.
* Enforce retention and access controls.
* Enable log integrity checks (e.g., hash chains or WORM storage).

Keystone Authentication Middleware Logs
=======================================

The Keystone auth middleware (``keystonemiddleware.auth_token``) records 
token validation, user identification, and policy enforcement events.

Example locations:

- ``/var/log/keystone/keystone.log``
- API service logs containing middleware messages (e.g., Nova API logs)

Enable verbose logging for token validation if required for audits:

.. code-block:: ini

   [keystone_authtoken]
   http_request_debug = true
   log_level = INFO

Auditing
========

* Enable audit notifications in Keystone, Nova, and Neutron.
* Forward audit events to a SIEM or monitoring system.
* Retain logs per compliance (e.g. 90–180 days).

Monitoring and Alerting
=======================

* Monitor certificate expiry, failed logins, API latency, and service availability.
* Integrate with Prometheus or Canonical Observability Stack.
* Define thresholds and alert routing to the on-call team.

Security Analytics
==================

* Correlate Keystone authentication anomalies (e.g., multiple failed tokens).
* Detect large volume API bursts (potential abuse).
* Use dashboards for per-service security posture.

References
==========

* :doc:`authentication`
* `Keystonemiddleware Docs <https://docs.openstack.org/keystonemiddleware/latest/>`_

