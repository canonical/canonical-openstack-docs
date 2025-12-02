# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-ldap]
sunbeam enable ldap
# [docs-view:enable-ldap-end]

# [docs-exec:enable-ldap]
sg snap_daemon 'sunbeam enable ldap'
# [docs-exec:enable-ldap-end]


# [docs-view:disable-ldap]
sunbeam disable ldap
# [docs-view:disable-ldap-end]

# [docs-exec:disable-ldap]
sg snap_daemon 'sunbeam disable ldap'
# [docs-exec:disable-ldap-end]


# [docs-view:ldap-add]
sunbeam ldap add-domain \
    --domain-config-file ./dom1.yaml \
    --ca-cert-file ./dom1.cert dom1
# [docs-view:ldap-add-end]


# [docs-view:ldap-update]
sunbeam ldap update-domain --domain-config-file ./dom1.yaml --ca-cert-file ./dom1.cert  dom1
# [docs-view:ldap-update-end]


# [docs-view:ldap-list]
sunbeam ldap list-domains
# [docs-view:ldap-list-end]


# [docs-view:ldap-remove]
sunbeam ldap remove-domain '<domain-name>'
# [docs-view:ldap-remove-end]
