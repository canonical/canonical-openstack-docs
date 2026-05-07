LDAP Integration
================

This feature integrates the OpenStack
`Keystone <https://docs.openstack.org/keystone>`__ service with an
external LDAP service. Effectively, the feature maps LDAP-based users to
cloud users via an OpenStack domain.

Enabling LDAP
-------------

To enable the LDAP feature, run the following command:

.. literalinclude:: ../snippets/ldap.task.sh
   :language: bash
   :start-after: [docs-view:enable-ldap]
   :end-before:  [docs-view:enable-ldap-end]

Disabling LDAP
--------------

To disable the LDAP feature, run the following command:

.. literalinclude:: ../snippets/ldap.task.sh
   :language: bash
   :start-after: [docs-view:disable-ldap]
   :end-before:  [docs-view:disable-ldap-end]

Usage
-----

Adding a domain
~~~~~~~~~~~~~~~

Adding a domain refers to integrating Keystone with one or more existing
LDAP servers.

1. Create a YAML file with details of how Keystone should integrate with
   the LDAP server. At a minimum, this should include a URL, user,
   password, and suffix. See the `Keystone LDAP integration
   guide <https://docs.openstack.org/keystone/2023.2/admin/configuration.html#integrate-identity-with-ldap>`__
   for configuration guidance.

   For example:

   **dom1.yaml**:

.. code:: text

       url: ldaps://ldap.example.com:636
       user: cn=admin,dc=example,dc=com
       password: mypassword
       suffix: dc=example,dc=com

2. If the connection requires TLS, place the CA certificate in a file:

   **dom1.cert**:

.. code:: text

       -----BEGIN CERTIFICATE-----
       ...
       -----END CERTIFICATE-----

3. Use the ``sunbeam ldap add-domain`` command to set up the domain,
   adding the ``--ca-cert-file`` option if TLS is in use:

.. literalinclude:: ../snippets/ldap.task.sh
   :language: bash
   :start-after: [docs-view:ldap-add]
   :end-before:  [docs-view:ldap-add-end]

4. A new LDAP-backed domain will be created in Keystone. Verify this
   with the native ``openstack`` CLI:

   openstack user list –domain dom1

.. code:: text

       +-------------------------------------------+---------------+
       |                                           | Name          |
       +-------------------------------------------+---------------+
       | 941b5daa177ea518b5fc3b85fe9269729eb6abbb1 | John Hethel   |
       | d3b9d2bea306a049d4f56d30d6bba97b24c6db882 | Ryan Trunch   |
       | 7b699dc9a8037d6968c42c5b7b5d5a020d0f58e40 | Michael Diss  |
       +-------------------------------------------+---------------+

Updating a domain
~~~~~~~~~~~~~~~~~

To update an LDAP domain the process is similar to adding one:

.. literalinclude:: ../snippets/ldap.task.sh
   :language: bash
   :start-after: [docs-view:ldap-update]
   :end-before:  [docs-view:ldap-update-end]

Listing domains
~~~~~~~~~~~~~~~

To list LDAP domains:

.. literalinclude:: ../snippets/ldap.task.sh
   :language: bash
   :start-after: [docs-view:ldap-list]
   :end-before:  [docs-view:ldap-list-end]

Removing a domain
~~~~~~~~~~~~~~~~~

To remove an LDAP domain:

.. literalinclude:: ../snippets/ldap.task.sh
   :language: bash
   :start-after: [docs-view:ldap-remove]
   :end-before:  [docs-view:ldap-remove-end]

.. important::
   Since configuration (e.g. OpenStack projects) could have been made to the
   domain after it was added, the ``remove-domain`` command only removes the
   LDAP connection. To completely remove the domain, the ``openstack`` CLI
   should be used (i.e. ``openstack domain delete``).
