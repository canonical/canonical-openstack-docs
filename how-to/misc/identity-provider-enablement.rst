Managing OpenStack Identity Providers
=====================================

Overview
--------

Perhaps one of the most important user facing features of any cloud is the authentication, authorization
and service discovery workflows that allow users to log into their account and create resources.
OpenStack, through the use of Keystone provides a plugable architecture for authentication while still
retaining the responsibility for authorization and service discovery.

In this document we'll walk through enabling additional authentication back-ends for keystone by integrating
with OpenID Connect providers such as Google, Okta, Entra ID or `Canonical Identity Platform <https://charmhub.io/topics/canonical-identity-platform>`_.

Implementation
--------------

Keystone does not directly support the needed authentication workflows needed for OpenID or SAML2. Rather,
it delegates that responsibility to Apache2, which then passes onto keystone the result of the authentication
via a set of variables which hold details about the user (full name, email, remote user ID, etc).

Keystone then uses this information to match the authenticated user to a project, based on a set of
rules configured by the cloud operator (detailed later).

Configuring federation has two major components:

* Making an IdP available to Keystone via Apache2 configurations.
* Enabling the IdP in OpenStack by creating the required keystone resources using the `openstack` command

Canonical OpenStack is responsible for the first part of that configuration process, which involves adding the needed URLs
in Apache2 and secrets to enable the authentication workflows. Making use of the newly enabled
capabilities falls on the cloud administrator, by leveraging standard openstack commands.


Requirements
------------

Before we begin, make sure that you have enabled TLS through the use of Vault. Virtually all providers require that
the redirect URL is TLS enabled. Moreover, some providers require that the redirect URL uses a fully qualified domain
name and not an IP address. This means that for the external host name you must also set a valid hostname. Both of
these operations can be done by enabling Vault.

Adding an Identity provider
---------------------------

There are two types of relations supported by Canonical OpenStack:

* External providers (Google, Okta, Entra ID) for both OpenID connect and SAML2
* `Canonical Identity Platform <https://charmhub.io/topics/canonical-identity-platform>`_ which is expected to be deployed in a different juju model.

Enabling Canonical Identity Platform as an IdP
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the purpose of this document we will assume you have a model called `iam` which contains a deployment of Canonical Identity Platform.
Integration is done by consuming an offer for the `oauth` endpoint of the `Hydra <https://charmhub.io/hydra>`_ charm. If your
identity platform uses a custom CA, you also need to consume the `send-ca-cert` endpoint deployed in your `iam` model.

Create the offers:

::

    juju offer iam.hydra:oauth
    juju offer iam.self-signed-certificates:send-ca-cert

Get the offer URLs. We'll need them when creating the config file:

::

    HYDRA_OFFER=$(juju list-offers --format=json -m iam hydra | jq -r '.hydra.["offer-url"]')
    SEND_CA_CERT_OFFER=$(
        juju list-offers \
        --format=json \
        -m iam \
        self-signed-certificates | jq -r '.["self-signed-certificates"].["offer-url"]')

Create the config file:

::

    cat << EOF > canonical-iam.yaml
    oauth_offer: $HYDRA_OFFER
    cert_offer: $SEND_CA_CERT_OFFER
    EOF

And finally add the provider:

::

    sunbeam identity provider add \
        canonical openid canonical-identity-platform \
        --config canonical-iam.yaml

In the above example we added a new identity provider of type `canonical` with the `openid` protocol and the name `canonical-identity-platform`.
the name is important in the case of providers of type `canonical` as the name is also used as a label in `Horizon` when selecting the IdP. So make
sure to use a descriptive name.

Now we can list the providers:

::

    sunbeam identity provider list
    +-----------------------------+------------+----------+------------+
    | Name                        | Provider   | Protocol | Remote ID  |
    +-----------------------------+------------+----------+------------+
    | Keystone Credentials        | Built-in   | keystone | N/A        |
    | canonical-identity-platform | canonical  | openid   | N/A        |
    +-----------------------------+------------+----------+------------+

