Secrets as a Service
====================

This feature deploys `Barbican`_, the OpenStack Key Manager service.

Enabling Secrets
----------------

To enable Secrets, run the following command:

::

   sunbeam enable secrets

The openstack CLI can now be used to manage Secrets. See the upstream
`Barbican CLI`_ documentation for details.

.. note::

   The :doc:`Vault </how-to/features/vault>` feature is a dependency of the
   Secrets feature and should be enabled prior to enabling Barbican.

Disabling Secrets
-----------------

To disable Secrets, run the following command:

::

   sunbeam disable secrets

Usage
-----

Users need the role ``creator`` to be able to create / read / destroy
secrets.

Verify if a user belongs to this role with (admin rights needed):

::

   openstack role assignment list --user <user id> --role creator
   +----------------------------------+----------------------------------+-------+----------------------------------+--------+--------+-----------+
   | Role                             | User                             | Group | Project                          | Domain | System | Inherited |   
   +----------------------------------+----------------------------------+-------+----------------------------------+--------+--------+-----------+
   | 3ef18094c76a403291ccf727851616ae | 4f2e8ef6b897403fb9865123b7b57a34 |       | 3e5bb39a247b471494e051ae8d0530fb |        |        | False     |
   +----------------------------------+----------------------------------+-------+----------------------------------+--------+--------+-----------+

Create a secret consisting of the string ``my_payload``, and request
just the ``Secret href`` field as output:

::

   openstack secret store --name my_secret --payload my_payload -c "Secret href"
   +-------------+-----------------------------------------------------------------------------------------+
   | Field       | Value                                                                                   |
   +-------------+-----------------------------------------------------------------------------------------+
   | Secret href | http://10.206.54.241/openstack-barbican/v1/secrets/65ad38a3-811e-4445-8472-13aa2fa5042d |
   +-------------+-----------------------------------------------------------------------------------------+

Retrieve the original secret (``my_payload``) via the secret href value:

::

   openstack secret get --payload http://10.206.54.241/openstack-barbican/v1/secrets/65ad38a3-811e-4445-8472-13aa2fa5042d
   +---------+-------------+
   | Field   | Value       |
   +---------+-------------+
   | Payload | my_payload  |
   +---------+-------------+

.. _audit-secret-decrypt-access:

Audit secret decrypt access
---------------------------

The ``secret-decrypter`` role allows a service user in the ``services`` project
to decrypt Barbican secret payloads. Audit users with this role regularly:

::

   openstack role assignment list \
      --names \
      --role secret-decrypter \
      --project services \
      --project-domain service_domain

Canonical OpenStack grants this role to the Masakari service user by default so
that instance recovery can rebuild servers with encrypted disks.

Remove secret decrypt access
----------------------------

Before removing this role, verify that the service user no longer needs to
decrypt Barbican secrets. For Masakari, disable the role request first with the
Instance Recovery configuration described in
:doc:`/how-to/features/instance-recovery`.

For each service user that should no longer have this role, run:

::

   openstack role remove \
      --user <service-user> \
      --user-domain service_domain \
      --project services \
      --project-domain service_domain \
      secret-decrypter
