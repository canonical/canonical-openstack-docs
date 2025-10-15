Load Balancer as a Service
==========================

This feature deploys
`Octavia <https://docs.openstack.org/octavia/latest/index.html>`__, the
OpenStack load balancing service. The feature supports only the `OVN
provider
driver <https://docs.openstack.org/octavia/latest/admin/providers/index.html#ovn-octavia-provider-driver>`__.

Enabling Load Balancer
----------------------

To enable Load Balancer, run the following command:

.. literalinclude:: ../snippets/load-balancer.task.sh
   :language: bash
   :start-after: [docs-view:enable-load-balancer]
   :end-before:  [docs-view:enable-load-balancer-end]

Use OpenStack CLI to manage load balancers. See the upstream `Octavia
documentation <https://docs.openstack.org/octavia/latest/user/guides/basic-cookbook.html>`__
for details. The OVN Octavia provider has certain limitations that are
documented
`here <https://docs.openstack.org/ovn-octavia-provider/latest/admin/driver.html#limitations-of-the-ovn-provider-driver>`__.

Disabling Load Balancer
-----------------------

To disable Load Balancer, run the following command:

.. literalinclude:: ../snippets/load-balancer.task.sh
   :language: bash
   :start-after: [docs-view:disable-load-balancer]
   :end-before:  [docs-view:disable-load-balancer-end]

Usage
-----

Users should have roles ``member`` and ``load-balancer_member`` to
create and manage load balancers within their project.

Go through all the following sub-sections.

Create a load balancer
~~~~~~~~~~~~~~~~~~~~~~

Create a load balancer using the following command:

::

   openstack loadbalancer create --name <name> --vip-network-id <network>

For example, create the load balancer ‘test’:

::

   openstack loadbalancer create --name test --vip-network-id demo-network --wait

Sample output:

::

   +---------------------+--------------------------------------+
   | Field               | Value                                |
   +---------------------+--------------------------------------+
   | admin_state_up      | True                                 |
   | availability_zone   | None                                 |
   | created_at          | 2023-10-11T09:20:17                  |
   | description         |                                      |
   | flavor_id           | None                                 |
   | id                  | 8bb11dba-113e-46df-b7bd-3e099669dcf4 |
   | listeners           |                                      |
   | name                | test                                 |
   | operating_status    | ONLINE                               |
   | pools               |                                      |
   | project_id          | cee090abc4d14819b9508e763e564984     |
   | provider            | ovn                                  |
   | provisioning_status | ACTIVE                               |
   | updated_at          | 2023-10-11T09:20:20                  |
   | vip_address         | 192.168.122.218                      |
   | vip_network_id      | 9cbb0646-9936-4ceb-9324-8f87ef118491 |
   | vip_port_id         | 749a598e-807c-475d-ab8d-26747bac2296 |
   | vip_qos_policy_id   | None                                 |
   | vip_subnet_id       | 642d7a6d-625e-455a-a171-31082cd39c31 |
   | tags                |                                      |
   | additional_vips     | []                                   |
   +---------------------+--------------------------------------+

Create a load balancer listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a load balancer listener using the following command:

::

   openstack loadbalancer listener create --name <name> --protocol <protocol> --protocol-port <port> <LB name>

For example, add a listener on port 5555 for the ‘test’ load balancer:

::

   openstack loadbalancer listener create --name test-listener --protocol TCP --protocol-port 5555 test --wait

Sample output:

::

   +-----------------------------+--------------------------------------+
   | Field                       | Value                                |
   +-----------------------------+--------------------------------------+
   | admin_state_up              | True                                 |
   | connection_limit            | -1                                   |
   | created_at                  | 2023-10-11T09:21:11                  |
   | default_pool_id             | None                                 |
   | default_tls_container_ref   | None                                 |
   | description                 |                                      |
   | id                          | 2412a8fa-ce0a-430b-80bb-5f8c8ec6168f |
   | insert_headers              | None                                 |
   | l7policies                  |                                      |
   | loadbalancers               | 8bb11dba-113e-46df-b7bd-3e099669dcf4 |
   | name                        | test-listener                        |
   | operating_status            | ONLINE                               |
   | project_id                  | cee090abc4d14819b9508e763e564984     |
   | protocol                    | TCP                                  |
   | protocol_port               | 5555                                 |
   | provisioning_status         | ACTIVE                               |
   | sni_container_refs          | []                                   |
   | timeout_client_data         | 50000                                |
   | timeout_member_connect      | 5000                                 |
   | timeout_member_data         | 50000                                |
   | timeout_tcp_inspect         | 0                                    |
   | updated_at                  | 2023-10-11T09:21:12                  |
   | client_ca_tls_container_ref | None                                 |
   | client_authentication       | NONE                                 |
   | client_crl_container_ref    | None                                 |
   | allowed_cidrs               | None                                 |
   | tls_ciphers                 | None                                 |
   | tls_versions                | None                                 |
   | alpn_protocols              | None                                 |
   | tags                        |                                      |
   +-----------------------------+--------------------------------------+

