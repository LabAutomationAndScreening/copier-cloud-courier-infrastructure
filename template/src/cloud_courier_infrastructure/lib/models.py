from ephemeral_pulumi_deploy import append_resource_suffix
from pydantic import BaseModel
from pydantic import Field

from .courier_config_models import AppConfig
from .courier_config_models import FolderToWatch


class AlertingConfig(BaseModel, frozen=True):
    emails: list[str]  # TODO: validate email format
    timeout_seconds: int = 300
    """How long to wait without seeing a heartbeat before alerting."""
    # TODO: add periods not to alert during (e.g. at night when the computer is turned off)


class ComputerLocation(BaseModel, frozen=True):
    name: str


class LabComputerConfig(BaseModel, frozen=True):
    name: str  # TODO: validate/coerce to kebab-case # TODO: add length limit based on AWS resource constraints
    """What do you want this computer to be known as."""
    location: ComputerLocation
    original_name: str | None = None
    original_location: ComputerLocation | None = None
    alerting_config: AlertingConfig
    app_config: AppConfig = Field(default_factory=AppConfig)
    folders_to_watch: dict[str, FolderToWatch] = Field(default_factory=dict)

    @property
    def resource_name(self) -> str:
        return f"{self.location.name.lower()}--{self.name.lower()}"

    @property
    def original_resource_name(self) -> str:
        resource_name = self.resource_name
        if self.original_name is not None:
            assert self.original_location is not None  # TODO: make a test for this
            resource_name = f"{self.original_location.name.lower()}--{self.original_name.lower()}"
        return resource_name

    @property
    def immutable_full_resource_name(self) -> str:
        return append_resource_suffix(self.original_resource_name)
