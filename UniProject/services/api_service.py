from typing import Dict, Optional

import requests


def call_api(url: str, headers: Optional[Dict[str, str]] = None, method: str = "GET") -> Optional[str]:
    """
    Call an external API using the specified URL, headers, and HTTP method.

    Args:
        url (str): The API endpoint URL.
        headers (Optional[Dict[str, str]]): Optional HTTP headers to include in the request.
        method (str): HTTP method to use ("GET" or "POST"). Defaults to "GET".

    Returns:
        str: The response text from the API, or an error message on failure.
    """
    try:
        if method.upper() == "POST":
            response = requests.post(url, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        return response.text
    except Exception as exception:
        return f"Error: {exception}"
