import gzip

import msgpack
import pandas


def parse_data(filepath: str) -> pandas.DataFrame:
    with gzip.open(filepath, mode="rb") as file:
        raw_data = msgpack.load(file)

    bench_type_list = []
    impl_type_list = []
    count_list = []
    mean_time_list = []
    time_standard_error_list = []

    for measurement in raw_data["measurements"]:
        bench_type = measurement["group_name"]
        impl_type = measurement["case_name"]
        count = measurement["params"]["count"]
        mean_time = measurement["durations"]["stat"]["mean"]
        time_standard_error = measurement["durations"]["stat"]["standard_error"]

        bench_type_list.append(bench_type)
        impl_type_list.append(impl_type)
        count_list.append(count)
        mean_time_list.append(mean_time)
        time_standard_error_list.append(time_standard_error)

    return pandas.DataFrame(
        {
            "bench_type": bench_type_list,
            "impl_type": impl_type_list,
            "count": count_list,
            "mean_time": mean_time_list,
            "time_standard_error": time_standard_error_list,
        }
    )
