Manifest file reference
=======================

This resource aims to provide a definitive structure of a deployment
manifest file will all its supported keys.

.. note::
   The manifest file is currently only supported in channel ``2023.2/edge`` of
   the **openstack** snap.

.. tip::
   For a conceptual overview of manifests, see the :doc:`Deployment manifest
   </explanation/deployment-manifest>` page.

.. code:: yaml

   deployment:

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
     
     addons:
       # MetalLB address allocation ranges
       metallb: <a.a.a.a-b.b.b.b>,<c,c,c,c-d.d.d.d>,...
       # Example:
       # metallb: 10.20.21.10-10.20.21.20

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

     # TLS
     certificates:
       <CSR x500UniqueIdentifier>:
         # Base64 encoded certificate for unit CSR Unique ID: subject
         certificate: <Base64 encoded certificate>

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
       #   channel: 2023.2/candidate
       # glance-k8s:
       #   channel: 2023.2/candidate
       #   revision: 66
       #   config:
       #     debug: true
       #     pool-type: replicated

     terraform:
       <plan>:
         source: <path-to-file>
       # Example:
       # hypervisor-plan:
       #   source: /home/ubuntu/deploy-openstack-hypervisor
