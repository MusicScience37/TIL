import typing

import msgpack
import pandas


def parse_data(filepath: str) -> pandas.DataFrame:
    with open(filepath, mode="rb") as file:
        raw_data = msgpack.load(file)

    df: typing.Optional[pandas.DataFrame] = None

    for measurement in raw_data["measurements"]:
        if measurement["measurer_name"] != "Processing Time":
            continue

        protocol = measurement["case_name"]
        data_size = measurement["params"]["size"]
        time_list = measurement["durations"]["values"][0]

        cur_df = pandas.DataFrame(
            {
                "protocol": [protocol] * len(time_list),
                "data_size": [data_size] * len(time_list),
                "time": time_list,
            }
        )
        if df is None:
            df = cur_df
        else:
            df = pandas.concat([df, cur_df])

    assert df is not None

    return df