At this point the configurations exist in apache, keystone and horizon that enable a cloud administrator to configure it as an authentication backend. We will
cover that part later.

External IdPs
~~~~~~~~~~~~~

Canonical OpenStack currently supports the following IdP types:

* `Google (OIDC) <https://developers.google.com/identity/openid-connect/openid-connect>`_
* `Google (SAML2) <https://cloud.google.com/chronicle/docs/soar/admin-tasks/saml-soar-only/saml-configuration-for-g-suite>`_
* `Okta (OIDC) <https://help.okta.com/en-us/content/topics/apps/apps_app_integration_wizard_oidc.htm>`_
* `Okta (SAML2) <https://developer.okta.com/docs/guides/add-an-external-idp/saml2/main/>`_
* `Entra ID (OIDC) <https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc#enable-id-tokens>`_
* `Entra ID (SAML2) <https://learn.microsoft.com/en-us/entra/architecture/auth-saml>`_
* Generic (SAML2 and OIDC)

Each of these provider types require specific configurations in order to enable them and each have their own procedure for creating the client credentials needed to initiate the authentication workflow.
You will have to consult the official documentation for each, in order to generate the required client credentials. The configuration formats that Canonical OpenStack requires are detailed below. The configuration
files are in `yaml` format.

When creating an OpenID Connect integration meant to be used with Canonical OpenStack, you will need the redirect URL that the IdP needs to call back into when a user authenticates. To display the redirect URL, you can run
the following command:

::

    sunbeam identity provider get-oidc-redirect-url
    https://sunbeam.example.com/openstack-keystone/v3/OS-FEDERATION/protocols/openid/redirect_uri

For SAML2 you will need to know the metadata URL of the Service Provider (Keystone in our case). The metadata URL will return the SP XML for keystone, where you can find
the signing certificate that keystone will use, the single sign out URL and the Assertion Consumer Service URL. You will need this information to set up the SAML2 application
in your provider of choice.

The metadata URL for a particular provider can be inferred from the FQDN of keystone, the provider name and the provider protocol.
If we have a provider named `entra` that uses `saml2` and our FQDN is `sunbeam.example.com` then the metadata URL will be:

::

    https://sunbeam.example.com/openstack-keystone/v3/OS-FEDERATION/identity_providers/entra/protocols/saml2/auth/mellon/metadata


Note, the schema **must** be **https** and you **should** have a fully qualified domain name configured instead of an IP address. Depending on IdP, this might be a requirement (Google for example). If that is not the case,
you should enable TLS in sunbeam, using Vault.

SAML2 special consideration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

When creating a SAML2 entry in Canonical OpenStack, there is a bit of a chicken and egg situation. The application needs to exist in the provider of choice before you
can add it to Canonical OpenStack, but you also need the information in the metadata XML we offer to configure the application in the IDP of choice. Luckily, the information
you use when creating the application does not need to be accurate. You will be able to create the application even with placeholder values. Once you create the application, you
can add it to Canonical OpenStack. Once added, you will be able to get the values from the metadata URL mentioned above and edit the application in the IDP of choice.

Another important consideration is that for SAML2 you will need to make sure you've added an x509 signing certificate and the corresponding key:

::

    sunbeam identity set-saml-x509 /path/to/cert.pem /path/to/key.pem


Google config format (OIDC)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two mandatory configuration parameters and one optional parameter:

* `client-id` - mandatory
* `client-secret` - mandatory
* `label` - optional

Example config:

::

    client-id: client_id_obtained_from_your_console
    client-secret: client_secret_associated_with_the_id
    label: "Log in with Google (OIDC)"

Google config format (SAML2)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is one mandatory configuration parameter and one optional parameter:

* `app-id` - mandatory
* `label` - optional

Example config:

