Enable and Disable Maintenance Mode
===================================

Overview
--------

Maintenance mode helps protect the cluster during potentially disruptive operations. It is particularly useful when an operator needs to manually perform tasks on a node that carry a risk of node failure or data loss.

Deploy OpenStack Watcher Before Proceeding
------------------------------------------

Maintenance mode relies on `OpenStack Watcher`_ to manage hypervisor services and virtual machine instances. If the compute role is active on your target node, ensure that Watcher is enabled before proceeding.

.. code:: text

   sunbeam enable resource-optimization

Enabling Maintenance Mode
-------------------------

Before enabling maintenance mode, you can perform a dry run to check for potential issues:

.. code:: text

   sunbeam cluster maintenance enable <node> --dry-run

If the dry run output shows no issues, proceed with enabling maintenance mode:

.. code:: text

   sunbeam cluster maintenance enable <node>

Disabling Maintenance Mode
--------------------------

To disable maintenance mode, you can first perform a dry run:

.. code:: text

   sunbeam cluster maintenance disable <node> --dry-run

Once confirmed, disable maintenance mode:

.. code:: text

   sunbeam cluster maintenance disable <node>

.. LINKS
.. _OpenStack Watcher: https://wiki.openstack.org/wiki/Watcher

