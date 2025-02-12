Enable and Disable Maintenance Mode
===================================

Overview
--------

Maintenance mode helps protect the cluster during operations that could be disruptive. It is particularly useful when an operator needs to manually perform tasks on a node that may pose a risk of failure or data loss.

Before proceeding, refer to the :doc:`Maintenance Mode </explanation/maintenance-mode>` to understand its functionality and impact.

Deploy OpenStack Watcher Before Proceeding
------------------------------------------

Maintenance mode relies on `OpenStack Watcher`_ to manage hypervisor services and virtual machine instances. If the target node has an active compute role, ensure that Watcher is enabled before proceeding:

.. code:: text

   sunbeam enable resource-optimization

Enabling Maintenance Mode
-------------------------

Before enabling maintenance mode, perform a dry run to check for potential issues:

.. code:: text

   sunbeam cluster maintenance enable <node> --dry-run

If no issues are reported, enable maintenance mode:

.. code:: text

   sunbeam cluster maintenance enable <node>

Disabling Maintenance Mode
--------------------------

To disable maintenance mode, first run a dry run to validate the operation:

.. code:: text

   sunbeam cluster maintenance disable <node> --dry-run

If the output confirms a safe transition, disable maintenance mode:

.. code:: text

   sunbeam cluster maintenance disable <node>

.. LINKS
.. _OpenStack Watcher: https://wiki.openstack.org/wiki/Watcher
