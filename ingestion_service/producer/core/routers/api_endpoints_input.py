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
# @File    : api_endpoints_input.py
# @Software: PyCharm

from fastapi import APIRouter, HTTPException, Body
from fastapi import File, Form, UploadFile
from fastapi.responses import JSONResponse
from core.configure_rabbit_mq import publish_message
import logging
from core.file_validator import validate_file_extension, validate_mime_type
import json
from core.pydantic_schema import InputJSONSLdchema, InputJSONSchema, InputTextSchema
from core.shared import is_valid_jsonld


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ingest/file", summary="Ingest a either CSV, JSON, EXCEL, PDF, RDF, TTL, JSONLD or TEXT files")
async def ingest_file(id: str = Form(...), user: str = Form(...), filename: str = Form(...), file: UploadFile = File(...)):
    logger.info("Started ingestion operation")

    if not validate_mime_type(file.content_type):
        raise HTTPException(status_code=400, detail="Only CSV, JSON, EXCEL, PDF, RDF, TTL, JSONLD and TEXT files are supported.")

    if not validate_file_extension(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file extension. Supported extensions: csv, json, xls, txt and pdf")

    content = await file.read()
    publish_message(content)
    logger.info("Successful ingestion operation")
    return JSONResponse(content={"message": "File uploaded successfully", "id": id, "user": user, "filename": filename})

@router.post("/ingest/raw/json")
async def ingest_json(jsoninput: InputJSONSchema):
    try:
        parsed_json = json.loads(jsoninput)
        publish_message(parsed_json)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON" + str(e))

    return JSONResponse(content={"message": "File uploaded successfully"})

@router.post("/ingest/raw/jsonld")
async def ingest_json(jsonldinput: InputJSONSLdchema):
    try:
        parsed_json = jsonldinput
        if is_valid_jsonld(str(parsed_json)):
            publish_message(parsed_json)
            return JSONResponse(content={"message": "File uploaded successfully"})
        else:
            return JSONResponse(content={"message": "Invalid format data! Please provide correct JSON-LD data."})

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON" + str(e))



@router.post("/ingest/raw/text/")
async def ingest_text(text: InputTextSchema):
    text_data = text
    publish_message(text_data)
    return JSONResponse(content={"message": "File uploaded successfully"})