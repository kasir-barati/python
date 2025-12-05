from typing import List, Dict, Any, TypedDict


class WireMockHeaders(TypedDict, total=False):
    """Headers dictionary with optional fields."""

    Host: str
    User_Agent: str
    Accept_Encoding: str
    Accept: str
    Connection: str
    Content_Length: str
    Content_Type: str
    Matched_Stub_Id: str


class WireMockRequestData(TypedDict):
    """Request data structure from WireMock."""

    url: str
    absoluteUrl: str
    method: str
    clientIp: str
    headers: WireMockHeaders
    cookies: Dict[str, Any]
    browserProxyRequest: bool
    loggedDate: int
    bodyAsBase64: str
    body: str
    protocol: str
    scheme: str
    host: str
    port: int
    loggedDateString: str
    queryParams: Dict[str, Any]
    formParams: Dict[str, Any]


class WireMockResponseDefinition(TypedDict):
    """Response definition structure."""

    status: int
    body: str
    headers: Dict[str, str]


class WireMockResponse(TypedDict):
    """Response structure."""

    status: int
    headers: WireMockHeaders
    bodyAsBase64: str
    body: str


class WireMockTiming(TypedDict):
    """Timing information structure."""

    addedDelay: int
    processTime: int
    responseSendTime: int
    serveTime: int
    totalTime: int


class WireMockStubRequestPattern(TypedDict, total=False):
    """Stub request pattern structure."""

    urlPath: str
    method: str
    headers: Dict[str, Dict[str, str]]
    bodyPatterns: List[Dict[str, str]]


class WireMockStubResponsePattern(TypedDict):
    """Stub response pattern structure."""

    status: int
    body: str
    headers: Dict[str, str]


class WireMockStubMapping(TypedDict):
    """Stub mapping structure."""

    id: str
    request: WireMockStubRequestPattern
    response: WireMockStubResponsePattern
    uuid: str


class WireMockRequestLog(TypedDict):
    """Complete WireMock request log structure."""

    id: str
    request: WireMockRequestData
    responseDefinition: WireMockResponseDefinition
    response: WireMockResponse
    wasMatched: bool
    timing: WireMockTiming
    subEvents: List[Any]
    stubMapping: WireMockStubMapping
