Implementing TLS using a third-party CA
=======================================

This page shows how to implement TLS when using an external Certificate
Authority for your certificates.

.. tip::
   For conceptual background on TLS in Canonical OpenStack see the
   :doc:`Service endpoint encryption </explanation/service-endpoint-encryption>`
   page.

.. caution::
   This feature is currently only supported in channel ``2023.2/edge`` of the
   **openstack** snap.

Enable the TLS CA feature
-------------------------

This method relies on the TLS CA feature. See the :doc:`TLS CA </how-to/features/tls-ca>`
feature page for how to enable it.

If the feature is ever disabled (see the feature page), to re-enable,
the entire procedure given below must be repeated.

Gather the certificate signing requests
---------------------------------------

You’ll need the certificate signing requests (CSRs) for each available
Traefik unit.

To retrieve CSRs for which certificates are not yet provided, run the
following command:

::

   sunbeam tls ca list_outstanding_csrs

Sample output for the above command:

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

In this example there are two CSRs - one for unit ``traefik/0``
(internal traffic) and one for unit ``traefik-public/0`` (public
traffic).

Request TLS certificates
------------------------

Request one TLS certificate for each generated CSR.

You’ll need to supply the Certificate Authority (identified in the
``enable`` command) with the CSRs. Do this via the certificate authority's
web site.

.. note::
   Ensure the TLS certificate from CA has Subject Alternative Name with IP
   Address of the service if DNS names are not used.

Input TLS certificates
----------------------

Run the below command to inject the newly acquired TLS certificates into
the cloud:

::

   sunbeam tls ca unit_certs

You will be prompted for a TLS certificate for each Traefik unit.

This example’s final total output is:

