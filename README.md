# Canonical OpenStack Documentation

[![Automatic doc checks](https://github.com/canonical/canonical-openstack-docs/actions/workflows/automatic-doc-checks.yml/badge.svg)](https://github.com/canonical/canonical-openstack-docs/actions/workflows/automatic-doc-checks.yml)

This repository contains the source for the [Canonical OpenStack documentation](https://canonical-openstack.readthedocs.io/).

Canonical OpenStack is an enterprise-grade cloud platform that delivers distilled upstream OpenStack excellence in a human-friendly product. It provides elastic, on-demand compute, network, and storage resources through a self-service portal or upstream OpenStack APIs.

## Documentation Structure

The documentation follows the [Diátaxis](https://diataxis.fr) framework:

- **Tutorials** – Hands-on introduction for new users
- **How-to guides** – Step-by-step guides for key operations and common tasks
- **Reference** – Technical specifications, APIs, architecture
- **Explanation** – Discussion and clarification of key topics

## Quickstart

### Prerequisites

- Python 3.10+
- `make`
- `git`

### Build Locally

```bash
git clone git@github.com:canonical/canonical-openstack-docs.git
cd canonical-openstack-docs/docs
make html serve
```

To preview with live reload at `http://127.0.0.1:8000`:

```bash
make run
```

### Run Checks Locally

```bash
make spelling      # Check spelling
make linkcheck     # Validate links
make woke          # Check inclusive language
make lint-md       # Check Markdown style
make vale          # Check style guide compliance (optional)
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Reporting issues
- Development setup
- Making changes
- Running tests
- Opening pull requests
- Code review process

### Quick Contribution Steps

1. Fork the repository
2. Create a branch: `git checkout -b <issue-id>-<description>`
3. Make your changes in the `docs/` directory
4. Build and test locally: `cd docs && make html && make spelling && make linkcheck`
5. Commit with a signed commit: `git commit -S -m "feat: your change"`
6. Push and open a PR

All contributions require a signed [Canonical Contributor License Agreement](https://ubuntu.com/legal/contributors).

## Community and Support

### Community (Sunbeam / Open Source)

- [Report a bug](https://bugs.launchpad.net/snap-openstack/+filebug)
- [Join the community chat](https://matrix.to/#/#openstack-sunbeam:ubuntu.com)
- [Contribute to Sunbeam](https://github.com/canonical/snap-openstack)

### Commercial (Canonical OpenStack)

- [Explore Canonical OpenStack](https://canonical.com/openstack)
- [Get Ubuntu Pro subscription](https://ubuntu.com/pro/subscribe)
- [Contact Canonical cloud experts](https://canonical.com/openstack#get-in-touch)

## License

This documentation is licensed under [GPL-3.0](LICENSE).
