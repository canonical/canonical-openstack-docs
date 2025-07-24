Implementing TLS using a third-party CA
=======================================

This page shows how to implement TLS when using an external Certificate
Authority for your certificates.

.. tip::
   For conceptual background on TLS in Canonical OpenStack see the
   :doc:`Service endpoint encryption </explanation/service-endpoint-encryption>` page.

Enable the TLS feature
----------------------

.. tab-set::
   :sync-group: backend

   .. tab-item:: CA
      :sync: ca
      :selected:

      This method relies on the TLS CA feature. See the :doc:`TLS CA </how-to/features/managing-tls/tls-ca>`
      feature page for how to enable it.

      If the feature is ever disabled (see the feature page), to re-enable,
      the entire procedure given below must be repeated.

   .. tab-item:: Vault
      :sync: vault

      This method relies on the TLS Vault feature. See the :doc:`TLS Vault </how-to/features/managing-tls/tls-vault>`
      feature page for how to enable it.

      If the feature is ever disabled (see the feature page), to re-enable,
      the entire procedure given below must be repeated.

Gather the certificate signing requests
---------------------------------------

You’ll need the certificate signing requests (CSRs) for each available
Traefik unit.

.. tab-set::
   :sync-group: backend

   .. tab-item:: CA
      :sync: ca
      :selected:

      To retrieve CSRs for which certificates are not yet provided, run:

      .. code-block:: console

         sunbeam tls ca list_outstanding_csrs

      Sample output:

      ::

         +------------------+------------------------------------------------------------------+
         | Unit name        | CSR                                                              |
         +------------------+------------------------------------------------------------------+
         | traefik/0        | -----BEGIN CERTIFICATE REQUEST-----                              |
         |                  | MIICrDCCAZQCAQAwRTEUMBIGA1UEAwwLMTAuMjAuMjEuMTMxLTArBgNVBC0MJDk3 |
         |                  | MmI3YTU3LTM0OTktNDVhNS04OWJkLTM3NjliYzk1MjY1ZTCCASIwDQYJKoZIhvcN |
         |                  | AQEBBQADggEPADCCAQoCggEBAIxYmLNAIxhbIjqQtVNg6faO4rnl1vHrXp9MdmpP |
         |                  | aED4lqq6/Zn+maeVv3Yh6de+GvyZIxXUBRpyZF5Z6qQSIJ4V63ZpCsSPDNUnjEmA |
         |                  | pHnNrAFI87JHvXEBMl+6nhnMJP4b2DsWF0orP8G/zvaMxABzMKlQ4GoKUkz24UJZ |
         |                  | wCrRnsiPiMgKGTW/zNSFgN0wigyFf0gxJTofKWOHv0KRK1H6zBojwZCBwi1x1A6d |
         |                  | 0PhwSz0GxMcrPOkc/Z1cNDg4dySJvm6rn0DLSHE77ZaCgdurS2rrE8WtpPp95E78 |
         |                  | wYRhbcTdLFQTdVkDPClSfYNZK4FjiybgkXq5WTojELt4pscCAwEAAaAiMCAGCSqG |
         |                  | SIb3DQEJDjETMBEwDwYDVR0RBAgwBocEChQVDTANBgkqhkiG9w0BAQsFAAOCAQEA |
         |                  | ZqR2aVYzFD1KvEEFajxJAz8agcpPJougSr9iKEK101/7pQVLDqeCvusJHfv5clYO |
         |                  | RCMxNoAuPFFt83j9V0Sg7FnVLc6ftT9f0C3jWWVbCxZbVMTJ4RcIiYKsjhC8PgpU |
         |                  | J94cQgo4xkcqWc2bpOsEIOyvXgK+AWe9TXhg3EihecDS4Sho7wtDRayR3BL/bOiF |
         |                  | rZGFgnkAgHCNoqHN9IhOqmKm0XWn0XNlP1t6IWih5dGGoYeka135+REKYo4G3kYe |
         |                  | EKqgE3AGkPtjp4nuD33oWa+XK30XPFCRHqdcvenjMfdAPRw+MwAsPWXmihnnSGFh |
         |                  | pVEcQwo0HC3L5LHCVZBdNA==                                         |
         |                  | -----END CERTIFICATE REQUEST-----                                |
         | traefik-public/0 | -----BEGIN CERTIFICATE REQUEST-----                              |
         |                  | MIICrDCCAZQCAQAwRTEUMBIGA1UEAwwLMTAuMjAuMjEuMTIxLTArBgNVBC0MJDI4 |
         |                  | NzllYjlmLTZhOWUtNGNjMC1hZGIyLWZmOWQ5YzU3ZThiMDCCASIwDQYJKoZIhvcN |
         |                  | AQEBBQADggEPADCCAQoCggEBANAr4HyhL70XlRAeEhc3Xia3dJ8hLtD4hDAzMRc3 |
         |                  | Cd0zdYoKhniZw9Crhp+zdzBwyiVaACj8XiHdl70u7aCts4IJ40GDw4CnWnM5/SHP |
         |                  | I5LYFi6PT4cHQL0SUlIhgaCVMpZQoFJT4TqcS/Wowyh5sl2ZlNDr0OMArHbtUeuG |
         |                  | FQ69cjvMyOxXhMcxPFr21jrXsVLenqJRfTieA7Qev05C9bxJpDcl2CPmTY3ehu0g |
         |                  | evqCkCD3/Kq8H12SFidwQSjip1C//z2Jlg7ndhapf1YXfP6BwrDzF6xxDqExb2Ie |
         |                  | RghC9m3zkNKvIuH4c3MKE6DQsFqf8/LpUMcW7IFyE7R0WgECAwEAAaAiMCAGCSqG |
         |                  | SIb3DQEJDjETMBEwDwYDVR0RBAgwBocEChQVDDANBgkqhkiG9w0BAQsFAAOCAQEA |
         |                  | ixa/O4qFUA69EJRgpTV/Wq/aojIJhBvKZcVt+wbniYo+XUsTbJJCH0v1Ja6p2CYX |
         |                  | uLkRN/NlxetQouAb7Iw8tNXgfxHbje6t+63+f8mmK1eVrJ1euDSdOi/cyyVLz/3H |
         |                  | MWU82Kzdk44EDi+NyQLDQttVJLdGMvME7/W8MNEEj4qYUoMDcbq4CnxS6P37TDO9 |
         |                  | sUwn5Q4Ygju4QH+wWasN0hhln0lc55azYXc7y3KAOee0NZQTAM/QjJkBQ4KoA2Bk |
         |                  | HN0GczVe9vj+8NYMgbdQ5u7b2ZxU1E1hFM/MhQUHP1vJlGVP6znmvojLo2FO07DH |
         |                  | qW/PnbNh7gQuYZOh+zW8+A==                                         |
         |                  | -----END CERTIFICATE REQUEST-----                                |
         +------------------+------------------------------------------------------------------+

      To get the output in YAML format, use option ``--format yaml``.

      In this example there are two CSRs - one for unit ``traefik/0`` (internal traffic)
      and one for unit ``traefik-public/0`` (public traffic).

   .. tab-item:: Vault
      :sync: vault

      To retrieve CSRs for which certificates are not yet provided, run:

      .. code-block:: console

         sunbeam tls vault list_outstanding_csrs

      Sample output:

      ::

         +------------------+------------------------------------------------------------------+
         | Unit name        | CSR                                                              |
         +------------------+------------------------------------------------------------------+
         | vault/0          | -----BEGIN CERTIFICATE REQUEST-----                              |
         |                  | MIIClTCCAX0CAQAwUDEfMB0GA1UEAwwWZGV2b3BzLXNvbHV0aW9ucy5jbG91ZDEt |
         |                  | MCsGA1UELQwkZDhlMzA2OGItOTgzYy00ODU4LWFiYTEtNjhkZGYyMGExNmE2MIIB |
         |                  | IjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo4vSTZ/vg3CbFzb1rwbnLZ0O |
         |                  | 6pMu0kcarXwsqfu+nB2Teqv613Zs7+1vGaA9ZyNbo/OquyDsXmBNPeBXAXpXYMmI |
         |                  | RVv6dMDaSOhTbKUYbqSblKhAV+bonHceP9NjFUlFzfcpJSXWFlJeYyQKNGzpgQBf |
         |                  | zyG/oiL0xJjsaM1Ezg5EA3dMnl5ssz3PH/SGHyhuoWytbqEDC5DUcnUEo1tZxEx8 |
         |                  | U4NdQKSFLZVA/pYonR9JeEzdaaqlXSFEOCJe+ktzHGGwXMMhfy4MITVwqr+ILDXD |
         |                  | dEtpDYLuF+GHXyBn2Q7EinuTliPQkt1toNs/1ZDKdiZRHlKg9B0nDO93UorIgQID |
         |                  | AQABoAAwDQYJKoZIhvcNAQELBQADggEBAAOiCoOKiFfGAH4xa9MBvptS53SGg/SH |
         |                  | uqXlN3LyBY2H0Rf9iQp/wZXsKoc/ngEvwQWWx/+isD8mmVo/0v5ar7LIGZScHL7g |
         |                  | n4mG9wlnpf4zYp1KmvP4+RWqmSHsLjicstUlAvcZQaJusZc/reorlGZWp6pXbL/G |
         |                  | 00BFThDc8MCR834Q3mEqJkpQ52gkUL4DxekW0+d56uwvEXaP3++/wZQ8GEdFTnYT |
         |                  | wfS3/inadYtpj5t5vQPJBeMqie47/TVRXUDqkCsZeQiX/VYHxpAlfqpHBrQZklap |
         |                  | 9KdhcRFpBmGy2LlrJYSJcZ7SGNGzHkpsgyAuR3XPV1N5ok9EAmftWMc=         |
         |                  | -----END CERTIFICATE REQUEST-----                                |
         +------------------+------------------------------------------------------------------+


