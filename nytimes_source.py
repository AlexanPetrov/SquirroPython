import logging
import requests
import os
from typing import Generator, List, Dict, Any
from utils import flatten_dict, retry_request, validate_pagination


class NYTimesSource:
    def __init__(self):
        """Set API credentials & validate that the API supports pagination"""
        self.api_key = os.getenv("NYTIMES_API_KEY")
        self.base_url = os.getenv("BASE_URL")
        self.page_size = int(os.getenv("NYT_PAGE_SIZE", 10))

        if not self.api_key:
            raise ValueError("NYTIMES_API_KEY not found in environment variables.")
        if not self.base_url:
            raise ValueError("BASE_URL not found in environment variables.")

        self.session = requests.Session()
        self.session.params = {"api-key": self.api_key}
        self.schema = set()

        validate_pagination(self.session, self.base_url)

    def connect(self, inc_column: str = None, max_inc_value: Any = None):
        """
        Connect to the source and reset schema
        """
        if inc_column is not None and not isinstance(inc_column, str):
            raise ValueError("Incremental column must be a string or None.")
        if max_inc_value is not None and not isinstance(max_inc_value, (int, float, str)):
            raise ValueError("Incremental value must be a string, integer, or float.")

        self.schema.clear()
        self.inc_column = inc_column
        self.max_inc_value = max_inc_value
        logging.debug("Incremental Column: %r", inc_column)
        logging.debug("Incremental Last Value: %r", max_inc_value)

    def disconnect(self):
        """
        Disconnect from the source
        """
        self.session.close()

    def getDataBatch(self, batch_size: int) -> Generator[List[Dict], None, None]:
        """
        Fetch data from the NYTimes API in batches
        """
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("Batch size must be a positive integer.")

        page = 0
        while True:
            params = {"page": page}
            try:
                data = retry_request(session=self.session, url=self.base_url, params=params)
                if not data:
                    logging.warning("No data received. Stopping fetch.")
                    break

                docs = data.get("response", {}).get("docs", [])
                if not docs:
                    logging.info("No more documents in API response. Stopping fetch.")
                    break

                batch = [flatten_dict(doc) for doc in docs[:batch_size]]
                self.schema.update(key for doc in batch for key in doc.keys())

                yield batch
                page += 1

                if len(docs) < self.page_size:
                    logging.info("Received fewer documents than expected. Stopping fetch.")
                    break
            except requests.exceptions.RequestException as e:
                logging.error(f"Error during API request: {e}")
                break

    def getSchema(self) -> List[str]:
        """
        Return the schema of the dataset
        """
        return sorted(self.schema)
