Cluster upgrades
================

Overview
--------

Use ``sunbeam cluster refresh`` to apply the latest charm updates to a running
deployment without changing the OpenStack release track. The command updates
all managed components to the latest available revision in their currently
configured channel.

.. note::

   Refreshing across release tracks is not supported. For example, you cannot
   use this command to upgrade from ``2024.1/stable`` to ``2025.1/stable``.

.. note::

   To ensure the latest charms are applied, refresh the ``openstack`` snap
   before running the cluster refresh command. For the **manual provider**,
   run ``sudo snap refresh openstack`` on all nodes. For the **MAAS provider**,
   run it on the sunbeam client node only.

Refresh the cluster
-------------------

To refresh the deployment, run:

.. code:: text

   sunbeam cluster refresh

If the snap has been refreshed to a different channel risk (for example, from
``stable`` to ``beta``) since the last update, the command will prompt you to
confirm before proceeding. It is recommended to supply a manifest in that case:

.. code:: text

   sunbeam cluster refresh --manifest <path-to-manifest>

Use ``--force`` to skip the confirmation prompt:

.. code:: text

   sunbeam cluster refresh --force

Refresh MySQL
-------------

The MySQL database requires a dedicated refresh command to ensure the database
remains available throughout the upgrade. If the upgrade is interrupted, it can
be safely re-run and will resume from where it left off.

.. code:: text

   sunbeam cluster refresh mysql

If the upgrade has been interrupted and is in an inconsistent state, use the
``--reset-mysql-upgrade-state`` flag to restart it from the beginning:

.. code:: text

   sunbeam cluster refresh mysql --reset-mysql-upgrade-state

You will be prompted to confirm before the reset takes effect.
