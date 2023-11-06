import uuid

from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from uuid import UUID
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi import HTTPException
from starlette.responses import Response

from dtos.auth import SessionData
from fullstack_token.base import AuthResponseHandlerBase

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="_cookie",
    identifier="general_verifier",
    auto_error=False,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)

backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
            self,
            *,
            identifier: str,
            auto_error: bool,
            backend: InMemoryBackend[UUID, SessionData],
            auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=False,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)


class AuthResponseHandlerSession(AuthResponseHandlerBase):
    async def send(self, res: Response, access: str, _: str, csrf: str, sub: str):
        session = uuid.uuid4()

        data = SessionData(data=sub)
        await backend.create(session, data)
        cookie.attach_to_response(res, session)
        res.set_cookie('csrf_token_cookie', csrf)

        return True

    async def logout(self, session_id: uuid.UUID, res: Response):
        await backend.delete(session_id)
        cookie.delete_from_response(res)
        res.delete_cookie('csrf_token_cookie')
