import logging
import mimetypes
from pathlib import Path

from werkzeug.utils import secure_filename


logger = logging.getLogger(__name__)


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf",
}

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "application/pdf",
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def is_allowed_file(file):
    """
    Validate uploaded file name, type and size.

    Args:
        file: Uploaded file object.

    Returns:
        bool: True if file is allowed, otherwise False.
    """

    try:
        if not file or file.filename == "":
            return False

        filename = secure_filename(file.filename)

        if not filename:
            logger.warning("Blocked file upload: invalid filename")
            return False

        extension = Path(filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            logger.warning(
                "Blocked file upload: invalid extension %s",
                extension,
            )
            return False

        mime_type, _ = mimetypes.guess_type(filename)

        if mime_type not in ALLOWED_MIME_TYPES:
            logger.warning(
                "Blocked file upload: invalid mime type %s",
                mime_type,
            )
            return False

        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_FILE_SIZE:
            logger.warning(
                "Blocked file upload: file too large (%s bytes)",
                file_size,
            )
            return False

        return True

    except Exception:
        logger.exception("File validation failed")
        return False
