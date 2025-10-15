# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-validation]
sunbeam enable validation
# [docs-view:enable-validation-end]

# [docs-exec:enable-validation]
sg snap_daemon 'sunbeam enable validation'
# [docs-exec:enable-validation-end]


# [docs-view:disable-validation]
sunbeam disable validation
# [docs-view:disable-validation-end]

# [docs-exec:disable-validation]
sg snap_daemon 'sunbeam disable validation'
# [docs-exec:disable-validation-end]