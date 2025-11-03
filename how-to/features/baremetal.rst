Baremetal deployment service
============================

This feature deploys `Ironic`_, the bare metal provisioning service for
OpenStack. It allows OpenStack users to provision bare metal machines,
as opposed to virtual machines.

Enabling Baremetal
------------------

This feature requires the storage role. To enable this feature, run the
following command:

::

   sunbeam enable baremetal

.. note::
   This feature requires the ``microceph`` charm channel to be on
   ``squid/edge`` or newer.

The openstack CLI can now be used to manage bare metal machines. See the
upstream `Ironic CLI`_ documentation for details.

The feature will be configured based on the cluster's manifest file.
Alternatively, a different manifest file can be specified during the feature
enablement:

::

   sunbeam enable --manifest baremetal-manifest.yaml baremetal


Sample `baremetal-manifest.yaml` file:

.. code-block:: yaml

    features:
      baremetal:
        software:
          charms:
            ironic-conductor-k8s:
              channel: 2025.1/edge
            ironic-k8s:
              channel: 2025.1/edge
            nova-ironic-k8s:
              channel: 2025.1/edge
            neutron-baremetal-switch-config-k8s:
              channel: 2025.1/edge
            neutron-generic-switch-config-k8s:
              channel: 2025.1/edge
        config:
          shards: ["shard0", "shard1"]
          conductor-groups: ["shard0", "shard1"]
          switchconfigs:
            netconf:
              nexus:
                configfile: |
                  ["nexus.example.net"]
                  driver = "netconf-openconfig"
                  device_params = "name:nexus"
                  switch_info = "nexus"
                  switch_id = "00:53:00:0a:0a:0a"
                  host = "nexus.example.net"
                  username = "user"
                  key_filename = "/etc/neutron/sshkeys/nexus-sshkey"
                additional-files:
                  nexus-sshkey: |
                    some key here.
            generic:
              arista:
                configfile: |
                  ["genericswitch:arista-hostname"]
                  device_type = "netmiko_arista_eos"
                  ngs_mac_address = "00:53:00:0a:0a:0a"
                  ip = "10.20.30.40"
                  username = "admin"
                  key_file = "/etc/neutron/sshkeys/arista-key"
                additional-files:
                  arista-key: |
                    some key here.

.. note::
   Rerunning the `sunbeam enable baremetal` command with a different manifest
   file will replace the previously deployed feature configuration (e.g.:
   deployed `nova-ironic` shards, Ironic Conductor groups, Neutron switch
   configurations).

For the switch configurations, the following restrictions apply:

- The `key_filename` and `key_file` config options base file paths must be
  `/etc/neutron/sshkeys`.
- The files referenced in `key_filename` or `key_file` as seen above will
  require those files to be defined as additional files as well.
- Unknown fields in the switch configurations are not allowed. See
  `netconf configuration options`_ and `generic switch configuration`_.
- For `generic` switch configurations, the `device_type` field is mandatory.

After the feature is enabled, you can use the `sunbeam baremetal` sub-command
to manage the deployed `nova-ironic` shards, Ironic Conductor groups, and
Neutron switch configurations.

Managing `nova-ironic` shards
-----------------------------

`nova-ironic` shards will be deployed while enabling the `baremetal` feature,
as mentioned above. Additional shards can be added through the following
command:

::

   sunbeam baremetal shard add SHARD

`nova-ironic` shards can be removed by running the following command:

::

   sunbeam baremetal shard delete SHARD

The following command can be used to list the currently deployed shards:

::

   sunbeam baremetal shard list


Managing Ironic Conductor groups
--------------------------------

By default, sunbeam deploys an `ironic-conductor-k8s` charm with an empty
`conductor-group` configuration option. Additional Ironic Conductor groups
will be deployed while enabling the `baremetal` feature, based on the
`conductor-groups` configuration mentioned above.

Additional Ironic Conductor groups can be added through the following command:

::

   sunbeam baremetal conductor-groups add GROUP-NAME

Ironic Conductor Groups can be removed by running the following command:

::

   sunbeam baremetal conductor-groups delete GROUP-NAME

The following command can be used to list the currently Ironic Conductor
Groups:

::

   sunbeam baremetal conductor-groups list

