Get started with OpenStack
##########################

Welcome!

If you are here, this likely means that you decided to give `Canonical OpenStack`_ a try. You might have heard from various sources that OpenStack is a complex piece of software. And you know what? This is true. OpenStack is complex for some very good reasons. However, you should also be aware that with the use of a proper tooling its complexity can be fully tamed.

In this tutorial we will show you how to get started with Canonical OpenStack in a few simple steps. We will walk you through its installation and configuration processes and get your first VM running on top of it. You will only need one machine for this purpose and around 30 minutes to spare.

Ready for the adventure? Let's explore OpenStack together!

.. note ::

   This tutorial is intended to serve for learning purposes only. If you've looking for detailed instructions on how to deploy a production-grade cloud, please refer to the :doc:`How-to Guides section</how-to/index>` of this documentation instead.

Requirements
++++++++++++

You will only need one dedicated physical machine with:

* 4+ core amd64 processor
* minimum of 16 GiB of RAM
* minimum of 100 GiB SSD storage on the ``rootfs`` partition
* fresh Ubuntu Desktop 24.04 LTS installed
* unlimited access to the Internet
* spare un-formatted disk for MicroCeph

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

.. literalinclude:: snippets/get-started-with-openstack.task.sh
   :language: bash
   :start-after: [docs-view:installation]
   :end-before:  [docs-view:installation-end]

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

   sunbeam prepare-node-script --bootstrap

However, if you simply want to execute all those commands at once, you can also pipe them directly to Bash instead:

.. literalinclude:: snippets/get-started-with-openstack.task.sh
   :language: bash
   :start-after: [docs-view:prepare-node-script]
   :end-before:  [docs-view:prepare-node-script-end]

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

.. literalinclude:: snippets/get-started-with-openstack.task.sh
   :language: bash
   :start-after: [docs-view:bootstrap]
   :end-before:  [docs-view:bootstrap-end]

.. important::

   Bootstrapping may fail if the ``rootfs`` partition does not have sufficient
   available storage, or if there is no free, un-partitioned disk for MicroCeph.
   If any issue is encountered, consult the :doc:`Troubleshooting guide </how-to/troubleshooting/inspecting-the-cluster>`.

Once it completes, you should be able to see the following message on your screen:

.. code-block :: text

   Node has been bootstrapped with roles: storage, control, compute

.. note ::

   Sunbeam uses a set of credentials for access to the Juju controller. The
   authenticated session expires after 24 hours. You can re-authenticate by
   running:

   .. code-block :: text

        sunbeam utils juju-login

Configure the cloud
-------------------

.. note ::

   **Duration:** 2 minutes (exact time might vary depending on your Internet connection speed)

At this point your Canonical OpenStack installation is already up and running. However, to be able to demonstrate its capabilities, we have to prepare the cloud for sample use. This includes creating a ``demo`` user, populating the cloud with some common templates and creating a sandbox project with some basic configuration where we'll be able to provision resources.

We will explore in :doc:`another tutorial</tutorial/on-board-your-users>` how this process usually looks like under the hood. However, for the time being we're simply going to let Sunbeam handle that.

To configure the cloud for sample usage, execute the following command:

.. literalinclude:: snippets/get-started-with-openstack.task.sh
   :language: bash
   :start-after: [docs-view:configure]
   :end-before:  [docs-view:configure-end]

Once it completes, you should be able to see the following message on your screen:

.. code-block :: text

   Writing openrc to demo-openrc ... done

Launch a VM
+++++++++++

.. note ::

   **Duration:** 1 minute (first VM launch always takes longer)

The best way to verify whether Canonical OpenStack has been deployed successfully is to try to launch a VM on top of it. We will explore in :doc:`another tutorial</tutorial/get-familiar-with-openstack>` how this process usually looks like under the hood. However, for the time being we're simply going to let Sunbeam handle that.

In order to launch a test VM, execute the following command:

.. literalinclude:: snippets/get-started-with-openstack.task.sh
   :language: bash
   :start-after: [docs-view:launch]
   :end-before:  [docs-view:launch-end]

Sample output:

.. code-block :: text

   Launching an OpenStack instance ...
   Access instance with `ssh -i /home/ubuntu/snap/openstack/584/sunbeam ubuntu@10.20.20.94`

.. TODO: Update once https://bugs.launchpad.net/snap-openstack/+bug/2045266 is solved

You should now be able to connect to your VM over SSH using the provided command:

.. literalinclude:: snippets/get-started-with-openstack.task.sh
   :language: bash
   :start-after: [docs-view:ssh]
   :end-before:  [docs-view:ssh-end]

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

* Move to the next tutorial in this series - :doc:`"Get familiar with OpenStack"</tutorial/get-familiar-with-openstack>`,
* If you need to clean up the node and start over, you can check :doc:`how to remove the node </how-to/operations/removing-the-primary-node>`,
* Explore :doc:`How-to Guides</how-to/index>` for instructions on setting up a production-grade environment.
