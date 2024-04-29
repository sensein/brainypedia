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
# @File    : databases.py
# @Software: PyCharm

import datetime

import sqlalchemy as sa

# https://docs.sqlalchemy.org/en/20/core/metadata.html
metadata = sa.MetaData()

# JWT User Table
jwt_user_table = sa.Table(
    "jwt_user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String, unique=True, nullable=False),
    sa.Column("password", sa.String, nullable=False),
    sa.Column(
        "created_at", sa.DateTime, nullable=False, default=datetime.datetime.utcnow
    ),
    sa.Column(
        "updated_at",
        sa.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    ),
)
