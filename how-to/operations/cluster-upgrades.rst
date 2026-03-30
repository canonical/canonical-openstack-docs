Cluster upgrades
================

Overview
--------

A full cluster refresh is a multi-step process. Some components require
dedicated refresh commands and must be refreshed in a specific order before
running the general ``sunbeam cluster refresh`` command.

.. note::
   Refreshing across release tracks is not supported. For example, you cannot
   use the refresh command to upgrade from ``2024.1/stable`` to ``2025.1/stable``.

Prerequisites
-------------

To ensure the latest updates are available to the cluster charms, refresh the
``openstack`` snap before running any cluster refresh commands.

* **Manual provider:** Run ``sudo snap refresh openstack`` on all nodes.
* **MAAS provider:** Run it on the sunbeam client node only.

.. important::
   Refreshing the ``openstack`` snap does not automatically refresh the
   cluster. You must explicitly run the dedicated cluster refresh commands
   described below to apply updates to the running services.

.. _refresh-vault:

Step 1 - Refresh Vault
----------------------

Vault requires a dedicated refresh command. Run:

.. code:: text

   sunbeam cluster refresh vault

Following a refresh, the Vault charm is left in a sealed state.
Unless Vault was enabled in dev mode, you must manually unseal it.

For detailed instructions on unsealing and authorizing Vault, see
:doc:`Vault feature</how-to/features/vault>`.

.. _refresh-mysql:

Step 2 - Refresh MySQL
----------------------

The MySQL database must be refreshed before the application charms that depend
on it. Run the following command to refresh the charm to the latest revision
in its channel:

.. code:: text

   sunbeam cluster refresh mysql

During this process, the MySQL cluster is temporarily scaled up to the
nearest odd number of units to maintain quorum while units are upgraded
on a rolling basis. To ensure the upgrade proceeds as intended, it should
be triggered from a healthy MySQL cluster state. If the cluster state is manually
manipulated during the upgrade, the process may not proceed as expected.

If the upgrade is interrupted, it can usually be re-run and will resume from
where it left off.

If the upgrade has been interrupted and is in an inconsistent state, use the
``--reset-mysql-upgrade-state`` flag to restart it from the beginning:

.. code:: text

   sunbeam cluster refresh mysql --reset-mysql-upgrade-state

You will be prompted to confirm before resetting the state. This action
resets the internal upgrade tracking and starts a new refresh process. It does
not revert any changes already applied to the cluster.

.. _refresh-cluster:

Step 3 - Refresh the cluster
-----------------------------

Once Vault and MySQL have been refreshed, refresh all remaining OpenStack
charms:

.. code:: text

   sunbeam cluster refresh

If the snap has been refreshed to a different risk level in its channel
(for example, from ``stable`` to ``beta``) since the last update, the command
will prompt you to confirm before proceeding. In this case, it is recommended
to supply a manifest file:

.. code:: text

   sunbeam cluster refresh --manifest <path-to-manifest>

Use ``--force`` to skip the confirmation prompt:

.. code:: text

   sunbeam cluster refresh --force

Use the ``--clear-manifest`` flag to remove a previously
stored manifest:

.. code:: text

   sunbeam cluster refresh --clear-manifest
