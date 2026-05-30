Get started with OpenStack
##########################

Welcome!

If you are here, this likely means that you decided to give `Canonical OpenStack`_ a try.
It's complex software that you can fully tame with the right tools.

This tutorial will help you get started with Canonical OpenStack in a few steps.
It will guide you through installing Canonical OpenStack, bootstrapping the cloud, and provisioning a VM.
To complete the tutorial, you need a single dedicated machine or VM and around 30 minutes to spare.

What you will build
+++++++++++++++++++

As a result of completing the tutorial, you will have a functioning single-node Canonical OpenStack cloud,
with the node serving the control, compute, and storage roles.
This cloud will be sufficient to complete all further tutorials in this documentation.
You will also understand the four key steps of each Canonical OpenStack deployment.

Ready for the adventure? Let's explore OpenStack together!

.. note ::

   This tutorial is intended to serve for learning purposes only.
   To deploy a production-grade cloud, refer to detailed instructions in the :doc:`How-to Guides section </how-to/index>`.

Requirements
++++++++++++

You need a dedicated physical machine with:

* 4+ core amd64 processor
* minimum of 16 GiB of RAM
* minimum of 100 GiB SSD storage on the ``rootfs`` partition
* a fresh installation of Ubuntu Desktop 24.04 LTS
* unlimited access to the Internet
* a spare unformatted disk for MicroCeph

You can also use a virtual machine instead, but you can expect some performance degradation in this case.

.. note ::

   This tutorial intentionally limits OpenStack deployment to a single machine.
   You will run all terminal commands and web browser examples from this machine,
   and it will not expose OpenStack APIs or any of the provisioned cloud resources
   (such as VMs and floating IPs) to your network.

   To learn about production-grade deployments, refer to :doc:`How-to Guides </how-to/index>`.


Deploy Canonical OpenStack
++++++++++++++++++++++++++

Canonical OpenStack can be deployed in four steps.
This tutorial will demonstrate these steps and their meaning without going into deep details.

Step 1: Install the OpenStack snap
----------------------------------

.. note ::

   **Duration:** 1 minute (depends on your Internet connection speed)

The `OpenStack snap`_ includes ``sunbeam``, a deployment and operations tool that you will use to deploy a cloud and provision resources.
Sunbeam acts as a high-level interface to Canonical OpenStack, effectively abstracting its complexity from operators.

To install the ``openstack`` snap, run the following terminal command:

.. code-block :: text
   
   sudo snap install openstack

Step 2: Prepare the machine
---------------------------

.. note ::

   **Duration:** 1 minute

You need to prepare the machine in order to bootstrap a Canonical OpenStack cloud.
This preparation includes two actions:

* ensure that all required software dependencies are installed, including the ``openssh-server``,
* configure passwordless access to the ``sudo`` command for all terminal commands for the currently logged in user (i.e. ``NOPASSWD:ALL``).

Sunbeam generates a script to facilitate this process.
You can pipe this script directly to Bash:

.. code-block :: text

   sunbeam prepare-node-script --bootstrap | bash -x && newgrp snap_daemon

.. note::

   You can also generate a script file to review and execute step-by-step:

   .. code-block :: text

      sunbeam prepare-node-script --bootstrap


Step 3: Bootstrap the cloud
---------------------------

.. note ::

   **Duration:** 20 minutes (depends on your Internet connection speed)

Once the machine is ready for Canonical OpenStack, you can bootstrap the cloud:

.. code-block :: text

   sunbeam cluster bootstrap --accept-defaults --role control,compute,storage

Once this command completes, you will see the following message:

.. code-block :: text

   Node has been bootstrapped with roles: storage, control, compute

During the bootstrap process, Sunbeam orchestrates the following actions:

* Installs `Canonical Kubernetes <https://ubuntu.com/kubernetes>`_ for the purpose of hosting
  cloud control functions,
* Installs `Canonical Juju`_ and bootstraps a Juju controller on top of Canonical Kubernetes,
* Installs and configures cloud control functions on top of Canonical Kubernetes,
* Installs the `OpenStack Hypervisor snap`_ and plugs it into cloud control services,
* Installs the `MicroCeph snap`_ and plugs it into cloud control services.

.. important::

   Bootstrapping may fail if the ``rootfs`` partition does not have sufficient
   available storage, or if there is no free, un-partitioned disk for MicroCeph.
   If any issue is encountered, consult the :doc:`Troubleshooting guide </how-to/troubleshooting/inspecting-the-cluster>`.

.. note ::

   Sunbeam uses a set of credentials for access to the Juju controller. The
   authenticated session expires after 24 hours. You can re-authenticate by
   running:

   .. code-block :: text

        sunbeam utils juju-login

Step 4: Configure the cloud
---------------------------

.. note ::

   **Duration:** 2 minutes (depends on your Internet connection speed)

Your Canonical OpenStack cloud is already up and running.
Now you need to prepare the cloud for provisioning sample resources (such as virtual machines) in a series of steps:

1. create a ``demo`` user;
2. populate the cloud with common templates;
3. create a sandbox project with basic configuration.

Use Sunbeam to handle these steps:

.. code-block :: text

   sunbeam configure --accept-defaults --openrc demo-openrc

Once the command completes, you will see the following message:

.. code-block :: text

   Writing openrc to demo-openrc ... done


.. hint::

   You will explore how cloud configuration works under the hood in the following tutorial: :doc:`On-board your users </tutorial/on-board-your-users>`.

Conclusion
----------

Your Canonical OpenStack cloud is now ready to provision resources.

Once you move forward with more advanced scenarios, you will see that each deployment procedure has these four steps,
regardless of the cloud architecture and the bare metal provider.

Launch a VM
+++++++++++

.. note ::

   **Duration:** 1 minute (first VM launch always takes longer)

Once you have a Canonical OpenStack cloud ready, you can provision a virtual machine on the cloud using Sunbeam.

To launch a test VM, execute the following command:

.. code-block :: text
   
   sunbeam launch ubuntu --name test

Sample output:

.. code-block :: text
   
   Launching an OpenStack instance ...
   Access instance with `ssh -i /home/ubuntu/.config/openstack/sunbeam ubuntu@10.20.20.200`

.. hint::

   You will explore how resource provisioning works under the hood in the following tutorial:
   :doc:`Get familiar with OpenStack </tutorial/get-familiar-with-openstack>`.

.. TODO: Update once https://bugs.launchpad.net/snap-openstack/+bug/2045266 is solved

Use the provided command to connect to the VM over SSH:

.. code-block :: text
   
   ssh -i /home/ubuntu/.config/openstack/sunbeam ubuntu@10.20.20.200

You can use regular shell commands to execute various tasks in the VM:

.. code-block :: text
   
   $ uptime
   10:54:29 up 1 min,  1 user,  load average: 0.00, 0.00, 0.00

To disconnect from the VM, type ``exit`` or press CTRL+D.

Next steps
++++++++++

Congratulations!
You have completed this tutorial.

Explore the next steps:

* Move to the next tutorial in this series: :doc:`Get familiar with OpenStack </tutorial/get-familiar-with-openstack>`.
* If you need to clean up and start the tutorial over, read :doc:`Removing the primary node </how-to/operations/removing-the-primary-node>`.
* Learn how to set up a production-grade environment from :doc:`How-to Guides </how-to/index>`.
