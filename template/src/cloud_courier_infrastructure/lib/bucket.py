from ephemeral_pulumi_deploy import append_resource_suffix
from ephemeral_pulumi_deploy import common_tags_native
from pulumi import ComponentResource
from pulumi import ResourceOptions
from pulumi import export
from pulumi_aws.iam import GetPolicyDocumentStatementArgs
from pulumi_aws.iam import GetPolicyDocumentStatementConditionArgs
from pulumi_aws.iam import GetPolicyDocumentStatementPrincipalArgs
from pulumi_aws.iam import get_policy_document
from pulumi_aws.organizations import get_organization
from pulumi_aws_native import s3


def create_bucket_policy(bucket_name: str) -> str:
    org_id = get_organization().id
    return get_policy_document(
        statements=[
            GetPolicyDocumentStatementArgs(
                effect="Allow",
                actions=["s3:GetObject", "s3:GetObjectVersion", "s3:GetObjectVersionTagging", "s3:GetObjectTagging"],
                principals=[
                    GetPolicyDocumentStatementPrincipalArgs(
                        type="*",
                        identifiers=["*"],  # Allows all principals
                    )
                ],
                resources=[f"arn:aws:s3:::{bucket_name}/*"],
                conditions=[
                    GetPolicyDocumentStatementConditionArgs(
                        test="StringEquals",
                        variable="aws:PrincipalOrgID",
                        values=[org_id],  # Limit to the AWS Organization
                    ),
                ],
            ),
            GetPolicyDocumentStatementArgs(
                effect="Allow",
                principals=[GetPolicyDocumentStatementPrincipalArgs(type="*", identifiers=["*"])],
                actions=["s3:ListBucket", "s3:ListBucketVersions"],
                resources=[f"arn:aws:s3:::{bucket_name}"],
                conditions=[
                    GetPolicyDocumentStatementConditionArgs(
                        test="StringEquals", variable="aws:PrincipalOrgID", values=[org_id]
                    ),
                ],
            ),
        ]
    ).json


class RawDataBucket(ComponentResource):
    def __init__(
        self,
    ):
        super().__init__(
            "labauto:AwsOrgWideRawDataBucket",
            append_resource_suffix("raw-data-bucket"),
            None,
        )
        bucket = s3.Bucket(
            append_resource_suffix("raw-data-bucket"),
            opts=ResourceOptions(parent=self),
            versioning_configuration=s3.BucketVersioningConfigurationArgs(
                status=s3.BucketVersioningConfigurationStatus.ENABLED
            ),
            tags=common_tags_native(),
        )
        self.bucket_name = bucket.id

        _ = (
            s3.BucketPolicy(
                append_resource_suffix("raw-data-bucket-policy"),
                bucket=self.bucket_name,
                policy_document=self.bucket_name.apply(lambda bucket_name: create_bucket_policy(bucket_name)),
                opts=ResourceOptions(parent=self),
            ),
        )
        export(
            "raw-data-bucket-name", self.bucket_name
        )  # cross-stack reference used to generate the SSO Permission Set
