Resource Optimization
=====================

This feature deploys `Watcher <https://docs.openstack.org/watcher/latest/index.html>`__, the
OpenStack Resource Optimization service.

Enabling Resource Optimization
------------------------------

To enable Resource Optimization, run the following command:

.. literalinclude:: ../snippets/resource-optimization.task.sh
    :language: bash
    :start-after: [docs-view:enable-resource-optimization]
    :end-before:  [docs-view:enable-resource-optimization-end]

Disabling Resource Optimization
-------------------------------

To disable Resource Optimization, run the following command:

.. literalinclude:: ../snippets/resource-optimization.task.sh
    :language: bash
    :start-after: [docs-view:disable-resource-optimization]
    :end-before:  [docs-view:disable-resource-optimization-end]

Usage
-----

List Goals
~~~~~~~~~~

List goals using the following command:

::

    openstack optimize goal list

Sample output:

::

    +--------------------------------------+----------------------+----------------------+
    | UUID                                 | Name                 | Display name         |
    +--------------------------------------+----------------------+----------------------+
    | 11ee813f-2ac3-4975-9529-706ba7025057 | airflow_optimization | Airflow Optimization |
    | 38817441-5df3-4f9d-8fd7-58a966f2e921 | cluster_maintaining  | Cluster Maintaining  |
    | 98504695-4052-43ec-a0a2-8cc945278fae | dummy                | Dummy goal           |
    | 2413258c-bfba-4adb-aeda-b2ef611084a7 | hardware_maintenance | Hardware Maintenance |
    | b92f38e9-7df7-4787-a7fd-29e5783e56f3 | noisy_neighbor       | Noisy Neighbor       |
    | 48348b46-cca2-4669-be0c-336cea0e9396 | saving_energy        | Saving Energy        |
    | f20ce098-df72-43ec-941e-ae72ad2ee0c6 | server_consolidation | Server Consolidation |
    | 4c7b7c77-acc9-44f5-a082-dd728bdb9f0d | thermal_optimization | Thermal Optimization |
    | 3c85d238-541d-479e-96e9-4038787c2fcf | unclassified         | Unclassified         |
    | 7c1f150e-39b4-44e4-a352-ed947b71a9ae | workload_balancing   | Workload Balancing   |
    +--------------------------------------+----------------------+----------------------+

List Strategies in a goal
~~~~~~~~~~~~~~~~~~~~~~~~~

List the strategies for a goal using the following command:

::

    openstack optimize strategy list --goal GOAL

For example, list the strategies for goal ‘cluster_maintaining’:

::

    openstack optimize strategy list --goal cluster_maintaining

Sample output:

::

    +--------------------------------------+------------------+---------------------------+---------------------+
    | UUID                                 | Name             | Display name              | Goal                |
    +--------------------------------------+------------------+---------------------------+---------------------+
    | 48351169-670f-4354-bac8-8d18061d1291 | host_maintenance | Host Maintenance Strategy | cluster_maintaining |
    +--------------------------------------+------------------+---------------------------+---------------------+

Create an Audit template
~~~~~~~~~~~~~~~~~~~~~~~~

Create an Audit template using the following command:

::

    openstack optimize audittemplate create NAME GOAL --strategy STRATEGY

For example, create an audit template ‘host-maintenance-template’ for goal ‘cluster_maintaining’ and strategy ‘host_maintenance’:

::

    openstack optimize audittemplate create host-maintenance-template cluster_maintaining --strategy host_maintenance

Sample output:

::

    +-------------+--------------------------------------+
    | Field       | Value                                |
    +-------------+--------------------------------------+
    | UUID        | bb7caee4-f555-4d4f-89f4-7db627ce44cc |
    | Created At  | 2024-09-13T03:38:52.858848+00:00     |
    | Updated At  | None                                 |
    | Deleted At  | None                                 |
    | Description | None                                 |
    | Name        | host-maintenance-template            |
    | Goal        | cluster_maintaining                  |
    | Strategy    | host_maintenance                     |
    | Audit Scope | []                                   |
    +-------------+--------------------------------------+

