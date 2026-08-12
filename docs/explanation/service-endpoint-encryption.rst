Service endpoint encryption
===========================

Overview
--------

The encryption of service API endpoints in an OpenStack cloud requires a
method for the creation and distribution of TLS certificates. Canonical
OpenStack supports enabling TLS via the Traefik application, which is the
ingress point for all service endpoints.

.. note::
   Currently, only the TLS CA (Certificate Authority) and TLS Vault methods are supported. TLS CA only works with certificates signed by an external Certificate Authority.

TLS CA feature
--------------

The TLS CA feature is the method to use for deployments that use a third
party CA for certificates.

.. tip::
   For a how-to on using TLS CA see :doc:`Implement TLS using a third-party CA
   </how-to/features/managing-tls/implement-tls-using-a-third-party-ca>`.

Points of interest for this design:

-  Enabling this method will deploy the `manual-tls-certificates
   operator <https://charmhub.io/manual-tls-certificates>`__ charm. It will
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

TLS Vault feature
-----------------

TLS Vault is a useful method for deployments that uses Vault as an intermediary CA.

.. tip::
   For a how-to on using the TLS Vault feature see :doc:`TLS Vault
   </how-to/features/managing-tls/tls-vault>`.

Points of interest for this design
----------------------------------

-  TLS Vault requires the Vault feature to be enabled in the
   cloud, which is done by following this guide :doc:`Enable Vault
   </how-to/features/vault>`.

-  Enabling TLS Vault will deploy the `manual-tls-certificates
   operator <https://charmhub.io/manual-tls-certificates>`__ charm. It will
   integrate the `manual-tls-certificates` application with the Vault application, which will act as an intermediary CA for the
   Traefik application. This step requires a third party CA certificate
   and a CA chain.

-  Certificate Signing Requests (CSRs) need to be retrieved for the Vault unit.

-  This method involves interfacing directly with the chosen Certificate
   Authority.

-  This method will also configure Vault's common name to the domain of the external hostnames configured for the endpoints during bootstrap. It will also configure the Traefik endpoints to use the configured external hostnames.
