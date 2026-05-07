# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-caas]
sunbeam enable caas
# [docs-view:enable-caas-end]

# [docs-exec:enable-caas]
sg snap_daemon 'sunbeam enable caas'
# [docs-exec:enable-caas-end]


# [docs-view:disable-caas]
sunbeam disable caas
# [docs-view:disable-caas-end]

# [docs-exec:disable-caas]
sg snap_daemon 'sunbeam disable caas'
# [docs-exec:disable-caas-end]
