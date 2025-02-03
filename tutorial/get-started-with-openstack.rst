Get started with OpenStack
##########################

Welcome!

If you are here, this likely means that you decided to give `Canonical OpenStack`_ a try. You might have heard from various sources that OpenStack is a complex piece of software. And you know what? This is true. OpenStack is complex for some very good reasons. However, you should also be aware that with the use of a proper tooling its complexity can be fully tamed.

In this tutorial we will show you how to get started with Canonical OpenStack in a few simple steps. We will walk you through its installation and configuration processes and get your first VM running on top of it. You will only need one machine for this purpose and around 30 minutes to spare.

Ready for the adventure? Let's explore OpenStack together!

.. note ::

   This tutorial is intended to serve for learning purposes only. If you've looking for detailed instructions on how to deploy a production-grade cloud, please refer to the How-to Guides section of this documentation instead.

.. TODO: Add a link to the "How-to guides" section

Requirements
++++++++++++

You will only need one dedicated physical machine with:

* 4+ core amd64 processor
* minimum of 16 GiB of RAM
* minimum of 50 GiB SSD storage on the ``rootfs`` partition
* fresh Ubuntu Desktop 24.04 LTS installed
* unlimited access to the Internet

.. TODO: Update once https://warthogs.atlassian.net/browse/OPEN-2486 is completed

.. TODO: TO be updated to Ubuntu Desktop 24.04 LTS once the re-base is complete

You can also use a virtual machine instead, but you can expect some performance degradation in this case.

.. warning ::

   All terminal commands used in this series of tutorials are run from the aforementioned machine. All web browser examples presented in this series of tutorials are run from the aforementioned machine. Neither OpenStack APIs nor any of the provisioned cloud resources, including VMs and floating IPs will be accessible from any other machine in your network than the aforementioned one. Everything runs on that machine. But it runs and it works!

Deploy Canonical OpenStack
++++++++++++++++++++++++++

.. note ::

   **Duration:** 1 minute (exact time might vary depending on your Internet connection speed)

Canonical OpenStack can be deployed for sample usage in four simple steps. Once you continue your journey with Canonical OpenStack and move forward with some more advanced scenarios you will find out that those steps are present in every single deployment procedure regardless of the cloud architecture and the bare metal provider being used. Thus, it is worth spending some time learning what exactly happens in each of those steps. Obviously, in more advanced scenarios, the exact procedure might vary slightly and some additional steps might be required.

Install the snap
----------------

We are going to start with installing the `OpenStack snap`_. The ``openstack`` snap includes the
``sunbeam`` command which we'll further use to bootstrap the cloud and to operate it
post-deployment. Sunbeam acts like a high-level interface to Canonical OpenStack, effectively
abstracting its complexity from operators.

To install the ``openstack`` snap, execute the following terminal command:

.. code-block :: text
   
   sudo snap install openstack

Prepare the machine
-------------------

.. note ::

   **Duration:** 1 minute

Before we'll be able to bootstrap the cloud, we have to prepare the machine for Canonical OpenStack usage. This process includes:

* ensuring all required software dependencies are installed, including the ``openssh-server``,
* configuring passwordless access to the ``sudo`` command for all terminal commands for the currently logged in user (i.e. ``NOPASSWD:ALL``).

In order to facilitate this process, Sunbeam can generate a script that you can further review
and execute step by step:

.. code-block :: text
   
   sunbeam prepare-node-script

However, if you simply want to execute all those commands at once, you can also pipe them directly to Bash instead:

.. code-block :: text
   
   sunbeam prepare-node-script | bash -x && newgrp snap_daemon

Bootstrap the cloud
-------------------

.. note ::

   **Duration:** 20 minutes (exact time might vary depending on your Internet connection speed)

Now, once the machine is ready for Canonical OpenStack usage, we can bootstrap the cloud on top of
it. Even though triggered by a single command, the overall process is relatively complex and takes
a while to complete. In principle, Sunbeam orchestrates the following actions in the background:

* Installs `Canonical Kubernetes <https://ubuntu.com/kubernetes>`_ for the purpose of hosting
  cloud control functions,
* Installs `Canonical Juju`_ and bootstraps a Juju controller on top of Canonical Kubernetes,
* Installs and configures cloud control functions on top of Canonical Kubernetes,
* Installs the `OpenStack Hypervisor snap`_ and plugs it into cloud control services,
* Installs the `MicroCeph snap`_ and plugs it into cloud control services.

To bootstrap the cloud for sample usage, execute the following command:

.. code-block :: text
   
   sunbeam cluster bootstrap --accept-defaults --role control,compute,storage

Once it completes, you should be able to see the following message on your screen:

.. code-block :: text
   
   Node has been bootstrapped with roles: storage, control, compute

Configure the cloud
-------------------

.. note ::

   **Duration:** 2 minutes (exact time might vary depending on your Internet connection speed)

At this point your Canonical OpenStack installation is already up and running. However, to be able to demonstrate its capabilities, we have to prepare the cloud for sample use. This includes creating a ``demo`` user, populating the cloud with some common templates and creating a sandbox project with some basic configuration where we'll be able to provision resources.

We will explore in another tutorial how this process usually looks like under the hood. However, for the time being we're simply going to let Sunbeam handle that.

.. TODO: Add a link to the tutorial III

To configure the cloud for sample usage, execute the following command:

.. code-block :: text
   
   sunbeam configure --accept-defaults --openrc demo-openrc

Once it completes, you should be able to see the following message on your screen:

.. code-block :: text

   Writing openrc to demo-openrc ... done

Launch a VM
+++++++++++

.. note ::

   **Duration:** 1 minute (first VM launch always takes longer)

The best way to verify whether Canonical OpenStack has been deployed successfully is to try to launch a VM on top of it. We will explore in another tutorial how this process usually looks like under the hood. However, for the time being we're simply going to let Sunbeam handle that.

.. TODO: Add a link to the tutorial II

In order to launch a test VM, execute the following command:

.. code-block :: text
   
   sunbeam launch ubuntu --name test

Sample output:

.. code-block :: text
   
   Launching an OpenStack instance ...
   Access instance with `ssh -i /home/ubuntu/snap/openstack/584/sunbeam ubuntu@10.20.20.94`

.. TODO: Update once https://bugs.launchpad.net/snap-openstack/+bug/2045266 is solved

You should now be able to connect to your VM over SSH using the provided command:

.. code-block :: text
   
   ssh -i /home/ubuntu/.config/openstack/sunbeam ubuntu@10.20.20.200

That's it. You're now connected to the VM. You can use regular shell commands to execute various tasks:

.. code-block :: text
   
   $ uptime
   10:54:29 up 1 min,  1 user,  load average: 0.00, 0.00, 0.00

To disconnect from the VM, type ``exit`` or press CTRL+D instead.

Next steps
++++++++++

Congratulations!

You have reached the end of this tutorial.

You can now:

* Move to the next tutorial in this series - "Get familiar with OpenStack",
* Explore How-to Guides for instructions on setting up a production-grade environment.

.. TODO: Add a link to the tutorial II
.. TODO: Add a link to the How-to guides section
