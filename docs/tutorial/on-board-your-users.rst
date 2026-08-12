On-board your users
###################

Welcome!

We hope you've had a great time so far exploring `Canonical OpenStack <https://canonical.com/openstack>`_. In the :doc:`previous tutorial</tutorial/get-familiar-with-openstack>` we learned how to use the OpenStack dashboard and the OpenStack client to interact with the cloud as both admin and a regular user, and how to provision cloud resources. Now that you're familiar with both tools, it's the highest time to start on-boarding your users.

In this tutorial we will demonstrate how to prepare Canonical OpenStack for your organization's
usage. We will show you how to create a new project from scratch, distribute credentials to your
colleagues and populate the cloud with some common templates used by your organization. Finally,
we will showcase how users can further customize their project according to their needs.

Ready to share OpenStack with your colleagues? Let's take it to the next level together!

.. note ::

   This tutorial is intended to serve for learning purposes only. If you're looking for detailed instructions on how to deploy a production-grade cloud, please refer to the :doc:`How-to Guides section</how-to/index>` of this documentation instead.

Requirements
++++++++++++

You will only need one dedicated physical machine with:

* Canonical OpenStack deployed according to instructions listed under the :doc:`"Get started with OpenStack"</tutorial/get-started-with-openstack>` tutorial,
* OpenStack dashboard and OpenStack client configured according to instructions listed under the :doc:`"Get familiar with OpenStack"</tutorial/get-familiar-with-openstack>` tutorial.

You can also use a virtual machine instead, but you can expect some performance degradation in this case.

.. warning ::

   All terminal commands used in this series of tutorials are run from the aforementioned machine. All web browser examples presented in this series of tutorials are run from the aforementioned machine. Neither OpenStack APIs nor any of the provisioned cloud resources, including VMs and floating IPs will be accessible from any other machine in your network than the aforementioned one. Everything runs on that machine. But it runs and it works!

Credentials
+++++++++++

Make sure you're logged in as the *admin* user and not as the *demo* user.

To log in as the *admin* user through the OpenStack client, execute the following command:

.. code-block :: text

   source <(sunbeam openrc)

To log in as the *admin* user through the OpenStack dashboard, refer to instructions under the :doc:`"Get familiar with OpenStack"</tutorial/get-familiar-with-openstack>` tutorial.

Populate OpenStack with templates
+++++++++++++++++++++++++++++++++

.. note ::

   **Duration:** 5 minutes

OpenStack uses the concept of `cloud images <https://docs.openstack.org/image-guide/>`_ which
serve as templates for virtual machines creation. They contain the guest OS and are customized by
`cloud-init <https://cloud-init.io/>`_ during the VM provisioning process. In this process,
various pre-defined or user-defined actions are handled in an automated way (for example,
cloud-init inserts public SSH keys of all authorized users).

The upstream community maintains an `list of repositories <https://docs.openstack
.org/image-guide/obtain-images.html>`_ from where users can download template images. For
example, the repository of Ubuntu cloud images is available
`here <https://cloud-images.ubuntu.com/>`__. However, users can also convert their existing
images when migrating to Canonical OpenStack from other virtualization platforms.

Converting images
-----------------

OpenStack uses qcow image format, meaning that any other images have to be converted first before
you'll be able to launch VMs. A typical use case here are VMware images which used VMDK format instead. In the following example we'll convert a VMDK image containing the Ubuntu 24.04 LTS OS that you can download from `here <https://cloud-images.ubuntu.com/daily/server/noble/current/noble-server-cloudimg-amd64.vmdk>`_.

To convert the image, first install the ``qemu-utils`` tool:

.. code-block :: text

   sudo apt update && sudo apt -y install qemu-utils

Then, use the tool to perform the actual conversion:

.. code-block :: text

   qemu-img convert -f vmdk -O qcow2 ~/Downloads/noble-server-cloudimg-amd64.vmdk ~/Downloads/noble.qcow2

Import the image through the OpenStack client
---------------------------------------------

To import the image, execute the following command:

.. code-block :: text

   openstack image create --disk-format qcow2 --min-disk 4 --min-ram 512 --file noble.qcow2 --public noble

To list all images, execute the following command:

.. code-block :: text

   openstack image list

Sample output:

.. code-block :: text

   +--------------------------------------+--------+--------+
   | ID                                   | Name   | Status |
   +--------------------------------------+--------+--------+
   | 6e2d8b2d-dea1-44e0-a95f-ab9fae22081d | noble  | active |
   | 5ebcdaf5-b594-4c12-836a-824ca88abaa8 | ubuntu | active |
   +--------------------------------------+--------+--------+

Import the image through the OpenStack dashboard
------------------------------------------------

