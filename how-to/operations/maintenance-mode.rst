Maintenance mode
================

Overview
--------

Maintenance mode helps by protecting the cluster from potentially disruptive maintenance operations. It is useful for performing maintenance tasks on a node that may result in a loss of data or disrupt running services such as firmware upgrades.

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

   Continue to run operations to enable maintenance mode for <node>:
           0: change_nova_service_state state=disabled resource=<node>
           1: Migrate instance type=live resource=test-vm1
           2: Migrate instance type=live resource=test-vm2
           3: set-noout-ops
           4: assert-noout-flag-set-ops

If no issues are reported, enable maintenance mode:

.. code:: text

   sunbeam cluster maintenance enable <node>

   Continue to run operations to enable maintenance mode for <node>:
           0: change_nova_service_state state=disabled resource=<node>
           1: Migrate instance type=live resource=test-vm1
           2: Migrate instance type=live resource=test-vm2
           3: set-noout-ops
           4: assert-noout-flag-set-ops
    [y/n]: y

   Operation result:
           0: change_nova_service_state state=disabled resource=<node> SUCCEEDED
           1: Migrate instance type=live resource=test-vm1 SUCCEEDED
           2: Migrate instance type=live resource=test-vm2 SUCCEEDED
           3: set-noout-ops SUCCEEDED
           4: assert-noout-flag-set-ops SUCCEEDED

   Enable maintenance for node: <node>


Controlling migration behavior
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, enabling maintenance mode will live migrate active instances and cold
migrate inactive instances. The ``--disable-migration`` flag allows operators to
control this behavior during maintenance.

.. note::

   If ``--disable-migration`` is not specified, the default behavior is unchanged.

To disable live migration (cold migrate both active and inactive instances):

.. code:: text

   sunbeam cluster maintenance enable <node> --disable-migration=live

To disable cold migration (live migrate active instances, ignore inactive instances):

.. code:: text

   sunbeam cluster maintenance enable <node> --disable-migration=cold

To disable all migration (only stop active instances, ignore inactive instances):

.. code:: text

   sunbeam cluster maintenance enable <node> --disable-migration=both

Or equivalently, without specifying a value:

.. code:: text

   sunbeam cluster maintenance enable <node> --disable-migration

The ``--disable-migration`` flag can be combined with ``--dry-run`` to preview the
effect before applying:

.. code:: text

   sunbeam cluster maintenance enable <node> --disable-migration=live --dry-run


Disabling Maintenance Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~

To disable maintenance mode, first run a dry run to validate the operation:

.. code:: text

   sunbeam cluster maintenance disable <node> --dry-run

   required operations to disable maintenance mode for <node>:
           0: EnableHypervisorStep
           1: unset-noout-ops
           2: assert-noout-flag-unset-ops
           3: start-osd-ops

   Disable maintenance for node: <node>

If the output confirms a safe transition, disable maintenance mode:

.. code:: text

   sunbeam cluster maintenance disable <node>

   Continue to run operations to disable maintenance mode for <node>:
           0: EnableHypervisorStep
           1: unset-noout-ops
           2: assert-noout-flag-unset-ops
           3: start-osd-ops
    [y/n]: y

   Operation result:
           0: EnableHypervisorStep SUCCEEDED
           1: unset-noout-ops SUCCEEDED
           2: assert-noout-flag-unset-ops SUCCEEDED
           3: start-osd-ops SUCCEEDED

   Disable maintenance for node: <node>

.. LINKS
.. _OpenStack Watcher: https://wiki.openstack.org/wiki/Watcher
