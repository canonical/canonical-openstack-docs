Scaling the cluster out
#######################

Canonical OpenStack scales out, meaning that you can add more machines to the cluster if you need more resources or if you're designing the cloud for high availability.

Make sure you get familiar with the following sections before proceeding with any instructions listed below:

* Architecture
* Design considerations
* Enterprise requirements
* Sample configuration

.. TODO: Add links to all the pages listed above

Scaling the cluster out using the manual bare metal provider
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The following section provides instructions on scaling the cluster out with the manual bare metal provider.

Requirements
------------

You will need:

* Canonical OpenStack already installed using the manual bare metal provider
* one dedicated physical machine with:

  * hardware specifications matching minimum hardware specifications as documented under the Enterprise requirements section
  * fresh Ubuntu Server 24.04 LTS installed

.. TODO: Add links to the "Install Canonical OpenStack using the manual bare metal provider" how-to guide and the Enterprise requirements section

.. TODO: TO be updated to Ubuntu Server 24.04 LTS once the re-base is complete

If you can't provide an unlimited access to the Internet, see the Manage a proxied environment section.

.. TODO: Add a link to the Manage a proxied environment section

Create a registration token
---------------------------

.. warning ::

   Clustering does not support base hostnames. Nodes are only recognised by their **FQDNs**.

A registration token has to be created first for the other machine to be able to join the existing Canonical OpenStack cluster.

In order to create a registration token for the new machine, execute the ``sunbeam cluster add`` command on the first machine in the cluster (aka primary node):

.. code-block :: text

   sunbeam cluster add FQDN --output FILE

``FQDN`` is a fully qualified domain name (FQDN) of the machine being added.

``FILE`` is a name of the file where to save the registration token.

For example, to create a registration token for the *cloud-2* machine from the example configuration section, execute the following command on the *cloud-1* machine:

.. TODO: Add a link to the Example configuration section

.. code-block :: text

   sunbeam cluster add cloud-2.example.com --output cloud-2.asc

Sample output:

.. code-block :: text

   Token written to file: /home/ubuntu/cloud-2.asc

Copy the file with the token (here ``cloud-2.asc``) to the machine that you want to add to the cluster.

Provision the new machine
-------------------------

Switch to the machine that you want to add and proceed with the provisioning procedure described below.

Install the snap
^^^^^^^^^^^^^^^^

First, install the ``openstack`` snap:

.. code-block :: text

   sudo snap install openstack

This will install the latest stable version by default. You can use the ``--channel`` switch to install a different version of OpenStack instead. All machines in the cluster must have the same version of OpenStack installed.

Prepare the machine
^^^^^^^^^^^^^^^^^^^

To prepare the machine for Canonical OpenStack usage, execute the following command:

.. code-block :: text

   sunbeam prepare-node-script | bash -x && newgrp snap_daemon

This command will:

* ensure all required software dependencies are installed, including the ``openssh-server``,
* configure passwordless access to the ``sudo`` command for all terminal commands for the currently logged in user (i.e. ``NOPASSWD:ALL``).

Add the machine to the cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to add the machine to the cluster, execute the ``sunbeam cluster join`` command on that machine

.. code-block :: text

   cat FILE | sunbeam cluster join --role ROLES -

``FILE`` is a name of the file with the registration token.

``ROLES``` is a comma-separated list of roles (``control``, ``compute``, ``storage``) to assign to the machine being added.

For example, to add the *cloud-2* machine from the example configuration section, execute the following command:

.. TODO: Add a link to the Example configuration section

.. code-block :: text

   cat cloud-2.asc | sunbeam cluster join --role control,compute,storage -

One finished, you should be able to see the following message on your screen:

.. code-block :: text

   Node joined cluster with roles: storage, control, compute

Resize the cluster
------------------

When provisioning new machines with the ``control`` role assigned, the cluster needs to be resized to make use of those machines for the purpose of hosting control functions.

To resize the cluster, execute the following command on any of the machines:

.. code-block :: text

   sunbeam cluster resize

Scaling the cluster out using Canonical MAAS
++++++++++++++++++++++++++++++++++++++++++++

The following section provides instructions on scaling the cluster out with Canonical MAAS.

.. NOTE: To scale the cluster out, re-run the `sunbeam cluster deploy` command

Requirements
------------

You will need:

* Canonical OpenStack already installed using Canonical MAAS
* one dedicated physical machine:

  * with hardware specifications matching minimum hardware specifications as documented under the Enterprise requirements section
  * ready to be used by MAAS (enlisted, commissioned, configured and tagged)

.. TODO: Add links to the "Install Canonical OpenStack using the manual bare metal provider" how-to guide and the Enterprise requirements section

Provision the new machine
-------------------------

To provision the machine, execute the following command on the first *Sunbeam Client* machine (aka primary node):

.. code-block :: text

   sunbeam cluster deploy
