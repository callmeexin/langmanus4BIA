"""SQLAlchemy model for storing file metadata and tracking processing states."""

from datetime import datetime
from typing import List
from typing import TypeVar, Dict, Any, Generic

from pydantic import BaseModel
from typing import Optional, Union
from pydantic import BaseModel, Field


class ContentItem(BaseModel):
    type: str = Field(..., description="The type of content (text, image, etc.)")
    text: Optional[str] = Field(None, description="The text content if type is 'text'")
    image_url: Optional[str] = Field(
        None, description="The image URL if type is 'image'"
    )


class ChatMessage(BaseModel):
    role: str = Field(
        ..., description="The role of the message sender (user or assistant)"
    )
    content: Union[str, List[ContentItem]] = Field(
        ...,
        description="The content of the message, either a string or a list of content items",
    )


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="The user input")
    debug: Optional[bool] = Field(False, description="Whether to enable debug logging")
    deep_thinking_mode: Optional[bool] = Field(
        False, description="Whether to enable deep thinking mode"
    )
    search_before_planning: Optional[bool] = Field(
        False, description="Whether to search before planning"
    )
    team_members: Optional[list] = Field(None, description="enabled team members")
    thread_id: Optional[str] = Field(
        "default", description="a specifc conversation identifier"
    )


class FileMetadataBase(BaseModel):
    session_id: str
    name: str
    path: str
    size: int

class FileMetadataCreate(FileMetadataBase):
    pass

class FileMetadata(FileMetadataBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FileListResponse(BaseModel):
    code: str
    figures: List[str]
    results: List[str]

class FileUploadResponse(BaseModel):
    id: int
    metadata: FileMetadata

class FileContentResponse(BaseModel):
    content: str



T = TypeVar("T")

DEFAULT_SUCCESS_CODE: int = 0
DEFAULT_FAIL_CODE: int = -1
DEFAULT_SUCCESS_MSG: str = "success"

class HttpResponse(BaseModel, Generic[T]):
    @staticmethod
    def success(
        data: T = None,
        msg: str = DEFAULT_SUCCESS_MSG,
        code: int = DEFAULT_SUCCESS_CODE,
    ) -> Dict[str, Any]:
        """
        Generate a success response dictionary

        Args:
            data: Response data of generic model DataType
            msg: Success message
            code: Success status code

        Returns:
            Dict containing response data
        """
        response = {"code": code, "msg": msg}
        if data is not None:
            response["data"] = data
        return response

    @staticmethod
    def fail(msg: str, code: int = DEFAULT_FAIL_CODE) -> Dict[str, Any]:
        """
        Generate a failure response dictionary

        Args:
            msg: Error message
            code: Error status code

        Returns:
            Dict containing error response
        """
        return {"code": code, "msg": msg}