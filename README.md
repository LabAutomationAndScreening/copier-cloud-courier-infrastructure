[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-black.json)](https://github.com/copier-org/copier)
[![Actions status](https://www.github.com/LabAutomationAndScreening/copier-cloud-courier-infrastructure/actions/workflows/ci.yaml/badge.svg?branch=main)](https://www.github.com/LabAutomationAndScreening/copier-cloud-courier-infrastructure/actions)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://www.github.com/LabAutomationAndScreening/copier-cloud-courier-infrastructure)


# Usage
To create a new repository using this template:
1. Create a basic devcontainer either using the Codespaces default or using the file `.devcontainer/devcontainer-to-instantiate-template.json` from [the base template repo](https://github.com/LabAutomationAndScreening/copier-base-template/blob/main/.devcontainer/devcontainer-to-instantiate-template.json)
1. Inside that devcontainer, run `python .devcontainer/install-ci-tooling.py` to install necessary tooling to instantiate the template (you can copy/paste the script from this
1. Delete all files currently in the repository. Optional...but makes it easiest to avoid git conflicts.
1. Run copier to instantiate the template: `copier copy --trust gh:LabAutomationAndScreening/copier-cloud-courier-infrastructure.git .`
1. Run `python .devcontainer/manual-setup-deps.py --optionally-check-lock` to generate the lock file(s)
1. Stage all files to prepare for commit (`git add .`)
1. Run `python3 .github/workflows/hash_git_files.py . --for-devcontainer-config-update` to update the hash for your devcontainer file
1. Commit the changes (optional)
1. Rebuild your new devcontainer



# Development


## Updating from the template
This repository uses a copier template. To pull in the latest updates from the template, use the command:
`copier update --trust --conflict rej --defaults`
