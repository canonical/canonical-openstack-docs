Configuring The Openstack Dashboard Theme
=========================================

Overview
--------

The dashboard theme can be set both at bootstrap via the manifest or managed after initial deployment is complete.


.. note ::
   For information on creating a custom theme view the `upstream documentation <https://docs.openstack.org/horizon/latest/configuration/index.html>`_ on configuring horizon.

Configuring via Manifest
------------------------

Setting a Theme
~~~~~~~~~~~~~~~

In order to set a theme in the manifest you must define the file path to you theme archive in the ``core.config`` section of the file:

::

  core:
    config:
      horizon:
        resources:
          custom_theme: </path/to/theme.tar.gz>


Post-Deployment Management
--------------------------

Setting a Theme
~~~~~~~~~~~~~~~

To set the theme after bootstrap is complete use the ``dashboard theme set`` command:

::
  
  sunbeam dashboard theme set


Clearing a Theme
~~~~~~~~~~~~~~~~

To clear an existing custom theme and return to the default use the ``dashboard theme clear`` command:

:: 

  sunbeam dashboard theme clear


Limitations When Used With a Manifest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When setting/clearing a theme using these imperative commands it will always override you manifest values. However, when a cluster operation is performed that re-evaluates the state of the control plane (f.e. ``sunbeam cluster refresh``) the manifest will always take priority over values provided after the fact. As such, when utilizing the manifest to declare your theme these commands should only be used as a "quick test" to ensure that your theme applies correctly before updating the manifest and supplying it on the next cluster operation to ensure that the changes are persistent.

