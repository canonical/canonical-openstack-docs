Maintenance
===========

Overview
--------

Maintenance mode helps protecting the cluster from potentially disruptive maintenance operations. It is particularly useful when an operator needs to manually perform tasks on a node that may pose a risk of failure or data loss.

Before proceeding, refer to the :doc:`Maintenance Mode </explanation/maintenance-mode>` to understand its functionality and impact.

Enabling Maintenance feature
----------------------------

.. code:: text

   sunbeam enable maintenance

Maintenance mode relies on `OpenStack Watcher`_ to manage hypervisor services and virtual machine instances. Enabling Maintenance mode feature will also enable resource optimization feature to deploy required applications like watcher.

Usage
-----

Enabling Maintenance Mode
~~~~~~~~~~~~~~~~~~~~~~~~~

Before enabling maintenance mode, perform a dry run to check for potential issues:

.. code:: text

   sunbeam cluster maintenance enable <node> --dry-run

If no issues are reported, enable maintenance mode:

.. code:: text

   sunbeam cluster maintenance enable <node>

Disabling Maintenance Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~

To disable maintenance mode, first run a dry run to validate the operation:

.. code:: text

   sunbeam cluster maintenance disable <node> --dry-run

If the output confirms a safe transition, disable maintenance mode:

.. code:: text

   sunbeam cluster maintenance disable <node>

.. LINKS
.. _OpenStack Watcher: https://wiki.openstack.org/wiki/Watcher


Known issues
-------------

Cold migration is not supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently cold migration is not supported in Sunbeam. So maintenance mode pre-flight check will block user to continue if there are any instances in SHOTOFF status.
This will blocked until upstream watcher support disabling cold migration in host maintenance strategy.
