Maintenance Mode
================

Overview
--------

Maintenance mode provides a safeguard for operators performing critical operations
that could potentially disrupt services or result in data loss. Before executing
any high-risk actions on a node, operators should enable maintenance mode to
minimize impact and ensure system stability.

States of the Node
------------------

A node in Sunbeam can exist in one of three states: **Active**, **Maintenance**, or **Decommissioned**.

- **Active**: The node is fully operational, healthy, and actively contributing to the cluster.
- **Maintenance**: The node remains part of the cluster, but safeguards are in place to ensure that its temporary unavailability does not impact overall system stability. Necessary precautions, such as disabling services or redistributing workloads, have been applied to make the node safe for maintenance operations. Once the maintenance operation is complete, the operator should disable maintenance mode to return the node to the **Active** state.
- **Decommissioned**: The node is no longer part of the cluster and does not participate in cluster activities. A **Decommissioned** node does not impact cluster operations, as its responsibilities have already been reassigned.

By defining these states, Sunbeam ensures that operators can perform maintenance efficiently while minimizing disruptions to the system.

.. note ::

    The states here differ from the `sunbeam cluster list` output, which displays the roles enabled on each node.
    Maintenance mode states are dynamic because an operator can manually trigger operations on the cluster at any time. A node is considered to be in maintenance mode only if it passes all necessary checks to confirm its status. However, since operations can occur at any moment, a node's status is not static.


Enabling Maintenance Mode
-------------------------

Each node in Sunbeam can have more than one role. When enabling maintenance mode, Sunbeam will
follow the "check, apply, and verify" pattern to ensure that all roles on the node reach
maintenance state. The **check** step ensures that the node meets the prerequisites to enter
maintenance state; the **apply** step runs the commands that put the node into maintenance state;
the **verify** step ensures the commands successfully put the node into maintenance state. When all
check, apply, and verify steps finished successfully, the node is considered in **Maintenance**
state.

The following section explains the steps for **enabling** maintenance mode for each role and some
general preflight checks:

General checks
~~~~~~~~~~~~~~

* Node exist

  * The node-to-be-maintained must exists

* No last node

  * The node-to-be-maintained must not be the last node


Compute Role
~~~~~~~~~~~~

Check
^^^^^

* Watcher exists

  * Watcher is required for compute role maintenance mode.

* Instances status

  * If there are any instance in **ERROR** status, operator should manually handle it first.

  * If there are any instance in **MIGRATING** status, operator should wait until migration
    finished.

  * If there are any instance in **SHUTOFF** status, the maintenance will be blocked, because
    sunbeam doesn't support cold migration now. This will blocked until we have disable cold
    migration feature support in watcher. See:
    https://bugs.launchpad.net/snap-openstack/+bug/2082056 and
    https://review.opendev.org/c/openstack/watcher-specs/+/943873.

* No ephemeral disks

  * Instances with ephemeral disk cannot be migrated, operator should handle it first.

Apply
^^^^^

* Audit action plan

  * Execute the watcher audit action plan.

Verify
^^^^^^

* No instances

  * Hypervisor services should remain active on the node.

  * No instances should be running on the node, ensuring that workloads are not affected during
    maintenance operations.

* Nova is disabled

  * Nova compute status should be set to **disabled**, preventing new instances from being
    scheduled on the node.


Network Role
~~~~~~~~~~~~

Network role maintenance mode is not supported yet.

Storage Role
~~~~~~~~~~~~

Check
^^^^^

* OSDs are ok-to-stop

  * OSDs on the node must be ``ok-to-stop``, ensuring sufficient redundancy to tolerate the loss of
    OSDs on the node. See ``ok-to-stop`` part in `ceph administration tool`_ for more information.

* Non-OSD services are enough

  * The number of running services must be greater than the minimum required for quorum, the
    numbers are 3 mons, 1 mds, 1 mgr.

Apply
^^^^^

* Bring the OSDs down (optional)

  * Operators can decide whether the OSDs should remain active during maintenance.

* Set noout for ceph cluster (optional)

  * Operators can decide whether automatic rebalancing is allowed or not during maintenance. See
    `stop without rebalancing`_ for more information.

Verify
^^^^^^

* N/A


Control Role
~~~~~~~~~~~~

Check
^^^^^


* Last control role

  * At least one active control role is required in the cluster during maintenance.

* K8s dqlite redundancy

  * If k8s dqlite is used as the datastore, the remaining k8s dqlite units should be enough to keep
    the k8s cluster in quorum.

* No Juju controller pod

  * When deploying using with :doc:`manual bare metal
    provider</how-to/install/install-canonical-openstack-using-the-manual-bare-metal-provider>`
    with internal Juju controller, the Juju controller pod is not HA. It's not possible to enable
    maintenance mode for the node hosting the juju controller pod without causing the cluster to go
    down. Enabling maintenance mode for the node hosting the juju controller pod is not allowed.

* Workload redundancy

  * The node-to-be-maintained should have at least one replica for all workloads (Deployment,
    StatefulSet, or ReplicaSet). If it only has less than or equal to one replica, draining the
    node could cause potential service downtime (e.g. some openstack related pods have PVC bound to
    a node, those pods cannot be rescheduled to another node after they are evicted). Operators
    should review the error message, and decide if it's okay to continue to drain the node.

Apply
^^^^^

* Cordon the node

  * Mark the node unschedulable to prevent new pods are scheduled to the node.

* Drain the node

  * Delete non-daemonset pods on the node. Pods with PVCs will remain in **Pending** state, and
    pods without PVCs will be rescheduled to different available nodes by the kube-scheduler. Users
    are recommended to take care of the rebalancing of the pods to avoid overloading certain nodes.

Verify
^^^^^^

* Node unschedulable

  * The node should be marked as unschedulable.

Once all roles on the node meet these conditions, the node is considered to be in **Maintenance** mode.

Disabling Maintenance Mode
--------------------------

The same logic of enabling maintenance mode applies to disabling the maintenance mode.

The following section explains the steps for **disabling** maintenance mode for each role and some
general preflight checks:

General checks
~~~~~~~~~~~~~~

* Node exist

  * The node-to-be-maintained must exists


Compute Role
~~~~~~~~~~~~

Check
^^^^^

* Watcher exists

  * Watcher is required for compute role maintenance mode.

Apply
^^^^^

* Enable openstack hypervisor services

* Enable instance rebalancing (optional)

  * Run workload rebalancing audit action plan to rebalance the instances across the nodes


Verify
^^^^^^

* N/A

Storage Role
~~~~~~~~~~~~

Check
^^^^^

* N/A

Apply
^^^^^

* Activate OSDs

  * Bring the OSDs up and enable the service

* Unset noout for ceph cluster

  * Remove noout flag to allow data migration from triggering after the planned maintenance slot.
    See `stop without rebalancing`_ for more information.

Verify
^^^^^^

* N/A


Control Role
~~~~~~~~~~~~

Check
^^^^^

* N/A

Apply
^^^^^

* Uncordon the node

  * Mark the node schedulable to allow new pods are scheduled to the node.


Verify
^^^^^^

* Node schedulable

  * The node should be marked as schedulable.

Once all roles on the node meet these conditions, the node is considered to be out of
**Maintenance** mode.

.. LINKS
.. _ceph administration tool: https://docs.ceph.com/en/reef/man/8/ceph/
.. _kubectl drain: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/
.. _kubectl cordon: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_cordon/
.. _stop without rebalancing: https://docs.ceph.com/en/reef/rados/troubleshooting/troubleshooting-osd/#stopping-without-rebalancing
