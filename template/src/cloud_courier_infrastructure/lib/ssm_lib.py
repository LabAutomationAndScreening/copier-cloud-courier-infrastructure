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


FOLDER_SUBPATH = r"LabAutomationAndScreening\CloudCourier"
STOP_FLAG_DIR = rf"$env:ProgramData\{FOLDER_SUBPATH}\stop-flag"
LOGS_DIR = rf"$env:ProgramData\{FOLDER_SUBPATH}\logs"
