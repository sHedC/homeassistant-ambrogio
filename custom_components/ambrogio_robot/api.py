"""Dummy API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout
import simplejson as json


class AmbrogioRobotApiClientError(Exception):
    """Exception to indicate a general API error."""


class AmbrogioRobotApiClientCommunicationError(AmbrogioRobotApiClientError):
    """Exception to indicate a communication error."""


class AmbrogioRobotApiClientAuthenticationError(AmbrogioRobotApiClientError):
    """Exception to indicate an authentication error."""


class AmbrogioRobotApiClient:
    """Sample API Client."""
    
    # Holds the current session identifier.
    _session_id = ""

    # If the last request succeeded or failed.
    _status = None

    # Holds the response data from the API call.
    _response = []

    # Holds any error returned by the API.
    _error = []

    def __init__(
        self,
        api_key: str,
        access_token: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._api_key = api_key
        self._access_token = access_token
        self._session = session

    async def async_check_api_connect(self) -> bool:
        """Check the API Connectivity is valid."""
        
        result = await self.execute("thing.find", {
            "key": self._access_token
        })
        if result == False:
            return False
        # Check, if given token is API Client
        response = await self.get_response()
        if response["defName"] != "Client":
            return False
        return True

    async def async_check_robot(self, robot_imei: str) -> bool:
        """Check the Robot Exists."""
        
        return await self.execute("thing.find", {
            "imei": robot_imei
        })

    async def async_get_api_id(self) -> str:
        """Get the API Token Key from Google APIs."""
        return "keythatshouldnotbeshared"
    
    # This method sends the TR50 request to the server and parses the response.
    # https://github.com/deviceWISE/sample_tr50_python
    # @param    mixed    data     The JSON command and arguments. This parameter can also be a dict that will be converted to a JSON string.
    # @return   bool     Success or failure to post.
    async def post(
        self,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> bool:
        """This method sends the TR50 request to the server and parses the response."""
        self._error = ""
        self._status = True
        self._response = ""
        
        if not type(data) is dict:
            data = json.loads(data)

        data = await self.set_json_auth(data)
        
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method="POST",
                    url="https://api-de.devicewise.com/api",
                    headers=headers,
                    json=data,
                )
                if not response.status == 200:
                    raise AmbrogioRobotApiClientError(
                        "Failed to POST to API"
                    )
                response.raise_for_status()
                
                self._response = await response.json()
                
                if "errorMessages" in self._response:
                    self._error = self._response["errorMessages"]
                
                if "success" in self._response:
                    self._status = self._response["success"]
                if "data" in self._response:
                    if "success" in self._response["data"]:
                        self._status = self._response["data"]["success"]
                if "auth" in self._response:
                    if "success" in self._response["auth"]:
                        self._status = self._response["auth"]["success"]
                
                if self._status == True:
                    return self._status
                else:
                    raise AmbrogioRobotApiClientCommunicationError(
                        "Communication failed: %s" % self._error
                    )
        except asyncio.TimeoutError as exception:
            raise AmbrogioRobotApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise AmbrogioRobotApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:
            raise AmbrogioRobotApiClientError(
                "Something really wrong happened!"
            ) from exception
    
    # Package the command and the params into an array and sends the command to the configured endpoint for processing.
    # https://github.com/deviceWISE/sample_tr50_python
    # @param    command    string    The TR50 command to execute.
    # @param    params     dict      The command parameters.
    # @return   bool       Success or failure to post.
    async def execute(
        self,
        command: str,
        params: dict | bool = False
    ) -> bool:
        """Package the command and the params into an array and sends the command to the configured endpoint for processing."""
        if command == "api.authenticate":
            parameters = {
                "auth" : {
                    "command" : "api.authenticate",
                    "params" : params
                }
            }
        else:
            parameters = {
                "data" : {
                    "command" : command
                }
            }
            if not params == False:
               parameters["data"]["params"] = params
        
        return await self.post(parameters)
    
    # Depending on the configuration, authenticate the app or the user, prefer the app.
    # https://github.com/deviceWISE/sample_tr50_python
    # @return    bool    Success or failure to authenticate.
    async def auth(
        self
    ) -> bool:
        """Depending on the configuration, authenticate the app."""
        
        if len(self._api_key) > 0 and len(self._access_token) > 0:
            return await self.app_auth(self._api_key, self._access_token)
        return False
    
    # Authenticate the application.
    # https://github.com/deviceWISE/sample_tr50_python
    # @param     string    api_key               The application ID.
    # @param     string    access_token          The application token and thing ID.
    # @param     bool      update_session_id     Update the object session ID.
    # @return    bool      Success or failure to authenticate.
    async def app_auth(
        self,
        api_key: str,
        access_token: str,
        update_session_id: bool = True
    ) -> bool:
        """Authenticate the application."""
        
        try:
            params = {
                "appId" : access_token,
                "appToken" : api_key,
                "thingKey" : access_token
            }
            response = await self.execute("api.authenticate", params)
            if response == True:
                if update_session_id:
                    self._session_id = self._response["auth"]["params"]["sessionId"]
                return True
            return False
        except AmbrogioRobotApiClientCommunicationError as exception:
            raise AmbrogioRobotApiClientAuthenticationError(
                "Authorization failed. Please check the application configuration.",
            ) from exception
        except Exception as exception:
            raise exception
    
    # Return the response data for the last command if the last command was successful.
    # https://github.com/deviceWISE/sample_tr50_python
    # @return    dict    The response data.
    async def get_response(
        self
    ) -> any:
        """Return the response data for the last command if the last command was successful."""
        if self._status and len(self._response["data"]) > 0 and "params" in self._response["data"]:
            return self._response["data"]["params"]
        return None
    
    # This method checks the JSON command for the auth parameter. If it is not set, it adds.
    # https://github.com/deviceWISE/sample_tr50_python
    # @param    mixed    data    A JSON string or the dict representation of JSON.
    # @return   string   A JSON string with the auth parameter.
    async def set_json_auth(
        self,
        data: str
    ) -> str:
        """This method checks the JSON command for the auth parameter. If it is not set, it adds."""
        if not type(data) is dict:
            data = json.loads(data)
        
        if not "auth" in data:
            if len(self._session_id) == 0:
                await self.auth()
            # if it is still empty, we cannot proceed
            if len(self._session_id) == 0:
                raise AmbrogioRobotApiClientAuthenticationError(
                    "Authorization failed. Please check the application configuration."
                )
            data["auth"] = {
                "sessionId" : self._session_id
            }
        
        return data
