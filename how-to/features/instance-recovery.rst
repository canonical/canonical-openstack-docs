Instance Recovery
=================

This feature deploys `Masakari`_, the OpenStack Instance High Availability service. This feature
requires at least two compute nodes in the deployment.

Enabling Instance Recovery
--------------------------

To enable Instance Recovery, run the following command:

.. literalinclude:: ../snippets/instance-recovery.task.sh
    :language: bash
    :start-after: [docs-view:enable-instance-recovery]
    :end-before:  [docs-view:enable-instance-recovery-end]

Disabling Instance Recovery
---------------------------

To disable Instance Recovery, run the following command:

.. literalinclude:: ../snippets/instance-recovery.task.sh
    :language: bash
    :start-after: [docs-view:disable-instance-recovery]
    :end-before:  [docs-view:disable-instance-recovery-end]

Instance Evacuation Recovery methods
------------------------------------

With Masakari, compute nodes are grouped into failover segments. In the event of a compute node
failure, that node’s instances are moved onto another compute node within the same segment.

The destination node is determined by the recovery method configured for the affected segment.
There are four methods:

* reserved_host
   The ``reserved_host`` recovery method relocates instances to a subset of non-active nodes.
   Because these nodes are not active and are typically resourced adequately for failover duty,
   there is a guarantee that sufficient resources will exist on a reserved node to accommodate
   migrated instances.
* auto
   The ``auto`` recovery method relocates instances to any available node in the same segment.
   Because all the nodes are active, contrarily to the ``reserved_host`` method, there is no
   guarantee that sufficient resources will exist on the destination node to accommodate migrated
   instances.
* rh_priority
   Attempts to evacuate instances using the ``reserved_host`` method. If the latter is unsuccessful
   the auto method will be used.
* auto_priority
   Attempts to evacuate instances using the ``auto`` method. If the latter is unsuccessful the
   ``reserved_host`` method will be used.

Create a failover segment
-------------------------

Run the following command to create a failover segment

::

    openstack segment create NAME RECOVERY_METHOD SERVICE_TYPE

For example, to create a service S1 with ``reserved_host`` for service type COMPUTE

::

    openstack segment create S1 reserved_host COMPUTE

Sample output for the above command:

::

    +-----------------+--------------------------------------+
    | Field           | Value                                |
    +-----------------+--------------------------------------+
    | created_at      | 2024-10-18T04:32:21.000000           |
    | updated_at      | None                                 |
    | uuid            | 7980f98d-8458-467b-a5cd-ceb5e6b94cdb |
    | name            | S1                                   |
    | description     | None                                 |
    | id              | 1                                    |
    | service_type    | COMPUTE                              |
    | recovery_method | reserved_host                        |
    | is_enabled      | True                                 |
    +-----------------+--------------------------------------+

Add hosts to failover segment

Run the following command to add host to a failover segment

::

    openstack segment host create NAME TYPE CONTROL_ATTRIBUTE SEGMENT [--reserved] [--on-maintenance]

For example, to add host `sunbeam1.maas` to segment S1, run the following command:

::

    openstack segment host create sunbeam1.maas COMPUTE SSH S1

Sample output of the above command:

::

    +---------------------+--------------------------------------+
    | Field               | Value                                |
    +---------------------+--------------------------------------+
    | created_at          | 2024-10-18T04:32:56.000000           |
    | updated_at          | None                                 |
    | uuid                | 7cd21df7-ab9e-4bc3-a69b-13df4f53b125 |
    | name                | sunbeam1.maas                        |
    | type                | COMPUTE                              |
    | control_attributes  | SSH                                  |
    | reserved            | False                                |
    | on_maintenance      | False                                |
    | failover_segment_id | 7980f98d-8458-467b-a5cd-ceb5e6b94cdb |
    +---------------------+--------------------------------------+

Hosts can be reserved when adding to failover segment. These hosts will be used in
``reserved_host`` recovery method. For example, to add host ``sunbeam3.maas`` as reserved,
run the following command:

::

    openstack segment host create --reserved True sunbeam3.maas COMPUTE SSH S1

Sample output of the above command:

