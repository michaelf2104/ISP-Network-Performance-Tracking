import logging
from influxdb_client import InfluxDBClient, BucketsApi
from influxdb_client.domain.bucket_retention_rules import BucketRetentionRules


class BucketManager:
    """
    Manages creation and verification of buckets in InfluxDB.
    """

    def __init__(self, influx_url: str, org: str, token: str):
        """
        Initializes the BucketManager.

        @param influx_url: InfluxDB instance URL
        @param org: Organization name in InfluxDB
        @param token: API token for authentication
        """
        self.client = InfluxDBClient(url=influx_url, token=token, org=org)
        self.buckets_api = self.client.buckets_api()
        logging.info("BucketManager initialized.")

    def bucket_exists(self, bucket_name: str) -> bool:
        """
        Checks if a bucket exists in InfluxDB.

        @param bucket_name: Name of the bucket
        @return: True if the bucket exists, False otherwise
        """
        try:
            return any(bucket.name == bucket_name for bucket in self.buckets_api.find_buckets(org=self.client.org).buckets)
        except Exception as e:
            logging.error(f"Error checking bucket existence: {e}")
            return False

    def create_bucket(self, bucket_name: str, retention_policy: str):
        """
        Creates a new bucket in InfluxDB with a specified retention policy.

        @param bucket_name: Name of the bucket to create
        @param retention_policy: Retention policy duration
        """
        retention_seconds = {
            "24 hours": 86400,
            "7 days": 604800,
            "14 days": 1209600
        }.get(retention_policy, 0)

        retention_rule = BucketRetentionRules(type="expire", every_seconds=retention_seconds)

        try:
            self.buckets_api.create_bucket(bucket_name=bucket_name, org=self.client.org, retention_rules=[retention_rule])
            logging.info(f"Bucket '{bucket_name}' with retention '{retention_policy}' created successfully.")
        except Exception as e:
            logging.error(f"Error creating bucket '{bucket_name}': {e}")

    def ensure_bucket(self, bucket_name: str, retention_policy: str):
        """
        Ensures that a bucket exists. Creates it if it does not exist.
        """
        logging.debug(f"Checking if bucket '{bucket_name}' exists.")
        if not self.bucket_exists(bucket_name):
            logging.debug(f"Bucket '{bucket_name}' does not exist. Creating now...")
            self.create_bucket(bucket_name, retention_policy)
        else:
            logging.debug(f"Bucket '{bucket_name}' already exists. Skipping creation.")

