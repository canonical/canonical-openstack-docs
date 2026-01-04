# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-resource-optimization]
sunbeam enable resource-optimization
# [docs-view:enable-resource-optimization-end]

# [docs-exec:enable-resource-optimization]
sg snap_daemon 'sunbeam enable resource-optimization'
# [docs-exec:enable-resource-optimization-end]


# [docs-view:disable-resource-optimization]
sunbeam disable resource-optimization
# [docs-view:disable-resource-optimization-end]

# [docs-exec:disable-resource-optimization]
sg snap_daemon 'sunbeam disable resource-optimization'
# [docs-exec:disable-resource-optimization-end]
