Managing CA
===========

This feature is used to encrypt all cloud service endpoints (both public
and private) using TLS certificates obtained from an external provider.
It does this by interfacing with the existing Traefik instances in the
cloud. A Traefik instance is associated with either public or private
cloud traffic.

Enable TLS CA
-------------

To enable TLS, you’ll need to provide information that identifies your
chosen Certificate Authority. Do this by specifying a CA certificate and
its CA certificate chain.

Run the following command to enable TLS for public endpoints:

::

   sunbeam enable tls ca --ca <base64 encoded ca certificate> --ca-chain <base64 encoded ca chain>

To enable TLS for public, internal and rgw endpoints, be explicit by
using the ``--endpoint`` option:

::

   sunbeam enable tls ca --ca <base64 encoded ca certificate> --ca-chain <base64 encoded ca chain> --endpoint public --endpoint internal --endpoint rgw

Use TLS CA
----------

TLS certificates must now be provided to the Traefik units. This is
covered on the :doc:`Implement TLS using a third-party CA
</how-to/features/managing-tls/implement-tls-using-a-third-party-ca>` page.

Disable TLS CA
--------------

To disable TLS in the cloud, run the following command:

::

   sunbeam disable tls ca

This command removes the `manual-tls-certificates` charm from being the certificate Authority and all services will work as if TLS was never enabled.
