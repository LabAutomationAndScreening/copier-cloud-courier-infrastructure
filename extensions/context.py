# adapted from https://github.com/copier-org/copier-templates-extensions#context-hook-extension
from typing import Any
from typing import override

from copier_templates_extensions import ContextHook


class ContextUpdater(ContextHook):
    update = False

    @override
    def hook(self, context: dict[Any, Any]) -> dict[Any, Any]:
        context["uv_version"] = "0.5.28"
        context["pre_commit_version"] = "4.0.1"
        context["pyright_version"] = "1.1.394"
        context["pytest_version"] = "8.3.4"
        context["pytest_randomly_version"] = "3.16.0"
        context["pytest_cov_version"] = "6.0.0"
        context["copier_version"] = "9.4.1"
        context["copier_templates_extension_version"] = "0.3.0"
        context["sphinx_version"] = "8.1.3"
        context["pulumi_version"] = "3.149.0"
        context["pulumi_aws_version"] = "6.67.0"
        context["pulumi_aws_native_version"] = "1.25.0"
        context["pulumi_command_version"] = "1.0.1"
        context["boto3_version"] = "1.36.3"
        context["ephemeral_pulumi_deploy_version"] = "0.0.2"
        context["pydantic_version"] = "2.10.6"
        context["pyinstaller_version"] = "6.12.0"

        context["gha_checkout"] = "v4.2.2"
        context["gha_setup_python"] = "v5.3.0"
        context["gha_cache"] = "v4.2.0"
        context["gha_upload_artifact"] = "v4.4.3"
        context["gha_configure_aws_credentials"] = "v4.0.2"
        context["gha_mutex"] = "d3d5b354d460d4b6a1e3ee5b7951678658327812 # v1.0.0-alpha.9"
        context["gha_linux_runner"] = "ubuntu-24.04"
        context["gha_windows_runner"] = "windows-2022"

        context["py311_version"] = ""
        context["py312_version"] = "3.12.7"
        context["py313_version"] = "3.13.1"
        return context
