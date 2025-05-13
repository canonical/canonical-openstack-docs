Service endpoint encryption
===========================

Overview
--------

The encryption of service API endpoints in an OpenStack cloud requires a
method for the creation and distribution of TLS certificates. Canonical
OpenStack supports enabling TLS via the Traefik application, which is the
ingress point for all service endpoints.

.. note::
   Currently, only the TLS CA feature method is supported. This feature only
   works with certificates signed by an external Certificate Authority.

TLS CA feature
--------------

The TLS CA feature is the method to use for deployments that use a third
party CA for certificates.

.. caution::
   This feature is currently only supported in channel ``2023.2/edge`` of the
   **openstack** snap.

.. tip::
   For a how-to on using the TLS CA feature see :doc:`Implement TLS using a third-party CA
   </how-to/misc/implement-tls-using-a-third-party-ca>`.

Points of interest for this design:

-  Enabling the feature will deploy charm `manual-tls-certificates
   operator <https://charmhub.io/manual-tls-certificates>`__. It will
   integrate the `manual-tls-certificates` application with the
   Traefik application. This step requires a third party CA certificate
   and a CA chain.

-  Certificate Signing Requests (CSRs) need to be retrieved for all
   Traefik units.

-  This method involves interfacing directly with the chosen Certificate
   Authority.

-  Each Traefik unit needs to be provided with a signed certificate.
   This updates endpoints with HTTPS and also distributes the CA
   certificates to all the application units across the cloud via
   Keystone.