::

    +---------------------+--------------------------------------+
    | Field               | Value                                |
    +---------------------+--------------------------------------+
    | created_at          | 2024-10-18T04:33:44.000000           |
    | updated_at          | None                                 |
    | uuid                | a641ce79-3610-4753-b59f-9902ee8da4c3 |
    | name                | sunbeam3.maas                        |
    | type                | COMPUTE                              |
    | control_attributes  | SSH                                  |
    | reserved            | True                                 |
    | on_maintenance      | False                                |
    | failover_segment_id | 7980f98d-8458-467b-a5cd-ceb5e6b94cdb |
    +---------------------+--------------------------------------+

List hosts in failover segment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run below command to list hosts in a failover segment:

::

    openstack segment host list S1 -c name -c reserved -c on_maintenance

Sample output of the above command:

::

    +---------------+----------+----------------+
    | name          | reserved | on_maintenance |
    +---------------+----------+----------------+
    | sunbeam3.maas | True     | False          |
    | sunbeam2.maas | False    | False          |
    | sunbeam1.maas | False    | False          |
    +---------------+----------+----------------+

Verify reserved_host recovery method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create failover segment and add hosts to the failover segment. Ensure add few hosts with
``--reserved`` flag. Once this is done, disable the reserved host using the following command:

::

    openstack compute service set --disable HOSTNAME nova-compute

Run the following command to check status of nova-compute services:

::

    openstack compute service list -c Host -c Status -c State --service nova-compute

Sample output of the above command:

::

    +---------------+----------+-------+
    | Host          | Status   | State |
    +---------------+----------+-------+
    | sunbeam1.maas | enabled  | up    |
    | sunbeam2.maas | enabled  | up    |
    | sunbeam3.maas | disabled | up    |
    +---------------+----------+-------+

In the above output, observe the state of reserved node ``sunbeam3.maas`` is disabled.

Check the instances running in the cloud using command

::

    openstack server list --long --all-projects -c Name -c Host

Sample output:

::

    +----------+---------------+
    | Name     | Host          |
    +----------+---------------+
    | testvm-2 | sunbeam1.maas |
    | testvm-1 | sunbeam1.maas |
    +----------+---------------+

Simulate a compute node failure by shutting down the interface or bringing down the interface. If
the interface is one of the management or data or storage networks, masakari service will trigger
actions based on recovery strategy. The actions that will be taken for each network failure are
as follows:

.. list-table:: Recovery actions based on network status
   :class: names
   :header-rows: 1

   * - Management Network
     - Tenant Network
     - Storage Network
     - Action
   * - up
     - up
     - up
     - --
   * - up
     - up
     - down
     - recovery
   * - up
     - down
     - up
     - --
   * - up
     - down
     - down
     - recovery
   * - down
     - up
     - up
     - --
   * - down
     - up
     - down
     - recovery
   * - down
     - down
     - up
     - --
   * - down
     - down
     - down
     - recovery


Verify Hosts in Failover segment once the failure is simulated:

::

    openstack segment host list S1 -c name -c reserved -c on_maintenance

Sample output after shutting down node 'sunbeam1.maas'

::

    +---------------+----------+----------------+
    | name          | reserved | on_maintenance |
    +---------------+----------+----------------+
    | sunbeam3.maas | False    | False          |
    | sunbeam2.maas | False    | False          |
    | sunbeam1.maas | False    | True           |
    +---------------+----------+----------------+

In the above output, observe the  failure node ``sunbeam1.maas`` is changed to maintenance mode and
reserved node ``sunbeam3.maas`` is no longer reserved.

Verify the compute service status

::

    openstack compute service list -c Host -c Status -c State --service nova-compute

Sample output:

::

    +---------------+----------+-------+
    | Host          | Status   | State |
    +---------------+----------+-------+
    | sunbeam1.maas | disabled | down  |
    | sunbeam3.maas | enabled  | up    |
    | sunbeam2.maas | enabled  | up    |
    +---------------+----------+-------+

In the above output, observe status of failed node is changed to disabled and reserved node is
changed to ``enabled``.

Verify if the instances are evacuated using the below command:

::

    openstack server list --long --all-projects -c Name -c Host

