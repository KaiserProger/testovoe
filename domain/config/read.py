from pydantic import parse_file_as
from domain.schemas.schemas import ConfigSchema


class ConfigReader:
    model: ConfigSchema

    def __init__(self) -> None:
        self.model = parse_file_as(ConfigSchema, "domain/config/config.json")