Create an Audit
~~~~~~~~~~~~~~~

Create an Audit using the following command:

::

    openstack optimize audit create -a AUDIT_TEMPLATE_NAME -p key=value

For example, create an audit with template ‘host-maintenance-template’ and passing strategy parameters maintenance_node

::

    openstack optimize audit create -a host-maintenance-template -p maintenance_node=solqa-lab1-server-45.nosilo.lab1.solutionsqa

Sample output:

::

    +---------------+-------------------------------------------------------------------------------------------------------------------------------------+
    | Field         | Value                                                                                                                               |
    +---------------+-------------------------------------------------------------------------------------------------------------------------------------+
    | UUID          | 2a4355b2-3e03-4a0f-80bf-92476e17b7da                                                                                                |
    | Name          | host_maintenance-2024-09-13T03:40:53.948011                                                                                         |
    | Created At    | 2024-09-13T03:40:53.992685+00:00                                                                                                    |
    | Updated At    | None                                                                                                                                |
    | Deleted At    | None                                                                                                                                |
    | State         | PENDING                                                                                                                             |
    | Audit Type    | ONESHOT                                                                                                                             |
    | Parameters    | {'maintenance_node': 'solqa-lab1-server-45.nosilo.lab1.solutionsqa'}                                                                |
    | Interval      | None                                                                                                                                |
    | Goal          | cluster_maintaining                                                                                                                 |
    | Strategy      | host_maintenance                                                                                                                    |
    | Audit Scope   | []                                                                                                                                  |
    | Auto Trigger  | False                                                                                                                               |
    | Next Run Time | None                                                                                                                                |
    | Hostname      | None                                                                                                                                |
    | Start Time    | None                                                                                                                                |
    | End Time      | None                                                                                                                                |
    | Force         | False                                                                                                                               |
    +---------------+-------------------------------------------------------------------------------------------------------------------------------------+

Show the Audit details
~~~~~~~~~~~~~~~~~~~~~~

Show the Audit details using the following command:

::

    openstack optimize audit show AUDIT_ID

Sample output:

::

    +---------------+-------------------------------------------------------------------------------------------------------------------------------------+
    | Field         | Value                                                                                                                               |
    +---------------+-------------------------------------------------------------------------------------------------------------------------------------+
    | UUID          | 2a4355b2-3e03-4a0f-80bf-92476e17b7da                                                                                                |
    | Name          | host_maintenance-2024-09-13T03:40:53.948011                                                                                         |
    | Created At    | 2024-09-13T03:40:54+00:00                                                                                                           |
    | Updated At    | 2024-09-13T03:41:07+00:00                                                                                                           |
    | Deleted At    | None                                                                                                                                |
    | State         | SUCCEEDED                                                                                                                           |
    | Audit Type    | ONESHOT                                                                                                                             |
    | Parameters    | {'maintenance_node': 'solqa-lab1-server-45.nosilo.lab1.solutionsqa'}                                                                |
    | Interval      | None                                                                                                                                |
    | Goal          | cluster_maintaining                                                                                                                 |
    | Strategy      | host_maintenance                                                                                                                    |
    | Audit Scope   | []                                                                                                                                  |
    | Auto Trigger  | False                                                                                                                               |
    | Next Run Time | None                                                                                                                                |
    | Hostname      | watcher-0                                                                                                                           |
    | Start Time    | None                                                                                                                                |
    | End Time      | None                                                                                                                                |
    | Force         | False                                                                                                                               |
    +---------------+-------------------------------------------------------------------------------------------------------------------------------------+

List Action plan for an Audit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list the Action plan for an Audit, run the following command:

::

    openstack optimize actionplan list --audit AUDIT_ID

Sample output:

::

    +--------------------------------------+--------------------------------------+-------------+------------+-----------------+
    | UUID                                 | Audit                                | State       | Updated At | Global efficacy |
    +--------------------------------------+--------------------------------------+-------------+------------+-----------------+
    | 16e76af5-edbd-48b0-a443-946d921ca514 | 2a4355b2-3e03-4a0f-80bf-92476e17b7da | RECOMMENDED | None       |                 |
    +--------------------------------------+--------------------------------------+-------------+------------+-----------------+

