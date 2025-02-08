"""convert XML results to CSV data"""

import os
import re
import xml.etree.ElementTree as ET
from typing import List, NamedTuple

import pandas as pd

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = THIS_DIR


class Catch2BenchResult(NamedTuple):
    """Benchmark result

    Attributes:
        name: name of benchmark
        mean: mean of time [nano seconds]
        lower_bound: lower bound of time [nano seconds]
        upper_bound: upper bound of time [nano seconds]
    """

    name: str
    mean: float
    lower_bound: float
    upper_bound: float


def parse_bench_in_xml(bench_result: ET.Element) -> Catch2BenchResult:
    """Parse a benchmark result in XML

    Args:
        bench_result (ET.Element): element of BenchmarkResults

    Returns:
        Catch2BenchResult: parsed data
    """

    name = bench_result.attrib["name"]
    mean_elem = bench_result.find("mean")
    mean = mean_elem.attrib["value"]
    lower_bound = mean_elem.attrib["lowerBound"]
    upper_bound = mean_elem.attrib["upperBound"]

    return Catch2BenchResult(
        name=name, mean=mean, lower_bound=lower_bound, upper_bound=upper_bound
    )


def parse_xml(filepath: str) -> pd.DataFrame:
    """Parse XML written by Catch2 library

    Args:
        filepath (str): filepath of XML

    Returns:
        pd.DataFrame: parsed data
    """

    tree = ET.parse(filepath)
    root = tree.getroot()

    bench_results = []
    for group in root.findall("Group"):
        for test_case in group.findall("TestCase"):
            for bench_result in test_case.findall("BenchmarkResults"):
                bench_results.append(parse_bench_in_xml(bench_result))

    return pd.DataFrame(
        [
            (result.name, result.mean, result.lower_bound, result.upper_bound)
            for result in bench_results
        ],
        columns=("name", "mean_ns", "lower_bound_ns", "upper_bound_ns"),
    )


def parse_bench_string() -> pd.DataFrame:
    """Parse benchmark results of strings

    Returns:
        pd.DataFrame: results
    """

    xml_results = parse_xml(DATA_DIR + "/bench_string.xml")
    parsed_name = xml_results["name"].str.extract(
        R"(?P<procedure>[a-z]*) string\((?P<data_size>\d*)\) with (?P<library>.*)"
    )
    bench_results = pd.concat([parsed_name, xml_results], axis=1)
    bench_results["data_type"] = "string"
    return bench_results


def parse_bench_double() -> pd.DataFrame:
    """Parse benchmark results of double arrays

    Returns:
        pd.DataFrame: results
    """

    xml_results = parse_xml(DATA_DIR + "/bench_double.xml")
    parsed_name = xml_results["name"].str.extract(
        R"(?P<procedure>[a-z]*) double\[(?P<data_size>\d*)\] with (?P<library>.*)"
    )
    bench_results = pd.concat([parsed_name, xml_results], axis=1)
    bench_results["data_type"] = "double"
    return bench_results


def parse_bench_struct() -> pd.DataFrame:
    """Parse benchmark results of structs

    Returns:
        pd.DataFrame: results
    """

    xml_results = parse_xml(DATA_DIR + "/bench_struct.xml")
    parsed_name = xml_results["name"].str.extract(
        R"(?P<procedure>[a-z]*) struct with (?P<library>.*)"
    )
    bench_results = pd.concat([parsed_name, xml_results], axis=1)
    bench_results["data_type"] = "struct"
    bench_results["data_size"] = 1
    return bench_results


def main():
    """Main function"""

    string_results = parse_bench_string()
    double_results = parse_bench_double()
    struct_results = parse_bench_struct()
    benchmarks = pd.concat(
        [string_results, double_results, struct_results], axis=0, ignore_index=True
    )
    print(benchmarks)
    benchmarks.to_csv(DATA_DIR + "/bench.csv", index=False)


if __name__ == "__main__":
    main()
