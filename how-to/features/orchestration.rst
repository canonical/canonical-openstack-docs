Orchestration
=============

This feature deploys `Heat <https://docs.openstack.org/heat>`__, the
OpenStack Orchestration service.

Enabling Orchestration
----------------------

To enable Orchestration, run the following command:

.. literalinclude:: ../snippets/orchestration.task.sh
   :language: bash
   :start-after: [docs-view:enable-orchestration]
   :end-before:  [docs-view:enable-orchestration-end]

Use OpenStack CLI to manage orchestration stacks. See the upstream `Heat
documentation <https://docs.openstack.org/heat/latest/getting_started/create_a_stack.html>`__
for details.

Disabling Orchestration
-----------------------

To disable Orchestration, run the following command:

::

   sunbeam disable orchestration

This will terminate the application but not remove it from the model. To
do that, run the following:

::

   juju remove-application --force --no-wait --no-prompt -m openstack \
      heat heat-cfn heat-mysql-router heat-cfn-mysql-router

Usage
-----

Create a Heat stack using the following command:

::

   openstack stack create \
      -t https://opendev.org/openstack/heat-templates/raw/branch/master/hot/servers_in_existing_neutron_net.yaml \
      --parameter key_name=sunbeam \
      --parameter image=ubuntu \
      --parameter flavor=m1.tiny \
      --parameter public_net_id=external-network \
      --parameter private_net_id=demo-network \
      --parameter private_subnet_id=demo-subnet \
      teststack

The Heat template referred to in the above command creates two servers
in network ``demo-subnet`` and assigns them floating IP addresses.

Sample output:

::

   +---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Field               | Value                                                                                                                                                                    |
   +---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | id                  | 952770ed-f40e-4547-8f22-4dba8b1c714b                                                                                                                                     |
   | stack_name          | teststack                                                                                                                                                                |
   | description         | HOT template to deploy two servers into an existing neutron tenant network and assign floating IP addresses to each server so they are routable from the public network. |
   |                     |                                                                                                                                                                          |
   | creation_time       | 2023-10-13T06:47:35Z                                                                                                                                                     |
   | updated_time        | None                                                                                                                                                                     |
   | stack_status        | CREATE_IN_PROGRESS                                                                                                                                                       |
   | stack_status_reason | Stack CREATE started                                                                                                                                                     |
   +---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Verify stack status and wait for completion:

::

   openstack stack list

Sample output:

::

   +--------------------------------------+------------+-----------------+----------------------+--------------+
   | ID                                   | Stack Name | Stack Status    | Creation Time        | Updated Time |
   +--------------------------------------+------------+-----------------+----------------------+--------------+
   | 952770ed-f40e-4547-8f22-4dba8b1c714b | teststack  | CREATE_COMPLETE | 2023-10-13T06:47:35Z | None         |
   +--------------------------------------+------------+-----------------+----------------------+--------------+

Get stack details using the below command:

::

   openstack stack show teststack

Sample output:

::

   +-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Field                 | Value                                                                                                                                                                    |
   +-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | id                    | 952770ed-f40e-4547-8f22-4dba8b1c714b                                                                                                                                     |
   | stack_name            | teststack                                                                                                                                                                |
   | description           | HOT template to deploy two servers into an existing neutron tenant network and assign floating IP addresses to each server so they are routable from the public network. |
   |                       |                                                                                                                                                                          |
   | creation_time         | 2023-10-13T06:47:35Z                                                                                                                                                     |
   | updated_time          | None                                                                                                                                                                     |
   | stack_status          | CREATE_COMPLETE                                                                                                                                                          |
   | stack_status_reason   | Stack CREATE completed successfully                                                                                                                                      |
   | parameters            | OS::project_id: 098db89856cb4306828b0be678667294                                                                                                                         |
   |                       | OS::stack_id: 952770ed-f40e-4547-8f22-4dba8b1c714b                                                                                                                       |
   |                       | OS::stack_name: teststack                                                                                                                                                |
   |                       | flavor: m1.tiny                                                                                                                                                          |
   |                       | image: ubuntu                                                                                                                                                            |
   |                       | key_name: sunbeam                                                                                                                                                        |
   |                       | private_net_id: demo-network                                                                                                                                             |
   |                       | private_subnet_id: demo-subnet                                                                                                                                           |
   |                       | public_net_id: external-network                                                                                                                                          |
   |                       |                                                                                                                                                                          |
   | outputs               | - description: IP address of server1 in private network                                                                                                                  |
   |                       |   output_key: server1_private_ip                                                                                                                                         |
   |                       |   output_value: 192.168.122.154                                                                                                                                          |
   |                       | - description: Floating IP address of server2 in public network                                                                                                          |
   |                       |   output_key: server2_public_ip                                                                                                                                          |
   |                       |   output_value: 10.20.20.157                                                                                                                                             |
   |                       | - description: Floating IP address of server1 in public network                                                                                                          |
   |                       |   output_key: server1_public_ip                                                                                                                                          |
   |                       |   output_value: 10.20.20.73                                                                                                                                              |
   |                       | - description: IP address of server2 in private network                                                                                                                  |
   |                       |   output_key: server2_private_ip                                                                                                                                         |
   |                       |   output_value: 192.168.122.157                                                                                                                                          |
   |                       |                                                                                                                                                                          |
   | links                 | - href: http://10.20.21.13/openstack-heat/v1/098db89856cb4306828b0be678667294/stacks/teststack/952770ed-f40e-4547-8f22-4dba8b1c714b                                      |
   |                       |   rel: self                                                                                                                                                              |
   |                       |                                                                                                                                                                          |
   | deletion_time         | None                                                                                                                                                                     |
   | notification_topics   | []                                                                                                                                                                       |
   | capabilities          | []                                                                                                                                                                       |
   | disable_rollback      | True                                                                                                                                                                     |
   | timeout_mins          | None                                                                                                                                                                     |
   | stack_owner           | demo                                                                                                                                                                     |
   | parent                | None                                                                                                                                                                     |
   | stack_user_project_id | 0dfde376b8544b0499e74c4d7a82cc27                                                                                                                                         |
   | tags                  | []                                                                                                                                                                       |
   |                       |                                                                                                                                                                          |
   +-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Verify if stack resources are created (i.e. if new servers are launched
or not):

::

   openstack server list
   +--------------------------------------+----------+--------+--------------------------------------------+--------+---------+
   | ID                                   | Name     | Status | Networks                                   | Image  | Flavor  |
   +--------------------------------------+----------+--------+--------------------------------------------+--------+---------+
   | 0ad5e745-8d5b-4cc3-8ccf-f460733a3af4 | Server2  | ACTIVE | demo-network=10.20.20.157, 192.168.122.157 | ubuntu | m1.tiny |
   | 07261def-a40b-4976-9399-0398319b4067 | Server1  | ACTIVE | demo-network=10.20.20.73, 192.168.122.154  | ubuntu | m1.tiny |
   +--------------------------------------+----------+--------+--------------------------------------------+--------+---------+
