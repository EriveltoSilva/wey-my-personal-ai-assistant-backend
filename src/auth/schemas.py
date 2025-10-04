"""Security module for schemas in authentication."""

from pydantic import BaseModel, ConfigDict, Field


class VerifyTokenRequestDTO(BaseModel):
    """Data Transfer Object for token verification request."""

    token: str = Field(..., description="Access token to be verified")

    model_config = ConfigDict(from_attributes=True, json_schema_extra={"example": {"token": "<TOKEN>"}})


class TokenResponseDTO(BaseModel):
    """Data Transfer Object for authentication token."""

    access_token: str = Field(description="Access token for the user")
    token_type: str = Field(default="Bearer", description="Type of the token")

    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"example": {"access_token": "<PASSWORD>", "token_type": "Bearer"}}
    )


class SignInWithUsernameRequestDTO(BaseModel):
    """Data Transfer Object for user login request."""

    username: str = Field(max_length=100, description="Username of the user")
    password: str = Field(min_length=6, max_length=32, description="Password of the user")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"username": "agostinho.neto@gmail.com", "password": "password123"}},
    )


class SignInWithPhoneNumberRequestDTO(BaseModel):
    """Data Transfer Object for user login request."""

    phone: str = Field(max_length=13, description="Phone Number of the user")
    password: str = Field(min_length=6, max_length=32, description="Password of the user")

    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"example": {"phone": "940000000", "password": "password123"}}
    )
