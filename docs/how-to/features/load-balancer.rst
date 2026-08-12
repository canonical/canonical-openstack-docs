Load Balancer as a Service
==========================

This feature deploys
`Octavia <https://docs.openstack.org/octavia/latest/index.html>`__, the
OpenStack load balancing service. Two provider backends are supported:

- **OVN provider** (default) – a lightweight, kernel-based provider
  implemented through Open Virtual Network. See the upstream `OVN
  Octavia provider documentation
  <https://docs.openstack.org/ovn-octavia-provider/latest/admin/driver.html>`__
  for supported features and limitations.
- **Amphora provider** (optional) – a VM-based provider that runs a
  dedicated HAProxy instance per load balancer, offering a broader
  feature set. Requires MicroOVN as the SDN. See the upstream `Amphora
  provider documentation
  <https://docs.openstack.org/octavia/latest/admin/providers/index.html#amphora>`__
  for details.

Enabling Load Balancer
----------------------

To enable Load Balancer, run the following command:

::

   sunbeam enable loadbalancer

This enables Octavia with the OVN provider. Use the OpenStack CLI to
manage load balancers. See the upstream `Octavia documentation
<https://docs.openstack.org/octavia/latest/user/guides/basic-cookbook.html>`__
for details.

Enabling the Amphora provider
-----------------------------

The Amphora provider is an optional add-on to the load balancer feature,
controlled through feature gates. It is not yet considered
production-ready. For general information about feature gates, see
:doc:`Manage experimental features
</how-to/operations/manage-experimental-features>`.

It requires the ``microovn-sdn`` and ``loadbalancer-amphora`` feature
gates to be active.

.. note::

   The Amphora provider requires MicroOVN as the SDN. MicroOVN SDN must be enabled
   before running ``sunbeam cluster bootstrap`` with:

   ::

      sudo snap set openstack feature.microovn-sdn=true
      sudo snap set openstack ovn.provider=microovn 

Step 1 – Enable the feature gate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enable the Amphora feature gate:

::

   sudo snap set openstack feature.loadbalancer-amphora=true

Step 2 – Configure the Amphora provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the interactive configuration command:

::

   sunbeam loadbalancer configure

The command presents a series of prompts. The table below describes each
option:

.. list-table::
   :header-rows: 1
   :widths: 35 10 55

   * - Prompt
     - Default
     - Description
   * - Enable Octavia Amphora provider?
     - ``y``
     - Activates the Amphora VM-based load-balancer backend.
   * - Amphora image tag
     - ``octavia-amphora``
     - Glance tag Octavia uses to locate the Amphora VM image. An image
       with this tag must exist in Glance before Octavia can create
       load-balancer instances.
   * - Auto-create Amphora image?
     - ``n``
     - If enabled, Sunbeam downloads the upstream Octavia Amphora image
       from ``tarballs.opendev.org``
       (``test-only-amphora-x64-haproxy-ubuntu-noble.qcow2``) and
       uploads it to Glance with the tag specified above. Skip this if
       you already have a suitable image in Glance.
   * - Auto-create Amphora Nova flavor?
     - ``y``
     - If enabled, Sunbeam creates a dedicated Nova flavor for Amphora
       VM instances automatically. Disable this if you already have a
       suitable flavor and want to provide its ID.
   * - Auto-create lb-mgmt network and subnet?
     - ``y``
     - If enabled, Sunbeam creates the Octavia ``lb-mgmt`` network and
       subnet automatically using an IPv6 ULA subnet
       (``fd00:a9fe:a9fe::/64``). Disable this if you already have a
       suitable network and want to provide its IDs.
   * - Auto-create Amphora security groups?
     - ``y``
     - If enabled, Sunbeam creates the Neutron security groups for
       Amphora VM ports automatically. Disable this if you already have
       suitable security groups and want to provide their IDs.

Step 3 – Provide TLS certificates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Octavia Amphora requires TLS certificates to secure communication
between the controller and the Amphora VM instances. You must obtain
two signed certificates from your Certificate Authority (CA):

- **Amphora controller certificate** – a leaf (non-CA) certificate used
  to authenticate the controller side of the Amphora TLS connection.
- **Amphora issuing CA certificate** – a CA certificate
  (``basicConstraints: CA:TRUE``) used by Octavia to sign certificates
  for individual Amphora instances.

Retrieve the Certificate Signing Requests (CSRs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List the outstanding CSRs:

::

   sunbeam loadbalancer list_outstanding_csrs --format yaml

Sample output:

::

   - app_name: octavia
     csr: |-
       -----BEGIN CERTIFICATE REQUEST-----
       <controller CSR PEM data>
       -----END CERTIFICATE REQUEST-----
     endpoint: amphora-controller-cert
     relation_id: '215'
     unit_name: null
   - app_name: octavia
     csr: |-
       -----BEGIN CERTIFICATE REQUEST-----
       <issuing CA CSR PEM data>
       -----END CERTIFICATE REQUEST-----
     endpoint: amphora-issuing-ca
     relation_id: '216'
     unit_name: null

Extract each CSR and submit it to your CA to obtain the signed
certificates. The ``endpoint`` field identifies the purpose of each CSR:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Certificate requirement
   * - ``amphora-controller-cert``
     - Leaf certificate (must **not** be a CA certificate).
   * - ``amphora-issuing-ca``
     - CA certificate (``basicConstraints: CA:TRUE``).

Provide the signed certificates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once your CA has returned the signed certificates, provide them to
Octavia:

::

   sunbeam loadbalancer provide_certificates

The command prompts for each certificate in turn. For both the
controller certificate and the issuing CA certificate, you will be asked
to supply:

- The signed certificate, base64-encoded (PEM).
- The CA certificate that signed it, base64-encoded (PEM).
- The full CA chain (intermediate + root CAs), base64-encoded (PEM) –
  leave empty if the CA certificate is self-signed or no chain is
  needed.

When all certificates have been accepted, the command confirms:

::

   TLS certificates provided to Octavia.

.. note::

   If the Amphora feature is re-configured or certificates expire,
   re-run ``sunbeam loadbalancer list_outstanding_csrs`` and
   ``sunbeam loadbalancer provide_certificates`` to renew them.

Disabling Load Balancer
-----------------------

To disable Load Balancer, run the following command:

::

   sunbeam disable loadbalancer

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

To use the Amphora provider instead of the default OVN provider, add
``--provider amphora`` to the command. This requires the Amphora
provider to be enabled and configured first (see
`Enabling the Amphora provider`_).

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