Sample output showing instances on failed node are now moved to reserved node.

::

    +----------+---------------+
    | Name     | Host          |
    +----------+---------------+
    | testvm-2 | sunbeam3.maas |
    | testvm-1 | sunbeam3.maas |
    +----------+---------------+

Verify auto recovery method
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create failover segment and add hosts to the failover segment without any `--reserved` flag.

Run below command to list hosts in a failover segment:

::

    openstack segment host list S1 -c name -c reserved -c on_maintenance

Sample output of the above command:

::

    +---------------+----------+----------------+
    | name          | reserved | on_maintenance |
    +---------------+----------+----------------+
    | sunbeam3.maas | False    | False          |
    | sunbeam2.maas | False    | False          |
    | sunbeam1.maas | False    | False          |
    +---------------+----------+----------------+

The reserved flag in all nodes is False.

Simulate the compute node failure and observe Verify Hosts in Failover segment :

::

    openstack segment host list S1 -c name -c reserved -c on_maintenance

Sample output after shutting down node ``sunbeam1.maas``

::

    +---------------+----------+----------------+
    | name          | reserved | on_maintenance |
    +---------------+----------+----------------+
    | sunbeam3.maas | False    | False          |
    | sunbeam2.maas | False    | False          |
    | sunbeam1.maas | False    | True           |
    +---------------+----------+----------------+

Observe in the above output node ``sunbeam1.maas`` is in Maintenance mode.

Verify if the instances are evacuated using the below command:

::

    openstack server list --long --all-projects -c Name -c Host

Sample output showing instances on failed node are now moved to different compute hosts.

::

    +----------+---------------+
    | Name     | Host          |
    +----------+---------------+
    | testvm-2 | sunbeam2.maas |
    | testvm-1 | sunbeam3.maas |
    +----------+---------------+

Observe in the above output the instances are scheduled to any available compute nodes.

## Instance Restart

The enabling of the instance restart feature is done on a per-instance basis.

For example, tag instance ``testvm-1`` as HA-enabled in order to have it restarted automatically on
its hypervisor:

::

    openstack server set --property HA_Enabled=True testvm-1

An instance failure can be simulated by killing its process. First determine its hypervisor and
``qemu`` guest name:

::

    openstack server show testvm-1 -c OS-EXT-SRV-ATTR:host -c OS-EXT-SRV-ATTR:instance_name

Sample output:

::

    +-------------------------------+-------------------+
    | Field                         | Value             |
    +-------------------------------+-------------------+
    | OS-EXT-SRV-ATTR:host          | sunbeam3.maas     |
    | OS-EXT-SRV-ATTR:instance_name | instance-00000001 |
    +-------------------------------+-------------------+

Check the current PID, kill the process, wait a minute, and verify that a new process gets started:

::

    juju exec --unit openstack-hypervisor/2 'pgrep -f guest=instance-00000001'
    juju exec --unit openstack-hypervisor/2 'sudo pkill -f -9 guest=instance-00000001'
    juju exec --unit openstack-hyperivsor/2 'pgrep -f guest=instance-00000001'

Supplementary information
-------------------------

This section contains information that can be useful when working with Masakari.

* Once a failed node has been re-inserted into the cloud it will show, in Nova, as ``disabled`` but
  ``up`` and, in Masakari, as ``on_maintenance``. It can become an active hypervisor with:

::

    openstack compute service set --enable HOSTNAME nova-compute
    openstack segment host update --on_maintenance=False SEGMENT HOSTNAME

* A segment’s recovery method can be updated with:

::

    openstack segment update --recovery_method RECOVERY_METHOD --service_type COMPUTE SEGMENT

* A node cannot be assigned to a segment while it’s assigned to another segment. It must first be
  removed from the current segment with:

::

    openstack segment host delete SEGMENT HOSTNAME

* A node’s reserved status can be updated with:

::

    openstack segment host update --reserved=<boolean> SEGMENT HOSTNAME

Limitations
-----------

* Recovery actions for Instance recovery methods can detect only Management network failure. For
  failure in tenant or storage network, recovery action is triggered by updating the compute
  node to maintenance but evacuation of instances does not happen.
