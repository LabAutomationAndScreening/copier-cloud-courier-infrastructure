from ephemeral_pulumi_deploy import append_resource_suffix
from ephemeral_pulumi_deploy import common_tags_native
from pulumi import ComponentResource
from pulumi import ResourceOptions
from pulumi import export
from pulumi_aws_native import s3


class SsmLogsBucket(ComponentResource):
    def __init__(
        self,
    ):
        super().__init__(
            "labauto:SsmLogsBucket",
            append_resource_suffix(),
            None,
        )
        bucket = s3.Bucket(
            append_resource_suffix("ssm-logs"),
            versioning_configuration=s3.BucketVersioningConfigurationArgs(
                status=s3.BucketVersioningConfigurationStatus.ENABLED
            ),
            object_lock_enabled=True,
            object_lock_configuration=s3.BucketObjectLockConfigurationArgs(
                object_lock_enabled="Enabled",
                rule=s3.BucketObjectLockRuleArgs(
                    default_retention=s3.BucketDefaultRetentionArgs(
                        mode=s3.BucketDefaultRetentionMode.GOVERNANCE, years=10
                    )
                ),
            ),
            tags=common_tags_native(),
            opts=ResourceOptions(parent=self),
        )
        self.bucket_name = bucket.id
        export(
            "ssm-logs-bucket-name", self.bucket_name
        )  # cross-stack reference used to generate the SSO Permission Set
