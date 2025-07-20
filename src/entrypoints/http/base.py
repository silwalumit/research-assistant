from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ApiRequestModelBase(BaseModel):
    model_config = ConfigDict(extra="forbid", alias_generator=to_camel)


class ApiResponseBase(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        use_enum_values=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
