import bson 
import jwt
import datetime
from decouple import config

def check_valid_id(id:str):
    return bson.objectid.ObjectId.is_valid(id)

class JWT:
    @staticmethod 
    def generate_jwt(data):
        payload = data
        payload["exp"] = datetime.datetime.utcnow()+datetime.timedelta(minutes=60)
        token = jwt.encode(
            payload,
            config('JWT_SECRET_KEY'),
        )
        return token 

    @staticmethod 
    def decode_jwt(token):
        try:
            decoded = jwt.decode(
                token,
                config('JWT_SECRET_KEY'),
                algorithms=['HS256']
            )
            return decoded
        except jwt.ExpiredSignatureError as e:
            raise e


# if __name__ == "__main__":
#     jwtUtils = JWT()
#     print(jwtUtils.generate_jwt({"name":"similoluwa2"}))
#     print(jwtUtils.decode_jwt("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoic2ltaWxvbHV3YTIiLCJleHAiOjE2MTY1MzQ0MDV9.9h3UQ16qddTqkv_Tgega6MQm3kS394z0YRT2XyMVmJA"))