import datetime
import jwt
import re
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from creates_app import creates_app
from Model.models import *
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from helper.validation.mailCheck import validate_email
from helper.validation.creditCardCheck import validate_credit_card
