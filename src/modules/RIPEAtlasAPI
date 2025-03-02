import logging
import requests
from typing import List, Dict, Any, Optional

class RIPEAtlasAPI:
    """
    Handles interaction with the RIPE Atlas API.
    """

    BASE_URL = "https://atlas.ripe.net/api/v2/"

    def __init__(self, api_key: str):
        """
        Initialize the API client with the API key.

        @param api_key: RIPE Atlas API key for authentication
        """
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Key {api_key}"})
        logging.info("RIPEAtlasAPI client initialized.")

    def fetch_measurement_results(self, measurement_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch measurement results from the RIPE Atlas API.

        @param measurement_id: ID of the measurement
        @return: List of measurement results or None if the request fails
        """
        url = f"{self.BASE_URL}measurements/{measurement_id}/results/"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch measurement data: {e}")
            return None
