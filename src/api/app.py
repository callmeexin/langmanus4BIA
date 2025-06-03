"""
FastAPI application for BiaGhosterCoder.
"""

import asyncio
import json
import logging
import os
import os.path
from pathlib import Path
from typing import List


from src.config.config import DEFAULT_WORK
from src.database import SessionLocal, engine
from src.entity.entity import FileMetadata as DBFileMetadata
from src.schema.schemas import HttpResponse, ChatRequest
from src.utils.file_utils import save_file, get_file_path, delete_file_async, list_files_in_task
from fastapi import HTTPException, Request
from fastapi import UploadFile, File, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi_offline import FastAPIOffline

from sse_starlette.sse import EventSourceResponse

from src.config import TEAM_MEMBER_CONFIGRATIONS, BROWSER_HISTORY_DIR
from src.graph import build_graph
from src.service.workflow_service import run_agent_workflow

# Configure logging
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPIOffline(
    root_path="/api",
    title="BiaGhosterCoder API",
    description="API for BiaGhosterCoder LangGraph-based agent workflow",
    version="0.1.0",
)
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create database tables
DBFileMetadata.metadata.create_all(bind=engine)

@app.post("/upload/")
async def upload_files(
        session_id: str = Form(),
        files: List[UploadFile] = File(...),
        storage_path: str = str(DEFAULT_WORK)
):
    """Upload multiple files and store their metadata in database.

    Args:
        session_id: ID of the current session
        files: List of files to upload
        storage_path: Path to store the files (defaults to DEFAULT_STORAGE)

    Returns:
        List of FileUploadResponse containing file IDs and metadata
    """
    results = []
    db = SessionLocal()

    try:
        for file in files:
            # Save file
            file_info = await save_file(session_id, file, Path(storage_path))

            # Save metadata to database
            db_file = DBFileMetadata(
                session_id=session_id,
                name=file.filename,
                path=file_info["path"],
                size=file_info["size"]
            )
            db.add(db_file)
            db.commit()
            db.refresh(db_file)

            results.append(db_file.path)

        return HttpResponse.success(results)
    finally:
        db.close()

@app.get("/files/{session_id}/{task_id}")
def get_files_by_task_id(session_id: str, task_id: str):
    """List all files associated with a specific task.

    Args:
        session_id: ID of the current session
        task_id: ID of the task to list files for

    Returns:
        FileListResponse containing list of files
    """
    result = list_files_in_task(session_id, task_id)
    return HttpResponse.success(result)

@app.get("/download/")
def download_file(session_id: str, task_id: str, filename: str):
    """Download a specific file by its filename.

    Args:
        session_id: ID of the current session
        task_id: ID of the associated task
        filename: Name of the file to download

    Returns:
        FileResponse for downloading the file

    Raises:
        HTTPException: 404 if file not found
    """
    session_id = "session_id"
    task_id = "task_id"
    file_path = get_file_path(session_id, task_id, filename)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

@app.get("/content/")
def get_file_content(session_id: str, task_id: str, filename: str):
    """Get the content of a text file as string.

    Args:
        session_id: ID of the current session
        task_id: ID of the associated task
        filename: Name of the file to read

    Returns:
        FileContentResponse containing file content

    Raises:
        HTTPException: 404 if file not found, 400 if read error
    """
    file_path = get_file_path(session_id, task_id, filename)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "r") as f:
            content = f.read()
        return HttpResponse.success({"content": content})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

@app.delete("/delete/")
def delete_file(
        background_tasks: BackgroundTasks,
        session_id: str,
        task_id: str,
        filename: str,
        file_id: int
):
    """Delete a file and its metadata (async operation).

    Args:
        background_tasks: FastAPI background tasks handler
        session_id: ID of the current session
        task_id: ID of the associated task
        filename: Name of the file to delete
        file_id: Database ID of the file metadata

    Returns:
        dict: Message confirming deletion scheduling

    Raises:
        HTTPException: 404 if file or metadata not found
    """
    file_path = get_file_path(session_id, task_id, filename)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    # Delete record from database
    db = SessionLocal()
    db_file = db.query(DBFileMetadata).filter(DBFileMetadata.id == file_id).first()
    if not db_file:
        db.close()
        raise HTTPException(status_code=404, detail="File metadata not found")

    db.delete(db_file)
    db.commit()
    db.close()

    # Async file deletion
    background_tasks.add_task(delete_file_async, file_path)

    return {"message": "File deletion scheduled"}

