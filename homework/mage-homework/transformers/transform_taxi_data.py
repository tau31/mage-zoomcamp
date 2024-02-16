if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
      - Remove rows where the passenger count is equal to 0 _and_ the trip distance is equal to zero.
        - Create a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date.
        - Rename columns in Camel Case to Snake Case, e.g. `VendorID` to `vendor_id`.
        - Add three assertions:
            - `vendor_id` is one of the existing values in the column (currently)
            - `passenger_count` is greater than 0
            - `trip_distance` is greater than 0
    """
    # Remove rows where the passenger count is equal to 0 _and_ the trip distance is equal to zero.
    data = data[data['passenger_count'] > 0]
    data = data[data['trip_distance'] > 0]

    #- Create a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date.
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
   
    # - Rename columns in Camel Case to Snake Case, e.g. `VendorID` to `vendor_id`.
    data = data.rename(columns = {
        "VendorID": "vendor_id", 
        "RatecodeID": "ratecode_id",
        "PULocationID": "pu_location_id",
        "DOLocationID": "do_location_id",   
    })
    return data

@test
def test_output(output, *args) -> None:
    """
    - Add three assertions:
    - `vendor_id` is one of the existing values in the column (currently)
    - `passenger_count` is greater than 0
    - `trip_distance` is greater than 0
    """
    assert 'vendor_id' in output, 'column vendor_id is not in the dataframe'
    assert output['passenger_count'].isin([0]).sum() == 0, 'rides with passenger counts equal to 0 still present'
    assert sum(output['trip_distance'] == 0) == 0, 'rides with trip_distance == 0 still in the data'
    assert output is not None, 'The output is undefined'