List actions
~~~~~~~~~~~~

To list the actions in Action plan, run the following command:

::

    openstack optimize action list --action-plan ACTION_PLAN_ID

Sample output:

::

    +--------------------------------------+----------------------------------------------------------------------------------+---------+--------------------------------------+---------------------------+
    | UUID                                 | Parents                                                                          | State   | Action Plan                          | Action                    |
    +--------------------------------------+----------------------------------------------------------------------------------+---------+--------------------------------------+---------------------------+
    | d7f52ae0-37b5-456e-a9ac-a465bcce8aed | []                                                                               | PENDING | 16e76af5-edbd-48b0-a443-946d921ca514 | change_nova_service_state |
    | 3f40421c-3f8d-4048-8b29-2c39bce9c16a | ['d7f52ae0-37b5-456e-a9ac-a465bcce8aed']                                         | PENDING | 16e76af5-edbd-48b0-a443-946d921ca514 | migrate                   |
    | 617bcd97-e90b-4ba7-868c-548a96cd8408 | ['d7f52ae0-37b5-456e-a9ac-a465bcce8aed']                                         | PENDING | 16e76af5-edbd-48b0-a443-946d921ca514 | migrate                   |
    | a5093f31-a9fd-41ef-a715-23761d282410 | ['3f40421c-3f8d-4048-8b29-2c39bce9c16a', '617bcd97-e90b-4ba7-868c-548a96cd8408'] | PENDING | 16e76af5-edbd-48b0-a443-946d921ca514 | migrate                   |
    +--------------------------------------+----------------------------------------------------------------------------------+---------+--------------------------------------+---------------------------+

To list the detailed actions, run the following command:

::

    openstack optimize action list --action-plan ACTION_PLAN_ID --detail

Start the Action plan
~~~~~~~~~~~~~~~~~~~~~

To start the action, run the following command:

::

    openstack optimize actionplan start ACTION_PLAN_ID

Sample output:

::

    +---------------------+--------------------------------------+
    | Field               | Value                                |
    +---------------------+--------------------------------------+
    | UUID                | 16e76af5-edbd-48b0-a443-946d921ca514 |
    | Created At          | 2024-09-13T03:41:06+00:00            |
    | Updated At          | 2024-09-13T03:45:32+00:00            |
    | Deleted At          | None                                 |
    | Audit               | 2a4355b2-3e03-4a0f-80bf-92476e17b7da |
    | Strategy            | host_maintenance                     |
    | State               | PENDING                              |
    | Efficacy indicators | []                                   |
    | Global efficacy     | []                                   |
    | Hostname            | None                                 |
    +---------------------+--------------------------------------+

Show status of Action plan
~~~~~~~~~~~~~~~~~~~~~~~~~~

To show the status of Action plan, run the following command:

::

    openstack optimize actionplan show ACTION_PLAN_ID

The state will be changed to SUCCEEDED once the actions complete.

Sample output:

::

    +---------------------+--------------------------------------+
    | Field               | Value                                |
    +---------------------+--------------------------------------+
    | UUID                | 16e76af5-edbd-48b0-a443-946d921ca514 |
    | Created At          | 2024-09-13T03:41:06+00:00            |
    | Updated At          | 2024-09-13T03:45:44+00:00            |
    | Deleted At          | None                                 |
    | Audit               | 2a4355b2-3e03-4a0f-80bf-92476e17b7da |
    | Strategy            | host_maintenance                     |
    | State               | SUCCEEDED                            |
    | Efficacy indicators | []                                   |
    |                     |                                      |
    | Global efficacy     |                                      |
    | Hostname            | watcher-0                            |
    +---------------------+--------------------------------------+

Limitations
-----------

#. Following goals are not supported:

    * airflow_optimization
    * thermal_optimization
    * noisy_neighbor

#. Strategies vm_workload_consolidation and workload_stabilization do not consider host memory usage in decision making as the metric hardware.memory.used is not currently collected.
