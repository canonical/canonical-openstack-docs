Baremetal as a Service
======================

This feature deploys `Ironic`_, the bare metal provisioning service for
OpenStack. It allows OpenStack users to provision bare metal machines,
as opposed to virtual machines.

Enabling Baremetal
------------------

This feature requires the storage role. To enable this feature, run the
following command:

::

   sunbeam enable baremetal

The openstack CLI can now be used to manage bare metal machines. See the
upstream `Ironic CLI`_ documentation for details.

The feature will be configured based on the cluster's manifest file.
Alternatively, a different manifest file can be specified during the feature
enablement:

::

   sunbeam enable --manifest baremetal-manifest.yaml baremetal

Sample `baremetal-manifest.yaml` file:

.. code-block:: yaml

    features:
      baremetal:
        software:
          charms:
            ironic-conductor-k8s:
              channel: 2025.1/edge
            ironic-k8s:
              channel: 2025.1/edge
            nova-ironic-k8s:
              channel: 2025.1/edge
            neutron-baremetal-switch-config-k8s:
              channel: 2025.1/edge
            neutron-generic-switch-config-k8s:
              channel: 2025.1/edge
        config:
          shards: ["shard0", "shard1"]
          conductor-groups: ["shard0", "shard1"]
          switchconfigs:
            netconf:
              nexus:
                configfile: |
                  [nexus.example.net]
                  driver = netconf-openconfig
                  device_params = name:nexus
                  switch_info = nexus
                  switch_id = 00:53:00:0a:0a:0a
                  host = nexus.example.net
                  username = user
                  key_filename = /etc/neutron/sshkeys/nexus-sshkey
                additional-files:
                  nexus-sshkey: |
                    some key here.
            generic:
              arista:
                configfile: |
                  [genericswitch:arista-hostname]
                  device_type = netmiko_arista_eos
                  ngs_mac_address = 00:53:00:0a:0a:0a
                  ip = 10.20.30.40
                  username = admin
                  key_file = /etc/neutron/sshkeys/arista-key
                additional-files:
                  arista-key: |
                    some key here.

.. note::
   Rerunning the `sunbeam enable baremetal` command with a different manifest
   file will replace the previously deployed feature configuration (e.g.:
   deployed `nova-ironic` shards, Ironic Conductor groups, Neutron switch
   configurations).

For the switch configurations, the following restrictions apply:

- The `key_filename` and `key_file` config options base file paths must be
  `/etc/neutron/sshkeys`.
- The files referenced in `key_filename` or `key_file` as seen above will
  require those files to be defined as additional files as well.
- Unknown fields in the switch configurations are not allowed. See
  `netconf configuration options`_ and `generic switch configuration`_.
- For `generic` switch configurations, the `device_type` field is mandatory.

After the feature is enabled, you can use the `sunbeam baremetal` sub-command
to manage the deployed `nova-ironic` shards, Ironic Conductor groups, and
Neutron switch configurations.

Managing `nova-ironic` shards
-----------------------------

`nova-ironic` shards will be deployed while enabling the `baremetal` feature,
as mentioned above. Additional shards can be added through the following
command:

::

   sunbeam baremetal shard add SHARD

`nova-ironic` shards can be removed by running the following command:

::

   sunbeam baremetal shard delete SHARD

The following command can be used to list the currently deployed shards:

::

   sunbeam baremetal shard list


Managing Ironic Conductor groups
--------------------------------

By default, sunbeam deploys an `ironic-conductor-k8s` charm with an empty
`conductor-group` configuration option. Additional Ironic Conductor groups
will be deployed while enabling the `baremetal` feature, based on the
`conductor-groups` configuration mentioned above.

Additional Ironic Conductor groups can be added through the following command:

::

   sunbeam baremetal conductor-groups add GROUP-NAME

Ironic Conductor Groups can be removed by running the following command:

::

   sunbeam baremetal conductor-groups delete GROUP-NAME

The following command can be used to list the currently Ironic Conductor
Groups:

::

   sunbeam baremetal conductor-groups list

Managing Neutron Switch Configurations
--------------------------------------

`netconf` and `generic` Neutron switch configurations will be added while
enabling the `baremetal` feature, as mentioned above. Additional configurations
can be added through the following command:

::

   sunbeam baremetal switch-config add netconf|generic NAME --config CONFIGFILE  [--additional-file <NAME FILEPATH>]

An existing switch configuration can be updated with the command:

::

   sunbeam baremetal switch-config update netconf|generic NAME --config CONFIGFILE  [--additional-file <NAME FILEPATH>]

.. note::
   For the add / update sub-commands, multiple additional files can be
   specified.

Note that the same restrictions for the switch configurations mentioned above
still apply when adding new ones or updating existing ones.

A switch configuration can be deleted with the following command:

::

   sunbeam baremetal switch-config delete NAME

The following command can be used to list the current Neutron switch
configurations and their protocol:

::

   sunbeam baremetal switch-config list

Disabling Baremetal
-------------------

To disable this feature, run the following command:

::

   sunbeam disable baremetal

For information on how to access and use Ironic, check the
:doc:`Baremetal feature nodes</explanation/baremetal-nodes>` page.

.. LINKS
.. _netconf configuration options: https://docs.openstack.org/networking-baremetal/2025.1/configuration/ml2/device_drivers/netconf-openconfig.html
.. _generic switch configuration: https://docs.openstack.org/networking-generic-switch/2025.1/configuration.html