::

    app-id: saml2_app_id
    label: "Log in with Google (SAML2)"


Okta config format (OIDC)
^^^^^^^^^^^^^^^^^^^^^^^^^

There are three mandatory configuration parameters and one optional parameter:

* `client-id` - mandatory
* `client-secret` - mandatory
* `okta-org` - mandatory
* `label` - optional

Example config:

::

    client-id: client_id_obtained_from_your_console
    client-secret: client_secret_associated_with_the_id
    okta-org: dev-123456
    label: "Log in with Okta"

Okta config format (SAML2)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two mandatory configuration parameters and one optional parameter:

* `app-id` - mandatory
* `okta-org` - mandatory
* `label` - optional

Example config:

::

    app-id: app_id_goes_here
    okta-org: dev-123456
    label: "Log in with Okta (SAML2)"

Entra ID config format (OIDC)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are three mandatory configuration parameters and one optional parameter:

* `client-id` - mandatory
* `client-secret` - mandatory
* `microsoft-tenant` - mandatory
* `label` - optional

Example config:

::

    client-id: client_id_obtained_from_your_console
    client-secret: client_secret_associated_with_the_id
    microsoft-tenant: tenant-uuid-goes-here
    label: "Log in with Entra ID (OIDC)"

Entra ID config format (SAML2)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two mandatory configuration parameters and one optional parameter:

* `app-id` - mandatory
* `microsoft-tenant` - mandatory
* `label` - optional

Example config:

::

    app-id: app_id_goes_here
    microsoft-tenant: tenant-uuid-goes-here
    label: "Log in with Entra ID (SAML2)"

Generic (OIDC)
^^^^^^^^^^^^^^

The generic provider allows you to configure any OIDC compatible provider.

There are three mandatory parameters and one optional parameter:

* `client-id` - mandatory
* `client-secret` - mandatory
* `issuer-url` - mandatory
* `label` - optional

Example config:

::

    client-id: client_id_obtained_from_your_console
    client-secret: client_secret_associated_with_the_id
    issuer-url: https://oidc.example.com
    label: "Log in with My OpenID connect provider"

A note about the `issuer-url`. This URL identifies the provider. It is also the URL from which we get the OpenID connect configuration.
The issuer URL, must have the well-known openid configuration URL available. This URL can be constructed by appending
`/.well-known/openid-configuration` to the issuer URL.

Example:

::

    https://accounts.google.com/.well-known/openid-configuration


In the above example, `https://accounts.google.com` is the `issuer-url`.

For the generic OpenID connect there is no option to specify a custom CA certificate chain to validate the `issuer-url`. You will need to use
a certificate issued by a CA that your deployment already trusts.

Generic (SAML2)
^^^^^^^^^^^^^^^

Similar to the OIDC generic provider, the generic SAML2 provider allow you to configure any SAML2 compliant IDP, as long as you know the metadata URL.

There is only one mandatory configuration parameter for the SAML2 provider and two optional parameters.


* `metadata-url` - mandatory
* `ca-chain` - optional
* `label` - optional

Example config:

::

    metadata-url: https://saml2.example.com/metadata
    ca-chain: base64-encoded-ca-chain-goes-here
    label: "Log in with My Custom SAML2 IDP"

The metadata URL must contain a XML response that identifies the IDP. The XML must contain the remote `entityID`, as well as the signing x509 keys of the remote IDP.
The value of the `entityID` property must be used when defining the IDP in Canonical OpenStack as the remote ID.


Adding an external IdP
~~~~~~~~~~~~~~~~~~~~~~

Adding an external IdP is similar to adding a Canonical Identity Platform provider:

::

    sunbeam identity provider add \
        google openid my-google-idp \
        --config google.yaml


Now we can list the providers:

