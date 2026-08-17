Identity and access
========================================

Canonical OpenStack relies on several distinct identity and authorization systems, not one. Keystone controls access to
OpenStack resources, but the systems that deploy, host, and provision that deployment, Juju, Kubernetes, MAAS, Ubuntu
hosts, storage platforms, and hardware-management interfaces, each authenticate and authorize access on their own terms.

This page explains how those systems relate. It covers how OpenStack identity is structured, how it differs from the
identities used to operate the infrastructure beneath it, and what that means for administrative access and credential
security. It builds on the planes introduced in :doc:`security-architecture-and-trust-model`.

Identity domains in Canonical OpenStack
------------------------------------------------------------------------

Different security planes rely on different identity systems. OpenStack identities are primarily mediated by Keystone
and OpenStack service policy, and they authorize access to cloud resources through the API. Deployment and orchestration
systems, Juju and Kubernetes, have their own administrative identities and authorization models that OpenStack policy
has no visibility into.

Hosts have operating-system identities and privileges of their own. Storage platforms can have administrative identities
separate from the OpenStack-facing storage API. Hardware-management interfaces have their own credentials and
authorization, independent of everything above them.

Exactly which of these systems are present, and how they're configured, depends on the deployment. Not every deployment
uses external identity integration, Vault, or every optional feature described below.

.. list-table:: Identity domains in Canonical OpenStack
   :header-rows: 1

   * - Identity domain
     - Examples
     - Typical authority
   * - OpenStack
     - Keystone users, groups, service identities
     - Cloud resources and APIs
   * - Deployment
     - Juju, Kubernetes
     - Application deployment and configuration
   * - Provisioning
     - MAAS
     - Machine lifecycle
   * - Host
     - Ubuntu accounts, root
     - Operating system and workload environment
   * - Storage
     - Storage administrative identities
     - Storage systems and tenant data paths
   * - Hardware
     - BMC/IPMI/Redfish identities
     - Machine power and hardware control

OpenStack identity
------------------------------------------------------------------------

Users and groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Keystone represents human and automated actors as users, and users can be organized into groups for easier role
assignment. A user's identity can come from Keystone's own backend or from an external source, an LDAP directory or a
federated provider, both covered later in this page.

Service accounts used for inter-service communication are also modeled as Keystone users. The next section treats them
separately because they play a different role in the security model than a person logging in to manage their own
resources.

Projects and domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Projects are the primary resource-ownership boundary in OpenStack. VMs, volumes, and networks belong to a project, and
most role assignments are scoped to one. Domains group projects and users under a shared administrative and namespace
boundary, and they're the mechanism used to attach an external identity source, an LDAP directory or a federated IdP, to
a distinct part of the user base.

Project separation restricts how resources are organized and who can act on them by default, but it isn't a complete
isolation boundary on its own. :doc:`security-architecture-and-trust-model` covers where project-level controls stop and
infrastructure-level trust takes over.

Roles, scope, and policy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What an identity can actually do depends on the combination of the roles it holds, the scope those roles are assigned
at, and the service policy that interprets them. A role by itself grants nothing. It only has an effect within the
project, domain, or system scope it's assigned to, and only for the operations the relevant service's policy maps to
that role.

Canonical OpenStack's role assignments can be scoped to a project, a domain, or the system as a whole.
:doc:`/explanation/baremetal-nodes` shows a concrete example of a system-scoped role in practice, where accessing the
Ironic API requires a role assigned at system scope rather than within a single project.

Exact role names and policy defaults follow upstream OpenStack for the deployed release. Where a deployment customizes
policy or role definitions, that configuration determines actual authority more precisely than any general description
can.

Administrative access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An OpenStack cloud administrator holds broad authority within the OpenStack service plane, altering resource policy,
quotas, user assignments, and domain integrations through the supported APIs. That authority is still bounded by what
the API and its policy model expose.

This is a different privilege domain from deployment, host, storage, or hardware administration.
:doc:`security-architecture-and-trust-model` covers why an OpenStack cloud administrator is not necessarily the
highest-privilege operator in a deployment.

Service identities
------------------------------------------------------------------------

OpenStack services authenticate to each other as themselves, not as the tenants whose requests they're processing. Nova,
Neutron, Cinder, and the other services use their own service identities and credentials to call internal APIs, and
those identities are typically Keystone users in a dedicated services project rather than personal accounts.

A concrete example is Barbican's secret-decryption role. Canonical OpenStack grants the ``secret-decrypter`` role to the
Masakari service user by default, so that instance recovery can rebuild servers with encrypted disks without a human
operator's involvement. That role is scoped to the services project and can be audited or removed with the standard
``openstack role`` commands.

Service credentials are provisioned by the deployment system rather than created by hand. Canonical OpenStack doesn't
publish the exact storage or rotation mechanism for every service credential, so treat that detail as
deployment-specific rather than assuming a single universal implementation.

