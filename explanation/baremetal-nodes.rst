Bare metal nodes
================

This document details how to interact with `Ironic`_ (the bare metal
provisioning service for OpenStack) in a Sunbeam deployment, which is made
available by :doc:`enabling the baremetal feature</how-to/features/baremetal>`.

Accessing the Ironic API
------------------------

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

Preparing Glance images for Ironic
----------------------------------

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
running on them for controlling and deploying baremetal nodes. Those images
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

Creating Nova flavors for Ironic
--------------------------------

Ironic bare metal nodes can be deployed as Nova instances. For this, special
bare metal flavors are required, allowing users to essentially deploy an
Ironic node based on its `resource_class`:

::

   # Change the ram, vcpus, and disk to match the hardware.
   openstack flavor create --ram 4096 --vcpus 2 --disk 40 metallic-flavor

   openstack flavor set --property resources:VCPU=0 metallic-flavor
   openstack flavor set --property resources:MEMORY_MB=0 metallic-flavor
   openstack flavor set --property resources:DISK_GB=0 metallic-flavor

   # note that CUSTOM_BAREMETAL directly relates to an Ironic node's --resource-class=baremetal.
   openstack flavor set --property resources:CUSTOM_BAREMETAL=1 metallic-flavor

Check the `Nova flavors for Ironic`_ documentation for more information.

Register a bare metal node in Ironic
------------------------------------

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

   echo "Managing 'ironic-machine1' and waiting for it to become 'manageable'..."
   openstack baremetal node manage ironic-machine1 --wait 300
   openstack baremetal node show ironic-machine1

   echo "Providing 'machine-machine1' and waiting for it to become 'available'... May take a while if automated_cleaning=true..."
   openstack baremetal node provide ironic-machine1 --wait=600
   openstack baremetal node show ironic-machine1

.. important::
   During deployment, Ironic machines must be able to contact the
   `ironic-conductor` HTTP and TFTP services (exposed via an internal Load
   Balancer IP), as well as the OpenStack Swift Object store endpoint.
   Therefore, the `IRONIC_NETWORK` mentioned above must be routable to these
   endpoints.

Deploying a Nova Instance
-------------------------

After the node has been registered and it became available, it can be deployed
as needed. It can also be deployed through Nova, using the flavor mentioned
above:

::

   openstack server create --image your-magnific-ironic-image \
     --flavor metallic-flavor --nic net-id=some-network \
     --key my-key baremetal-instance

After a while, the Ironic node should have enter the `active` provisioning
state, and the Nova server should have an `ACTIVE` status:

::

   openstack baremetal node list
   +--------------------------------------+-----------------+--------------------------------------+-------------+--------------------+-------------+
   | UUID                                 | Name            | Instance UUID                        | Power State | Provisioning State | Maintenance |
   +--------------------------------------+-----------------+--------------------------------------+-------------+--------------------+-------------+
   | 12f9f792-2d7e-4447-929e-1e183798ecff | ironic-machine1 | 53a5efd0-acc5-41ac-a683-be67559ca743 | power on    | active             | False       |
   +--------------------------------------+-----------------+--------------------------------------+-------------+--------------------+-------------+

   openstack server list
   +--------------------------------------+--------------------+--------+-------------------------------+--------------------------+-----------------+
   | ID                                   | Name               | Status | Networks                      | Image                    | Flavor          |
   +--------------------------------------+--------------------+--------+-------------------------------+--------------------------+-----------------+
   | 53a5efd0-acc5-41ac-a683-be67559ca743 | baremetal-instance | ACTIVE | physnet2-network=10.27.187.66 | cirros-0.6.2-x86_64-disk | metallic-flavor |
   +--------------------------------------+--------------------+--------+-------------------------------+--------------------------+-----------------+

For more information on how to use Ironic, check the `Ironic User Guide`_.

.. LINKS
.. _disk-image-builder: https://docs.openstack.org/ironic/2025.1/user/creating-images.html
.. _uploaded to Glance: https://docs.openstack.org/ironic/2025.1/install/configure-glance-images.html
.. _Ironic Python Agent Builder: https://docs.openstack.org/ironic-python-agent-builder/2025.1/
.. _Nova flavors for Ironic: https://docs.openstack.org/ironic/2025.1/install/configure-nova-flavors.html
.. _Ironic User Guide: https://docs.openstack.org/ironic/2025.1/user/index.html
