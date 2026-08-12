Manage workloads with Juju
==========================

Once Canonical OpenStack has been deployed, you have the option of managing
workloads manually (i.e. via the ``openstack`` CLI) or with Juju. This
document shows how to set up the latter: How to manage OpenStack
workloads with Juju.

There is more than one way to proceed depending on your local networking
but in this document a bastion (jump host) will first be created. Juju
workloads will then be managed from that system.

.. tip::
   The :doc:`Images Sync </how-to/features/images-sync>` feature is a dependency of the Juju
   workload feature. Make sure to enable it.

Set up the bastion
------------------

The steps in this section are performed on any host that has already
installed the **openstack** snap. Generally, it would be the host that
you are using as a management client.

Create the bastion:

::

   sunbeam launch --name bastion

   Access instance with `ssh -i /home/ubuntu/snap/openstack/477/sunbeam ubuntu@10.20.30.188

Send the cloud init file that was generated during cloud deployment to
the bastion. This file provides normal user access to the cloud:

::

   scp -i /home/ubuntu/snap/openstack/current/sunbeam demo-openrc ubuntu@10.20.30.188:/home/ubuntu

Finally, log in to the bastion:

::

   ssh -i /home/ubuntu/snap/openstack/current/sunbeam ubuntu@10.20.30.188

Install and configure the Juju client
-------------------------------------

The steps in this section are performed on the bastion.

Install Juju:

::

   sudo snap install juju

Source the cloud init file that was recently transferred:

::

   source demo-openrc

Create the file ``clouds.yaml`` to define the existing cloud:

.. code:: yaml

   clouds:
     sunbeam:
       type: openstack
       auth-types: [userpass]
       regions:
         RegionOne:
           endpoint: $OS_AUTH_URL

Replace ``$OS_AUTH_URL`` with the value for your environment. It can be
queried in this way:

::

   echo $OS_AUTH_URL

Inform Juju about the cloud:

::

   juju add-cloud --client sunbeam ./clouds.yaml

Example output:

::

   Cloud "sunbeam" successfully added to your local client.
   You will need to add a credential for this cloud (`juju add-credential sunbeam`)
   before you can use it to bootstrap a controller (`juju bootstrap sunbeam`) or
   to create a model (`juju add-model <your model name> sunbeam`).

Create the file ``credentials.yaml`` to define your cloud credentials:

.. code:: yaml

   credentials:
     sunbeam:
       sunbeam-creds:
         auth-type: userpass
         username: $OS_USERNAME
         password: $OS_PASSWORD
         tenant-name: $OS_PROJECT_NAME
         project-domain-name: $OS_USER_DOMAIN_NAME
         user-domain-name: $OS_USER_DOMAIN_NAME
         version: "$OS_AUTH_VERSION"

Like before, you can query for the value of each variable. Note that the
value for ``version`` is in double quotes.

Add your credentials to Juju:

::

   juju add-credential sunbeam --client -f credentials.yaml

Example output:

::

   Credential "sunbeam-creds" added locally for cloud "sunbeam".

Create a Juju controller
------------------------

The steps in this section are also performed on the bastion.

Create a Juju controller, here named ``my-controller``:

::

   juju bootstrap sunbeam my-controller

End of example output:

::

   Running machine configuration script...
   Bootstrap agent now started
   Contacting Juju controller at 192.168.122.220 to verify accessibility...

   Bootstrap complete, controller "my-controller" is now available
   Controller machines are in the "controller" model

   Now you can run
           juju add-model <model-name>
   to create a new model to deploy workloads.

Deploy an application
---------------------

You can now use standard Juju practices to manage applications. See the
`Juju documentation <https://juju.is/docs/juju>`__ for help with Juju.

Below, we’ll create a model and add the ``ubuntu`` application to it.

::

   juju add-model my-model
   juju deploy ubuntu --base ubuntu@22.04

To inspect the model:

::

   juju status

Example output:

::

   Model     Controller     Cloud/Region       Version  SLA          Timestamp
   my-model  my-controller  sunbeam/RegionOne  3.4.2    unsupported  15:07:44Z

   App     Version  Status  Scale  Charm   Channel        Rev  Exposed  Message
   ubuntu  22.04    active      1  ubuntu  latest/stable   24  no

   Unit       Workload  Agent  Machine  Public address  Ports  Message
   ubuntu/0*  active    idle   0        192.168.122.52

   Machine  State    Address         Inst id                               Base          AZ    Message
   0        started  192.168.122.52  4c147f10-9f9e-449b-b58a-6b9534553e4a  ubuntu@22.04  nova  ACTIVE

Log out of the bastion in preparation for the next section:

::

   exit

Verify the OpenStack server instances
-------------------------------------

On the client host, via the ``openstack`` CLI, you can see the OpenStack
server instances that correspond to the workload machine, the Juju controller,
and the bastion (respectively, from top to bottom, in the output below):

::

   openstack server list

   +--------------------------------------+--------------------------+--------+-------------------------------------------+--------------------------------------------------------------+-----------+
   | ID                                   | Name                     | Status | Networks                                  | Image                                                        | Flavor    |
   +--------------------------------------+--------------------------+--------+-------------------------------------------+--------------------------------------------------------------+-----------+
   | 4c147f10-9f9e-449b-b58a-6b9534553e4a | juju-08056b-my-model-0   | ACTIVE | demo-network=192.168.122.52               | auto-sync/ubuntu-jammy-22.04-amd64-server-20240319-disk1.img | m1.small  |
   | e0b7858f-4529-442e-8440-b8fde6819347 | juju-8cf50d-controller-0 | ACTIVE | demo-network=192.168.122.220              | auto-sync/ubuntu-jammy-22.04-amd64-server-20240319-disk1.img | m1.medium |
   | ba8c4cfe-0e27-4471-9923-a7fbedf774c5 | bastion                  | ACTIVE | demo-network=10.20.30.188, 192.168.122.32 | ubuntu                                                       | m1.tiny   |
   +--------------------------------------+--------------------------+--------+-------------------------------------------+--------------------------------------------------------------+-----------+