Create a load balancer pool
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a load balancer pool using the following command:

::

   openstack loadbalancer pool create --name <name> --protocol <protocol> --lb-algorithm <algorithm> --listener <LB listener name>

For example, create the load balancer pool ‘test-pool’ for the
‘test-listener’ listener:

::

   openstack loadbalancer pool create --name test-pool --protocol TCP --lb-algorithm SOURCE_IP_PORT --listener test-listener --wait

Sample output:

::

   +----------------------+--------------------------------------+
   | Field                | Value                                |
   +----------------------+--------------------------------------+
   | admin_state_up       | True                                 |
   | created_at           | 2023-10-11T09:21:48                  |
   | description          |                                      |
   | healthmonitor_id     |                                      |
   | id                   | b7d9ac9f-5bfe-4786-a805-1a59fba98ee4 |
   | lb_algorithm         | SOURCE_IP_PORT                       |
   | listeners            | 2412a8fa-ce0a-430b-80bb-5f8c8ec6168f |
   | loadbalancers        | 8bb11dba-113e-46df-b7bd-3e099669dcf4 |
   | members              |                                      |
   | name                 | test-pool                            |
   | operating_status     | ONLINE                               |
   | project_id           | cee090abc4d14819b9508e763e564984     |
   | protocol             | TCP                                  |
   | provisioning_status  | ACTIVE                               |
   | session_persistence  | None                                 |
   | updated_at           | 2023-10-11T09:21:48                  |
   | tls_container_ref    | None                                 |
   | ca_tls_container_ref | None                                 |
   | crl_container_ref    | None                                 |
   | tls_enabled          | False                                |
   | tls_ciphers          | None                                 |
   | tls_versions         | None                                 |
   | tags                 |                                      |
   | alpn_protocols       | None                                 |
   +----------------------+--------------------------------------+

Add members to the load balancer pool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add members to the load balancer pool using the following command:

::

   openstack loadbalancer member create --name <name> --address <application ip address> --protocol-port <application port> <LB pool name>

Run the above command multiple times to add new members to the load
balancer pool.

For example, to add member ‘test-pool-member1’ to the ‘test-pool’
pool, whose service is running on IP 192.168.122.183 and port 80:

::

   openstack loadbalancer member create --name test-pool-member1 --address 192.168.122.183 --protocol-port 80 test-pool --wait

Sample output:

::

   +---------------------+--------------------------------------+
   | Field               | Value                                |
   +---------------------+--------------------------------------+
   | address             | 192.168.122.183                      |
   | admin_state_up      | True                                 |
   | created_at          | 2023-10-11T09:23:23                  |
   | id                  | e386e580-8278-4253-8bbb-91f412d935e1 |
   | name                | test-pool-member1                    |
   | operating_status    | NO_MONITOR                           |
   | project_id          | cee090abc4d14819b9508e763e564984     |
   | protocol_port       | 80                                   |
   | provisioning_status | ACTIVE                               |
   | subnet_id           | None                                 |
   | updated_at          | 2023-10-11T09:23:24                  |
   | weight              | 1                                    |
   | monitor_port        | None                                 |
   | monitor_address     | None                                 |
   | backup              | False                                |
   | tags                |                                      |
   +---------------------+--------------------------------------+

Add a health monitor to the load balancer pool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a health monitor to the load balancer pool using the following
command:

::

   openstack loadbalancer healthmonitor create --name <name> --delay <delay> --timeout <timeout> --max-retries <max retries> --type <protocol> <LB pool name>

For example, to add health monitor ‘test-monitor’ to the ‘test-pool’
pool:

::

   openstack loadbalancer healthmonitor create --name test-monitor --delay 7 --timeout 5 --max-retries 3 --type TCP test-pool --wait

Sample output:

