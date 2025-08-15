Inspecting the cluster
======================

Overview
--------

Sunbeam aims to remove the need for an operator to know all of the
technical detail about how to deploy an OpenStack cloud; however when
something does go wrong it’s important to be able to inspect the various
components in order to discover the nature of the problem.

Juju
----

Sunbeam makes extensive use of Juju to manage the components of the
OpenStack cloud across both the underlying nodes and on Kubernetes (see
Canonical Kubernetes).

Sunbeam uses two Juju models for managing the various components
deployed to create the OpenStack cloud.

Juju controller authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sunbeam uses a set of credentials for each node in the cluster for
access to the Juju controller. The authenticated session for each node
expires after 24 hours so to use the ``juju`` command directly it may be
necessary to re-authenticate.

Juju commands will prompt for a password once the session has expired -
the password for the node’s user can be found in
``${HOME}/snap/openstack/current/account.yaml``.

Alternatively the ``juju-login`` helper can be used to re-authenticate
with the Juju controller:

::

   sunbeam utils juju-login

Controller model
~~~~~~~~~~~~~~~~

The ``controller`` model contains the Canonical OpenStack components that are
placed directly on the nodes that make up the deployment. The status of
this model can be queried using the following command:

::

   juju status -m admin/controller

This should work from any node in the deployment

This model contains the application deployments for the Canonical K8s
(control role), MicroCeph (storage role) and OpenStack Hypervisor
(compute role) components of Canonical OpenStack.

Depending on the roles assigned to individual machines, a unit of each
of the applications should be present in the model.

The controller application is a special application that represents the
Juju controller.

OpenStack model
~~~~~~~~~~~~~~~

The ``openstack`` model contains all of the components of the OpenStack
Cloud that are deployed on top of Kubernetes (provided by Canonical K8s
from the ``controller`` model).

The status of this model can be queried using the following command:

::

   juju status -m openstack

This should work from any node in the deployment.

.. caution::
   If the storage role is not specified for any nodes in the deployment the
   ``cinder-ceph`` application will remain in a blocked state. This is expected
   and means that the deployed OpenStack cloud does not support the block storage
   service.

OpenStack Hypervisor
--------------------

The OpenStack Hypervisor is a snap based component that provides all of
the core functionality needed to operate a hypervisor as part of an
OpenStack Cloud. This include Nova Compute, Libvirt+QEMU for hardware
based virtualization, OVN and OVS for software defined networking and
supporting services to provide metadata to instances.

The status of the snap’s services can be checked using:

::

   sudo systemctl status snap.openstack-hypervisor.*

All log output for the services can be captured by consulting the
journal:

::

   sudo journalctl -xe -u snap.openstack-hypervisor.*

This component is deployed and integrated into the cloud using the
``openstack-hypervisor`` charm that is deployed in the ``controller``
model.

Canonical Kubernetes
--------------------

Canonical Kubernetes (K8s) provides Kubernetes as part of Canonical OpenStack.

The current status of the K8s cluster can be checked by running:

::

   sudo k8s status

A more in-depth inspection and generation of a archive suitable for use
as part of a bug submission can also be completed by running:

::

   sudo k8s inspect

Services hosted on Canonical Kubernetes
---------------------------------------

Components of OpenStack Control Plane are hosted on K8S.

You can get the different units by running:

::

   sudo k8s kubectl get pods --namespace openstack

If a pod is in an error state, or is stuck in a ``Pending`` state, you
can retrieve more information on it and events related to it by running:

::

   sudo k8s kubectl describe --namespace openstack pod <pod_name>

To fetch the logs of a specific unit on K8S, it is necessary to
know the name of the containers running inside a given pod. To get the
names of the containers:

::

   sudo k8s kubectl get pod --namespace openstack -o jsonpath="{.spec.containers[*].name}" <pod_name>

A Juju unit will always have a ``charm`` container running the Juju
agent responsible for running the charm. To fetch logs associated with
the charm of a particular unit:

::

   sudo k8s kubectl logs --namespace openstack --container charm <pod_name>

.. note::
   The charm container logs are also available through ``juju debug-log -m openstack``,
   and will be present in the sunbeam inspection report.

To fetch the payload logs, use:

::

   sudo k8s kubectl logs --namespace openstack --container <container_name> <pod_name>

MicroCeph
---------

If nodes are deployed with the storage role enabled, MicroCeph will be
deployed as part of the cluster.

The status of MicroCeph can be checked using:

::

   sudo microceph status

and the status of the Ceph cluster can be displayed using:

::

   sudo ceph -s

Sunbeam MicroCluster
--------------------

Sunbeam MicroCluster provides some basic cluster coordination and state
sharing services as part of Canonical OpenStack. The status of the nodes
participating in the Sunbeam MicroCluster can be queried using the
following command:

::

   sunbeam cluster list

The state of the local daemon managing the nodes participation in the
cluster can also be checked and the log output captured if need be:

.. code:: text

   sudo systemctl status snap.openstack.clusterd.service
   sudo journalctl -xe -u snap.openstack.clusterd.service

Terraform plans
-----------------------

Sunbeam makes extensive use of Terraform to deploy OpenStack. In some
rare cases a Terraform plan can stay locked making it impossible to
re-run commands on the bootstrap node or add new nodes to the
deployment.

To list the current lock state of all Terraform plans:

::

   sunbeam plans list

To unlock a specific Terraform plan:

::

   sunbeam plans unlock <plan_name>

This command may prompt you to confirm unlocking depending on how recent
the lock timestamp is.

.. caution::
   Ensure that there are no administrative operations underway in the
   deployment when unlocking a Terraform plan. Otherwise, the deployment’s
   integrity can be compromised.

Docker registry timeouts
--------------------------

While bootstrapping the controller on Kubernetes, the Sunbeam default
bootstrap configuration uses `docker.io` for pulling images. If the pods
fail to pull images, use the following `ghcr.io` registry configuration
in the custom manifest file, as shown below:

::

   core:
   software:
     juju:
       bootstrap_args:
         - --config
         - caas-image-repo=ghcr.io/juju

.. caution::
   Ensure that the above configuration is added to the full manifest.

Use the above manifest as:

::

   sunbeam cluster bootstrap --manifest <name-of-the-file>
