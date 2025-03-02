import time
import logging
import requests
import urllib3
from influxdb_client import Point
from typing import List, Dict, Any, Optional

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # avoid 

class DataProcessor:
    """
    Processes measurement data for storage in InfluxDB.
    """

    def __init__(self):
        """
        Initializes the DataProcessor class.
        """
        self.geoip_api_url = "https://ipapi.co/{}/json/"  # public GeoIP API

    """ 
    currently outcommented, because visualization for traceroute in grafana is not possible due to private/reserved ip-address spaces which can not be 
    used to searched for geo-addresses. Keep this problem in mind for further development!
    """
    # def get_geo_coordinates(self, ip_address: str) -> Optional[Dict[str, float]]:
    #     """
    #     Fetches latitude and longitude for an IP address using ip-api.com.

    #     @param ip_address: The IP address to look up
    #     @return: A dictionary with latitude and longitude or None if lookup fails
    #     """
    #     api_url = f"http://ip-api.com/json/{ip_address}?fields=status,lat,lon"

    #     try:
    #         response = requests.get(api_url, timeout=5)
    #         data = response.json()

    #         if data.get("status") == "success":
    #             return {
    #                 "latitude": data.get("lat"),
    #                 "longitude": data.get("lon")
    #             }
    #         else:
    #             logging.warning(f"GeoIP lookup failed for {ip_address}: {data}")
    #     except Exception as e:
    #         logging.warning(f"Failed to fetch GeoIP data for {ip_address}: {e}")

    #     return None


    def prepare_latency_data_for_influxdb(self, measurement_results: List[Dict[str, Any]], retention_seconds: int) -> List[Point]:
        """
        Prepares latency data for InfluxDB.

        @param measurement_results: List of measurement results
        @param retention_seconds: Retention period in seconds
        @return: List of InfluxDB Point objects
        """
        points = []
        current_time = int(time.time())

        for result in measurement_results:
            try:
                timestamp = result.get("timestamp", current_time)
                latency = result.get("avg")
                probe_id = result.get("prb_id", "unknown")
                target = result.get("dst_addr", "unknown")
                source = result.get("src_addr", "unknown")
                measurement_id = result.get("msm_id", "unknown")

                if latency is not None and current_time - timestamp <= retention_seconds:
                    points.append(
                        Point("latency")
                        .tag("target", str(target))
                        .tag("source", str(source))
                        .tag("probe_id", str(probe_id))
                        .tag("msm_id", str(measurement_id))
                        .field("latency", latency)
                        .time(timestamp * 1_000_000_000)  # convert to nanoseconds
                    )
            except Exception as e:
                logging.warning(f"Error processing latency result: {e}")

        logging.info(f"Prepared {len(points)} latency metrics for InfluxDB.")
        return points


    def prepare_packetloss_data_for_influxdb(self, measurement_results: List[Dict[str, Any]], retention_seconds: int) -> List[Point]:
        """
        Prepares packet loss data for InfluxDB.

        @param measurement_results: List of measurement results
        @param retention_seconds: Retention period in seconds
        @return: List of InfluxDB Point objects
        """
        points = []
        current_time = int(time.time())

        for result in measurement_results:
            try:
                timestamp = result.get("timestamp", current_time)
                packet_loss = result.get("sent", 0) - result.get("rcvd", 0)
                probe_id = result.get("prb_id", "unknown")
                target = result.get("dst_addr", "unknown")
                source = result.get("dst_addr", "unknown")
                measurement_id = result.get("msm_id", "unknown")

                if packet_loss is not None and current_time - timestamp <= retention_seconds:
                    points.append(
                        Point("packetloss")
                        .tag("target", str(target))
                        .tag("source", str(source))
                        .tag("probe_id", str(probe_id))
                        .tag("msm_id", str(measurement_id))
                        .field("packetloss", packet_loss)
                        .time(timestamp * 1_000_000_000) # convert to nanoseconds
                    )
            except Exception as e:
                logging.warning(f"Error processing packet loss result: {e}")

        logging.info(f"Prepared {len(points)} packet loss metrics for InfluxDB.")
        return points

    """ 
    currently outcommented, because visualization for traceroute in grafana is not possible due to private/reserved ip-address spaces which can not be 
    used to searched for geo-addresses. Keep this problem in mind for further development!
    """
    # def prepare_traceroute_data_for_influxdb(self, measurement_results: List[Dict[str, Any]], retention_seconds: int) -> List[Point]:
    #     """
    #     Prepare traceroute data for InfluxDB while respecting the retention policy.
    #     Format the data to match the Geomap Panel requirements in Grafana.

    #     @param measurement_results: List of traceroute measurement results.
    #     @param retention_seconds: Retention period in seconds.
    #     @return: List of InfluxDB Point objects.
    #     """
    #     points = []
    #     current_time = int(time.time())

    #     for result in measurement_results:
    #         try:
    #             timestamp = result.get("timestamp", current_time)
    #             probe_id = result.get("prb_id", "unknown")
    #             src_ip = result.get("from", "unknown")
    #             dst_ip = result.get("dst_addr", "unknown")
    #             hops = result.get("result", [])

    #             # Only process data within the retention policy period
    #             if current_time - timestamp <= retention_seconds:
    #                 for hop in hops:
    #                     hop_index = hop.get("hop")
    #                     for hop_detail in hop.get("result", []):
    #                         hop_ip = hop_detail.get("from", "unknown")
    #                         rtt = hop_detail.get("rtt", None)

    #                         # get geo-coordinates for the hop IP
    #                         geo_data = self.get_geo_coordinates(hop_ip) if hop_ip != "unknown" else None
    #                         latitude = geo_data["latitude"] if geo_data else None
    #                         longitude = geo_data["longitude"] if geo_data else None
    #                         # Ensure valid data before storing
    #                         if rtt is not None and latitude is not None and longitude is not None:
    #                             point = Point("traceroute") \
    #                                 .tag("probe_id", str(probe_id)) \
    #                                 .tag("hop_ip", str(hop_ip)) \
    #                                 .tag("src_ip", str(src_ip)) \
    #                                 .tag("dst_ip", str(dst_ip)) \
    #                                 .field("hop", hop_index) \
    #                                 .field("rtt", rtt) \
    #                                 .field("latitude", latitude) \
    #                                 .field("longitude", longitude) \
    #                                 .time(timestamp * 1_000_000_000)  # convert to nanoseconds

    #                             points.append(point)
    #         except Exception as e:
    #             logging.warning(f"Error processing traceroute result: {e}")

    #     logging.info(f"Prepared {len(points)} traceroute metrics for InfluxDB.")
    #     return points
