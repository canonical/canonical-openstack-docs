Security in Canonical OpenStack
================================

Canonical OpenStack is a layered system consisting of Ubuntu, Juju, MAAS, Kubernetes, Ceph, and upstream OpenStack
services combined to form a deployable cloud platform. No single layer secures the entire cloud. Cloud security depends
on the design of the deployment, the network layout, the operator's configuration choices, and the security of the
surrounding infrastructure, as much as on the product itself.

This page orients the reader to that security model before the more detailed topics covered elsewhere in this
documentation set, in particular :doc:`security-architecture-and-trust-model`.

Shared responsibility
--------------------------------------------------------------------

Canonical OpenStack provides security controls as a product, but many critical protections depend on how the cloud is
installed and operated.

Controls provided by Canonical OpenStack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Canonical OpenStack organizes deployments around governance, control-plane, compute and networking, and storage
functions, deployed and operated through a combination of charms, rocks, and snaps on Ubuntu. Depending on the chosen
cloud architecture, from hyper-converged to fully disaggregated, these functions can share machines or run on dedicated
nodes. See :doc:`architecture` and :doc:`design-considerations` for the available topologies.

Canonical OpenStack also provides several security capabilities.

* network traffic isolation through MAAS spaces and Sunbeam cloud-network mappings, with the degree of isolation set by
  how many subnets and spaces the cloud architect defines
* optional TLS protection for service endpoints through Traefik, with either an external CA or Vault-based CA flow
* an optional Vault feature for secret management and certificate issuance
* optional Barbican secret management for OpenStack services and workloads
* external identity integration with LDAP and federation providers such as OIDC and SAML2 through Keystone
* audit logging for most OpenStack API services in CADF format
* Ubuntu Pro support for extended security maintenance and Livepatch support where enabled

None of these capabilities alone constitutes a complete security baseline. Each addresses a specific part of the
security model, and the overall posture depends on how they are combined and configured.

Controls that require operator configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many security outcomes are determined by operator choices. Deployments can be configured with different network
topologies, feature sets, and security-sensitive settings. Examples include the following.

* whether to isolate traffic on different MAAS spaces and subnets
* whether to enable TLS for public and internal endpoints
* whether to enable Vault, Barbican, or external federation
* whether to enable Ubuntu Pro and which services to attach
* how identity providers are connected and what roles are assigned to users or service accounts
* how MAAS machine tags, reserved IP ranges, and network assignment are set up
* what network and security-group policies are applied to tenants

Canonical OpenStack provides the primitives. The operator decides which ones to enable and how they are placed in the
deployment architecture.

Infrastructure and tenant responsibilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Canonical OpenStack depends on infrastructure outside the OpenStack control plane itself, MAAS, Juju, Kubernetes, and
the Ubuntu hosts underneath it, and its overall security depends on the security of those systems and the administrative
access used to manage them. An OpenStack administrator is not necessarily the highest-privilege operator in a
deployment. Access to MAAS, Juju, Kubernetes, hosts, storage administration, Vault, or hardware-management interfaces
can have a larger impact than ordinary OpenStack role assignments. :doc:`security-architecture-and-trust-model` covers
this in detail.

Tenant security remains a tenant concern. Canonical OpenStack provides network and identity primitives, but protecting
workloads, guest images, application configuration, access keys, and project-level network policy still depends on how
the tenant uses the platform.

Trust boundaries and privilege
--------------------------------------------------------------------

A production deployment is best understood as several layers, from physical hardware and Ubuntu hosts, through the
Sunbeam, Juju, and Kubernetes orchestration layer, to the OpenStack control plane and tenant workloads, each with its
own trust assumptions and administrative boundary. Privilege at the infrastructure layers, MAAS, Juju, Kubernetes, host
access, storage administration, and hardware management, can affect the cloud in ways ordinary OpenStack role
assignments cannot reach. :doc:`security-architecture-and-trust-model` walks through these boundaries and privilege
relationships in detail.

Security principles
--------------------------------------------------------------------

A secure production deployment follows several recurring principles.

* restrict access to the minimum roles, network paths, and credentials needed, including the Vault secret-decryption
  role
* separate hardware, host, orchestration, control-plane, and workload layers so no single control carries the whole
  burden
* isolate management, internal, public, storage, and data traffic on distinct networks
* authenticate through Keystone, backed by LDAP or OIDC/SAML2 federation where configured
* apply TLS to service endpoints where enabled, keeping in mind that endpoint TLS is a separate capability from
  data-at-rest encryption
* rely on CADF audit logging and the Ubuntu and Ubuntu Pro maintenance lifecycle for operational visibility and timely
  patching

Production security posture
--------------------------------------------------------------------

A well-secured deployment has clear separation between public API access, internal service traffic, management traffic,
and tenant data, documented identity sources, explicit service roles, and an operating model that keeps deployment
orchestration separate from tenant usage.

This page is not a hardening checklist. The forthcoming hardening guide covers the operational controls, network policy,
service exposure, patching, and role assignment, specific to a given deployment.

Security capabilities and limitations
--------------------------------------------------------------------

Canonical OpenStack provides network segmentation, service API TLS, Vault-backed secrets and certificates, external
identity support, security groups and floating IP handling, API auditing, and Ubuntu Pro/ESM support as part of its
security posture.

Some protections stay outside the product boundary and remain the infrastructure operator's responsibility. Host
hardening, BMC/IPMI/Redfish hardening, and data-at-rest encryption across all storage and backup paths depend on how the
surrounding infrastructure is built and operated. Canonical OpenStack does not make CIS-compliance, STIG-compliance, or
FIPS-validation claims.

Related security topics
--------------------------------------------------------------------

For more detailed information, refer to the following topic areas.

.. TODO: link these as :doc: references once the target pages exist.

* :doc:`security-architecture-and-trust-model`
* Identity and access
* Network security
* Cryptography, certificates, and secrets
* Workload and data protection
* Host, operations, and infrastructure security
* Harden your Canonical OpenStack deployment

These pages are complementary views of the same deployment model. Product controls, operational responsibilities, and
infrastructure dependencies all matter together.

Canonical OpenStack provides a strong foundation for secure cloud operations, but its security posture depends on the
correct design and operation of the surrounding architecture.
