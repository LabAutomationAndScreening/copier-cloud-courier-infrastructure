import math
from typing import Any

from ephemeral_pulumi_deploy import append_resource_suffix
from ephemeral_pulumi_deploy import common_tags_native
from pulumi import ComponentResource
from pulumi import Output
from pulumi import ResourceOptions
from pulumi_aws_native import cloudwatch
from pulumi_aws_native import sns

from .courier_config_models import CLOUDWATCH_HEARTBEAT_NAMESPACE
from .courier_config_models import CLOUDWATCH_INSTANCE_ID_DIMENSION_NAME
from .courier_config_models import HEARTBEAT_METRIC_NAME
from .models import LabComputerConfig


class NodeAlert(ComponentResource):
    def __init__(
        self,
        *,
        lab_computer_config: LabComputerConfig,
    ):
        super().__init__(
            "labauto:OnPremComputerAlert",
            lab_computer_config.immutable_full_resource_name,
            None,
        )
        self.lab_computer_config = lab_computer_config
        sns_topic = sns.Topic(
            append_resource_suffix(f"{lab_computer_config.resource_name}-alert"),
            opts=ResourceOptions(parent=self),
            tags=common_tags_native(),
        )
        # TODO: consider some sort of different structure where there's just a single SNS topic per email address...that may result in fewer "SNS Subscription" emails
        for email_address in lab_computer_config.alerting_config.emails:
            formatted_address = email_address.replace("@", "-at-").replace(".", "-dot-")
            _ = sns.Subscription(
                append_resource_suffix(f"{lab_computer_config.resource_name}--{formatted_address}", max_length=100),
                topic_arn=sns_topic.topic_arn,
                protocol="email",
                endpoint=email_address,
                opts=ResourceOptions(parent=self),
            )
        self.alarm = cloudwatch.Alarm(
            append_resource_suffix(lab_computer_config.resource_name),
            comparison_operator="LessThanThreshold",
            evaluation_periods=1,
            alarm_description=f"The CloudCourier agent for {lab_computer_config.name} at {lab_computer_config.location.name} is unresponsive.",
            alarm_name=lab_computer_config.immutable_full_resource_name,
            metric_name=HEARTBEAT_METRIC_NAME,
            namespace=CLOUDWATCH_HEARTBEAT_NAMESPACE,
            period=lab_computer_config.alerting_config.timeout_seconds,
            statistic="Sum",
            threshold=1,
            treat_missing_data="breaching",
            dimensions=[
                cloudwatch.AlarmDimensionArgs(name="Application", value="CloudCourier"),
                cloudwatch.AlarmDimensionArgs(
                    name=CLOUDWATCH_INSTANCE_ID_DIMENSION_NAME, value=lab_computer_config.immutable_full_resource_name
                ),
            ],
            alarm_actions=[sns_topic.topic_arn],
            opts=ResourceOptions(parent=self),
            tags=common_tags_native(),
        )


class Dashboard(ComponentResource):
    def __init__(
        self,
        *,
        node_alerts: list[NodeAlert],
    ):
        super().__init__(
            "labauto:OnPremComputerStatusDashboard",
            append_resource_suffix("computer-status-dashboard", max_length=100),
            None,
        )
        widgets: list[dict[str, Any]] = []  # TODO: use JSON type hint

        # Define dimensions for metric widgets.
        widget_width = 6
        widget_height = 6

        alarm_status_height = 2

        # Create a metric widget for each installation.
        for index, node_alert in enumerate(node_alerts):
            metric_widget: dict[str, Any] = {
                "type": "metric",
                "x": widget_width * math.floor((index) / 2),
                "y": index * widget_height + alarm_status_height,  # Stack widgets vertically.
                "width": widget_width,
                "height": widget_height,
                "properties": {
                    "metrics": [
                        [
                            "CloudCourier/Heartbeat",
                            HEARTBEAT_METRIC_NAME,
                            "Application",
                            "CloudCourier",
                            CLOUDWATCH_INSTANCE_ID_DIMENSION_NAME,
                            node_alert.lab_computer_config.immutable_full_resource_name,
                        ]
                    ],
                    "period": 60,
                    "stat": "Sum",
                    "region": "us-east-1",  # Update to your region.
                    "title": f"Heartbeat for {node_alert.lab_computer_config.name} at {node_alert.lab_computer_config.location.name}",
                },
            }
            widgets.append(metric_widget)

        # Create an alarm widget that lists all installation alarms.
        # Assume you have one alarm per installation with names like "MyAppHeartbeatAlarm-inst1", etc.
        alarm_names = [inst.alarm.arn for inst in node_alerts]

        alarm_widget = {
            "type": "alarm",
            "x": 0,  # Position this widget to the right of the metric widgets.
            "y": 0,
            "width": widget_width * 2,
            "height": alarm_status_height,
            "properties": {"alarms": alarm_names, "title": "Upload Agent Alarm Status"},
        }

        widgets.append(alarm_widget)

        dashboard_body = Output.json_dumps({"widgets": widgets})

        _ = cloudwatch.Dashboard(
            append_resource_suffix("agent-status"),
            dashboard_body=dashboard_body,
            opts=ResourceOptions(parent=self),
            dashboard_name=append_resource_suffix("agent-status"),
        )
        # TODO: figure out way to export the URL to the dashboard
