from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import requests
import logging
from datetime import datetime

class APIEndpoint(Enum):
    """
    Enumeration of available API endpoints.
    
    This enum provides a centralized way to manage API endpoints and ensures
    type safety when selecting endpoints for requests.
    """
    CHAT_COMPLETION = "chatx-completion"

class APIEnvironment(Enum):
    """
    Enumeration of available API environments.
    
    Supports different deployment environments for the API client.
    """
    PRODUCTION = "https://www.pizzagpt.it"
    STAGING = "https://staging.pizzagpt.it"
    DEVELOPMENT = "https://dev.pizzagpt.it"

@dataclass(frozen=True)
class APICredentials:
    """
    Immutable container for API authentication credentials.
    
    Attributes:
        secret_key: The API secret key for authentication
        origin: The allowed origin for API requests
    """
    secret_key: str
    origin: str

class PizzaGPTError(Exception):
    """Base exception class for PizzaGPT client errors."""
    pass

class APIConnectionError(PizzaGPTError):
    """Raised when there is an error connecting to the API."""
    pass

class APIResponseError(PizzaGPTError):
    """Raised when the API returns an error response."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")

@dataclass
class APIResponse:
    """
    Container for API response data.
    
    Attributes:
        content: The response content from the API
        timestamp: The time when the response was received
        raw_response: The complete raw response data
    """
    content: str
    timestamp: datetime
    raw_response: Dict[str, Any]

class APIClient(ABC):
    """
    Abstract base class defining the interface for API clients.
    
    This abstract class ensures that all API client implementations
    follow a consistent interface.
    """
    
    @abstractmethod
    def send_request(self, endpoint: APIEndpoint, data: Dict[str, Any]) -> APIResponse:
        """
        Send a request to the specified API endpoint.
        
        Args:
            endpoint: The API endpoint to send the request to
            data: The data to send with the request
            
        Returns:
            APIResponse object containing the response data
            
        Raises:
            APIConnectionError: If there is an error connecting to the API
            APIResponseError: If the API returns an error response
        """
        pass

class PizzaGPTClient(APIClient):
    """
    Implementation of the PizzaGPT API client.
    
    This class provides a robust interface for interacting with the PizzaGPT API,
    including proper error handling and response processing.
    
    Attributes:
        environment: The API environment to use
        credentials: The API credentials for authentication
        session: The requests session for making HTTP requests
    """
    
    def __init__(
        self,
        environment: APIEnvironment = APIEnvironment.PRODUCTION,
        credentials: Optional[APICredentials] = None,
        timeout: int = 30
    ):
        """
        Initialize the PizzaGPT client.
        
        Args:
            environment: The API environment to use
            credentials: Optional API credentials (defaults will be used if not provided)
            timeout: Request timeout in seconds
        """
        self.environment = environment
        self.credentials = credentials or APICredentials(
            secret_key="Marinara",
            origin=environment.value
        )
        self.timeout = timeout
        self.session = requests.Session()
        self._configure_session()
    
    def _configure_session(self) -> None:
        """Configure the HTTP session with default headers and settings."""
        self.session.headers.update({
            'accept': 'application/json',
            'content-type': 'application/json',
            'origin': self.credentials.origin,
            'x-secret': self.credentials.secret_key
        })
    
    def send_request(self, endpoint: APIEndpoint, data: Dict[str, Any]) -> APIResponse:
        """
        Implementation of the abstract send_request method.
        
        Args:
            endpoint: The API endpoint to send the request to
            data: The data to send with the request
            
        Returns:
            APIResponse object containing the response data
            
        Raises:
            APIConnectionError: If there is an error connecting to the API
            APIResponseError: If the API returns an error response
        """
        url = f"{self.environment.value}/api/{endpoint.value}"
        
        try:
            response = self.session.post(
                url,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            response_data = response.json()
            
            return APIResponse(
                content=response_data['content'],
                timestamp=datetime.now(),
                raw_response=response_data
            )
            
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection error: {str(e)}")
            raise APIConnectionError(f"Failed to connect to {url}: {str(e)}")
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {str(e)}")
            if response := getattr(e, 'response', None):
                try:
                    error_data = response.json()
                    raise APIResponseError(
                        error_data.get('statusCode', response.status_code),
                        error_data.get('message', str(e))
                    )
                except ValueError:
                    raise APIResponseError(response.status_code, str(e))
            raise APIConnectionError(f"Request failed: {str(e)}")

class PizzaGPTService:
    """
    High-level service class for interacting with PizzaGPT.
    
    This class provides a simplified interface for common PizzaGPT operations
    while handling all the complexity of API interactions internally.
    """
    
    def __init__(self, client: Optional[PizzaGPTClient] = None):
        """
        Initialize the PizzaGPT service.
        
        Args:
            client: Optional PizzaGPTClient instance (a default will be created if not provided)
        """
        self.client = client or PizzaGPTClient()
    
    def get_response(self, question: str) -> str:
        """
        Get a response from PizzaGPT for the given question.
        
        Args:
            question: The question to send to PizzaGPT
            
        Returns:
            The response content from PizzaGPT
            
        Raises:
            PizzaGPTError: If there is an error getting the response
        """
        try:
            response = self.client.send_request(
                APIEndpoint.CHAT_COMPLETION,
                {"question": question}
            )
            return response.content
        except (APIConnectionError, APIResponseError) as e:
            logging.error(f"Failed to get PizzaGPT response: {str(e)}")
            raise

def main():
    """Example usage of the PizzaGPT service."""
    service = PizzaGPTService()
    try:
        response = service.get_response("Hi")
        print(f"Response: {response}")
    except PizzaGPTError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()