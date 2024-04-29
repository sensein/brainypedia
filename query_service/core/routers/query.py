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
# @File    : query.py
# @Software: PyCharm
from fastapi import APIRouter, Body
from core.graph_database_connection_manager import fetch_data_gdb

router = APIRouter()

@router.get("/query/sparql/")
async def sparql_query(sparql_query: str ):
    response = fetch_data_gdb(sparql_query)
    return response