Request TLS certificates
------------------------

Request one TLS certificate for each generated CSR.

.. tab-set::
   :sync-group: backend

   .. tab-item:: CA
      :sync: ca

      You’ll need to supply the Certificate Authority (identified in the
      ``enable`` command) with the CSRs. Do this via the certificate authority's web site.

      .. note::
         Ensure the TLS certificate from CA has Subject Alternative Name with IP
         Address of the service if DNS names are not used.

   .. tab-item:: Vault
      :sync: vault

      You’ll need to supply the Certificate Authority (identified in the
      ``enable`` command) with the CSRs. Do this via the certificate authority's web site.

      .. note::
         The CA certificate needs to be generated as a CA certificate, not as a regular TLS certificate. Vault will set its `common_name` configuration option to the domain from `external_hostname` configuration set during the bootstrapping of sunbeam. The CA certificate must have the same domain defined in the `alt_names` section of the CA configuration file used to sign the CSR.


Input TLS certificates
----------------------

Run the command below to inject the newly acquired TLS certificates into the cloud:

.. tab-set::
   :sync-group: backend

   .. tab-item:: CA
      :sync: ca

      .. code-block:: console

         sunbeam tls ca unit_certs

      You will be prompted for a TLS certificate for each Traefik unit.

      This example’s final total output is:

      ::

         Base64 encoded Certificate for traefik/0 CSR Unique ID: 9c90972f-ec72-41b9-b6e4-2793ee052531: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1J...

         Base64 encoded Certificate for traefik-public/0 CSR Unique ID: be71a3bd-8d3a-411b-b258-2413d36100ce: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1J...

         CA certs configured

      Alternatively, to avoid prompts, update TLS certificates in the manifest file
      (see the certificates block in :doc:`manifest reference </reference/manifest-file-reference>`):

      .. code-block:: console

         sunbeam tls ca unit_certs --manifest <Manifest file path>

   .. tab-item:: Vault
      :sync: vault

      .. code-block:: console

         sunbeam tls vault unit_certs

      You will be prompted for a TLS certificate for the Vault unit.

      This example’s final total output is:

      ::

         Base64 encoded Certificate for vault/0 CSR Unique ID: d8e3068b-983c-4858-aba1-68ddf20a16a6: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1J...

         CA certs configured

      Alternatively, to avoid prompts, update TLS certificates in the manifest file
      (see the certificates block in :doc:`manifest reference </reference/manifest-file-reference>`):

      .. code-block:: console

         sunbeam tls vault unit_certs --manifest <Manifest file path>

      Once the signed certificate is deployed, Vault will automatically issue TLS certificates for the endpoints specified during the TLS Vault enablement process. These certificates will be used by the Traefik instances to secure the cloud service endpoints.