@app.get("/image/")
async def get_image(img_path: str) -> FileResponse:
    """Retrieve an image file by its relative path.

    Fetches and returns an image file from the default storage directory based on the provided relative path.
    The image can be directly previewed in browsers or used by frontend applications.

    Args:
        img_path (str): Relative path to the image from the default storage directory.
                       Example: 'products/123.jpg' or 'users/avatar.png'

    Returns:
        FileResponse: FastAPI FileResponse object that streams the image file with proper
                     content-type headers for browser preview.

    Raises:
        HTTPException 400: If the path is invalid or contains directory traversal attempts
        HTTPException 404: If the requested image doesn't exist

    Examples:
        Example request:
        ```http
        GET /image/?img_path=products/123.jpg
        ```

        Example response:
        ```http
        HTTP/1.1 200 OK
        Content-Type: image/jpeg
        [image binary data]
        ```
    """
    # Security check: prevent directory traversal attacks
    if not img_path or '../' in img_path:
        raise HTTPException(status_code=400, detail="Invalid image path")

    image_abs_path = os.path.join(str(DEFAULT_WORK), img_path)

    # Verify file exists
    if not os.path.isfile(image_abs_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_abs_path)
# Create the graph
graph = build_graph()


@app.post("/chat/stream")
async def chat_endpoint(request: ChatRequest, req: Request):
    """
    Chat endpoint for LangGraph invoke.

    Args:
        request: The chat request
        req: The FastAPI request object for connection state checking

    Returns:
        The streamed response
    """
    try:
        # Convert Pydantic models to dictionaries and normalize content format
        messages = []
        for msg in request.messages:
            message_dict = {"role": msg.role}

            # Handle both string content and list of content items
            if isinstance(msg.content, str):
                message_dict["content"] = msg.content
            else:
                # For content as a list, convert to the format expected by the workflow
                content_items = []
                for item in msg.content:
                    if item.type == "text" and item.text:
                        content_items.append({"type": "text", "text": item.text})
                    elif item.type == "image" and item.image_url:
                        content_items.append(
                            {"type": "image", "image_url": item.image_url}
                        )

                message_dict["content"] = content_items

            messages.append(message_dict)

        async def event_generator():
            try:
                async for event in run_agent_workflow(
                    messages,
                    request.debug,
                    request.deep_thinking_mode,
                    request.search_before_planning,
                    request.team_members,
                    request.session_id,
                ):
                    # Check if client is still connected
                    if await req.is_disconnected():
                        logger.info("Client disconnected, stopping workflow")
                        break
                    yield {
                        "event": event["event"],
                        "data": json.dumps(event["data"], ensure_ascii=False),
                    }
            except asyncio.CancelledError:
                logger.info("Stream processing cancelled")
                raise
            except Exception as e:
                logger.error(f"Error in workflow: {e}")
                raise

        return EventSourceResponse(
            event_generator(),
            media_type="text/event-stream",
            sep="\n",
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/browser_history/{filename}")
async def get_browser_history_file(filename: str):
    """
    Get a specific browser history GIF file.

    Args:
        filename: The filename of the GIF to retrieve

    Returns:
        The GIF file
    """
    try:
        file_path = os.path.join(BROWSER_HISTORY_DIR, filename)
        if not os.path.exists(file_path) or not filename.endswith(".gif"):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(file_path, media_type="image/gif", filename=filename)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving browser history file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/team_members")
async def get_team_members():
    """
    Get the configuration of all team members.

    Returns:
        dict: A dictionary containing team member configurations
    """
    try:
        return {"team_members": TEAM_MEMBER_CONFIGRATIONS}
    except Exception as e:
        logger.error(f"Error getting team members: {e}")
        raise HTTPException(status_code=500, detail=str(e))


