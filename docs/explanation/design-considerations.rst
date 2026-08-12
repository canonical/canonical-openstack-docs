Design considerations
=====================

There are a few design considerations that need to be taken into account before proceeding with Canonical OpenStack deployment. Understanding them and adjusting the design to fit individual requirements helps avoid costly changes at further stages of the project.

Network architecture
++++++++++++++++++++

In general, Canonical OpenStack is agnostic to the underlying network architecture. However, the best price-performance can be achieved by using as few tiers as possible. The most typical scenarios include a one-tier architecture and a two-tier architecture (aka Spine-Leaf).

Network traffic segregation
+++++++++++++++++++++++++++

Canonical OpenStack requires at least two physical networks to function properly:

* **External** – used to provide an inbound (south) access to virtual machines (VMs) running on top of OpenStack through the mechanism of floating IPs, and outbound (north) access from instances to networks outside of OpenStack.
* **Generic** – used for any other purposes (machine provisioning, machine management, providing access to OpenStack APIs, etc.).

Customers can optionally use more physical networks or VLANs to further segregate network traffic when using Canonical MAAS as a :ref:`bare metal provider<Bare metal provider>`. Network traffic isolation with MAAS is handled through the concept of network spaces and :doc:`space mappings </explanation/network-traffic-isolation-with-maas>`.

Cloud architecture
++++++++++++++++++

Canonical OpenStack supports the following cloud architectures:

* **Hyper-Converged** – each machine (aka Cloud node) in the cluster hosts governance, control, compute & network and storage functions.
* **Converged** – each machine (aka Cloud node) in the cluster hosts control, compute & network and storage functions, while dedicated machines (aka Governor nodes) exist to host governance functions.
* **Fully-Disaggregated** – dedicated machines (aka Governor, Control, Compute & Network and Storage nodes) exist to host individual cloud functions.
* **Disaggregated** – some functions (e.g. compute & network and storage) are co-hosted, while dedicated machines exist to host remaining cloud functions.

Control, compute, network and storage function assignment is modeled through the concept of roles which are assigned during the initial deployment or when adding new machines to an existing cluster.

.. _Bare metal provider:

Bare metal provider
+++++++++++++++++++

Canonical OpenStack can be deployed on top of the following bare metal providers:

* **Manual** – a human operator is responsible for the initial installation and configuration of all machines. The operator can still use a standalone Canonical MAAS instance or any other third-party bare metal provider to automate the provisioning process of those machines.
* **Canonical MAAS** – Canonical OpenStack relies on Canonical MAAS to provision all machines but Governor Nodes. The Governor nodes must be manually installed and configured by a human operator unless automated.

The decision on which bare metal provider to use must be taken at the design phase of the project. There is no way to transition from one provider to another once the deployment is completed.

Scale
+++++

It is important to understand what the size of the Canonical OpenStack is going to be at the deployment time and whether the cloud is expected to grow quickly in the foreseeable future as the scale has a direct impact on some design decisions.

The list of recommended options, depending on the scale, is shown in Tab. 1:

.. list-table :: Tab. 1. Recommended options depending on the scale.
   :widths: 15 25 30 20
   :header-rows: 1

   * - Scale
     - Network architecture
     - Cloud architecture
     - Bare metal provider
   * - Small (1-9)
     - One-Tier
     - Hyper-Converged
     - Manual
   * - Large (10+)
     - Two-Tier (aka Spine-Leaf)
     - Converged, Disaggregated or Fully-Disaggregated
     - Canonical MAAS

High availability
+++++++++++++++++

Canonical OpenStack can be deployed with or without high availability (HA). However, Canonical
recommends using HA to minimize service disruption and avoid data loss in the event of hardware
failure. At least 3 instances of every machine type are required for full HA regardless of the
cloud architecture being used.

Availability zones
++++++++++++++++++

Availability Zones (AZs) are an end-user visible logical abstraction for partitioning the cloud according to its underlying physical architecture. AZs provide segregation into failure domains, ensuring that any application deployed across multiple AZs can survive a failure of a single physical zone.

Regions
+++++++

Regions are general divisions of an OpenStack cloud with their own API endpoints and resources (compute, network and storage), while sharing the same identity records. The purpose of regions is to facilitate deployments of OpenStack across geographically distributed locations.

In general, Canonical recommends running several small clouds rather than one big cloud and using :ref:`third-party tools<Third-party software>`, such as a Cloud Platform Management (CPM) solution to manage them centrally.

See the :doc:`multi-region guide</how-to/misc/multiregion-deployments>` for more details.

Cells
+++++

Cells are OpenStack’s internal concept that enables cloud deployments on a large scale by sharding some of its internal components, such as databases and messaging queues.

In general, Canonical recommends running several small clouds rather than one big cloud and using :ref:`third-party tools<Third-party software>`, such as a Cloud Platform Management (CPM) solution to manage them centrally.

Hypervisor
++++++++++

Canonical OpenStack uses a virtualization stack consisting of QEMU, KVM and Libvirt as the only
available and supported option for running a hypervisor.

SDN
+++

Canonical OpenStack uses an Open Virtual Network (OVN) software-defined networking (SDN) platform as the only available and supported option.

Storage
+++++++

Canonical OpenStack uses Ceph software-defined storage (SDS) platform as the only available and supported option. Integrations with third-party storage platforms will be available soon.

Air-gapped and offline deployments
++++++++++++++++++++++++++++++++++

Canonical OpenStack can be deployed in an air-gapped mode by using an :doc:`external proxy
</how-to/misc/manage-a-proxied-environment>` to download all necessary artifacts
from the Internet. Fully offline deployments will be available soon.

.. _Third-party software:

Third-party software
++++++++++++++++++++

Since Canonical OpenStack is built using pure upstream open source projects, it can be easily integrated with various third-party software components as long as they support OpenStack APIs. Integrations with third-party software that requires low-level access to Canonical OpenStack internals are only possible under Canonical’s :ref:`consulting services<Commercial services>` for Canonical OpenStack.

.. _Commercial services:

Commercial services
+++++++++++++++++++

Even though project Sunbeam was launched to lower the barrier to entry for people with no
previous OpenStack background and fully revolutionize its operational experience, some
organizations might still struggle when figuring out the right design, deploying Canonical
OpenStack at scale, integrating it with third-party software and storage platforms, and operating
it post-deployment.

In response to those challenges, Canonical provides a wide variety of commercial services
available for enterprise customers. Those include:

* **Consulting** - design, delivery, integration and on-boarding services
* **Security** - expanded security maintenance (up to 12 years)
* **Support** - phone and ticket support with guaranteed SLAs
* **Firefighting** - managed-service-level support in high severity situations
* **Managed** - fully-managed cloud service
* **Training** - professional training courses

Please refer to the `product website <https://canonical.com/openstack>`_ for a detailed
description of Canonical’s commercial services for Canonical OpenStack.

Related sections
++++++++++++++++

* :doc:`Architecture</explanation/architecture>`
* :doc:`Enterprise requirements</reference/enterprise-requirements>`
