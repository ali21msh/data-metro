import abc
from typing import Dict

from pyspark.sql import DataFrame

from nodes.node import Node
from utils.spark_util import SparkUtil


class ProcessingNode(Node):

    def __init__(self, name: str, type: str, format: str, options: dict, spark_util: SparkUtil):
        super().__init__(name, type, format, options, spark_util)

    @abc.abstractmethod
    def process(self, dfs: Dict[str, DataFrame]):
        pass
