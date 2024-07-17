import abc

from utils.spark_util import SparkUtil


class Node(abc.ABC):
    name: str
    type: str
    format: str
    options: dict
    spark_util: SparkUtil

    def __init__(self, name: str, type: str, format: str, options: dict, spark_util: SparkUtil):
        self.name = name
        self.type = type
        self.format = format
        self.options = options
        self.spark_util = spark_util