::

   +---------------------+--------------------------------------+
   | Field               | Value                                |
   +---------------------+--------------------------------------+
   | project_id          | cee090abc4d14819b9508e763e564984     |
   | name                | test-monitor                         |
   | admin_state_up      | True                                 |
   | pools               | b7d9ac9f-5bfe-4786-a805-1a59fba98ee4 |
   | created_at          | 2023-10-11T09:33:33                  |
   | provisioning_status | ACTIVE                               |
   | updated_at          | 2023-10-11T09:33:34                  |
   | delay               | 7                                    |
   | expected_codes      | None                                 |
   | max_retries         | 3                                    |
   | http_method         | None                                 |
   | timeout             | 5                                    |
   | max_retries_down    | 3                                    |
   | url_path            | None                                 |
   | type                | TCP                                  |
   | id                  | 7f2cbe52-b024-4ede-a24b-7fa3cc6aa606 |
   | operating_status    | ONLINE                               |
   | http_version        | None                                 |
   | domain_name         | None                                 |
   | tags                |                                      |
   +---------------------+--------------------------------------+

Verify load balancer pool member operating status using the following
command:

::

   openstack loadbalancer member list <LB pool name>

For example:

::

   openstack loadbalancer member list test-pool

Sample output:

::

   +--------------------------------------+-------------------+----------------------------------+---------------------+-----------------+---------------+------------------+--------+
   | id                                   | name              | project_id                       | provisioning_status | address         | protocol_port | operating_status | weight |
   +--------------------------------------+-------------------+----------------------------------+---------------------+-----------------+---------------+------------------+--------+
   | e386e580-8278-4253-8bbb-91f412d935e1 | test-pool-member1 | cee090abc4d14819b9508e763e564984 | ACTIVE              | 192.168.122.183 |            80 | ONLINE           |      1 |
   +--------------------------------------+-------------------+----------------------------------+---------------------+-----------------+---------------+------------------+--------+

Verify the load balancer details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verify the details of the load balancer using the following command:

::

   openstack loadbalancer status show <LB name>

For example:

::

   openstack loadbalancer status show test

Sample output:

::

   {
       "loadbalancer": {
           "id": "8bb11dba-113e-46df-b7bd-3e099669dcf4",
           "name": "test",
           "operating_status": "ONLINE",
           "provisioning_status": "ACTIVE",
           "listeners": [
               {
                   "id": "2412a8fa-ce0a-430b-80bb-5f8c8ec6168f",
                   "name": "test-listener",
                   "operating_status": "ONLINE",
                   "provisioning_status": "ACTIVE",
                   "pools": [
                       {
                           "id": "b7d9ac9f-5bfe-4786-a805-1a59fba98ee4",
                           "name": "test-pool",
                           "provisioning_status": "ACTIVE",
                           "operating_status": "ONLINE",
                           "health_monitor": {
                               "id": "7f2cbe52-b024-4ede-a24b-7fa3cc6aa606",
                               "name": "test-monitor",
                               "type": "TCP",
                               "provisioning_status": "ACTIVE",
                               "operating_status": "ONLINE"
                           },
                           "members": [
                               {
                                   "id": "e386e580-8278-4253-8bbb-91f412d935e1",
                                   "name": "test-pool-member1",
                                   "operating_status": "ONLINE",
                                   "provisioning_status": "ACTIVE",
                                   "address": "192.168.122.183",
                                   "protocol_port": 80
                               },
                               {
                                   "id": "856fb894-714a-4d1d-beda-8cd2bc77485a",
                                   "name": "test-pool-member2",
                                   "operating_status": "ONLINE",
                                   "provisioning_status": "ACTIVE",
                                   "address": "192.168.122.248",
                                   "protocol_port": 80
                               }
                           ]
                       }
                   ]
               }
           ]
       }
   }

Attach a floating IP address to the load balancer VIP port
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a floating IP address and attach it to the load balancer VIP
port, use the below snippet:

::

   vip_port=$(openstack loadbalancer show test -c vip_port_id -f value)
   fip_id=$(openstack floating ip create external-network -c ID -f value)
   openstack floating ip set --port $vip_port $fip_id
   lb_fip=$(openstack floating ip list --port $vip_port -c 'Floating IP Address' -f value)
   echo $lb_fip

The above snippet outputs the load balancer VIP address:

::

   10.20.20.68

Verify load balancer functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To verify load balancer functionality, apply the ``nc`` utility to the
load balancer VIP and listener port:

::

   nc -vz 10.20.20.68 5555

The output will report success if the load balancer connection to the
backend service is made:

::

   Connection to 10.20.20.68 5555 port [tcp/*] succeeded!
