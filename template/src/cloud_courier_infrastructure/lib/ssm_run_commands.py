import inspect
import json

import pulumi_aws
from ephemeral_pulumi_deploy import append_resource_suffix
from ephemeral_pulumi_deploy import common_tags_native
from pulumi import ComponentResource
from pulumi import ResourceOptions
from pulumi_aws_native import ssm

from .ssm_lib import FOLDER_SUBPATH
from .ssm_lib import LOGS_DIR
from .ssm_lib import STOP_FLAG_DIR
from .ssm_lib import add_boilerplate_to_ps_command_lines


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
                                "timeoutSeconds": 75,
                                "runCommand": add_boilerplate_to_ps_command_lines(
                                    inspect.cleandoc(
                                        "".join(
                                            [
                                                r"""
                                                $processName = "cloud-courier"  # without the .exe extension
                                                $process = Get-Process -Name $processName -ErrorAction SilentlyContinue

                                                if ($process) {
                                                    Write-Host "$processName is already running."
                                                } else {
                                                    Write-Host "$processName is not running."
                                                    """,
                                                rf"""
                                                    $destination = "$env:ProgramFiles\{FOLDER_SUBPATH}"
                                                    $exePath = "$destination\cloud-courier\cloud-courier.exe"
                                                    $stopFlagDir = "{STOP_FLAG_DIR}"
                                                    $logsDir = "{LOGS_DIR}"
                                                    $arguments = "--aws-region={pulumi_aws.config.region} --stop-flag-dir=$stopFlagDir --log-folder=$logsDir --no-console-logging"
                                                """,
                                                # console logging causes weird problems with SSM Run command interpreting it as a Powershell command to try and execute somehow
                                                r"""
                                                    $commandLine = "`"$exePath`" $arguments"
                                                    # Launch as a completely separate process. Using Start-Process will cause the SSM Command to hang, even without -Wait.
                                                    Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $commandLine }

                                                    # Initially wait for 10 seconds to ensure it started without error
                                                    Start-Sleep -Seconds 10
                                                    # Poll loop: check every 5 seconds if the process has started
                                                    $maxAttempts = 10
                                                    $attempt = 0
                                                    $runningProcess = $null

                                                    while ($attempt -lt $maxAttempts) {
                                                        $runningProcess = Get-Process -Name $processName -ErrorAction SilentlyContinue
                                                        if ($runningProcess) {
                                                            Write-Host "$processName has started successfully."
                                                            break
                                                        } else {
                                                            Write-Host "Waiting for $processName to start... (Attempt: $($attempt + 1))"
                                                            Start-Sleep -Seconds 5
                                                        }
                                                        $attempt++
                                                    }

                                                    if (-not $runningProcess) {
                                                        throw "Failed to detect $processName after $maxAttempts attempts."
                                                    }


                                                 }

                                            """,
                                            ]
                                        )
                                    ).split("\n")
                                ),
                            },
                        },
                    ],
                }
            ),
        )
        _ = ssm.Document(
            append_resource_suffix("StopCloudCourier-Windows"),
            opts=ResourceOptions(parent=self),
            document_type=ssm.DocumentType.COMMAND,
            update_method=ssm.DocumentUpdateMethod.NEW_VERSION,
            tags=common_tags_native(),
            content=json.dumps(
                {
                    "schemaVersion": "2.2",
                    "description": "Stop the executable running (if it's currently active).",
                    "mainSteps": [
                        {
                            "action": "aws:runPowerShellScript",
                            "name": "StartCloudCourier",
                            "precondition": {"StringEquals": ["platformType", "Windows"]},
                            "inputs": {
                                "timeoutSeconds": 600,
                                "runCommand": add_boilerplate_to_ps_command_lines(
                                    inspect.cleandoc(
                                        "".join(
                                            [
                                                r"""
                                                $processName = "cloud-courier"  # without the .exe extension
                                                $process = Get-Process -Name $processName -ErrorAction SilentlyContinue

                                                if ($process) {
                                                    Write-Host "$processName is already running."
                                                    """,
                                                rf"""
                                                    $stopFlagDir = "{STOP_FLAG_DIR}"
                                                    $uuid = [guid]::NewGuid().ToString()
                                                    $filePath = Join-Path -Path $stopFlagDir -ChildPath "$uuid.txt"
                                                    New-Item -ItemType File -Path $filePath -Force
                                                    """,
                                                r"""
                                                    # Poll loop: check every 5 seconds if the process has started
                                                    Start-Sleep -Seconds 15
                                                    $maxAttempts = 100
                                                    $attempt = 0
                                                    $runningProcess = $null

                                                    while ($attempt -lt $maxAttempts) {
                                                        $runningProcess = Get-Process -Name $processName -ErrorAction SilentlyContinue
                                                        if (-not $runningProcess) {
                                                            Write-Host "$processName has stopped successfully."
                                                            break
                                                        } else {
                                                            Write-Host "Waiting for $processName to stop... (Attempt: $($attempt + 1))"
                                                            Start-Sleep -Seconds 5
                                                        }
                                                        $attempt++
                                                    }

                                                    if ($runningProcess) {
                                                        throw "Failed to stop $processName after $maxAttempts attempts."
                                                    }
                                                """,
                                                r"""
                                                } else {
                                                    Write-Host "$processName is not running."
                                                 }

                                            """,
                                            ]
                                        )
                                    ).split("\n")
                                ),
                            },
                        },
                    ],
                }
            ),
        )