Compromise of a service identity can have broader consequences than compromise of an ordinary tenant identity, because a
service identity's access is often wider than any one tenant's and because other services trust it implicitly. The
Masakari example above illustrates why. A service identity with decrypt access, if compromised, could expose data that
individual tenants can't otherwise reach directly.

External identity integration
------------------------------------------------------------------------

Canonical OpenStack supports two distinct ways to bring external identity into Keystone, LDAP integration and
federation.

LDAP integration maps an existing LDAP directory to a Keystone domain. Enabling it adds a domain backed by that
directory, and users authenticate with their existing LDAP credentials once the domain is configured.

Federation lets Keystone accept authentication from an external identity provider using OIDC or SAML2, currently
supporting configured providers such as Google, Okta, and Entra ID, a generic OIDC or SAML2 provider, or Canonical
Identity Platform. Both federation protocols require TLS on the redirect or metadata URL, which in practice means Vault
or another CA-backed TLS setup needs to be enabled first.

Adding an external provider only makes it available to Keystone. A cloud administrator still has to map incoming
federated identities to a domain, group, project, and role before a federated user has any access, using the same
domain, group, and role-assignment mechanisms as a locally created user. Authorization after that point works exactly as
it does for any other identity. Keystone roles, scope, and service policy decide what the identity can do.

Where multi-factor authentication applies to a federated login, it's enforced by the external identity provider or by
Canonical Identity Platform before the assertion ever reaches Keystone. Canonical OpenStack does not implement MFA
itself.

External identity integration changes where a human's credentials live and how sign-in works. It doesn't change
infrastructure identity. A user authenticated through a federated IdP still has no inherent access to Juju, host
accounts, or hardware-management interfaces unless that access is separately and explicitly granted.

Infrastructure and orchestration identities
------------------------------------------------------------------------

Juju
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Juju users are added to a controller and granted a permission level, such as ``superuser``, that determines what they
can do across the models that controller manages. This is entirely separate from any OpenStack role. A Juju controller
identity governs the deployment and lifecycle of the applications that implement OpenStack, not the OpenStack API
surface itself.

Whoever holds sufficient Juju controller access can change application configuration, relations, and placement across
every model on that controller, including the ones running Canonical OpenStack's control plane. That reach is why
:doc:`security-architecture-and-trust-model` treats deployment administration as a distinct, more powerful privilege
domain than OpenStack cloud administration.

Kubernetes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The OpenStack control-plane services run as workloads on a Canonical Kubernetes cluster. In this deployment model,
cluster-administrative access is obtained through host-level access, running ``k8s kubectl`` with root privileges on a
control-plane node, rather than through a separately documented Kubernetes user-identity system exposed to operators.

That means Kubernetes administrative access is, in practice, tied closely to host administration on the nodes running
the cluster. Anyone with root on a control node can reach every workload the cluster hosts, including the charmed
OpenStack services, which is one reason host administration is treated as its own high-privilege domain rather than as a
subset of OpenStack administration.

MAAS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sunbeam authenticates to MAAS using an API key, supplied when a MAAS-backed deployment is registered. That key is a MAAS
credential, unrelated to Keystone, and it's what lets Sunbeam and Juju provision and manage machines through MAAS.

MAAS itself uses hardware-management interfaces, BMC, IPMI, or Redfish, to carry out machine lifecycle operations such
as power control and OS deployment. MAAS is not itself the hardware-management identity system. It's a consumer of those
credentials, which are a separate identity domain in their own right.

Vault
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Where Vault is deployed, it maintains its own credentials and policies, independent of Keystone. Initializing Vault
produces a root token and a set of unseal keys, and the charm is authorized to act on the cloud's behalf using that root
token, not an OpenStack or Juju credential.

Vault administration is one of the most security-sensitive identity domains in a deployment that uses it, since Vault
can hold the secrets and certificates other services rely on. Access to Vault's root token or a sufficiently privileged
Vault policy is a different, and generally higher-consequence, privilege than any OpenStack role. Vault isn't present in
every deployment. Where it isn't enabled, the certificate and secret-management responsibilities it would otherwise
carry fall to whatever CA or secret-management approach the deployment uses instead.

Host, storage, and hardware identities
------------------------------------------------------------------------

Host access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ubuntu hosts have their own local accounts, typically reached over SSH, and root or sudo access on a host is a distinct
identity from anything in Keystone. Host administrative access can affect any workload or service running on that host,
OpenStack or otherwise, regardless of what OpenStack role, if any, the person holds.

This page doesn't cover how to secure SSH or host accounts. That belongs with host and infrastructure hardening.

Storage administration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Storage platforms can maintain administrative identities that are separate from the OpenStack-facing storage API. Where
Ceph is used, this means there's a distinction between the Cinder or Glance access a tenant or OpenStack service uses to
consume storage, and direct administrative access to the Ceph cluster itself.

