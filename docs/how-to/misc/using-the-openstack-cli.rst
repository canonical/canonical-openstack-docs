.. _Using the OpenStack CLI:

Using the OpenStack CLI
=======================

Once OpenStack has been deployed you can interact with your cloud via
the CLI by using the standard ``openstack`` client commands. The CLI
client is provided as part of the ``openstack`` snap.

The client recognizes the environment variables stored in generated
credential files. Source a cloud credentials file to set these environment
variables in the current shell before using the client:

::

   source <init-file>

For help with command syntax see the documentation for the
`python-openstackclient <https://docs.openstack.org/python-openstackclient/latest/cli/command-list.html>`__
package.

Unprivileged vs admin user credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unprivileged user credentials are generated at cloud-configuration time
with the ``sunbeam configure`` command.

Admin user credentials are generated with the ``sunbeam openrc``
command. Here, the file ``admin-openrc`` is chosen as init file:

::

   sunbeam openrc > admin-openrc

