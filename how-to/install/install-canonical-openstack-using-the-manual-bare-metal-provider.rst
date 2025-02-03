Install Canonical OpenStack using the manual bare metal provider
################################################################

This how-to guide provides all necessary information to install `Canonical OpenStack`_ with
Sunbeam using the manual bare metal provider.

Make sure you get familiar with the following sections before proceeding with any instructions
listed below:

* Architecture
* Design considerations
* Enterprise requirements
* Sample configuration

.. TODO: Add links to all the pages listed above

.. note ::

   This how-to guide is intended to serve operators willing to deploy a production-grade cloud.
   If you're looking for some simple learning materials instead, please refer to the Tutorials
   section of this documentation.

.. TODO: Add a link to the Tutorials page

Requirements
++++++++++++

You will need:

* two dedicated physical networks with an unlimited access to the Internet
* one dedicated physical machine with:

  * hardware specifications matching minimum hardware specifications for the *Cloud* node as
    documented under the Enterprise requirements section
  * fresh Ubuntu Server 24.04 LTS installed

.. TODO: Add a link to the Enterprise requirements section

.. TODO: TO be updated to Ubuntu Server 24.04 LTS once the re-base is complete

If you can't provide an unlimited access to the Internet, see the Manage a proxied environment
section.

.. TODO: Add a link to the Manage a proxied environment section

Additional machines can be added later. See the Scaling the cluster out how-to guide.

.. TODO: Add a link to the Scaling the cluster out how-to guide

Install Canonical OpenStack
+++++++++++++++++++++++++++

When using the manual bare metal provider, Canonical OpenStack installation process is
relatively simple and takes around 30 minutes to complete, depending on your Internet connection
speed.

.. warning ::

   Canonical Juju does not yet support controller HA modelling capabilities when deployed on top
   Kubernetes. This means that Canonical OpenStack clouds deployed using the manual bare metal
   provider do not provide HA for all types of governance functions by default. To bypass this
   limitation Canonical recommends using an external highly available Juju controller. External
   controller has to be registered before running the ``sunbeam cluster bootstrap`` command.

.. TODO: Add a link to the Using an existing Juju controller how-to guide

Install the snap
----------------

First, install the ``openstack`` snap:

.. code-block :: text

   sudo snap install openstack

This will install the latest stable version by default. You can use the ``--channel`` switch to
install a different version of OpenStack instead.

To list all available versions, execute the following command:

.. code-block :: text

   snap info openstack

Prepare the machine
-------------------

As a prerequisite, deploy LXD based Juju controller on the node. Refer :doc:`Bootstrap LXD based Juju controller on single node </how-to/misc/bootstrap-single-node-lxd-based-juju-controller>` for detailed procedure.

To prepare the machine for Canonical OpenStack usage, execute the following command:

.. code-block :: text
   
   sunbeam prepare-node-script | bash -x && newgrp snap_daemon

This command will:

* ensure all required software dependencies are installed, including the ``openssh-server``,
* configure passwordless access to the ``sudo`` command for all terminal commands for the
  currently logged in user (i.e. ``NOPASSWD:ALL``).

Alternatively, you can let Sunbeam generate a script that you can further review and execute
step by step:

.. code-block :: text

   sunbeam prepare-node-script

Bootstrap the cloud
-------------------

To bootstrap the cloud, execute the following command:

.. code-block :: text

   sunbeam cluster bootstrap --role control,compute,storage

This will assign all roles (``control``, ``compute``, ``storage``) to the machine by default.
You can use the ``--role`` switch to narrow them down. See the Architecture section for more
details.

.. TODO: Add a link to the Architecture section

When prompted, answer some interactive questions. Below is a sample output from the *cloud-1*
machine from the example configuration:

.. TODO: Add a link to the Example configuration seciton

.. code-block :: text

   Management network (172.16.1.0/24): 172.16.1.0/24
   Use proxy to access external network resources? [y/n] (n): n
   Enter a region name (cannot be changed later) (RegionOne): RegionOne
   OpenStack APIs IP ranges (172.16.1.201-172.16.1.240): 172.16.1.201-172.16.1.240
   Ceph devices (/dev/disk/by-id/wwn-0x500a0751e86b8eee): /dev/sdb

You can also refer to the Interactive configuration prompts section for detailed description of
each of those questions and some examples.

.. TODO: Add a link to the Interactive configuration prompts section

Also note that answers to all those questions can be automated with the use of a Deployment
manifest.

.. TODO: Add a link to the Deployment manifest section

One finished, you should be able to see the following message on your screen:

.. code-block :: text

   Node has been bootstrapped with roles: storage, compute, control

Configure the cloud
-------------------

Finally, configure the cloud for sample usage:

.. TODO: text

   sunbeam configure

Unless directed otherwise, this command will create sample project and user account. You can use
the ``--openrc`` switch to automatically generate an OpenStack RC file for this user (e.g.
``--openrc my-openrc``).

When prompted, answer some interactive questions. Below is a sample output from the *cloud-1*
machine from the example configuration:

.. TODO: Add a link to the Example configuration seciton

.. code-block :: text

   Local or remote access to VMs [local/remote] (local): remote
   External network (172.16.2.0/24): 172.16.2.0/24
   External network's gateway (172.16.2.1): 172.16.2.1
   External network's allocation range (172.16.2.2-172.16.2.254): 172.16.2.2-172.16.2.254
   External network's type  [flat/vlan] (flat): flat
   Populate OpenStack cloud with demo user, default images, flavors etc [y/n] (y): y
   Username to use for access to OpenStack (demo): demo
   Password to use for access to OpenStack (IY********): 
   Project network (192.168.0.0/24): 192.168.0.0/24
   Project network's nameservers (172.16.1.11 8.8.8.8 172.16.1.1 192.168.2.22 172.16.1.14): 8.8.8.8
   Enable ping and SSH access to instances? [y/n] (y): y
   External network's interface [eno2] (eno2): eno2

You can also refer to the Interactive configuration prompts section for detailed description of
each of those questions and some examples.

.. TODO: Add a link to the Interactive configuration prompts section

Also note that answers to all those questions can be automated with the use of a Deployment
manifest.

.. TODO: Add a link to the Deployment manifest section

One finished, you should be able to see the following message on your screen:

.. code-block :: text

   The cloud has been configured for sample usage.
   You can start using the OpenStack client or access the OpenStack dashboard at http://172.16.1.203:80/openstack-horizon

Note that the IP address of the OpenStack dashboard (here ``172.16.1.203``) might be different
in your environment.

Related how-to guides
+++++++++++++++++++++

Now that Canonical OpenStack is installed, you might want to check out the following how-to guides:

* Using the OpenStack dashboard
* Using the OpenStack client
* Scaling the cluster out

.. TODO: Add links to the how-to guides listed above