Navigate to **Admin** → **Compute** → **Images** and click the **Create Image** button on the right:

.. figure:: images/on-board-your-users-01.png
   :align: center

To import the image, fill in the form as follows:

* **Image Name** - Type *noble*
* **File** - Click Browse and find the *noble.qcow2* file in your *Downloads* directory
* **Format** - Select *QCOW2 - QEMU Emulator*
* **Minimum Disk (GB)** - Type *4*
* **Minimum RAM (MB)** - Type *512*
* **Visibility** - Select *Public*

Then click the **Create Image** button:

.. figure:: images/on-board-your-users-02.png
   :align: center

You should now able to see two images under the OpenStack dashboard:

.. figure:: images/on-board-your-users-03.png
   :align: center

Set up a new project
++++++++++++++++++++

.. note ::

   **Duration:** 5 minutes

OpenStack is multi-tenant by default, meaning that more than one user can use the platform at
the time without having an access to other users' resources, impacting their work in any way or
even noticing their existence. Multi-tenancy is provided through the concept of domains and
projects which are an abstraction used by other OpenStack services to group and isolate various
types of resources (e.g. VMs).

In turn, authentication and authorization functions are handled through the concept of users,
groups and roles. Even though we're going to use the default database backend in this tutorial,
organizations can also plug their Canonical OpenStack into an enterprise identity and access
management system, such as :doc:`LDAP</how-to/features/ldap>`.

In the following example we'll create a new project and a user under the *users* domain, assign
a *member* role to this user, and demonstrate how to distribute the newly created users'
credentials to your colleagues so that they could also start their journey with Canonical OpenStack.

Create necessary records
------------------------

To create a new project called *myproject*, execute the following command:

.. code-block :: text

   openstack project create --domain users myproject

To create a new user called *myuser* with the *mypassword* password, execute the following command:

.. code-block :: text

   openstack user create --domain users --password mypassword myuser

Lastly, to assign the *member* role to this user, execute the following command:

.. code-block :: text

   openstack role add --project myproject --project-domain users --user myuser --user-domain users member

You could obviously use the OpenStack dashboard for this purpose too, but thing about all the users you have to on-board now. It's usually smarter and faster to use the client when performing administrative operations at scale.

Distribute credentials to your users
------------------------------------

At this point your colleagues should be able to log in to the dashboard using the following credentials:

* **User Name**: *myuser*
* **Password**: *mypassword*
* **Domain**: *users*

.. figure:: images/on-board-your-users-04.png
   :align: center

However, to interact with the cloud through the client, they are first going to need an OpenStack RC file. The OpenStack RC file contains all necessary environmental variables that enable a remote client to connect to the cloud. We've been setting those variables with the ``source`` command in previous examples in these tutorials.

To download the RC file for the *myuser* user, navigate to the *myuser* drop-down menu on the top right, click it, and then select **OpenStack RC File**:

.. figure:: images/on-board-your-users-05.png
   :align: center

The RC file can now be sourced to interact with the cloud as the *myuser* user:

.. code-block :: text

   $ source ~/Downloads/myproject-openrc.sh
   Please enter your OpenStack Password for project myproject as user myuser:
   $ openstack project list
   +----------------------------------+-----------+
   | ID                               | Name      |
   +----------------------------------+-----------+
   | 9fbd66cff2ed4fb18a488cb168339849 | myproject |
   +----------------------------------+-----------+

Make sure you type ``mypassword`` when asked for the *myuser* user's password.

Configure the project
+++++++++++++++++++++

.. note ::

   **Duration:** 10 minutes

Now that your colleagues have got their own account created and that they have got their own project to work with, they can start provisioning cloud resources. However, to be able to launch VMs, the project has to be configured first.

In previous tutorials we used the ``sunbeam configure`` command to configure the *demo* project for sample usage. In the following steps we're going to see how this process looks like in detail under the hood.

We will use OpenStack client for this purpose. However, all those actions can also be executed through the dashboard. We will also use *myuser* user's credentials. However, all those actions could also be performed by the *admin* user.

Create a key pair
-----------------

Key pairs are used to provide an access to VMs over SSH. Your users can either upload their existing public SSH key or create a new key pair instead.

To create a key pair called *mykeypair*, execute the following command:

.. code-block :: text

   openstack keypair create --type ssh --private-key myprivatekey.pem mykeypair

The private key is now saved in the ``myprivatekey.pem`` file:

.. code-block :: text

   $ cat myprivatekey.pem
   -----BEGIN OPENSSH PRIVATE KEY-----
   b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZWQyNTUx
   OQAAACB2i1S1y1htYNl3KV+TZCgjvnEOhhv32vXNl66D+lhRqgAAAIiv8FXSr/BV0gAAAAtzc2gt
   ZWQyNTUxOQAAACB2i1S1y1htYNl3KV+TZCgjvnEOhhv32vXNl66D+lhRqgAAAECEWPKBt9pTqtpk
   uS/pDCwnUHRmu/5PdrGKHmuyqJjXo3aLVLXLWG1g2XcpX5NkKCO+cQ6GG/fa9c2XroP6WFGqAAAA
   AAECAwQF
   -----END OPENSSH PRIVATE KEY-----

To narrow down permissions to this file so that we could use it later, execute the following command:

.. code-block :: text

   chmod 0600 myprivatekey.pem

Create a project network
------------------------

Project networks are virtual networks that provide an inter-VM communication for tenant's workloads running inside of the project. Those networks and their subnets are not routable outside of the OpenStack environment. Your users can use the concept of :ref:`floating IPs<floatingips>` to provide an access to their VMs instead.

To create a project network called *mynetwork*, execute the following command:

.. code-block :: text

   openstack network create mynetwork

Then, to create a sample subnet on this network called *mysubnet*, execute the following command:

.. code-block :: text

   openstack subnet create --network mynetwork --subnet-range 192.168.0.0/24 --allocation-pool start=192.168.0.2,end=192.168.0.254 --dns-nameserver 8.8.8.8 mysubnet

Connect the project network to the external network
---------------------------------------------------

By default newly created project networks are not connected to any other networks. This means that VMs attached to the *mysubnet* subnet would be able to communicate with each other, but not with the host. To enable this communication we have to create a virtual router.

To create a router called *myrouter*, execute the following command:

.. code-block :: text

   openstack router create myrouter

Then, to attach the *mysubnet* subnet to this router, execute the following command:

.. code-block :: text

   openstack router add subnet myrouter mysubnet

Lastly, we have to attach the *external-network* network to this router and configure the router to use it as its gateway.

.. code-block :: text

   openstack router set --external-gateway external-network myrouter

The *external-network* network is the external network that is attached to the host. It was
created automatically by Sunbeam during the Canonical OpenStack deployment.

.. _floatingips:

Allocate floating IPs
---------------------

Floating IPs are used to provide a remote access to VMs running in the project. They are allocated from the external network's subnet and attached to VMs after they get launched. The traffic is NATed by the router so you can think of them as a pool of public IPs that you get from your ISP.

To allocate floating IP, execute the following command:

.. code-block :: text

   openstack floating ip create external-network

Allow inbound traffic
---------------------

OpenStack uses the concept of security groups to manage inbound and outbound network traffic. Those serve as virtual firewalls enforcing ACLs against incoming and outgoing network connections.

By default newly create projects would only have the *default* security group defined. However,
this group doesn't allow inbound SSH connections out of the box.

To allow inbound SSH traffic under the *default* security group, execute the following command:

.. code-block :: text

   openstack security group rule create --remote-ip 0.0.0.0/0 --dst-port 22:22 --protocol tcp --ingress default

Launch a VM
-----------

At this point your colleagues should be able to launch VMs in the *myproject* project.

To launch a VM with the following configuration:

* **Name**: myinstance,
* **Image**: noble,
* **Flavor**: m1.small,
* **Network**: mynetwork,
* **Key pair**: mykeypair,

execute the following command:

.. code-block :: text

   openstack server create --image noble --flavor m1.small --network mynetwork --key-name mykeypair myinstance

Then, to associate the floating IP with this instance that we allocated in the previous step, execute the following commands:

.. code-block :: text

   IP=$(openstack floating ip list | awk '/None/ { print $4 }')
   openstack server add floating ip myinstance $IP

To connect to this instance over SSH, execute the following command:

.. code-block :: text

   ssh -i myprivatekey.pem ubuntu@$IP

To disconnect, type ``exit`` or press CTRL+D instead.

Finally, go to the OpenStack dashboard and navigate to **Project** → **Network** → **Network Topology**. You should be able to see both network, the router between them and the newly created VM attached to the *mynetwork* network.

.. figure:: images/on-board-your-users-06.png
   :align: center

To terminate the *myinstance* VM, execute the following command:

.. code-block :: text

   openstack server delete myinstance

To release the floating IP, execute the following command:

.. code-block :: text

   openstack floating ip delete $IP 

Next steps
++++++++++

Congratulations!

You have reached the end of this tutorial.

You can now:

* Move to the next tutorial in this series - :doc:`"Explore full potential of OpenStack"</tutorial/explore-full-potential-of-openstack>`,
* Explore :doc:`How-to Guides</how-to/index>` for instructions on setting up a production-grade environment.
