from pydantic import BaseModel, ConfigDict, field_validator


class UserSchema(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    @field_validator('username')
    def username_length(cls, v):
        assert len(v) >= 3, 'must be at least 3 characters'
        return v

    @field_validator('password')
    def password_length(cls, v):
        assert len(v) >= 8, 'must be at least 8 characters'
        return v


class UserPublicSchema(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(
        from_attributes=True,
    )


class UserListSchema(BaseModel):
    users: list[UserPublicSchema]
