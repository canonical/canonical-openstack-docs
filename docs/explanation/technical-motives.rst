Technical motives
=================

This page describes the technical motivations behind Canonical OpenStack 
(based on Sunbeam), a second generation of Canonical's commercial OpenStack
product, with `Canonical OpenStack (based on OpenStack Charms), aka Charmed
OpenStack <https://docs.openstack.org/charm-guide/latest/>`__ being the
first generation.

The last decade
---------------

Over the last ten years, the OpenStack Charms project has developed a
successful and proven set of tooling using `Juju <https://juju.is/>`__
in conjunction with `MAAS <https://maas.io/>`__ and
`LXD <https://linuxcontainers.org/lxd/>`__ to deploy and operate
OpenStack for both public and private cloud deployments.

However, this solution has not proven to be a good fit for smaller
footprint deployments due to the infrastructure overheads of Juju and
MAAS.

This set of use cases is the target for the first release of Canonical
OpenStack, which has provided a beta-grade solution for single and small
multi-node deployments without incurring the overheads of Juju and MAAS.
However, it compromises by not having the same set of operational semantics as
an OpenStack charm deployed cloud.

Technology evolution
--------------------

As expected, technology has evolved over the same period of time.

The new paradigm for managing applications in the form of
`Kubernetes <https://kubernetes.io/>`__ (K8S) has proven itself as a
production-grade solution. Juju has also grown to support deploying and
managing applications on K8S using Charms (Charmed K8S Operators). The
image-based approach that K8S brings results in fully repeatable
deployment and faster, more reliable upgrades.

Ubuntu has introduced the concept of
`Snap <https://snapcraft.io/about>`__ packages, which provide an
image-based approach for deploying applications directly to servers with
full sandboxing, fast upgrades, and rollback in the event of upgrade
failure.

A reflection point
------------------

How can we leverage the features of the evolved technology around us to
improve the experience of deploying and operating OpenStack, while
ensuring we can support all use cases - from a single node running in a
virtual machine on a developer’s laptop to large deployments of
thousands of physical servers in data centers?

The majority of the OpenStack Control Plane (API and RPC services, Web
Apps, Databases) is a great candidate for deployment and operation on
Kubernetes. However, hypervisor and storage components are not; they are
still best placed directly onto the bare metal.

By using Juju and Charmed Operators to manage both K8S and machine
deployment components, and making use of a concept called cross-model
relations, we can apply the same set of operational semantics that have
proven so useful in the OpenStack Charms to manage a hybrid
container/machine-based deployment. This approach leverages the
image-based approach of both K8S and Snaps to improve repeatability and
speed of upgrades.

Sunbeam
-------

Sunbeam is the project that provides the core set of technology in the
form of Charmed Operators, Snaps, and OCI containers of OpenStack
components. These can be assembled into small single and multi-node
deployments with lightweight overheads or used with platforms such as
MAAS to enable fully automated deployment of large-scale OpenStack
clouds.
