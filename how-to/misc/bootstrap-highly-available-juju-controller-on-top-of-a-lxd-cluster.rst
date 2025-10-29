Bootstrap highly available Juju controller on top of a LXD cluster
##################################################################

Canonical Juju does not yet support controller HA modeling capabilities when deployed on top
Kubernetes. This means that Canonical OpenStack clouds deployed using the
:doc:`manual bare metal provider</how-to/install/install-canonical-openstack-using-the-manual-bare-metal-provider>`
do not provide HA for all types of governance functions by default. To bypass this
limitation Canonical recommends using an external highly available Juju controller. Such a
controller can be bootstrapped on top of a LXD cluster, for example, running across the same
machines that are used in the Canonical OpenStack deployment.

This how-to guide provides all necessary information on how to perform aforementioned actions.

Requirements
++++++++++++

You will need:

* one dedicated physical network with:
  
  * unlimited access to the Internet
  * DHCP server configured to serve LXD containers

* at least three dedicated physical machines with:

  * hardware specifications matching minimum hardware specifications for the *Cloud* node as documented under the :doc:`Enterprise requirements</reference/enterprise-requirements>` section
  * fresh Ubuntu Server 24.04 LTS installed

Prepare machines
++++++++++++++++

All machines have to be configured first to use `bridges <https://ubuntu.com/server/docs/configuring-networks#bridging-multiple-interfaces>`_ instead of physical network interfaces on the Generic network.

For example, to prepare the *cloud-1* machine from the example configuration section, execute the following commands:

.. code-block :: text

   sudo bash -c 'cat <<EOF > /etc/netplan/config.yaml
   network:
       bridges:
           br0:
               addresses:
               - 172.16.1.101/24
               interfaces:
               - eno1
               routes:
               - to: default
                 via: 172.16.1.1
               nameservers:
                   addresses:
                   - 8.8.8.8
                   search:
                   - example.com
       ethernets:
           eno1:
               set-name: eno1
           eno2:
               set-name: eno2
       version: 2
   EOF'
   sudo netplan apply

Set up a LXD cluster
++++++++++++++++++++

In the first step, set up a `LXD cluster <https://canonical.com/lxd>`_ across at least three machines.

Bootstrap the cluster
---------------------

To bootstrap the cluster, execute the ``lxd init`` command on the first machine in the cluster (aka primary node):

.. code-block :: text

   lxd init

When prompted, answer some interactive questions. Below is a sample output from the *cloud-1* machine from the :doc:`Example physical configuration</reference/example-physical-configuration>`:

.. code-block :: text

   Installing LXD snap, please be patient.
   Would you like to use LXD clustering? (yes/no) [default=no]: yes
   What IP address or DNS name should be used to reach this server? [default=172.16.1.101]: 172.16.1.101
   Are you joining an existing cluster? (yes/no) [default=no]: no
   What member name should be used to identify this server in the cluster? [default=cloud-1]: cloud-1
   Do you want to configure a new local storage pool? (yes/no) [default=yes]: yes
   Name of the storage backend to use (btrfs, dir, lvm, zfs) [default=zfs]: zfs
   Create a new ZFS pool? (yes/no) [default=yes]: yes
   Would you like to use an existing empty block device (e.g. a disk or partition)? (yes/no) [default=no]: no
   Size in GiB of the new loop device (1GiB minimum) [default=30GiB]: 30GiB
   Do you want to configure a new remote storage pool? (yes/no) [default=no]: no
   Would you like to connect to a MAAS server? (yes/no) [default=no]: no
   Would you like to configure LXD to use an existing bridge or host interface? (yes/no) [default=no]: yes
   Name of the existing bridge or host interface: br0
   Would you like stale cached images to be updated automatically? (yes/no) [default=yes]: yes
   Would you like a YAML "lxd init" preseed to be printed? (yes/no) [default=no]: no

Refer to the `LXD documentation <https://documentation.ubuntu.com/lxd/en/latest/>`_ for detailed description of each of those questions and some examples.

Create registration tokens
--------------------------

Registration tokens have to be created first for the other machine to be able to join the newly bootstrapped cluster.

In order to create a registration token for the new machine, execute the ``lxc cluster add`` command on the primary node:

.. code-block :: text

   lxc cluster add NAME

``NAME`` is the name of the machine being added.

For example, to create a registration token for the *cloud-2* machine from the :doc:`Example physical configuration</reference/example-physical-configuration>` section, execute the following command on the *cloud-1* machine:

.. code-block :: text

   lxc cluster add cloud-2

Sample output (token):

