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

       # Use local network proxy to access external resources
       proxy:
         proxy_required: [true,false]
         # Proxy variables to use if 'true' is chosen above
         http_proxy: <url>:<port>
         https_proxy: <url>:<port>
         no_proxy: <host>,<host>,...

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
