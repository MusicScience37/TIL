import json
import pathlib

THIS_DIR = pathlib.Path(__file__).absolute().parent


def json_to_csv() -> None:
    json_path = THIS_DIR / "bench.json"
    with open(str(json_path), mode="r", encoding="ascii") as file:
        raw_data = json.load(file)

    csv_path = THIS_DIR / "bench.csv"
    with open(str(csv_path), mode="w", encoding="ascii") as file:
        file.write(
            "Protocol,Data Size [byte],Mean Time [sec],Max Time [sec],Min Time [sec]\n"
        )

        for measurement in raw_data["measurements"]:
            if (
                measurement["group_name"] != "send_messages"
                or measurement["measurer_name"] != "Processing Time"
            ):
                continue

            protocol = measurement["case_name"]
            data_size = measurement["params"]["size"]
            stats = measurement["durations"]["stat"]

            file.write(
                f'{protocol},{data_size},{stats["mean"]},{stats["max"]},{stats["min"]}\n'
            )


if __name__ == "__main__":
    json_to_csv()