.. code-block :: text

   Member cloud-2 join token:
   eyJzZXJ2ZXJfbmFtZSI6ImNsb3VkLTIuZXhhbXBsZS5jb20iLCJmaW5nZXJwcmludCI6IjFhZmYyZGQ3ZDhmZmUwZWE1MzliODA2ZWExNmE4NTRlYTBmYmNjZDU1MTJjYjlmMTk1YmU4YTY4ZTZkYzRkNzYiLCJhZGRyZXNzZXMiOlsiY2xvdWQtMS5leGFtcGxlLmNvbTo4NDQzIl0sInNlY3JldCI6ImYxZmIzMzcxOTlmZmRlNmIzMjYwYjQ1NGY5MTBmNTJhMzE3NGE2OTQ2MTAwMzU1OGU2ZmM3YjEyNDA2NmU2ZWIiLCJleHBpcmVzX2F0IjoiMjAyNC0xMS0wNFQxNToxNDoxOC4zMDE4NTEwNThaIn0=

Remember the value of the token. It will be needed in the next step of this how-to guide.

Add machines to the cluster
---------------------------

Now that the cluster has been bootstrapped and registration tokens have been created, other machines should be able to join the cluster.

To join the cluster, execute the ``sudo lxd init`` command on all remaining machines:

.. code-block :: text

   sudo lxd init

When prompted, answer some interactive questions. Below is a sample output from the *cloud-2* machine from the :doc:`Example physical configuration</reference/example-physical-configuration>`:

.. code-block :: text

   Installing LXD snap, please be patient.
   Would you like to use LXD clustering? (yes/no) [default=no]: yes
   What IP address or DNS name should be used to reach this server? [default=172.16.1.102]: 172.16.1.102
   Are you joining an existing cluster? (yes/no) [default=no]: yes
   Do you have a join token? (yes/no/[token]) [default=no]: yes
   Please provide join token: eyJzZXJ2ZXJfbmFtZSI6ImNsb3VkLTIiLCJmaW5nZXJwcmludCI6IjI5Y2UzNzJmYzVkZDg4ODE3NmMxNTNmYTc2OGJlOGJhMjIyNWQ1MGY5NWY2NmUwZTdlNDc4YzM3ODA1Y2U5MmIiLCJhZGRyZXNzZXMiOlsiMTcyLjE2LjEuMTAxOjg0NDMiXSwic2VjcmV0IjoiNjAxNjZmMDY0ODg4Y2ZkY2U1NzZiODgzMmYwYjRlNmVhYzZiOWY1MTU4Nzk3ZDE4MWM3YWFmMTAwZTVjY2ZjYSIsImV4cGlyZXNfYXQiOiIyMDI0LTExLTA0VDE1OjQ4OjU1LjQxMjg1NTg4OFoifQ==
   All existing data is lost when joining a cluster, continue? (yes/no) [default=no] yes
   Choose "size" property for storage pool "local": 
   Choose "source" property for storage pool "local": 
   Choose "zfs.pool_name" property for storage pool "local": 
   Would you like a YAML "lxd init" preseed to be printed? (yes/no) [default=no]: no 

Refer to the `LXD documentation <https://documentation.ubuntu.com/lxd/en/latest/>`_ for detailed description of each of those questions and some examples.

Verify cluster setup
--------------------

To verify cluster setup, execute the ``lxc cluster list`` command on any machine in the cluster:

.. code-block :: text

   lxc cluster list

You should be able to see all machines being used.

Sample output (based on the :doc:`Example physical configuration</reference/example-physical-configuration>` section):

.. code-block :: text

   +---------+---------------------------+-----------------+--------------+----------------+-------------+--------+-------------------+
   |  NAME   |            URL            |      ROLES      | ARCHITECTURE | FAILURE DOMAIN | DESCRIPTION | STATE  |      MESSAGE      |
   +---------+---------------------------+-----------------+--------------+----------------+-------------+--------+-------------------+
   | cloud-1 | https://172.16.1.101:8443 | database-leader | x86_64       | default        |             | ONLINE | Fully operational |
   |         |                           | database        |              |                |             |        |                   |
   +---------+---------------------------+-----------------+--------------+----------------+-------------+--------+-------------------+
   | cloud-2 | https://172.16.1.102:8443 | database        | x86_64       | default        |             | ONLINE | Fully operational |
   +---------+---------------------------+-----------------+--------------+----------------+-------------+--------+-------------------+
   | cloud-3 | https://172.16.1.103:8443 | database        | x86_64       | default        |             | ONLINE | Fully operational |
   +---------+---------------------------+-----------------+--------------+----------------+-------------+--------+-------------------+

Set trust password
------------------

