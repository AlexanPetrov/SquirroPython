import time
import logging
import requests

def flatten_dict(d, parent_key="", sep=".", items=None):
    """
    Converts nested dictionaries into a flat dictionary format
    where all keys are concatenated with a separator
    """
    if items is None:
        items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            flatten_dict(v, new_key, sep, items)
        else:
            items.append((new_key, v))
    return dict(items)

def retry_request(session=None, url=None, params=None, max_retries=5, initial_delay=10, max_delay=60):
    """
    Handles HTTP requests to the NYTimes API with built-in retry logic for robustness
    against failures such as rate limiting or temporary network issues
    """
    retries, delay = 0, initial_delay
    while retries < max_retries:
        try:
            response = session.get(url, params=params)
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                delay = min(int(retry_after) if retry_after and retry_after.isdigit() else delay, max_delay)
                raise requests.exceptions.RequestException(f"Rate limit: Retry after {delay}s")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if retries < max_retries - 1:
                logging.warning(f"Retrying ({retries + 1}/{max_retries}) due to {e}. Delay: {delay}s.")
                time.sleep(delay)
                retries += 1
            else:
                logging.error("Max retries reached. Request failed.")
                return None

def validate_pagination(session, base_url, test_params=None):
    """
    Validate that the API supports pagination using the 'page' parameter
    """
    if test_params is None:
        test_params = {"page": 0, "q": "test"}

    try:
        response = session.get(base_url, params=test_params)
        response.raise_for_status()

        data = response.json()
        if "response" not in data or not isinstance(data["response"], dict):
            raise ValueError("API response structure does not support pagination with 'page'.")
    except Exception as e:
        raise ValueError(f"Pagination validation failed: {e}") from e