Verify that TLS is active
-------------------------

Generate an openrc file:

.. code-block:: console

   sunbeam openrc

This file should use an HTTPS link for ``OS_AUTH_URL`` (Keystone) and a value for ``OS_CACERT``,
which is the file path to the CA certificate.

.. tab-set::
   :sync-group: backend

   .. tab-item:: CA
      :sync: ca

      ::

         # openrc for access to OpenStack
         export OS_USERNAME=admin
         export OS_PASSWORD=*******
         export OS_AUTH_URL=https://10.20.21.12/openstack-keystone/v3
         export OS_USER_DOMAIN_NAME=admin_domain
         export OS_PROJECT_DOMAIN_NAME=admin_domain
         export OS_PROJECT_NAME=admin
         export OS_AUTH_VERSION=3
         export OS_IDENTITY_API_VERSION=3
         export OS_CACERT=/home/ubuntu/.config/openstack/ca_bundle.pem

   .. tab-item:: Vault
      :sync: vault

      ::

         # openrc for access to OpenStack
         export OS_USERNAME=admin
         export OS_PASSWORD=*******
         export OS_AUTH_URL=https://public.mydomain.com/openstack-keystone/v3
         export OS_USER_DOMAIN_NAME=admin_domain
         export OS_PROJECT_DOMAIN_NAME=admin_domain
         export OS_PROJECT_NAME=admin
         export OS_AUTH_VERSION=3
         export OS_IDENTITY_API_VERSION=3
         export OS_CACERT=/home/ubuntu/.config/openstack/ca_bundle.pem

