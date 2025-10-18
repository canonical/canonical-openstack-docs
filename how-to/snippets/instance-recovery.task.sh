# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-instance-recovery]
sunbeam enable instance-recovery
# [docs-view:enable-instance-recovery-end]

# [docs-exec:enable-instance-recovery]
sg snap_daemon 'sunbeam enable instance-recovery'
# [docs-exec:enable-instance-recovery-end]


# [docs-view:disable-instance-recovery]
sunbeam disable instance-recovery
# [docs-view:disable-instance-recovery-end]

# [docs-exec:disable-instance-recovery]
sg snap_daemon 'sunbeam disable instance-recovery'
# [docs-exec:disable-instance-recovery-end]