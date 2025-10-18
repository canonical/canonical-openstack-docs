================================
Authentication and Authorization
================================

.. _security-authentication:

This guide focuses on identity management, Fernet tokens, and service credentials.

Keystone Overview
=================

Keystone provides authentication, authorization, and service discovery for OpenStack.  
Sunbeam configures Keystone automatically and registers service users via Juju.

Key Concepts
------------

* **Domains**: logical boundaries for users and projects.
* **Projects**: map to tenants or teams.
* **Roles**: define permissions; assign to users per project or domain.

Example commands:

.. code-block:: bash

   openstack user create --domain default --project demo demo-user
   openstack role add --project demo --user demo-user member

Fernet Token Management
=======================

Sunbeam supports only Fernet tokens for authentication.  
These are lightweight, stateless, and cryptographically signed.

* Keys are distributed and rotated via Juju secrets.
* Default rotation interval: 30–90 days.
* Rotation command (for reference):

.. code-block:: bash

   juju run keystone/leader "keystone-manage fernet_rotate"

Juju Secrets and Service Authentication
=======================================

All inter-service credentials (e.g., Nova→Keystone, Neutron→RabbitMQ) are exchanged using **Juju secrets**.

* Secrets are encrypted and versioned automatically.
* They can be revoked, refreshed, and audited.
* Avoid storing credentials in plain charm config.

Federated Identity (Optional)
=============================

Keystone supports SAML or OIDC federation for SSO.

* Validate IdP metadata signatures.
* Map external attributes carefully to local roles.
* Restrict project scopes for federated users.

References
==========

* :doc:`logging-monitoring`
* `Keystone Security Guide <https://docs.openstack.org/keystone/latest/admin/>`_

