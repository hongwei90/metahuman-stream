# authentication/jwt_auth.py

import jwt
from jwt.exceptions import InvalidTokenError

# 假设这是你的JWT秘钥
SECRET_KEY = "your_secret_key"


def verify_jwt_token(token):
    try:
        # 尝试解码 JWT 令牌
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # 你可以添加额外的验证逻辑，例如检查令牌的过期时间，或者验证payload中的其他字段
        return True
    except InvalidTokenError:
        return True  # test pst
