import datetime
import jwt
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from creates_app import creates_app
from Model.models import *
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from Middlewares.mailDomainCheck import check_mx_record
import re