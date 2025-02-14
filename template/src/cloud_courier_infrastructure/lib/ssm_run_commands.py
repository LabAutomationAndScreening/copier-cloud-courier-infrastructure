import json

from ephemeral_pulumi_deploy import append_resource_suffix
from ephemeral_pulumi_deploy import common_tags_native
from pulumi import ComponentResource
from pulumi import ResourceOptions
from pulumi_aws_native import ssm


def add_boilerplate_to_ps_command_lines(commands: list[str]) -> list[str]:
    """Add boilerplate.

    In place update of list to add powershell for error trapping and logging.

    Returns:
        The list. This allows for easier function chaining
    """
    commands[:0] = [
        "Set-PSDebug -Trace 1",
        "$ErrorActionPreference = 'Stop'",
        "whoami",
        "try {",
    ]
    commands.extend(
        [
            "} catch {",
            "$_",
            "exit 1",
            "}",
        ]
    )
    return commands


def add_boilerplate_to_ps_script(script: str) -> str:
    commands = [script]
    _ = add_boilerplate_to_ps_command_lines(commands)
    return "\n".join(commands)


class CloudCourierSsmCommands(ComponentResource):
    def __init__(
        self,
    ):
        super().__init__(
            "labauto:cloud-courier",
            append_resource_suffix("ssm-commands"),
            None,
        )
        _ = ssm.Document(
            append_resource_suffix("StartCloudCourier-Windows"),
            opts=ResourceOptions(parent=self),
            document_type=ssm.DocumentType.COMMAND,
            update_method=ssm.DocumentUpdateMethod.NEW_VERSION,
            tags=common_tags_native(),
            content=json.dumps(
                {
                    "schemaVersion": "2.2",
                    "description": "Start the executable running (if it's not already).",
                    "mainSteps": [
                        {
                            "action": "aws:runPowerShellScript",
                            "name": "StartCloudCourier",
                            "precondition": {"StringEquals": ["platformType", "Windows"]},
                            "inputs": {
                                "timeoutSeconds": 10,
                                "runCommand": add_boilerplate_to_ps_command_lines(['echo "Hello, World!"']),
                            },
                        },
                    ],
                }
            ),
        )
