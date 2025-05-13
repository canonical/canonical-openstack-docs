Deployment manifest
===================

A deployment manifest allows a user to override the default configuration
settings for Canonical OpenStack.

Manifests are supported by the following commands:

-  ``sunbeam cluster bootstrap``
-  ``sunbeam cluster refresh``
-  ``sunbeam configure``
-  ``sunbeam enable``

.. note::
   For a how-to on using manifests see
   :doc:`Managing deployment manifests </how-to/misc/managing-deployment-manifests>`.

A manifest file
---------------

A manifest is a YAML file that consists of two sections: ``deployment``
and ``software``. It has the following structure:

.. code:: text

   deployment:
     <deployment configuration>
   software:
     <software configuration>

See the :doc:`Manifest file reference </reference/manifest-file-reference>`
page for details on the structure and possible contents of this file.

Deployment configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Any infrastructure related configuration like hardware and networking
are specified in this section. If a key’s value is deemed necessary for
your deployment and it has not been provided by means of a manifest
file, you will be asked to enter it via an
:doc:`interactive prompt </reference/interactive-configuration-prompts>`.

Here is an example deployment configuration:

.. code:: yaml

   deployment:

     proxy:
       proxy_required: false

     bootstrap:
       management_cidr: 192.168.123.0/24

     addons:
       metallb: 192.168.123.81-192.168.123.90

     microceph_config:
       sunbeam-1.localdomain:
         osd_devices: /dev/vdc

Software configuration
~~~~~~~~~~~~~~~~~~~~~~

The software configuration consists of three subsections: ``juju``,
``charms``, and ``terraform``.

Here is an example software configuration:

.. code:: yaml

   software:

     juju:
       bootstrap_args:
       - --debug
       - --agent-version=3.2.4

     charms:
       glance-k8s:
         channel: 2023.2/candidate
         revision: 66
         config:
           debug: True
           pool-type: replicated

     terraform:
       hypervisor-plan:
         source: /home/ubuntu/deploy-openstack-hypervisor

``juju`` section
^^^^^^^^^^^^^^^^

This section allows users to pass bootstrap arguments to Juju.

+-----------------------------------+-----------------------------------+
| Option                            | Description                       |
+===================================+===================================+
| :code:`bootstrap_args`            | list of arguments that will be    |
|                                   | passed to the ``juju bootstrap``  |
|                                   | command                           |
+-----------------------------------+-----------------------------------+

``charms`` section
^^^^^^^^^^^^^^^^^^

This section allows users to set specific versions of charm to be
deployed and the charm configurations. This section is a dictionary of
charm and its options. The options that can be set for each charm are
described below.

============ ==========================
Option       Description
============ ==========================
**channel**  charm channel to use
**revision** charm revision to use
**config**   charm configuration to set
============ ==========================

Charm channel/revision and their configuration are set by default and
are known to work together. Use all default values in production and
introduce a new setting only when necessary. For example, only change
the channel/revision to get a possible hot fix or change a configuration
setting as per the local environment (e.g. Keystone LDAP URL).

It is recommended to test any customization in a staging environment
before applying them in production.

.. tip::
   Available charms and their configuration options are listed on the
   :doc:`Underlying projects and charms </reference/underlying-projects-and-charms>`
   page.

``terraform`` section
^^^^^^^^^^^^^^^^^^^^^

This section allows users to set local Terraform plans. This section is
a dictionary of Terraform plans and their options. The options that can
be set for each plan are described below.

========== ================================
Option     Description
========== ================================
**source** Local path of the Terraform plan
========== ================================

This section is for demonstration and development purposes only.

.. caution::
   There is significant risk of misconfiguration when using a local Terraform
   plan due to the fact that Sunbeam depends heavily on the plan variables.
