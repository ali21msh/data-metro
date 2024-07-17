import abc

from pyspark.sql import DataFrame

from nodes.node import Node
from utils.spark_util import SparkUtil


class ConnectionNode(Node):
    mode: str
    parent: str
    stream: bool

    def __init__(self, name: str, type: str, format: str,stream: bool, options: dict, spark_util: SparkUtil,
                 mode: str, parent: str):
        super().__init__(name, type, format, options, spark_util)
        self.mode = mode
        self.parent = parent
        self.stream = stream

    @abc.abstractmethod
    def read(self):
        pass

    @abc.abstractmethod
    def write(self, dataframe: DataFrame):
        pass
