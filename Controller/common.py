from flask import jsonify, request
import datetime
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from sqlalchemy.exc import IntegrityError
from create_app import create_app
from Model.models import *
from helper.userValidation import validate_password, validate_email, validate_credit_card
from helper.sendMail import send_email
from flasgger import  swag_from