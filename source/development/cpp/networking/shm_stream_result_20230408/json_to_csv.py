import json
import pathlib

THIS_DIR = pathlib.Path(__file__).absolute().parent


def json_to_csv_one(name: str) -> None:
    json_path = THIS_DIR / f"{name}.json"
    with open(str(json_path), mode="r", encoding="ascii") as file:
        raw_data = json.load(file)

    csv_path = THIS_DIR / f"{name}.csv"
    with open(str(csv_path), mode="w", encoding="ascii") as file:
        file.write(
            "Protocol,Data Size [byte],Mean Time [sec],Max Time [sec],Min Time [sec]\n"
        )

        for measurement in raw_data["measurements"]:
            if measurement["measurer_name"] != "Processing Time":
                continue

            protocol = measurement["case_name"]
            data_size = measurement["params"]["size"]
            stats = measurement["durations"]["stat"]

            file.write(
                f'{protocol},{data_size},{stats["mean"]},{stats["max"]},{stats["min"]}\n'
            )


def json_to_csv() -> None:
    json_to_csv_one("send_messages")
    json_to_csv_one("ping_pong")


if __name__ == "__main__":
    json_to_csv()
