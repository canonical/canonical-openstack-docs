# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-secrets]
sunbeam enable secrets
# [docs-view:enable-secrets-end]

# [docs-exec:enable-secrets]
sg snap_daemon 'sunbeam enable secrets'
# [docs-exec:enable-secrets-end]


# [docs-view:disable-secrets]
sunbeam disable secrets
# [docs-view:disable-secrets-end]

# [docs-exec:disable-secrets]
sg snap_daemon 'sunbeam disable secrets'
# [docs-exec:disable-secrets-end]
