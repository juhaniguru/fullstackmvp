import os

from fastapi import FastAPI
import uvicorn
from h11 import Request
from starlette.middleware.cors import CORSMiddleware

from starlette.responses import JSONResponse

import fullstack_token.token
import models

from controllers import auth_controller, user_controller, location_controller
from dotenv import load_dotenv

# https://www.section.io/engineering-education/how-to-get-ssl-https-for-localhost/?fbclid=IwAR1uk5NY4TTLg4MpnMMwYMLB6hB7tjjkBlcvAzZhAjyuybhlcNa3o1eRPZ8


app = FastAPI()

"""

@app.middleware("http")
async def check_csrf(request: Request, call_next):
    # tässä on bugi. jos call_next-kutsutaan täällä, requesti on jo mennyt ja middleware suoritetaan sitten
    # response = await call_next(request)
    if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:

        if str(request.url).find('login') == -1 and str(request.url).find('register') == -1:
            try:

                _token = fullstack_token.token.init_token()
                csrf = _token.validate(request.cookies.get('csrf_token_cookie'))
                access = _token.validate(request.cookies.get('access_token_cookie'))
                if csrf is None or access is None:
                    return JSONResponse(content={'err': 'forbidden'}, status_code=403)
                if csrf['sub'] != access['csrf']:
                    return JSONResponse(content={'err': 'forbidden'}, status_code=403)
            except Exception as e:
                return JSONResponse(content={'err': 'forbidden'}, status_code=403)
    response = await call_next(request) # kun call_next kutustaan vasta viimeisenä, csrf-tunniste tarkistetaan ensin
    return response

"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(location_controller.router)

if __name__ == '__main__':

    models.metadata.create_all(bind=models.engine)

    if os.getenv('SSL') == '0':
        uvicorn.run('main:app', port=8002, reload=False)
    elif os.getenv('SSL') == '1':
        uvicorn.run('main:app', port=8002, reload=False, ssl_keyfile='./cert/CA/localhost/localhost.decrypted.key',
                    ssl_certfile='./cert/CA/localhost/localhost.crt')