Managing Neutron Switch Configurations
--------------------------------------

`netconf` and `generic` Neutron switch configurations will be added while
enabling the `baremetal` feature, as mentioned above. Additional configurations
can be added through the following command:

::

   sunbeam baremetal switch-config add netconf|generic NAME --config CONFIGFILE  [--additional-file <NAME FILEPATH>]

An existing switch configuration can be updated with the command:

::

   sunbeam baremetal switch-config update netconf|generic NAME --config CONFIGFILE  [--additional-file <NAME FILEPATH>]

.. note::
   For the add / update sub-commands, multiple additional files can be
   specified.

Note that the same restrictions for the switch configurations mentioned above
still apply when adding new ones or updating existing ones.

A switch configuration can be deleted with the following command:

::

   sunbeam baremetal switch-config delete NAME


The following command can be used to list the current Neutron switch
configurations and their protocol:

::

   sunbeam baremetal switch-config list

Disabling Baremetal
-------------------

To disable this feature, run the following command:

::

   sunbeam disable baremetal

Usage
-----

.. important::
   In order to access the Ironic API, the OpenStack credentials used needs to
   have a system-scoped role. A user's assigned roles can be seen by running
   the following command:

::

   openstack role assignment list --user USER --names

A system-scoped role can be added to a user by running the following command:

::

   openstack role add --system all --user USER ROLE

Finally, for system-scoped requests, the project name and project domain name
may not be used (`OS_PROJECT_NAME` and `OS_PROJECT_DOMAIN_NAME` environment
variables), and the system scope "all" needs to be used. Here is a sample
`.openrc-system` file:

::

   # openrc for system-scoped access to OpenStack
   export OS_USERNAME=system-admin
   export OS_PASSWORD=correct-horse-battery-staple
   export OS_AUTH_URL=https://sunbeam.deployment/openstack-keystone/v3
   export OS_USER_DOMAIN_NAME=default
   export OS_AUTH_VERSION=3
   export OS_IDENTITY_API_VERSION=3
   export OS_SYSTEM_SCOPE=all

The `.openrc-system` file can be loaded by running:

::

   source .openrc-system

The Ironic API can now be accessed:

::

   openstack baremetal driver list

   +---------------------+---------------------------------------------------------------------------+
   | Supported driver(s) | Active host(s)                                                            |
   +---------------------+---------------------------------------------------------------------------+
   | intel-ipmi          | ironic-conductor-0.ironic-conductor-endpoints.openstack.svc.cluster.local |
   | ipmi                | ironic-conductor-0.ironic-conductor-endpoints.openstack.svc.cluster.local |
   +---------------------+---------------------------------------------------------------------------+

User images for Ironic bare metal deployments can be created using the
`disk-image-builder`_, which are then `uploaded to Glance`_ to the Swift data
store. You can verify that the image is in the right store by checking the
image properties:

::

   openstack image show your-magnific-ironic-image

If the image is not in the Swift store, you can import it by running the
following command:

::

   openstack image import your-magnific-ironic-image --method copy-image --store swift

The command above creates a Glance Task, which can be checked if it finished
or not.

.. warning ::

   Even if the Glance Task Status shows `success`, you should check that the
   image is in the Swift store by checking the image properties, as shown
   above. If the image properties does not show that it is in the Swift store,
   it means that the Glance worker failed to upload it, and you should check
   the `glance-api`'s logs for additional details.

Ironic depends on having deploy images with ironic-python-agent (IPA) service
running on it for controlling and deploying baremetal nodes. Those images
can be built with the `Ironic Python Agent Builder`_, or community-built
images can be used instead:

::

   # load OpenStack admin credentials.
   . ~/.openrc
   unset OS_SYSTEM_SCOPE

   wget https://tarballs.openstack.org/ironic-python-agent/tinyipa/files/tinyipa-master.vmlinuz
   wget https://tarballs.openstack.org/ironic-python-agent/tinyipa/files/tinyipa-master.gz

   DEPLOY_VMLINUZ_UUID="$(openstack image create tinyipa-deploy-ipmi.vmlinuz --public --disk-format=raw --container-format=bare --file ./tinyipa-master.vmlinuz -f value -c id)"
   DEPLOY_INITRD_UUID="$(openstack image create tinyipa-deploy-ipmi.initramfs --public --disk-format=raw --container-format=bare --file ./tinyipa-master.gz -f value -c id)"

   openstack image import tinyipa-deploy-ipmi.vmlinuz --method copy-image --store swift
   openstack image import tinyipa-deploy-ipmi.initramfs --method copy-image --store swift

