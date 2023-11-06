import uuid

from starlette.responses import Response


class AuthResponseHandlerBase:
    def send(self, res: Response, access: str, refresh: str, csrf: str, sub: str):
        pass

    async def logout(self, session_id: uuid.UUID, res: Response):
        pass
