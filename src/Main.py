from ast import Dict
import logging
import time
import threading
import configparser
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
from gui import MeasurementApp
from modules.BucketManager import BucketManager
from modules.DataProcessor import DataProcessor
from modules.RIPEAtlasAPI import RIPEAtlasAPI
from modules.SQLiteManager import SQLiteManager


def background_worker(db_manager: SQLiteManager, bucket_manager: BucketManager, data_processor: DataProcessor, ripe_api: RIPEAtlasAPI, influx_client: InfluxDBClient):
    """
    Background worker to fetch and process measurement data at regular intervals.
    
    @param db_manager: SQLiteManager instance
    @param bucket_manager: BucketManager instance
    @param data_processor: DataProcessor instance
    @param ripe_api: RIPEAtlasAPI instance
    @param influx_client: InfluxDBClient instance
    """
    write_api = influx_client.write_api(write_options=ASYNCHRONOUS)
    
    while True:
        measurements = db_manager.get_measurements()
        if not measurements:
            logging.info("No measurements to process. Sleeping for 60 seconds...")
            time.sleep(60)
            continue

        for measurement in measurements:
            try:
                measurement_id, _, bucket_name, retention_policy, _, measurement_type = measurement[1:7]
                bucket_manager.ensure_bucket(bucket_name, retention_policy)
                last_timestamp = db_manager.get_last_processed(measurement_id)
                results = ripe_api.fetch_measurement_results(measurement_id=int(measurement_id))
                
                if results:
                    new_results = [r for r in results if r.get("timestamp", 0) > last_timestamp]
                    if new_results:
                        retention_seconds = {"24 hours": 86400, "7 days": 604800, "14 days": 1209600}.get(retention_policy, 0)
                        points = []
                        
                        logging.info(f"ID: {measurement_id} - preparing data")

                        if measurement_type.lower() in ["ping", "packetloss"]:
                            points += data_processor.prepare_latency_data_for_influxdb(new_results, retention_seconds)
                            points += data_processor.prepare_packetloss_data_for_influxdb(new_results, retention_seconds)
                        elif measurement_type.lower() == "traceroute":
                            points += data_processor.prepare_traceroute_data_for_influxdb(new_results, retention_seconds)
                        
                        for point in points:
                            write_api.write(bucket=bucket_name, record=point)
                        
                        max_timestamp = max(r["timestamp"] for r in new_results)
                        db_manager.update_last_processed(measurement_id, max_timestamp)
                        logging.info(f"ID: {measurement_id} processed.")
                    else:
                        logging.info(f"ID: {measurement_id} - no new data.")
            except Exception as e:
                logging.error(f"Error processing measurement ID {measurement_id}: {e}")

        logging.info("Sleeping for 60 seconds...")
        time.sleep(60)


def load_config(config_file="config/config.ini") -> Dict:
    """
    Load configuration from an external config file.
    
    @param config_file: Path to the configuration file
    @return: Dictionary containing configuration values
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return {
        "influx_url": config.get("InfluxDB", "url"),
        "influx_token": config.get("InfluxDB", "token"),
        "influx_org": config.get("InfluxDB", "org"),
        "api_key": config.get("RIPEAtlas", "api_key"),
        "db_path": config.get("Database", "db_path")
    }


def main():
    """
    Main function to initialize components and start the background worker and GUI.
    """
    config = load_config()
    
    logging.info("Initializing components...")
    db_manager = SQLiteManager(db_path=config["db_path"])
    bucket_manager = BucketManager(influx_url=config["influx_url"], org=config["influx_org"], token=config["influx_token"])
    data_processor = DataProcessor()
    ripe_api = RIPEAtlasAPI(api_key=config["api_key"])
    influx_client = InfluxDBClient(url=config["influx_url"], token=config["influx_token"], org=config["influx_org"])
    
    logging.info("------------------Initialization completed------------------")

    worker_thread = threading.Thread(
        target=background_worker,
        args=(db_manager, bucket_manager, data_processor, ripe_api, influx_client),
        daemon=True
    )
    worker_thread.start()
    
    gui_app = MeasurementApp(db_manager=db_manager)
    gui_app.run()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    main()
