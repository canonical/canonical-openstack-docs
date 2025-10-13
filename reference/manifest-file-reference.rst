Manifest file reference
=======================

This resource aims to provide a definitive structure of a deployment
manifest file will all its supported keys.

.. tip::
   For a conceptual overview of manifests, see the :doc:`Deployment manifest
   </explanation/deployment-manifest>` page.

.. code:: yaml

   core:

     config:
       # The identity section allows the configuration of different
       # identity providers. At this point, this section configures OpenID Connect
       # and SAML2 keystone federated providers.
       identity:
         # The SAML2 Service Provider x509 certificate and key. When enabling any SAML2
         # IDP, this option becomes mandatory.
         saml2_x509:
           certificate: "/home/ubuntu/cert.pem"
           key: "/home/ubuntu/key.pem"
         # This section defines the providers we want to enable.
         profiles:
           # The name of the provider. This will be used as a provider ID when configured
           # in OpenStack.
           openid-example:
             # The provider type. There are several specific provider types and one generic
             # type.
             provider: entra | google | okta | canonical | generic
             # The federated identity protocol. The "canonical" provider type only supports
             # "openid" for now.
             protocol: openid | saml2
             # Configuration options for the above mentioned provider/protocol pair.
             config: {}
           # Examples:
           # entra-saml2:
           #   provider: entra
           #   protocol: saml2
           #   config:
           #     app-id: 82590875-2a9c-48cb-ba04-5125f0bed664
           #     microsoft-tenant: 86e92722-ba4c-4b8d-95f2-216e612a9bc3
           #     label: "Log in with Entra ID (SAML2)"
           # entra-openid:
           #   provider: entra
           #   protocol: openid
           #   config:
           #     client-id: "the-client-id-goes-here"
           #     client-secret: "super-secret-client-secret"
           #     microsoft-tenant: 86e92722-ba4c-4b8d-95f2-216e612a9bc3
           #     label: "Log in with Entra ID (OIDC)"
           # okta-saml2:
           #   provider: okta
           #   protocol: saml2
           #   config:
           #     app-id: app-id-goes-here
           #     okta-org: dev-123456
           #     label: "Log in with Okta (SAML2)"
           # okta-openid:
           #   provider: okta
           #   protocol: openid
           #   config:
           #     client-id: "the-client-id-goes-here"
           #     client-secret: "super-secret-client-secret"
           #     okta-org: dev-123456
           #     label: "Log in with Okta (OIDC)"
           # google-saml2:
           #   provider: google
           #   protocol: saml2
           #   config:
           #     app-id: 82590875-2a9c-48cb-ba04-5125f0bed664
           #     label: "Log in with Google (SAML2)"
           # google-openid:
           #   provider: google
           #   protocol: openid
           #   config:
           #     client-id: "the-client-id-goes-here"
           #     client-secret: "super-secret-client-secret"
           #     label: "Log in with Google (OIDC)"
           # canonical-openid:
           #   provider: canonical
           #   protocol: openid
           #   config:
           #     # This is the offer for the oauth endpoint of the hydra deployment
           #     # in canonical identity platform
           #     oauth-offer: "iam.controller/iam.hydra"
           #     # Optional: the offer for the CA certificate provider of the
           #     # canonical identity platform.
           #     cert-offer: iam.controller/iam.self-signed-certificates
           # generic-saml2:
           #   provider: generic
           #   protocol: saml2
           #   config:
           #     metadata-url: https://saml2.example.com/app/sso/saml/metadata
           #     # optional: The CA chain to validate the IDP.
           #     ca-chain: /path/to/ca-chain.pem
           #     label: "Log in with My-SAML2-IDP"
           # generic-openid:
           #   provider: generic
           #   protocol: openid
           #   config:
           #     client-id: "the-client-id-goes-here"
           #     client-secret: "super-secret-client-secret"
           #     issuer-url: https://oidc.example.com/.well-known/openid-configuration
           #     label: "Log in with My-OIDC-IDP"
       # Use local network proxy to access external resources
       proxy:
         proxy_required: [true,false]
         # Proxy variables to use if 'true' is chosen above
         http_proxy: <url>:<port>
         https_proxy: <url>:<port>
         no_proxy: <host>,<host>,...

       # Configure OVS DPDK datapath (userspace), improving network performance.
       dpdk:
         # If enabled, OVS bridges are configured to use the netdev (DPDK) datapath
         # instead of the standard system datapath.
         enabled: [true, false]
         # The number of CPU cores to allocate for OVS control plane processing.
         control_plane_cores: 1
         # The number of CPU cores to allocate for OVS data plane processing.
         dataplane_cores: 1
         # The amount of hugepage memory (MB) to reserve for OVS DPDK.
         memory: 1024
         # The DPDK compatible driver that will be assigned to physical
         # interfaces connected to the DPDK dapapath.
         driver: vfio-pci
         # A list of physical interfaces to use with DPDK for each node.
         #
         # The interfaces will be persistently bound to the configured DPDK
         # compatible driver, no longer being visible to the host.
         #
         # OVS bridges containing those interfaces (or bonds) are expected to
         # be defined through Netplan or MAAS. Canonical Openstack will move
         # the corresponding Netplan configuration to OVS, using the resulting
         # OVS DPDK physical ports.
         #
         # Example:
         # ports:
         #   r740-dc1-ceph.maas:
         #     - eno2
         #     - enp94s0
         ports:
           <host-fqdn>:
             - <iface1>
             - <iface2>

       # This section defines PCI passthrough configuration, allowing SR-IOV
       # VFs, GPUs and other PCI devices to be exposed to Openstack instances.
       pci:
         # A list of PCI filters specifying which devices to expose.
         # The specs can contain exact PCI addresses, address wildcards,
         # address regular expressions or vendor/product id tuples.
         # SR-IOV interfaces may also contain a Neutron physical network,
         # usually known as "physnet".
         #
         # See the Nova documentation for more details.
         # https://docs.openstack.org/nova/latest/configuration/config.html#pci.device_spec
         #
         # Note that the following list applies to all compute nodes, use
         # the "excluded_devices" field to define per-node exclusion lists.
         #
         # Example:
         # device_specs:
         #   - address: "0000:1b:00.0"
         #     vendor_id: "8086"
         #     product_id: "1563"
         #     physical_network: "physnet1"
         device_specs: []
         # Per-node PCI device exclusion list, containing excluded PCI addresses.
         #
         # Example:
         # excluded_devices:
         #   r740-dc1-ceph.maas:
         #     - "0000:19:00.0"
         #     - "0000:19:00.1"
         excluded_devices:
           <host-fqdn>:
             - <pci-addr1>
             - <pci-addr2>
         # A list of aliases that can be used to request PCI devices through
         # Nova flavor extra specs.
         #
         # See the Nova documentation for more details.
         # https://docs.openstack.org/nova/latest/configuration/config.html#pci.alias
         #
         # Example:
         # aliases:
         #   - vendor_id: "8086"
         #     product_id: "1565"
         #     device_type: type-VF
         #     name: "intel-vf"
         aliases: {}

       bootstrap:
         # Management networks shared by hosts
         management_cidr: <cidr>,<cidr>,...
         # Example:
         # management_cidr: 192.168.29.0/24

       # Enter database toplogy: single/multi (cannot be changed later)
       # This will configure number of databases, single for entire cluster or multiple databases with one per openstack service.
       database: single

       # Enter a region name (cannot be changed later)
       region: <region>
       # Example:
       # region: RegionOne

       k8s-addons:
         # Load balancer ranges
         loadbalancer: <cidr>,<cidr>,...

       user:
         # Populate OpenStack cloud with demo user, default images, flavors etc
         run_demo_setup: [true,false]
         # Username to use for access to OpenStack
         username: <username>
         # Password to use for access to OpenStack
         password: <password>
         # Network to use for initial project network
         cidr: <cidr>
         # Nameservers that guests should use for DNS resolution
         nameservers: <ip-address> <ip-address> ...
         # Enable ping and SSH access to instances
         security_group_rules: [true,false]
         # Local or remote access to VMs
         # Local mode - single node only
         remote_access_location: [local,remote]

       # External networking
       external_network:
         nic: <interface-name> # deprecated
         nics:
           <node-hostname>: <interface-name>
           # Examples:
           # sunbeam-1.localdomain: enp5s0
           # sunbeam-2.localdomain: enp8s0
           # sunbeam-3.localdomain: eno3
         # CIDR of OpenStack external network
         cidr: <cidr>
         # IP address of default gateway for external network
         gateway: <ip-address>
         # Start of IP allocation range
         start: <ip-address>
         # End of IP allocation range
         end: <ip-address>
         # Network type for access to external network
         network_type: [flat,vlan]
         # VLAN ID if 'vlan' is chosen above
         segmentation_id: <vlan-id>

       # MicroCeph
       microceph_config:
         # Disks to attach to MicroCeph nodes
         <node-hostname>:
           osd_devices: <device>,<device>,...
         # Examples:
         # sunbeam-1.localdomain:
         #   osd_devices: /dev/vdc,/dev/vdd
         # sunbeam-2.localdomain:
         #   osd_devices: /dev/vdc,/dev/vdd
         # sunbeam-3.localdomain:
         #   osd_devices: /dev/vdc,/dev/vdd

       traefik_endpoints:
         traefik: <traefik_external_hostname>
         traefik-public: <traefik_public_external_hostname>
         traefik-rgw: <traefik_rgw_external_hostname>

     software:

       juju:
         bootstrap_args:
         - <argument>
         - <argument>
         - ...
         # Examples:
         # - --debug
         # - --agent-version=3.2.4
         # - --model-default=test-mode=true
         # - --model-default=logging-config=<root>=INFO;unit=DEBUG

       charms:
         <charm>:
           channel: <channel>
           revision: <revision>
           config:
             <option>: <value>
             <option>: <value>
         ...
         ...
         # Examples:
         # keystone-k8s:
         #   channel: 2024.1/candidate
         # glance-k8s:
         #   channel: 2024.1/candidate
         #   revision: 66
         #   config:
         #     debug: true
         #     pool-type: replicated

         # Special cases

         # Configure mysql storage in single mysql scenario
         # mysql-k8s:
         #   storage:
         #     database: <value>

         # Configure mysql storage in multi mysql scenario
         # mysql-k8s:
         #   storage-map:
         #     keystone-k8s:
         #       database: <value>
         #     glance-k8s:
         #       database: <value>
         #     ...

         # Configure mysql configs in multi mysql scenario
         # mysql-k8s:
         #   config-map:
         #     keystone-k8s:
         #       <option>: <value>
         #     glance-k8s:
         #       <option>: <value>
         #     ...

         # Configure glance image repository for local storage
         # glance-k8s:
         #   storage:
         #     local-repository: <value>

       terraform:
         <plan>:
           source: <path-to-file>
         # Example:
         # hypervisor-plan:
         #   source: /home/ubuntu/deploy-openstack-hypervisor

   features:

     loadbalancer:
       config:
         <option>: <value>
       software:
         charms:
           <charm>:
             channel: <channel>
             revision: <revision>
             config:
               <option>: <value>
               <option>: <value>
           ...

     tls:
       ca:
         config:
           # TLS
           certificates:
             <CSR x500UniqueIdentifier>:
               # Base64 encoded certificate for unit CSR Unique ID: subject
               certificate: <Base64 encoded certificate>
       vault:
         config:
           # TLS
           certificates:
             <CSR x500UniqueIdentifier>:
               # Base64 encoded certificate for unit CSR Unique ID: subject
               certificate: <Base64 encoded certificate>
      ...
