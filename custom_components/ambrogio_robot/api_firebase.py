"""The API for accessing firebase used by the App."""
from urllib.parse import urljoin
import json

import aiohttp

URL_BASE = "https://www.googleapis.com"
VERIFY_PASSWORD = "/identitytoolkit/v3/relyingparty/verifyPassword"

API_KEY = "AIzaSyCUGSbVrwZ3X7BHU6oiUSmdzQwx-QXypUI"
ACCESS_TOKEN = ""


class AmbrogioRobotAuthException(Exception):
    """Exception Ambrogio Auth Exceptions."""

    def __init__(self, status, message):
        """Initialize."""
        super().__init__(status)
        self.status = status
        self.message = message


class AmbrogioRobotFirebaseAPI:
    """Client for the Ambrogio Firebase API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initiate Firebase API."""
        self._session = session

        # TODO: Get from Web Socket Send Access Token as Param Key
        # Returns Configured Robots

    async def verify_password(self, email: str, password: str) -> dict:
        """Verify the username and password with the googleapis site."""
        auth_data: dict = {
            "email": email,
            "password": password,
            "returnSecureToken": "true",
        }

        response = await self._session.post(
            urljoin(
                URL_BASE,
                f"{VERIFY_PASSWORD}?key={API_KEY}",
            ),
            data=json.dumps(auth_data),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9;",
            },
        )

        response_json = await response.json()

        if "error" in response_json:
            raise AmbrogioRobotAuthException(
                response_json["error"]["code"], response_json["error"]["message"]
            )

        valid_data = {
            "AccessToken": response_json["localId"],
            "SessionToken": response_json["idToken"],
        }
        return valid_data
