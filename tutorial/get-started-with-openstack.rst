Get started with OpenStack
##########################

Welcome!

This tutorial will guide you through deploying a `Canonical OpenStack`_ cloud and provisioning a VM in this cloud.

What you will build
+++++++++++++++++++

As a result of completing the tutorial, you will have a functioning single-node Canonical OpenStack cloud.
This cloud will be sufficient to complete all further tutorials in this documentation.

This tutorial intentionally limits OpenStack deployment to a single machine.
APIs and cloud resources provisioned during the tutorial
are accessible only from that machine.

.. note ::

   This tutorial is intended for learning purposes.
   To deploy a production-grade cloud, refer to detailed instructions in the :doc:`How-to Guides section </how-to/index>`.

Requirements
++++++++++++

To complete the tutorial, you need a single dedicated machine with the following configuration:

* 4+ core amd64 processor
* minimum of 16 GiB of RAM
* minimum of 100 GiB SSD storage on the ``rootfs`` partition
* a fresh installation of Ubuntu Desktop 24.04 LTS
* unlimited access to the Internet
* a spare unformatted disk for MicroCeph

You can also use a virtual machine instead, but you can expect some performance degradation in this case.

Deploy Canonical OpenStack
++++++++++++++++++++++++++

Canonical OpenStack can be deployed in four steps.
This tutorial guides you through these steps and explains their purpose.

Step 1: Install the OpenStack snap
----------------------------------

.. note ::

   **Duration:** 1 minute (depends on your Internet connection speed)

Log in to the machine used in this tutorial and run the following command to install the ``openstack`` snap:

.. code-block :: text
   
   sudo snap install openstack

The `OpenStack snap`_ includes ``sunbeam``, a deployment and operations tool that you will use to deploy a cloud and provision resources.

Step 2: Prepare the machine
---------------------------

.. note ::

   **Duration:** 1 minute

Run the following command to prepare the machine for bootstrapping a Canonical OpenStack cloud:

.. code-block :: text

   sunbeam prepare-node-script --bootstrap | bash -x && newgrp snap_daemon

Once the command completes, the machine is ready to bootstrap a cloud.

.. dropdown:: What happens during this step?

   The script generated and executed in the command above performs two actions:

   1. Installs all required software dependencies (including the ``openssh-server``).
   2. Configures passwordless access to the ``sudo`` command for the currently logged in user (i.e. ``NOPASSWD:ALL``).

   You can generate a script file and review the performed actions:

   .. code-block :: text

      sunbeam prepare-node-script --bootstrap


Step 3: Bootstrap the cloud
---------------------------

.. note ::

   **Duration:** 20 minutes (depends on your Internet connection speed)

Run the following command to bootstrap a Canonical OpenStack cloud on the machine:

.. code-block :: text

   sunbeam cluster bootstrap --accept-defaults --role control,compute,storage

Once this command completes, you will see the following message:

.. code-block :: text

   Node has been bootstrapped with roles: storage, control, compute

.. dropdown:: What happens during this step?

   During the bootstrap process, Sunbeam orchestrates the following actions:

   1. Installs `Canonical Kubernetes <https://ubuntu.com/kubernetes>`_ for the purpose of hosting
      cloud control functions.
   2. Installs `Canonical Juju`_ and bootstraps a Juju controller on top of Canonical Kubernetes.
   3. Installs and configures cloud control functions on top of Canonical Kubernetes.
   4. Installs the `OpenStack Hypervisor snap`_ and plugs it into cloud control services.
   5. Installs the `MicroCeph snap`_ and plugs it into cloud control services.

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

Run the following command to prepare the cloud for provisioning resources:

.. code-block :: text

   sunbeam configure --accept-defaults --openrc demo-openrc

Once the command completes, you will see the following message:

.. code-block :: text

   Writing openrc to demo-openrc ... done

.. dropdown:: What happens during this step?

   The cloud preparation command performs the following actions:

   1. Creates a ``demo`` user.
   2. Populates the cloud with common templates.
   3. Creates a sandbox project with basic configuration.

   .. note::

      You will further explore cloud configuration in the following tutorial: :doc:`On-board your users </tutorial/on-board-your-users>`.

Conclusion
----------

You now have a single-node Canonical OpenStack cloud that is ready to provision resources.
The node, deployed on your dedicated machine or VM, serves the control, compute, and storage roles.

Launch a VM
+++++++++++

.. note ::

   **Duration:** 1 minute (first VM launch always takes longer)

You can now provision a virtual machine on your Canonical OpenStack cloud using Sunbeam.

Execute the following command to provision a VM named "test":

.. code-block :: text

   sunbeam launch ubuntu --name test

Sample output:

.. code-block :: text
   
   Launching an OpenStack instance ...
   Access instance with `ssh -i /home/ubuntu/.config/openstack/sunbeam ubuntu@10.20.20.200`

.. note::

   You will further explore resource provisioning in the following tutorial:
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
