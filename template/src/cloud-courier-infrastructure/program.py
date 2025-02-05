import logging

from ephemeral_pulumi_deploy import get_aws_account_id
from ephemeral_pulumi_deploy import get_config
from pulumi import export

logger = logging.getLogger(__name__)


def pulumi_program() -> None:
    """Execute creating the stack."""
    env = get_config("proj:env")
    export("env", env)
    aws_account_id = get_aws_account_id()
    export("aws-account-id", aws_account_id)

    # Create Resources Here
