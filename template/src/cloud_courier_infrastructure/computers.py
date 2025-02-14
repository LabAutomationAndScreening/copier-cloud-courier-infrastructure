from .lib import AlertingConfig
from .lib import ComputerLocation
from .lib import FolderToWatch
from .lib import LabComputerConfig

EXAMPLE_LAB_NAME = ComputerLocation(name="Cambridge")
example_computer_config = LabComputerConfig(
    name="Cytation-5",
    location=EXAMPLE_LAB_NAME,
    alerting_config=AlertingConfig(emails=["gregor.mendel@gmail.com"]),
    folders_to_watch={"images": FolderToWatch(folder_path=r"C:\data\images")},
)


def create_all_computer_configs() -> list[LabComputerConfig]:
    all_computers: list[LabComputerConfig] = []

    all_computers.extend(
        [
            # Put LabComputerConfig objects here
        ]
    )

    return all_computers