Not every supported storage backend necessarily uses the same identity model, so the specifics depend on which backend a
deployment uses.

Hardware management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BMC, IPMI, and Redfish credentials authenticate directly to a machine's management controller, independent of the
operating system, MAAS, or OpenStack. These credentials appear in more than one place in a deployment. MAAS uses them to
control the cloud's own physical nodes, and where the baremetal feature is enabled, Ironic can be configured with
per-node BMC credentials to provision bare-metal instances on behalf of tenants.

Either way, hardware-management identities operate outside every layer of OpenStack authorization.

Credential types and application access
------------------------------------------------------------------------

An operator will encounter several different kinds of credentials across a deployment, and they don't carry the same
weight. Human users typically authenticate with a password, or with whatever mechanism an external identity provider
issues. Keystone then exchanges that authentication for a scoped token used for subsequent API calls.

OpenStack also supports application credentials, a Keystone mechanism that lets a user create a separate, restricted
credential for an application or script rather than sharing their own token or password. An application credential can
be scoped more narrowly than the user who created it and revoked independently, without affecting that user's own
access. Horizon exposes application credentials as their own resource type alongside users, groups, and roles.

Service credentials, discussed above, authenticate services to each other rather than a human or application to the API.
Infrastructure administrative credentials, Juju controller access, Vault tokens, MAAS API keys, host SSH keys, and
hardware-management credentials, are a different category again. They don't go through Keystone at all, and their
compromise has consequences outside the OpenStack authorization model entirely.

Certificates and keys used for TLS and service trust are covered in more detail in the Cryptography, certificates, and
secrets page.

Privileged access
------------------------------------------------------------------------

Privileged identities exist at every layer described on this page, an OpenStack cloud administrator, a Juju controller
superuser, a host root account, a Vault root token holder, and each deserves handling proportionate to what it can
reach.

Narrow assignment matters more than broad delegation. Giving an identity only the role, scope, or permission level it
actually needs limits what a compromised credential can do, and it makes the set of people or systems capable of a given
action small enough to reason about.

Individual accountability matters too. Shared administrative accounts, whether an OpenStack admin login or a Juju
controller credential used by more than one person, make it difficult to attribute an action to a specific operator
after the fact. Where emergency or break-glass access is needed, it should still be traceable to whoever used it, even
if the credential itself is normally locked away. Canonical OpenStack doesn't provide a specific break-glass or
privileged-access-management implementation of its own. How emergency access is handled is an operational decision for
the deployment.

Automation and service identities deserve the same discipline as human privileged accounts. An automation credential
with administrative reach is just as consequential as a human administrator's, and it should be scoped, monitored, and
audited the same way.

Identity lifecycle
------------------------------------------------------------------------

An identity's security doesn't end once it's created. Provisioning, role assignment, credential issuance, role changes,
and eventual revocation or removal all affect how much standing access exists in a deployment at any given time.

Unused identities and stale role assignments are a common source of unnecessary exposure. A former project member who
still holds a role, or a service credential left over from a disabled feature, is access that no longer serves a purpose
but can still be used if compromised.

External identity federation moves some of this lifecycle to the identity provider. Account creation, deactivation, and
credential rotation for a federated user typically happen in the enterprise IdP rather than in Keystone directly. What
federation doesn't remove is the cloud-side half of the work. Role assignments, project membership, and policy still
need periodic review on the OpenStack side, since a deactivated IdP account doesn't automatically revoke roles that were
already assigned in Keystone.

Canonical OpenStack doesn't currently document an automated credential-rotation or identity-cleanup mechanism that
operates across all these identity domains at once. Where rotation or cleanup is required, it's handled per system, in
Keystone, in Juju, in Vault, and so on, rather than centrally.

Separation of human and service identities
------------------------------------------------------------------------

Humans generally shouldn't use service identities for day-to-day work, and automation generally shouldn't run under a
personal administrator's credentials. Mixing the two makes it harder to tell, after the fact, whether a given action
came from a person or from a script, and it ties a service's ongoing operation to one person's account lifecycle.

Keeping identities scoped to their actual purpose also makes credential rotation more practical. A service credential
can be rotated on its own schedule without disrupting anyone's personal access, and a person's access can be revoked
without breaking automation that depends on a separate service identity.

This is an operational practice that Canonical OpenStack's identity model supports, not a technical restriction the
platform enforces on its own.

Related topics
------------------------------------------------------------------------

This page is intended to be read alongside the other security explanations in this documentation set.

.. TODO: link these as :doc: references once the target pages exist.

* :doc:`security-in-canonical-openstack`
* :doc:`security-architecture-and-trust-model`
* Network security
* Cryptography, certificates, and secrets
* Workload and data protection
* Host, operations, and infrastructure security
* Harden your Canonical OpenStack deployment
