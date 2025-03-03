[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-black.json)](https://github.com/copier-org/copier)
[![Actions status](https://www.github.com/LabAutomationAndScreening/copier-cloud-courier-infrastructure/actions/workflows/ci.yaml/badge.svg?branch=main)](https://www.github.com/LabAutomationAndScreening/copier-cloud-courier-infrastructure/actions)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://www.github.com/LabAutomationAndScreening/copier-cloud-courier-infrastructure)


# Usage
To create a new repository using this template:
1. Install `copier` and `copier-templates-extensions`. An easy way to do that is to copy the `.devcontainer/install-ci-tooling.sh` script in this repository into your new repo and then run it.
2. Run copier to instantiate the template: `copier copy --trust gh:LabAutomationAndScreening/copier-cloud-courier-infrastructure.git`
3. Run `uv lock` to generate the lock file
4. Commit the changes
5. Rebuild your new devcontainer



# Development


## Updating from the template
This repository uses a copier template. To pull in the latest updates from the template, use the command:
`copier update --trust --conflict rej --defaults`
