import pyarrow as pa
import pyarrow.parquet as pq
import os

### - Write your data as Parquet files to a bucket in GCP, partioned by `lpep_pickup_date`. Use the `pyarrow` library!

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/personal-gcp.json'

bucket_name = 'zoomcamp-tiago-411410_gc_bucket_dem'
project_id = 'zoomcamp-tiago-411410'
table_name = 'nyc_green_taxi_data'

root_path = f'{bucket_name}/{table_name}'



@data_exporter
def export_data(data, *args, **kwargs):
    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()
    pq.write_to_dataset(
        table, 
        root_path = root_path, 
        partition_cols = ['lpep_pickup_date'],
        filesystem = gcs
    )

    # Specify your data exporting logic here