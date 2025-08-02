# adapted from https://github.com/copier-org/copier-template-extensions#context-hook-extension
from typing import Any
from typing import override

from copier_template_extensions import ContextHook


class ContextUpdater(ContextHook):
    update = False

    @override
    def hook(self, context: dict[Any, Any]) -> dict[Any, Any]:
        context["uv_version"] = "0.8.3"
        context["pnpm_version"] = "10.14.0"
        context["pre_commit_version"] = "4.2.0"
        context["pyright_version"] = "1.1.403"
        context["pytest_version"] = "8.4.1"
        context["pytest_randomly_version"] = "3.16.0"
        context["pytest_cov_version"] = "6.2.1"
        context["copier_version"] = "9.8.0"
        context["copier_template_extensions_version"] = "0.3.2"
        context["sphinx_version"] = "8.1.3"
        context["pulumi_version"] = "3.186.0"
        context["pulumi_aws_version"] = "7.1.0"
        context["pulumi_aws_native_version"] = "1.31.0"
        context["pulumi_command_version"] = "1.1.0"
        context["pulumi_github_version"] = "6.7.3"
        context["pulumi_okta_version"] = "4.20.0"
        context["boto3_version"] = "1.39.14"
        context["ephemeral_pulumi_deploy_version"] = "0.0.4"
        context["pydantic_version"] = "2.11.7"
        context["pyinstaller_version"] = "6.13.0"
        context["setuptools_version"] = "80.7.1"
        context["strawberry_graphql_version"] = "0.270.4"
        context["fastapi_version"] = "0.115.14"
        context["uvicorn_version"] = "0.35.0"
        context["lab_auto_pulumi_version"] = "0.1.15"

        context["nuxt_ui_version"] = "^3.3.0"
        context["nuxt_version"] = "^3.18.0"
        context["typescript_version"] = "^5.8.2"
        context["dot_env_cli_version"] = "^9.0.0"
        context["playwright_version"] = "^1.52.0"
        context["vue_version"] = "^3.5.18"
        context["vue_router_version"] = "^4.5.1"
        context["faker_version"] = "^9.9.0"
        context["graphql_codegen_cli_version"] = "^5.0.5"
        context["graphql_codegen_typescript_version"] = "^4.1.6"

        context["gha_checkout"] = "v4.2.2"
        context["gha_setup_python"] = "v5.6.0"
        context["gha_cache"] = "v4.2.3"
        context["gha_upload_artifact"] = "v4.6.2"
        context["gha_download_artifact"] = "v4.3.0"
        context["gha_github_script"] = "v7.0.1"
        context["gha_setup_buildx"] = "v3.10.0"
        context["buildx_version"] = "v0.22.0"
        context["gha_docker_build_push"] = "v6.16.0"
        context["gha_configure_aws_credentials"] = "v4.2.0"
        context["gha_amazon_ecr_login"] = "v2.0.1"
        context["gha_setup_node"] = "v4.4.0"
        context["gha_action_gh_release"] = "v2.2.1"
        context["gha_mutex"] = "1ebad517141198e08d47cf72f3c0975316620a65 # v1.0.0-alpha.10"
        context["gha_pypi_publish"] = "v1.12.4"
        context["gha_sleep"] = "v2.0.3"
        context["gha_linux_runner"] = "ubuntu-24.04"
        context["gha_windows_runner"] = "windows-2025"

        context["py311_version"] = ""
        context["py312_version"] = "3.12.7"
        context["py313_version"] = "3.13.2"

        context["debian_release_name"] = "bookworm"
        context["alpine_image_version"] = "3.21"
        context["nginx_image_version"] = "1.28.0"

        # Kludge to be able to help symlinked jinja files in the child and grandchild templates
        context["template_uses_vuejs"] = False
        context["template_uses_javascript"] = False
        return context
