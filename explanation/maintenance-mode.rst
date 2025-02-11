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

Definition of Maintenance Mode in Sunbeam
-----------------------------------------

In the Sunbeam architecture, each node in a deployment can assume one or more roles. 
When maintenance mode is enabled, Sunbeam ensures that all roles on the node reach 
a maintainable state before proceeding.

The following sections define the maintenance mode status for each role:

Compute Role
~~~~~~~~~~~~

- Nova compute status is set to *disabled*, preventing new instances from being scheduled on the node.
- No instances are running on the node, ensuring that workloads are not affected during maintenance operations.
- Hypervisor services remain active.

Storage Role
~~~~~~~~~~~~

- OSD (Object Storage Daemon):
    - OSDs on the node must be ``ok-to-stop``, ensuring sufficient redundancy to tolerate the loss of OSDs on the node. See ``ok-to-stop`` part in `ceph administration tool`_ for more information.
    - *(Optional)* OSDs on the node must be either:
      - ``IN`` and ``UP``, or
      - ``OUT`` and ``DOWN``.
      This allows the operator to decide whether the OSDs should remain active during maintenance.
    - *(Optional)* Rebalancing is disabled to prevent automatic rebalancing from being triggered during maintenance.

- Non-OSD services (MDS, MGR, MON, RGW):
    - The number of running services must be greater than the minimum required for quorum.

Control Role (Future work)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The node should be in a state equivalent to running `kubectl drain <node-name>`, which will evict all of your pods from a node and mark it as unschedulable. See `kubectl drain`_ and `kubectl cordon`_ for more information.

- No local Persistent Volumes (PV) should be served by the node.

Once all roles on the node meet these conditions, the node is considered to be in maintenance mode.

.. LINKS
.. _ceph administration tool: https://docs.ceph.com/en/reef/man/8/ceph/
.. _kubectl drain: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/
.. _kubectl cordon: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_cordon/
