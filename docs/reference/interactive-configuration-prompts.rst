.. _Interactive configuration prompts:

Interactive configuration prompts
=================================

The ``sunbeam cluster bootstrap``, ``sunbeam configure``, and
``sunbeam cluster join`` commands may involve interactive prompts. This
allows the user to specify hardware and networking options particular to
their environment. This reference page provides a detailed description
of each prompt (question).

.. tip::
   Some of these questions’ values can be provided by means of a
   :doc:`manifest file </explanation/deployment-manifest>`
   file passed to the ``sunbeam cluster bootstrap`` and ``sunbeam configure``
   commands.

Below are all of the questions that can potentially be asked. What
questions get asked are sometimes dependent upon the response given in a
preceding question.


.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Questions
     - Meaning
   * - **Use proxy to access external network resources?**
     - | Whether to enable usage of a network proxy that may constrain network traffic. If 'Yes', the default values for the ensuing questions will be populated from the settings that should reside in the local ``/etc/environment`` file.
   * - **http_proxy**
     - | *Question will appear if proxy usage is enabled.*
       |
       | Example value: ``http://squid.proxy:3128``
   * - **https_proxy**
     - | *Question will appear if proxy usage is enabled.*
       | Example value: ``http://squid.proxy:3128``
   * - **no_proxy**
     - | *Question will appear if proxy usage is enabled.*
       |
       | Example value: ``localhost,127.0.0.1,localhost,10.121.193.0/24,10.20.21.0/27``
   * - **Management network**
     - | The network addresses of the subnets used for management traffic. This is typically the same as the network used by the machines supporting the deployment. Multiple CIDRs can be specified, separated by commas.
   * - **OpenStack APIs IP ranges**
     - | OpenStack services are exposed via virtual IP addresses. This range should contain at least ten addresses and must not overlap with external network CIDR. To access APIs from a remote host, the range must reside within the subnet that the primary network interface is on.
       |
       | On multi-node deployments, the range must be addressable from all nodes in the deployment.
   * - **Hostname for Traefik internal endpoint**
     - | The hostname for the internal endpoint of the Traefik service. This is used to configure TLS Vault.
   * - **Hostname for Traefik public endpoint**
     - | The hostname for the public endpoint of the Traefik service. This is used to configure TLS Vault.
   * - **Hostname for Traefik RGW endpoint**
     - | The hostname for the RGW endpoint of the Traefik service. This is used to configure TLS Vault.
   * - **Local or remote access to VMs**
     - | If 'local' is selected then VMs will **only** be accessible from the local host, whereas if 'remote' is selected then VMs will **only** be accessible from remote hosts.
       |
       | For the remote case, you will subsequently be asked to specify what network interface to dedicate to VM access traffic. The intended remote hosts must have connectivity to this interface.
   * - **External network - arbitrary but must not be in use**
     - | *Question will appear for local access only.*
       |
       | CIDR of network for assigning addresses to VMs intended to be accessed from the local host. It is arbitrary but should not conflict with another network known to the host.
   * - **External network**
     - | *Question will appear for remote access only.*
       |
       | CIDR of network for assigning addresses to VMs intended to be accessed from remote hosts. It represents a portion of the physical network (outside of the OpenStack installation) whose IP addresses are dedicated for this purpose.
       |
       | **Caution:** If you opted to access OpenStack APIs externally in the ``bootstrap`` step **and** you opted to access OpenStack VMs externally in the current ``configure`` step, ensure that these ranges do not overlap.
   * - **External network's gateway**
     - | *Question will appear for remote access only.*
       |
       | IP address of existing default gateway for external network.
   * - **External network's allocation range**
     - VMs intended to be accessed from remote hosts will be assigned dedicated addresses from a portion of the physical network (outside OpenStack). Takes the form of an IP range.
   * - **External network's type**
     - | Network type for access to external network - 'flat' (untagged) or 'vlan' (tagged).
   * - **External network's segmentation id**
     - | *Question will appear for VLAN network type only.*
       |
       | VLAN ID to use for the external network.
   * - **External network's interface**
     - | *Question will appear for remote access only.*
       |
       | The network interface used for external access to VMs. The interface should be connected to an appropriate physical network. Detected unconfigured (free) interfaces will be listed as acceptable values. However, an interface not appearing in the list can still be entered.
       |
       | Remote hosts intending to access VMs must be able to contact this interface.
   * - **Populate OpenStack cloud with demo user, default images, flavors, etc.**
     - | Whether the cloud is to be pre-populated with common OpenStack artifacts. In most cases this is desirable.
   * - **Username to use for access to OpenStack**
     - | The username of the demo user.
   * - **Password to use for access to OpenStack**
     - | The password for the demo user. The default password is randomly generated.
   * - **Project network**
     - CIDR of the private network for the demo user's project. This is typically an unroutable (RFC 1918) network like 192.168.122.0/24.
   * - **Project network's nameservers**
     - | A list of DNS server IP addresses (comma separated) that should be used for external DNS resolution from cloud instances.
   * - **Enable ping and SSH access to instances**
     - | Whether security group rules are to be added that allow ICMP and SSH traffic to reach VMs. In most cases this is desirable.
