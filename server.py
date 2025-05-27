"""
Server script for running the BiaGhosterCoder API.
"""

import logging
import uvicorn
import sys

from src.utils.path_utils import find_and_add_target_path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

find_and_add_target_path()
logger.info(sys.path)

if __name__ == "__main__":
    logger.info("Starting BiaGhosterCoder API server")
    reload = False
    if sys.platform.startswith("win"):
        reload = False
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=reload,
        log_level="info",
    )