::

    sunbeam identity provider list
    +-----------------------------+------------+----------+------------------------------+
    | Name                        | Provider   | Protocol | Remote ID                    |
    +-----------------------------+------------+----------+------------------------------|
    │ Keystone Credentials        │ Built-in   │ keystone │ N/A                          │
    | canonical-identity-platform | canonical  | openid   | N/A                          |
    │ my-google-idp               │ google     │ openid   │ https://accounts.google.com  │
    +-----------------------------+------------+----------+------------------------------|

Adding a SAML2 or OIDC provider has a similar procedure for all above mentioned options.

Make a note of the name of the provider and of the protocol. We will use them in the next steps to enable these providers in keystone.

Note, you should already see them in `Horizon`, but you will only be able to use them after we've mapped them to domains and projects. Examples below.

Removing a provider
~~~~~~~~~~~~~~~~~~~

Removing a provider is a matter of running:

::

    sunbeam identity provider remove my-google-idp --yes-i-mean-it


Note, this will not remove any resources created by the cloud administrator using the `openstack` command.

Making use of the new providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that we've made the providers available to the cloud, we can enable them in keystone, map them to a domain and create rules on how users should
be mapped to projects.

You can create a new domain or you can use an existing domain to map it to the IdP. For the purposes of this guide, we'll create a new one:

::

    openstack domain create \
        --description="Federated Google domain" \
        google

Get the issuer URL for the desired IdP. In this case we'll go with `my-google-idp` from the output above:

::

    REMOTE_ID=$(sunbeam identity provider list \
        --format=yaml |  yq -r '.openid."my-google-idp".remote_id')

Note, if you're configuring a saml2 IDP, you will need to adapt the `yq` arguments in the above command.

Create the identity provider in Keystone:

::

    openstack identity provider create \
        --remote-id $REMOTE_ID \
        --domain google \
        my-google-idp


Note, the name of the identity provider must match the name in the table outputted by sunbeam.

Create a group which we will assign to federated users:

::

    openstack group create federated_users \
        --domain google

Create a project. The following example creates a project named ``federated_project``:

::

    openstack project create \
        --domain google \
        federated_project

Add a role for the group on the project we want to use:

::

    openstack role add \
        --group federated_users \
        --project federated_project \
        --group-domain google \
        --project-domain google \
        member


Next, we need to create some mapping rules between the remote users that come in from the IdP and local openstack users. The rules instruct Keystone how
to automatically create local users and to assign them to groups, projects, domains, etc. You may consult `the official documentation <https://docs.openstack.org/keystone/latest/admin/federation/mapping_combinations.html>`_
on how to write the rules. In this guide we'll create a simple rule set which will be used for the `openid` protocol of the `my-google-idp` provider to map
users to the group we created above. That will automatically grant them **member** access in the **federated_project** of the **google** domain.

This file can be as complex as you need it to be, based on your needs.

Create a file with the rules:

::

    cat > rules.json <<EOF
    [
        {
            "local": [
                {
                    "user": {
                        "name": "{0}"
                    },
                    "group": {
                        "domain": {
                            "name": "google"
                        },
                        "name": "federated_users"
                    }
                }
            ],
            "remote": [
                {
                    "type": "REMOTE_USER"
                }
            ]
        }
    ]
    EOF

Note, we're using **REMOTE_USER** as the remote user ID, but you may also use other attributes like **OIDC-preferred_username** or **OIDC-email**. But that
is a call left to the cloud administrator. The above rules will create a user and add it to the group **federated_users** in the domain **google**.

Create the mapping:

::

    openstack mapping create \
        --rules rules.json google_openid

You can only have one mapping per IdP/protocol combination. But the same mapping (created above) can be used for multiple providers.

And lastly, we can create the protocol:

::

    openstack federation protocol create \
        --identity-provider my-google-idp \
        --mapping google_openid \
        openid

Note, the identity provider name and the protocol must match the name and the protocol returned by the ``sunbeam identity provider list`` command.

And that should do it. You should now be able to log into the horizon dashboard using the Google IdP.
