Live Migration
==============

Overview
--------

An instance migration is the relocation of an instance from one
hypervisor to another.

When an instance has a live migration performed it is not shut down
during the process. This is useful when there is an imperative to not
interrupt the applications that are running on the instance.

Points to consider:

-  network usage may be significantly impacted if block migration mode
   is used
-  instances with intensive memory workloads may require pausing for
   live migration to succeed

Ensure adequate capacity on the destination host
------------------------------------------------

Oversubscribing the destination host (hypervisor) can lead to service
outages. This is only an issue when a destination host is explicitly
selected by the operator.

The following commands are useful for discovering a instance’s flavor,
listing flavor parameters, and viewing the available capacity of a
destination host:

.. code:: text

   openstack server show <instance-name> -c flavor
   openstack flavor show <flavor> -c vcpus -c ram -c disk
   openstack hypervisor list
   openstack host show <destination-host>

Live migrate an instance
------------------------

Live migration commands require the user to have the admin role.

To live migrate to any hypervisor with sufficient capacity:

::

   openstack server migrate --live-migration <server-id>

To live migrate to a specific hypervisor:

::

   openstack server migrate --live-migration --os-compute-api-version 2.30 --host <hypervisor-name> <server-id>

If the instance has local storage, you must also specify the
``--block-migration`` option:

::

   openstack server migrate --block-migration --live-migration <server id>
