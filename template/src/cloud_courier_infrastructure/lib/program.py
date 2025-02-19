import logging

from ephemeral_pulumi_deploy import get_aws_account_id
from ephemeral_pulumi_deploy import get_config
from pulumi import export

from ..computers import create_all_computer_configs
from . import CloudCourierAgentInstaller
from . import CloudCourierSsmCommands
from . import Dashboard
from . import DistributorFileToPackage
from . import NodeAlert
from . import OnPremNode
from . import RawDataBucket
from . import SsmLogsBucket
from .constants import DOWNLOAD_EXE_FROM_GITHUB

logger = logging.getLogger(__name__)


def pulumi_program() -> None:
    """Execute creating the stack."""
    env = get_config("proj:env")
    export("env", env)
    aws_account_id = get_aws_account_id()
    export("aws-account-id", aws_account_id)

    # Create Resources Here
    # TODO: add ability for custom bucket lifecycle policy
    # TODO: add ability for customization of the bucket policy
    raw_data_bucket = RawDataBucket()
    ssm_logs_bucket = SsmLogsBucket()
    _ = CloudCourierSsmCommands()
    all_computer_configs = create_all_computer_configs()
    all_node_alerts: list[NodeAlert] = []
    for computer_config in all_computer_configs:
        _ = OnPremNode(
            lab_computer_config=computer_config,
            ssm_logs_bucket_name=ssm_logs_bucket.bucket_name,
            data_bucket_name=raw_data_bucket.bucket_name,
        )
        all_node_alerts.append(NodeAlert(lab_computer_config=computer_config))
    _ = Dashboard(node_alerts=all_node_alerts)
    _ = CloudCourierAgentInstaller(
        version="0.0.3",
        files_to_package=[
            DistributorFileToPackage(
                source_path="s3://manual-artifacts--artifact-stores--prod-82ba004/cloud-courier/v0.0.3/exe-windows-2022-3.12.7.zip",
                local_name="exe-v0.0.3.zip",
            )
        ],
        download_exe_from_github=DOWNLOAD_EXE_FROM_GITHUB,
    )