::

   Base64 encoded Certificate for traefik/0 CSR Unique ID: 9c90972f-ec72-41b9-b6e4-2793ee052531: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURNakNDQWhvQ0ZCLzMyRmlqZEhZRmJqa01yYTFxVEJHM1o5WFhNQTBHQ1NxR1NJYjNEUUVCQ3dVQU1HWXgKQ3pBSkJnTlZCQVlUQWtsT01Rc3dDUVlEVlFRSURBSkJVREVNTUFvR0ExVUVCd3dEVmxSYU1SQXdEZ1lEVlFRSwpEQWRsZUdGdGNHeGxNUkF3RGdZRFZRUUxEQWRsZUdGdGNHeGxNUmd3RmdZRFZRUUREQTlsZUdGdGNHeGxMblJsCmMzUXVhVzh3SGhjTk1qUXdNakl5TURFek9ESXhXaGNOTWpZd05USTNNREV6T0RJeFdqQkZNUlF3RWdZRFZRUUQKREFzeE1DNHlNQzR5TVM0eE16RXRNQ3NHQTFVRUxRd2taakF6TVdVMU56VXRNemczWWkwME1qTTVMVGcwWXpVdApaVEJtWXpWbU5HVmxNV1psTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFqRmlZCnMwQWpHRnNpT3BDMVUyRHA5bzdpdWVYVzhldGVuMHgyYWs5b1FQaVdxcnI5bWY2WnA1Vy9kaUhwMTc0YS9Ka2oKRmRRRkduSmtYbG5xcEJJZ25oWHJkbWtLeEk4TTFTZU1TWUNrZWMyc0FVanpza2U5Y1FFeVg3cWVHY3drL2h2WQpPeFlYU2lzL3diL085b3pFQUhNd3FWRGdhZ3BTVFBiaFFsbkFLdEdleUkrSXlBb1pOYi9NMUlXQTNUQ0tESVYvClNERWxPaDhwWTRlL1FwRXJVZnJNR2lQQmtJSENMWEhVRHAzUStIQkxQUWJFeHlzODZSejluVncwT0RoM0pJbSsKYnF1ZlFNdEljVHZ0bG9LQjI2dExhdXNUeGEyaytuM2tUdnpCaEdGdHhOMHNWQk4xV1FNOEtWSjlnMWtyZ1dPTApKdUNSZXJsWk9pTVF1M2lteHdJREFRQUJNQTBHQ1NxR1NJYjNEUUVCQ3dVQUE0SUJBUUFJVG5TVC84L3E5NXdvCjlFNDZiQ3pDblBCelIzMjhDbnd3TXFaTW5mczJtb2RxTDJDNFZHTGx1VUFiUE1jKzRROGd3U3ZER216RzhWdTgKMlp2WTRtMFlZa2VZMHd0ZmpGdVNnck80ZEVJSHJERGtmZDBxS1dNWWxWY3k2LzlwVHNGWjkwbU9LVFFCOUhoeQpZNE14ODE0enNXYnZuTVFISDJFbkJ6Z0pWZXdXS2FvdE1tZ2g4SnkrT0pRb0dWb1E5ZVJHa0JXSUpFcDVyU0RKClR6T2p4UGVxVmFUNURpQmdUM0l5ODAvSHpueDZUajNiSjVtZjQ4TlgzdFQ3clZvUmVGL1hsUkdwU0luT2pWVCsKQU14c0QvdDlxYUtsS3lUV2FFZUdIM085bGRVUVROaTM0eVpOL0ZyeWxWcmxrRHlHL3IyQjNwaDZvb211MHdFRQpzTzhYdTd1dAotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==

   Base64 encoded Certificate for traefik-public/0 CSR Unique ID: be71a3bd-8d3a-411b-b258-2413d36100ce: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURNakNDQWhvQ0ZBZzNsWTVvM0cxc2VvNWNYZktvQ2JJQ0hUMHNNQTBHQ1NxR1NJYjNEUUVCQ3dVQU1HWXgKQ3pBSkJnTlZCQVlUQWtsT01Rc3dDUVlEVlFRSURBSkJVREVNTUFvR0ExVUVCd3dEVmxSYU1SQXdEZ1lEVlFRSwpEQWRsZUdGdGNHeGxNUkF3RGdZRFZRUUxEQWRsZUdGdGNHeGxNUmd3RmdZRFZRUUREQTlsZUdGdGNHeGxMblJsCmMzUXVhVzh3SGhjTk1qUXdNakl5TURFek9ETXhXaGNOTWpZd05USTNNREV6T0RNeFdqQkZNUlF3RWdZRFZRUUQKREFzeE1DNHlNQzR5TVM0eE1qRXRNQ3NHQTFVRUxRd2taVEk0WmpreU1qa3RZekZpWkMwME4yVmhMVGsxTVRFdApNVEpoWVRnNU4yUTFNREl5TUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUEwQ3ZnCmZLRXZ2UmVWRUI0U0Z6ZGVKcmQwbnlFdTBQaUVNRE14RnpjSjNUTjFpZ3FHZUpuRDBLdUduN04zTUhES0pWb0EKS1B4ZUlkMlh2Uzd0b0syemdnbmpRWVBEZ0tkYWN6bjlJYzhqa3RnV0xvOVBod2RBdlJKU1VpR0JvSlV5bGxDZwpVbFBoT3B4TDlhakRLSG15WFptVTBPdlE0d0NzZHUxUjY0WVZEcjF5Tzh6STdGZUV4ekU4V3ZiV090ZXhVdDZlCm9sRjlPSjREdEI2L1RrTDF2RW1rTnlYWUkrWk5qZDZHN1NCNitvS1FJUGY4cXJ3ZlhaSVdKM0JCS09LblVMLy8KUFltV0R1ZDJGcWwvVmhkOC9vSENzUE1YckhFT29URnZZaDVHQ0VMMmJmT1EwcThpNGZoemN3b1RvTkN3V3Avego4dWxReHhic2dYSVR0SFJhQVFJREFRQUJNQTBHQ1NxR1NJYjNEUUVCQ3dVQUE0SUJBUUFHbTVVd1NLNy9FQXdrClV3Z2NvdmQzVDV0UmlXandlWjJ6N1pORVp4UmZqc0UreXhOQm5kNFcwK0FDZWoyYlNGaGwxOGx0QmhzNVNablMKMXhXU25MdDlKQjlqYXhleC9aMFZuYitCSElpZmt4dEhBaCtZNnBuUjVlZFJLWHE3RFFleUUvN0FPckdOSVBIWgpNd1lQRkFTd0lBQnhpUFQ3dFZkdmVvRmhoR1dpNklaNFZqSHJvVERJSjkvbGVMMy9ianJ3OEwyRHlSSGsrenpGCng2NU1hdzRUK0paQ0NHeGE1bFhWalA0ZlFrTXlMS1IwRUlCU1ZvWU9EMmluVlJpa0lGb3N0UnlFcURHS0NvM0YKSVo1dUxHYzFQNEpGQ1hWNGYzbTNsNUpNaUYwVUdkVklKY0twckVEM08zR2tmS04wNEYvWTNZRHVweXRxSjdSQQpYWGhqYi8vQgotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
   CA certs configured

Alternatively to avoid prompt, update TLS certificates in manifest file,
see certificates block in :doc:`manifest reference </reference/manifest-file-reference>`. Run the
below command to inject TLS certificates into the cloud:

::

   sunbeam tls ca unit_certs --manifest <Manifest file path> 

Verify that TLS is active
-------------------------

Generate an openrc file:

::

   sunbeam openrc

This file should use an HTTPS link for ``OS_AUTH_URL`` (Keystone) and a
value for ``OS_CACERT``, which is the file path to the CA certificate.

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

Generate a cloud-config file:

::

   sunbeam cloud-config --admin --update

Similarly, this file should use HTTPS for ``auth_url`` and have a file
for ``cacert``:

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

Set ``OS_CLOUD`` to use the credentials generated by ``cloud-config``:

::

   export OS_CLOUD=sunbeam-admin

To verify **public** endpoints, run the command:

::

   openstack endpoint list --interface public

The output should use HTTPS for all URLs:

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

To verify **internal** endpoints, run the command:

::

   openstack endpoint list --interface internal

The output should use HTTPS for all URLs:

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

To query for available cloud images, run the command:

::

   openstack image list

This should not result in any errors; the images should be displayed:

::

   +--------------------------------------+--------+--------+
   | ID                                   | Name   | Status |
   +--------------------------------------+--------+--------+
   | 01a247e1-74cb-477d-80ca-5d834be8639b | ubuntu | active |
   +--------------------------------------+--------+--------+