Generate a cloud-config file:

.. code-block:: console

   sunbeam cloud-config --admin --update

Similarly, this file should use HTTPS for ``auth_url`` and have a file for ``cacert``:

.. tab-set::
   :sync-group: backend

   .. tab-item:: CA
      :sync: ca

      ::

         clouds:
         sunbeam-admin:
            auth:
               auth_url: https://10.20.21.12/openstack-keystone/v3
               password: pS6glK5TQRNf
               project_domain_name: admin_domain
               project_name: admin
               user_domain_name: admin_domain
               username: admin
            cacert: /home/ubuntu/.config/openstack/ca_bundle.pem

   .. tab-item:: Vault
      :sync: vault

      ::

         clouds:
         sunbeam-admin:
            auth:
               auth_url: https://public.mydomain.com/openstack-keystone/v3
               password: pS6glK5TQRNf
               project_domain_name: admin_domain
               project_name: admin
               user_domain_name: admin_domain
               username: admin
            cacert: /home/ubuntu/.config/openstack/ca_bundle.pem

Set ``OS_CLOUD`` to use the credentials generated by ``cloud-config``:

.. code-block:: bash

   export OS_CLOUD=sunbeam-admin

To verify **public** endpoints, run:

.. code-block:: console

   openstack endpoint list --interface public

The output should use HTTPS for all URLs:

.. tab-set::
   :sync-group: backend

   .. tab-item:: CA
      :sync: ca

      ::

         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+
         | ID                               | Region    | Service Name | Service Type | Enabled | Interface | URL                                                       |
         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+
         | 05dd03b906af463cbbf85164bb4c208a | RegionOne | nova         | compute      | True    | public    | https://10.20.21.12:443/openstack-nova/v2.1               |
         | 4880f1558ed94739ae9729d638cea95f | RegionOne | cinderv2     | volumev2     | True    | public    | https://10.20.21.12:443/openstack-cinder/v2/$(tenant_id)s |
         | 809d07f8b2e84f49afa2b3ebcabbad03 | RegionOne | cinderv3     | volumev3     | True    | public    | https://10.20.21.12:443/openstack-cinder/v3/$(tenant_id)s |
         | 9c10da39bb2e46588c05018a3098f1aa | RegionOne | neutron      | network      | True    | public    | https://10.20.21.12:443/openstack-neutron                 |
         | bfdfca65a8a24e4ebe8340dd169b8012 | RegionOne | glance       | image        | True    | public    | https://10.20.21.12:443/openstack-glance                  |
         | cd7490239e6845ffa8c6651300264e5a | RegionOne | keystone     | identity     | True    | public    | https://10.20.21.12/openstack-keystone/v3                 |
         | f7552dc54b4e4d11a1ffa1289957088c | RegionOne | placement    | placement    | True    | public    | https://10.20.21.12:443/openstack-placement               |
         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+

   .. tab-item:: Vault
      :sync: vault

      ::

         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+
         | ID                               | Region    | Service Name | Service Type | Enabled | Interface | URL                                                       |
         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+
         | 05dd03b906af463cbbf85164bb4c208a | RegionOne | nova         | compute      | True    | public    | https://public.mydomain.com:443/openstack-nova/v2.1               |
         | 4880f1558ed94739ae9729d638cea95f | RegionOne | cinderv2     | volumev2     | True    | public    | https://public.mydomain.com:443/openstack-cinder/v2/$(tenant_id)s |
         | 809d07f8b2e84f49afa2b3ebcabbad03 | RegionOne | cinderv3     | volumev3     | True    | public    | https://public.mydomain.com:443/openstack-cinder/v3/$(tenant_id)s |
         | 9c10da39bb2e46588c05018a3098f1aa | RegionOne | neutron      | network      | True    | public    | https://public.mydomain.com:443/openstack-neutron                 |
         | bfdfca65a8a24e4ebe8340dd169b8012 | RegionOne | glance       | image        | True    | public    | https://public.mydomain.com:443/openstack-glance                  |
         | cd7490239e6845ffa8c6651300264e5a | RegionOne | keystone     | identity     | True    | public    | https://public.mydomain.com/openstack-keystone/v3                 |
         | f7552dc54b4e4d11a1ffa1289957088c | RegionOne | placement    | placement    | True    | public    | https://public.mydomain.com:443/openstack-placement               |
         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+    