Finally, set a trust password so that the cluster can later be registered as a Juju cloud by executing the following command on the primary node:

.. code-block :: text

   lxc config set core.trust_password PASSWORD

``PASSWORD`` is the trust password.

For example:

.. code-block :: text

   lxc config set core.trust_password mytrustpassword

Bootstrap Juju controllers
++++++++++++++++++++++++++

In the next step, bootstrap highly available `Juju controllers <https://juju.is/>`_ across all machines in the cluster.

Create system account
---------------------

.. note ::

   Canonical OpenStack cannot be installed under the same system account that is used to perform the initial bootstrap of the external Juju controller. As a result, dedicated system account has to be created first.

To create a dedicated system account and to switch into it, execute the following commands on the primary node:

.. code-block :: text

   sudo adduser bootstrap
   sudo usermod -a -G lxd,sudo bootstrap
   su bootstrap
   cd

Install the snap
----------------

Then, install the ``juju`` snap:

.. code-block :: text

   sudo snap install juju

Register the LXD cluster as a Juju cloud
----------------------------------------

Later, register the newly bootstrapped LXD cluster as a Juju cloud by performing the following actions.

Add the LXD cluster to the local LXC config:

.. code-block :: text

   lxc remote add NAME IP --password PASSWORD

``NAME`` is the name of the LXD cluster.

``IP`` is the IP address of the primary node in the cluster.

``PASSWORD`` is the trust password that was set in one of the previous steps.

When prompted, type ``y``.

For example, to register the LXD cluster from the :doc:`Example physical configuration</reference/example-physical-configuration>` section as ``mylxdcluster`` cloud, execute the following commands:

.. code-block :: text

   $ lxc remote add mylxdcluster 172.16.1.101 --password mytrustpassword
   Certificate fingerprint: 29ce372fc5dd888176c153fa768be8ba2225d50f95f66e0e7e478c37805ce92b
   ok (y/n/[fingerprint])? y

You should now be able to see ``mylxdcluster`` on the list of available Juju clouds:

.. code-block :: text

   $ juju clouds
   Only clouds with registered credentials are shown.
   There are more clouds, use --all to see them.
   You can bootstrap a new controller using one of these clouds...
   
   Clouds available on the client:
   Cloud         Regions  Default    Type  Credentials  Source    Description
   localhost     1        localhost  lxd   0            built-in  LXD Container Hypervisor
   mylxdcluster  1        default    lxd   0            built-in  LXD Cluster

Bootstrap a Juju controller
---------------------------

To bootstrap a Juju controller on the ``mylxdclluster`` cloud, execute the following command on the primary node:

.. code-block :: text

   juju bootstrap mylxdcluster

One finished, you should be able to see the following message on the screen:

.. code-block :: text

   Bootstrap complete, controller "mylxdcluster-default" is now available
   Controller machines are in the "controller" model

   Now you can run
   	   juju add-model <model-name>
   to create a new model to deploy workloads.

Make the controller highly available
------------------------------------

To make the controller highly available, execute the following command on the primary node:

.. code-block :: text

   juju enable-ha

Sample output:

.. code-block :: text

   maintaining machines: 0
   adding machines: 1, 2

The rest now happens in the background. Once finished, you should be able to see your Juju controller being highly available (indicated by ``3`` under the ``HA`` column):

.. code-block :: text

   $ juju controllers --refresh
   Controller             Model  User   Access     Cloud/Region          Models  Nodes  HA  Version
   mylxdcluster-default*  -      admin  superuser  mylxdcluster/default       1      3   3  3.5.4  

.. warning ::

   **Bug 1969667**

   At the moment, due to `lp1969667 <https://bugs.launchpad.net/juju/+bug/1969667>`_, LXC containers hosting Juju controller units do not get distributed equally across all nodes in the LXD cluster by default.

To workaround the aforementioned issue, run the ``lxc list`` command first:

.. code-block :: text

   lxc list

Sample output:

.. code-block :: text

   +---------------+---------+---------------------+------+-----------+-----------+----------+
   |     NAME      |  STATE  |        IPV4         | IPV6 |   TYPE    | SNAPSHOTS | LOCATION |
   +---------------+---------+---------------------+------+-----------+-----------+----------+
   | juju-e4ce90-0 | RUNNING | 172.16.1.248 (eth0) |      | CONTAINER | 0         | cloud-1  |
   +---------------+---------+---------------------+------+-----------+-----------+----------+
   | juju-e4ce90-1 | RUNNING | 172.16.1.249 (eth0) |      | CONTAINER | 0         | cloud-2  |
   +---------------+---------+---------------------+------+-----------+-----------+----------+
   | juju-e4ce90-2 | RUNNING | 172.16.1.250 (eth0) |      | CONTAINER | 0         | cloud-2  |
   +---------------+---------+---------------------+------+-----------+-----------+----------+

