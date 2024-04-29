# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# DISCLAIMER: This software is provided "as is" without any warranty,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose, and non-infringement.
#
# In no event shall the authors or copyright holders be liable for any
# claim, damages, or other liability, whether in an action of contract,
# tort, or otherwise, arising from, out of, or in connection with the
# software or the use or other dealings in the software.
# -----------------------------------------------------------------------------

# @Author  : Tek Raj Chhetri
# @Email   : tekraj@mit.edu
# @Web     : https://tekrajchhetri.com/
# @File    : text.py
# @Software: PyCharm

from fastapi import APIRouter, HTTPException
from fastapi import File, Form, UploadFile
from fastapi.responses import JSONResponse
from core.configure_rabbit_mq import publish_message
import logging
from core.file_validator import validate_file_extension, validate_mime_type


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ingest/text/file")
async def ingest_text(id: str = Form(...), filename: str = Form(...), file: UploadFile = File(...)):
    logger.info("Started ingestion operation")

    if not validate_mime_type(file.content_type):
        raise HTTPException(status_code=400, detail="Only CSV, JSON, EXCEL, PDF and TEXT files are supported.")

    if not validate_file_extension(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file extension. Supported extensions: csv, json, xls, txt and pdf")

    content = await file.read()
    publish_message(content)
    return JSONResponse(content={"message": "File uploaded successfully", "id": id, "filename": filename})
