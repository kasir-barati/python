from typing import List
from http import HTTPMethod
import httpx
import json

from tests.types.wiremock import WireMockRequestLog


class PaymentService:
    """Service to manage WireMock server interactions."""

    __slots__ = ["base_url", "__admin_url", "__client", "path_prefix"]

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        api_version = "v1"
        self.path_prefix = f"/api/{api_version}"
        self.__admin_url = f"{self.base_url}/__admin"
        self.__client = httpx.AsyncClient(timeout=30.0)

    async def mock_callback_api(self) -> None:
        stub = {
            "request": {
                "method": "POST",
                "urlPath": f"{self.path_prefix}/callback",
                "headers": {"Content-Type": {"equalTo": "application/json"}},
                "bodyPatterns": [
                    {
                        "matchesJsonPath": "$.message",
                    },
                ],
            },
            "response": {
                "status": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(
                    {
                        "message": "Payment processed successfully",
                    }
                ),
            },
        }

        response = await self.__client.post(
            f"{self.__admin_url}/mappings",
            json=stub,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

    async def get_all_requests(self) -> List[WireMockRequestLog]:
        response = await self.__client.get(f"{self.__admin_url}/requests")
        response.raise_for_status()
        data: WireMockRequestLog = response.json()
        return data.get("requests", [])

    async def get_requests_for_endpoint(
        self, url_path: str, method: HTTPMethod = HTTPMethod.POST
    ) -> List[WireMockRequestLog]:
        all_requests = await self.get_all_requests()
        return [
            req
            for req in all_requests
            if req.get("request", {}).get("url") == url_path
            and req.get("request", {}).get("method") == method.value
        ]

    async def get_callback_requests(self) -> List[WireMockRequestLog]:
        return await self.get_requests_for_endpoint(
            f"{self.path_prefix}/callback", HTTPMethod.POST
        )

    async def reset(self) -> None:
        """Reset all stubs and request logs."""
        response = await self.__client.post(f"{self.__admin_url}/reset")
        response.raise_for_status()

    async def get_stub_mappings(self) -> List[WireMockRequestLog]:
        """Get all configured stub mappings."""
        response = await self.__client.get(f"{self.__admin_url}/mappings")
        response.raise_for_status()
        data: WireMockRequestLog = response.json()
        return data.get("mappings", [])

    async def close(self):
        """Close the HTTP client."""
        await self.__client.aclose()
