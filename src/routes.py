from flask import Blueprint
from flask_restful import Api

from src.resources.resource_device import DeviceResourceList, DeviceResourceByUUID
from src.resources.resource_user import UserResourceList, UserResourceByUUID, UserResourceByUsername, \
    UserLoginResource, UserChangePasswordResource, UserVerifyResource
from src.system.resources.ping import Ping

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
bp_users = Blueprint('users', __name__, url_prefix='/api/users')
bp_devices = Blueprint('devices', __name__, url_prefix='/api/devices')

# 1
Api(bp_system).add_resource(Ping, '/ping')

# 2
api_users = Api(bp_users)
api_users.add_resource(UserResourceList, '')
api_users.add_resource(UserResourceByUUID, '/uuid/<string:uuid>')
api_users.add_resource(UserResourceByUsername, '/username/<string:username>')
api_users.add_resource(UserLoginResource, '/login', endpoint="login")
api_users.add_resource(UserChangePasswordResource, '/change_password')
api_users.add_resource(UserVerifyResource, '/verify')

# 3
api_devices = Api(bp_devices)
api_devices.add_resource(DeviceResourceList, '')
api_devices.add_resource(DeviceResourceByUUID, '/uuid/<string:uuid>')
