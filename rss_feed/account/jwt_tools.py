# In the name of GOD

from django.core.cache import caches
from django.conf import settings

from rest_framework.exceptions import AuthenticationFailed, ParseError

from datetime import timedelta, datetime
import uuid
import jwt





def decode_jwt_token(jwt_token):
    try:
        # jw_key = jwk_from_dict({'kty':'oct', 'k':settings.SECRET_KEY[:-1]})
        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        return None, AuthenticationFailed('Invalid signature')
    except jwt.exceptions.ExpiredSignatureError:
        return None, AuthenticationFailed('Token has expired')
    except Exception as e:
        print(e)
        return None, ParseError()
    return payload , None # Return payload and error if accures 


def verify_jti(payload:dict):
    jti = payload.get('jti')
    if not caches['users_white_list'].get(jti):
        raise AuthenticationFailed('Token not found')
    if user_id:= caches['users_white_list'].get(jti):
        return user_id
    return None

def verify_exp(payload:dict):
    exp = payload.get('exp')
    return exp > datetime.now().timestamp()




def store_in_cash(jwt_token):
    payload, error = decode_jwt_token(jwt_token)
    if payload:
        jti = payload['jti']
        user_id = payload['user_identifier']
        timeout = payload['exp'] - payload['iat']
        caches['users_white_list'].set(key=jti, value=user_id, timeout=timeout)
    else:
        raise error

def create_jwt(user, expiration_hours, jti=None):
    payload = {
        'user_identifier': user.id,
        'exp': int((datetime.now() + timedelta(hours=expiration_hours)).timestamp()),
        'iat': datetime.now().timestamp(),
        'jti': jti or uuid.uuid4().hex,
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token

def delete_jti_from_cache(jti):
    caches['users_white_list'].delete(jti)