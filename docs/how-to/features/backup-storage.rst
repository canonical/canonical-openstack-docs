Backup storage
==============

Use ``sunbeam configure backup`` to deploy and configure S3 storage integrations
for MySQL and Vault in the ``openstack`` model.

Requirements
------------

* A deployed MySQL application and, optionally, Vault.
* An S3 bucket and endpoint accessible from the deployment.
* An access key and secret key with permission to use the bucket.

For production deployments, store backups outside the OpenStack cluster.

Setting up backup storage
-------------------------

To set up Sunbeam-managed backup storage, run:

.. code:: text

   sunbeam configure backup

When managed backup storage has not been set up, Sunbeam asks whether to deploy
the integrations. Confirm to proceed; declining leaves the deployment unchanged.
This confirmation is separate from the optional S3 configuration prompt below.

Sunbeam deploys one s3-integrator application for each eligible MySQL or Vault
application and relates it to that application.

For example, ``mysql`` uses ``mysql-s3-integrator``, ``keystone-mysql`` uses
``keystone-s3-integrator``, and ``vault`` uses ``vault-s3-integrator``.

Applications with an existing, externally managed S3 relation are skipped. Sunbeam
also skips an application if its expected integrator name is already in use by an
application it does not manage. Existing S3 configurations are not adopted or
overwritten.

Configuring S3
--------------

Answer ``y`` to ``Configure all s3-integrators?`` to configure the integrators
managed by Sunbeam. Sunbeam prompts for:

* S3 bucket
* S3 path prefix (default: ``/``)
* S3 region (default: ``us-east-2``)
* S3 endpoint (default: ``https://s3.us-east-2.amazonaws.com``)
* S3 access key
* S3 secret key

The endpoint must begin with ``http://`` or ``https://``. Both credential prompts
hide the entered value.

All managed integrators use the same bucket, endpoint, region, and credentials.
Sunbeam appends each target application name to the path prefix to separate its
backups. For example, a prefix of ``/cloud-backups`` produces
``/cloud-backups/keystone-mysql`` and ``/cloud-backups/vault``.

The default answer to the S3 configuration prompt during setup is ``n``. In this
case, after deployment has been confirmed, Sunbeam deploys the integrators and
relations without supplying S3 settings or credentials. Run
``sunbeam configure backup`` again and choose to update the
managed integrations, or configure them manually using the s3-integrator
procedure in :doc:`/how-to/operations/backup-and-restore`.

Check the application status after setup:

.. code:: text

   juju status -m openstack

Setup can complete while integrators are blocked pending configuration.
Resolve their status messages and verify the MySQL and Vault applications are
ready before following :doc:`/how-to/operations/backup-and-restore`.

To inspect discovered MySQL and Vault targets, their S3 integrations, and backup
readiness:

.. code:: text

   sunbeam cluster backup target list

This read-only command identifies Sunbeam-managed or externally managed
integrations where ownership is known. It is available even when Sunbeam-managed
backup storage has not been set up.

Updating backup storage
-----------------------

Run ``sunbeam configure backup`` after managed backup storage has been set up to
choose whether to keep the current configuration, update managed integrations,
or remove them. Keeping the current configuration is the default. Updating uses
the S3 prompts above.

Removing backup storage
-----------------------

To remove the integrations managed by Sunbeam, run:

.. code:: text

   sunbeam configure backup

Choose removal and confirm the affected resources when prompted. This removes
the managed s3-integrator applications, their relations, and the Juju secrets
created for their credentials. Externally managed S3 integrations
are left in place. The S3 bucket and stored backups are not deleted.

Applications whose integrations were removed need an S3 integration configured
again before they can back up or restore data. Reuse the original bucket and
application paths to access their existing backups.