As you can see the ``juju-e4ce90-2`` container runs on the ``cloud-2`` node, while it should run on the ``cloud-3`` node instead.

To move the ``juju-e4ce90-2`` container from ``cloud-2`` to ``cloud-3``, execute the following commands:

.. code-block :: text

   lxc stop juju-e4ce90-2
   lxc move juju-e4ce90-2 --target cloud-3
   lxc start juju-e4ce90-2

At this point you should be able to see all three containers being equally distributed across all the nodes forming the LXD cluster:

.. code-block :: text

   $ lxc list
   +---------------+---------+---------------------+------+-----------+-----------+----------+
   |     NAME      |  STATE  |        IPV4         | IPV6 |   TYPE    | SNAPSHOTS | LOCATION |
   +---------------+---------+---------------------+------+-----------+-----------+----------+
   | juju-e4ce90-0 | RUNNING | 172.16.1.248 (eth0) |      | CONTAINER | 0         | cloud-1  |
   +---------------+---------+---------------------+------+-----------+-----------+----------+
   | juju-e4ce90-1 | RUNNING | 172.16.1.249 (eth0) |      | CONTAINER | 0         | cloud-2  |
   +---------------+---------+---------------------+------+-----------+-----------+----------+
   | juju-e4ce90-2 | RUNNING | 172.16.1.250 (eth0) |      | CONTAINER | 0         | cloud-3  |
   +---------------+---------+---------------------+------+-----------+-----------+----------+

.. warning ::

   To avoid an unintended change of IPs and thus, loosing connectivity with Juju controllers post-deployment, reconfigure LXD containers to use static IP addresses at this point. Use the same IPs that were assigned during bootstrap. In order to reconfigure LXD containers to use static IP addresses, refer to the `Netplan documentation <https://documentation.ubuntu.com/server/explanation/networking/about-netplan/>`_.

Create necessary credentials for the Sunbeam client
---------------------------------------------------

To be able to use the newly bootstrapped, highly available Juju controller in the Sunbeam client, `add a new user <https://juju.is/docs/juju/manage-users#add-a-user>`_ to the controller and `grant necessary permissions <https://juju.is/docs/juju/juju-grant>`_ (``superuser``) to this user on the controller.

To add a new user, run:

.. code-block :: text

   juju add-user sunbeam

Sample output:

.. code-block :: text

   User "sunbeam" added
   Please send this command to sunbeam:
       juju register MHwTB3N1bmJlYW0wPBMSMTcyLjE2LjEuMTIxOjE3MDcwExIxNzIuMTYuMS4xMjI6MTcwNzATEjE3Mi4xNi4xLjEyMzoxNzA3MAQgJIknLboGwWOWObzGW1NFQ45z_TnBIEKt5kwfDL7ZSLsTD215Y2xvdWQtZGVmYXVsdBMA

   "sunbeam" has not been granted access to any models. You can use "juju grant" to grant access.

Remember the value of the token from the output as it will be needed in next steps.

To grant the user necessary permissions, run:

.. code-block :: text

   juju grant -c mylxdcluster-default sunbeam superuser

Register Juju controller in the Sunbeam client
++++++++++++++++++++++++++++++++++++++++++++++

First, log out from the ``bootstrap`` account:

.. code-block :: text

   exit

To register ``mylxdcluster-default`` controller in the Sunbeam client, execute the following command:

.. code-block :: text

   sunbeam juju register-controller mylxdcluster-default TOKEN

Replace ``TOKEN`` with the token obtained when creating the ``sunbeam`` user.

For example:

.. code-block :: text

   sunbeam juju register-controller mylxdcluster-default MHwTB3N1bmJlYW0wPBMSMTcyLjE2LjEuMTIxOjE3MDcwExIxNzIuMTYuMS4xMjI6MTcwNzATEjE3Mi4xNi4xLjEyMzoxNzA3MAQgJIknLboGwWOWObzGW1NFQ45z_TnBIEKt5kwfDL7ZSLsTD215Y2xvdWQtZGVmYXVsdBMA

At this point, you can bootstrap Canonical OpenStack cluster with Sunbeam while using the
``mylxdcluster-default`` controller.

For example:

.. code-block :: text

   sunbeam prepare-node-script --bootstrap | bash -x && newgrp snap_daemon
   sunbeam cluster bootstrap --role control,compute,storage --controller mylxdcluster-default
