from flask import Blueprint

auth = Blueprint('auth', __name__)
#这里主要处理用户系统的
from . import views
