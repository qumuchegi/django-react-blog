secret_for_user_JWT = 'qwewfw12131x1erqe231d2re4rwd'
import jwt
JWT_algorithm = 'HS256'

def generate_JWT_token(payload):
  return  jwt.encode(payload, secret_for_user_JWT, algorithm=JWT_algorithm)

def decode_JWT_token(token):
  return jwt.decode(token,secret_for_user_JWT, algorithms=[JWT_algorithm])

def JWT_auth(request):
  try:
    '''
    jwt token 是 b'xxxxxxx' 这样的格式，在解码是必须要先去掉前后的 b' 和 '，不热返回无效头部填充的错误
    '''
    JWT_token = request.COOKIES['jwt_token'].replace("b'",'').replace("'",'')
    print('-------JWT_token:', JWT_token,request.COOKIES)
    decoded=decode_JWT_token(JWT_token)
    print('解码后的 JWT token 中的 userid:',decoded['userid'],'\nrequest userid:',request.GET['userid'])
    if int(request.GET['userid']) == int(decoded['userid']):
      print('123')
      return True
    else:
      return False
  except:
   return False