To verify **internal** endpoints, run:

.. code-block:: console

   openstack endpoint list --interface internal

The output should use HTTPS for all URLs:

.. tab-set::
   :sync-group: backend

   .. tab-item:: CA
      :sync: ca

      ::

         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+
         | ID                               | Region    | Service Name | Service Type | Enabled | Interface | URL                                                       |
         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+
         | 04f9fb67ac6d4295a15d19ac829845b1 | RegionOne | neutron      | network      | True    | internal  | https://10.20.21.13:443/openstack-neutron                 |
         | 05dda52ae04b424fa7f6083d4a888be2 | RegionOne | glance       | image        | True    | internal  | https://10.20.21.13:443/openstack-glance                  |
         | 3fa47154d2c3425d987081600ab6b284 | RegionOne | keystone     | identity     | True    | internal  | https://10.20.21.13/openstack-keystone/v3                 |
         | 6240b34b08cc462a98ab4d37e1ea2770 | RegionOne | placement    | placement    | True    | internal  | https://10.20.21.13:443/openstack-placement               |
         | 6f7ef31c3f994d8a8f66fb749871ff26 | RegionOne | nova         | compute      | True    | internal  | https://10.20.21.13:443/openstack-nova/v2.1               |
         | a9b1ad2b2e524db5b6147abfcca20eea | RegionOne | cinderv2     | volumev2     | True    | internal  | https://10.20.21.13:443/openstack-cinder/v2/$(tenant_id)s |
         | ef9b8eeb54df468ebfd65adc851092b1 | RegionOne | cinderv3     | volumev3     | True    | internal  | https://10.20.21.13:443/openstack-cinder/v3/$(tenant_id)s |
         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+

   .. tab-item:: Vault
      :sync: vault

      ::

         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+
         | ID                               | Region    | Service Name | Service Type | Enabled | Interface | URL                                                       |
         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+
         | 04f9fb67ac6d4295a15d19ac829845b1 | RegionOne | neutron      | network      | True    | internal  | https://internal.mydomain.com:443/openstack-neutron                 |
         | 05dda52ae04b424fa7f6083d4a888be2 | RegionOne | glance       | image        | True    | internal  | https://internal.mydomain.com:443/openstack-glance                  |
         | 3fa47154d2c3425d987081600ab6b284 | RegionOne | keystone     | identity     | True    | internal  | https://internal.mydomain.com/openstack-keystone/v3                 |
         | 6240b34b08cc462a98ab4d37e1ea2770 | RegionOne | placement    | placement    | True    | internal  | https://internal.mydomain.com:443/openstack-placement               |
         | 6f7ef31c3f994d8a8f66fb749871ff26 | RegionOne | nova         | compute      | True    | internal  | https://internal.mydomain.com:443/openstack-nova/v2.1               |
         | a9b1ad2b2e524db5b6147abfcca20eea | RegionOne | cinderv2     | volumev2     | True    | internal  | https://internal.mydomain.com:443/openstack-cinder/v2/$(tenant_id)s |
         | ef9b8eeb54df468ebfd65adc851092b1 | RegionOne | cinderv3     | volumev3     | True    | internal  | https://internal.mydomain.com:443/openstack-cinder/v3/$(tenant_id)s |
         +----------------------------------+-----------+--------------+--------------+---------+-----------+-----------------------------------------------------------+

To query for available cloud images, run:

.. code-block:: console

   openstack image list

This should not result in any errors; the images should be displayed:

::

   +--------------------------------------+--------+--------+
   | ID                                   | Name   | Status |
   +--------------------------------------+--------+--------+
   | 01a247e1-74cb-477d-80ca-5d834be8639b | ubuntu | active |
   +--------------------------------------+--------+--------+
