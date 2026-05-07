Telemetry
=========

This feature deploys the OpenStack Telemetry services Ceilometer, Aodh,
Gnocchi, and OpenStack Exporter.

Enabling Telemetry
------------------

To enable Telemetry, run the following command:

.. literalinclude:: ../snippets/telemetry.task.sh
   :language: bash
   :start-after: [docs-view:enable-telemetry]
   :end-before:  [docs-view:enable-telemetry-end]

Use the OpenStack CLI to create and manage alarms. See the upstream
`Aodh
documentation <https://docs.openstack.org/aodh/latest/admin/telemetry-alarms.html#using-alarms>`__
for details.

Disabling Telemetry
-------------------

To disable Telemetry, run the following command:

.. literalinclude:: ../snippets/telemetry.task.sh
   :language: bash
   :start-after: [docs-view:disable-telemetry]
   :end-before:  [docs-view:disable-telemetry-end]

This will terminate the application but not remove it from the model. To
do that, run the following:

::

   juju remove-application --force --no-wait --no-prompt -m openstack \
      ceilometer gnocchi gnocchi-mysql-router aodh aodh-mysql-router

Usage
-----

Alarms
~~~~~~

Users need the role ``admin`` to be able to manage alarms.

Create alarm ``memory_high`` with metric ``metric.usage`` and alarm
action ``log`` using the following command:

::

    openstack alarm create \
       --name memory_high \
       --type gnocchi_resources_threshold \
       --description 'instance consuming memory' \
       --metric memory.usage \
       --threshold 2000 \
       --comparison-operator gt \
       --aggregation-method mean \
       --granularity 300 \
       --evaluation-periods 3 \
       --alarm-action 'log://' \
       --resource-id <INSTANCE ID> \
       --resource-type instance

Sample output:

::

   +---------------------------+--------------------------------------+
   | Field                     | Value                                |
   +---------------------------+--------------------------------------+
   | aggregation_method        | mean                                 |
   | alarm_actions             | ['log:']                             |
   | alarm_id                  | d365506b-fc14-479d-b34d-0f3ae267a858 |
   | comparison_operator       | gt                                   |
   | description               | instance consuming memory            |
   | enabled                   | True                                 |
   | evaluate_timestamp        | 2023-10-13T04:07:14.849164           |
   | evaluation_periods        | 3                                    |
   | granularity               | 300                                  |
   | insufficient_data_actions | []                                   |
   | metric                    | memory.usage                         |
   | name                      | memory_high                          |
   | ok_actions                | []                                   |
   | project_id                | 815325ab42e443fbb6fc6eb8905c5aa8     |
   | repeat_actions            | False                                |
   | resource_id               | 1f12876c-b320-436a-9ae9-5fd8e065e69f |
   | resource_type             | instance                             |
   | severity                  | low                                  |
   | state                     | insufficient data                    |
   | state_reason              | Not evaluated yet                    |
   | state_timestamp           | 2023-10-13T04:07:14.792561           |
   | threshold                 | 2000.0                               |
   | time_constraints          | []                                   |
   | timestamp                 | 2023-10-13T04:07:14.792561           |
   | type                      | gnocchi_resources_threshold          |
   | user_id                   | d9730bd835bc4620ab3e6b06c5b17477     |
   +---------------------------+--------------------------------------+

Check the metrics for ``memory.usage`` using the following command:

::

    openstack metric measures show -r <INSTANCE ID> memory.usage --granularity 300

Sample output:

::

   +---------------------------+-------------+---------------+
   | timestamp                 | granularity |         value |
   +---------------------------+-------------+---------------+
   | 2023-10-13T03:45:00+00:00 |       300.0 | 2138.51171875 |
   | 2023-10-13T03:50:00+00:00 |       300.0 |    2138.46875 |
   | 2023-10-13T03:55:00+00:00 |       300.0 |  2138.4609375 |
   | 2023-10-13T04:00:00+00:00 |       300.0 |  2138.4609375 |
   | 2023-10-13T04:05:00+00:00 |       300.0 |  2138.4609375 |
   +---------------------------+-------------+---------------+

Check alarm history for any alarm events triggered using the following
command:

::

   openstack alarm-history show <ALARM ID> --fit-width

Sample output:

::

   +----------------------------+------------------+-------------------------------------------------------------------------------------------------------------------+--------------------------------------+
   | timestamp                  | type             | detail                                                                                                            | event_id                             |
   +----------------------------+------------------+-------------------------------------------------------------------------------------------------------------------+--------------------------------------+
   | 2023-10-13T04:08:45.607387 | state transition | {"state": "alarm", "transition_reason": "Transition to alarm due to 3 samples outside threshold, most recent:     | 1ae90db8-124a-4e9a-9e76-5a81216ac54c |
   |                            |                  | 2138.4609375"}                                                                                                    |                                      |
   | 2023-10-13T04:07:14.792561 | creation         | {"alarm_id": "d365506b-fc14-479d-b34d-0f3ae267a858", "type": "gnocchi_resources_threshold", "enabled": true,      | b991407b-511e-40ba-a353-f63e8e60782c |
   |                            |                  | "name": "memory_high", "description": "instance consuming memory", "timestamp": "2023-10-13T04:07:14.792561",     |                                      |
   |                            |                  | "user_id": "d9730bd835bc4620ab3e6b06c5b17477", "project_id": "815325ab42e443fbb6fc6eb8905c5aa8", "state":         |                                      |
   |                            |                  | "insufficient data", "state_timestamp": "2023-10-13T04:07:14.792561", "state_reason": "Not evaluated yet",        |                                      |
   |                            |                  | "ok_actions": [], "alarm_actions": ["log://"], "insufficient_data_actions": [], "repeat_actions": false,          |                                      |
   |                            |                  | "time_constraints": [], "severity": "low", "rule": {"granularity": 300, "comparison_operator": "gt", "threshold": |                                      |
   |                            |                  | 2000.0, "aggregation_method": "mean", "evaluation_periods": 3, "metric": "memory.usage", "resource_id":           |                                      |
   |                            |                  | "1f12876c-b320-436a-9ae9-5fd8e065e69f", "resource_type": "instance"}}                                             |                                      |
   +----------------------------+------------------+-------------------------------------------------------------------------------------------------------------------+--------------------------------------+

Alarm ``memory_high`` is created with alarm action ``log``, so check for
log events on ``aodh-evaluator``:

::

   sudo k8s kubectl -n openstack logs aodh-0 -c aodh-notifier | grep memory_high

   2023-10-13T04:08:45.650Z [aodh-notifier] 2023-10-13 04:08:45.648 17 INFO aodh.notifier.log [-]
   Notifying alarm memory_high d365506b-fc14-479d-b34d-0f3ae267a858 of low priority from insufficient data to alarm with action log: because Transition to alarm due to 3 samples outside threshold, most recent:  2138.4609375.

OpenStack Exporter
~~~~~~~~~~~~~~~~~~

When the :doc:`Observability </how-to/features/observability>` feature is enabled, you’ll have
access to the Grafana OpenStack dashboards, providing insights about the
cloud usage.

-  OpenStack Dashboard: an overview of the various OpenStack components
-  OpenStack Overview: higher level overview of the OpenStack deployment
-  OpenStack Hypervisor Overview: detailed information of the
   hypervisors