As an example, let's consider registering a bare metal node into Ironic using
the IPMI driver:

::

   # considering that the admin has a system-scoped role, as mentioned above.
   unset OS_PROJECT_NAME OS_PROJECT_DOMAIN_NAME
   export OS_SYSTEM_SCOPE=all

   # provide values for the following variables:
   IPMI_ADDR=""
   IPMI_PORT=""
   IPMI_USER=""
   IPMI_PASS=""
   IRONIC_NETWORK=""
   NODE_MAC_ADDR=""
   SWITCH_INFO=""
   SWITCH_ID=""

   # register the node.
   chassis_id=$(openstack baremetal chassis create -f value -c uuid)
   machine_uuid="$(openstack baremetal node create --name ironic-machine1 --driver ipmi --chassis $chassis_id -c uuid -f value)"
   openstack baremetal node set ironic-machine1 \
     --resource-class baremetal \
     --driver-info ipmi_address=$IPMI_ADDR --driver-info ipmi_port=$IPMI_PORT \
     --driver-info ipmi_username=$IPMI_USER --driver-info ipmi_password=$IPMI_PASS \
     --driver-info deploy_kernel=$DEPLOY_VMLINUZ_UUID \
     --driver-info deploy_ramdisk=$DEPLOY_INITRD_UUID \
     --driver-info cleaning_network=$IRONIC_NETWORK \
     --driver-info provisioning_network=$IRONIC_NETWORK

   # register a port for the node.
   port_uuid="$(openstack baremetal port create $NODE_MAC_ADDR --node $machine_uuid -c uuid -f value)"
   openstack baremetal port set $port_uuid --local-link-connection switch_info=$SWITCH_INFO \
     --local-link-connection switch_id=$SWITCH_ID --local-link-connection port_id=$NODE_MAC_ADDR

   # validate and provide the node; it should become available.
   openstack baremetal node validate ironic-machine1
   openstack baremetal node manage ironic-machine1
   openstack baremetal node show ironic-machine1
   openstack baremetal node provide ironic-machine1

.. important::
   The `IRONIC_NETWORK` network mentioned above must be a network that can reach
   its associated `ironic-conductor` HTTP and TFTP services, exposed through
   its Internal Load Balancer IP.

After the node has been registered and it became available, it can be deployed
as needed. It can also be deployed through Nova, though it will require a
special flavor for it:

::

   openstack flavor create --ram $RAM_MB --vcpus $CPU --disk $DISK_GB barely-metallic-flavor
   openstack flavor set --property resources:VCPU=0 barely-metallic-flavor
   openstack flavor set --property resources:MEMORY_MB=0 barely-metallic-flavor
   openstack flavor set --property resources:DISK_GB=0 barely-metallic-flavor

   # note that CUSTOM_BAREMETAL directly relates to the --resource-class baremetal above.
   openstack flavor set --property resources:CUSTOM_BAREMETAL=1 barely-metallic-flavor

Finally, you can deploy the bare metal node:

::

   openstack server create --image your-magnific-ironic-image \
     --flavor barely-metallic-flavor --nic net-id=some-network \
     --key my-key baremetal-instance

For more information on how to use Ironic, check the `Ironic User Guide`_.

.. LINKS
.. _netconf configuration options: https://docs.openstack.org/networking-baremetal/2025.1/configuration/ml2/device_drivers/netconf-openconfig.html
.. _generic switch configuration: https://docs.openstack.org/networking-generic-switch/2025.1/configuration.html
.. _disk-image-builder: https://docs.openstack.org/ironic/2025.1/user/creating-images.html
.. _uploaded to Glance: https://docs.openstack.org/ironic/2025.1/install/configure-glance-images.html
.. _Ironic Python Agent Builder: https://docs.openstack.org/ironic-python-agent-builder/2025.1/
.. _Ironic User Guide: https://docs.openstack.org/ironic/2025.1/user/index.html
