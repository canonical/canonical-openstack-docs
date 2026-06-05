# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-telemetry]
sunbeam enable telemetry
# [docs-view:enable-telemetry-end]

# [docs-exec:enable-telemetry]
sg snap_daemon 'sunbeam enable telemetry'
# [docs-exec:enable-telemetry-end]


# [docs-view:disable-telemetry]
sunbeam disable telemetry
# [docs-view:disable-telemetry-end]

# [docs-exec:disable-telemetry]
sg snap_daemon 'sunbeam disable telemetry'
# [docs-exec:disable-telemetry-end]
