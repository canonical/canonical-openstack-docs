Backup and restore access to a MAAS deployment
==============================================

Overview
--------

As part of the management of a MAAS deployment of Canonical OpenStack it is good practice to backup the information and credentials required to access a deployment.  This backup can also be used to provide additional nodes with access to the deployment.

For the purposes of this document, the MAAS deployment name is `mycloud`; all example commands will use this name.

Backup
------

Export the Canonical OpenStack MAAS deployment
++++++++++++++++++++++++++++++++++++++++++++++

Export the Canonical OpenStack deployment configuration and access credentials:

.. code-block :: text

    sunbeam deployment export mycloud
    Deployment exported to '/home/ubuntu/.local/share/openstack/mycloud.yaml'

`mycloud.yaml` contains all of the details required to grant access to the Canonical OpenStack Cluster deployment from a different node.

Backup Juju configuration and credentials
+++++++++++++++++++++++++++++++++++++++++

Backup the Juju client configuration from a governor node with access to the deployment:

.. code-block :: text

    tar -czf juju-credentials.tar.gz .local/share/juju/*

`juju-credentials.tar.gz` contains a backup of configuration and credentials (including SSH keys) to access the Juju controller used as part of the Canonical OpenStack deployment.

Restore
-------

Prepare the new client node for access
++++++++++++++++++++++++++++++++++++++

On the new node ensure that the `openstack` snap is installed and the node is prepared for client access to the deployment:

.. code-block :: text

    sudo snap install --channel 2024.1/edge openstack
    sunbeam prepare-node-script --client | bash -x

Import the Canonical OpenStack MAAS deployment
++++++++++++++++++++++++++++++++++++++++++++++

Import the deployment using the `mycloud.yaml` file created as part of exporting the deployment configuration and verify that it is accessible using the sunbeam command:

.. code-block :: text

    sunbeam deployment import --file mycloud.yaml
    sunbeam deployment list
    ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
    ┃ Deployment ┃ Endpoint                     ┃ Type ┃
    ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
    │ mycloud*   │ http://10.4.5.6:5240/MAAS    │ maas │
    └────────────┴──────────────────────────────┴──────┘
     sunbeam cluster list
                              openstack-infra
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┓
    ┃ Node                              ┃ Machine ┃ Cluster ┃ Clusterd ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━┩
    │ mycloud-infra-0                   │ running │ ONLINE  │  active  │
    └───────────────────────────────────┴─────────┴─────────┴──────────┘
                                 openstack-machines
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
    ┃ Node                              ┃ Machine ┃ Compute ┃ Control ┃ Storage ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
    │ mycloud-hosts-0                   │ running │ active  │ active  │ active  │
    │ mycloud-hosts-1                   │ running │ active  │ active  │ active  │
    │ mycloud-hosts-2                   │ running │ active  │ active  │ active  │
    └───────────────────────────────────┴─────────┴─────────┴─────────┴─────────┘

Restore Juju configuration and credentials
++++++++++++++++++++++++++++++++++++++++++

.. note ::

   This step will overwrite and existing Juju configuration and credentials and should only be executed on a clean node.

Using the `juju-credentials.tar.gz` created as part of backing up the Juju configuration from the home directory of the user:

.. code-block :: text

    tar -xzf juju-credentials.tar.gz

and then validate that the Juju controller and Canonical OpenStack models are accessible:

.. code-block :: text

    juju controllers
    Controller       Model      User   Access     Cloud/Region  Models  Nodes    HA  Version
    mycloud-controller*  openstack  admin  superuser  mycloud/default        4      2  none  3.6.1
    juju models
    Model               Cloud/Region           Type        Status     Machines  Cores  Units  Access  Last connection
    controller          mycloud/default        maas        available         1      2  1      admin   just now
    openstack*          mycloud-k8s/localhost  kubernetes  available         0      -  118    admin   3 minutes ago
    openstack-infra     mycloud/default        maas        available         1      2  2      admin   1 minute ago
    openstack-machines  mycloud/default        maas        available         3     24  12     admin   1 minute ago
