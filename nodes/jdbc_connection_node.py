from pyspark.sql import DataFrame

from nodes.connection_node import ConnectionNode
from utils.spark_util import SparkUtil


class JDBCConnectionNode(ConnectionNode):

    def __init__(self, name: str, type: str, format: str, stream: bool, options: dict, spark_util: SparkUtil,
                 mode: str, parent: str):
        super().__init__(name, type, format, stream, options, spark_util, mode, parent)

    def read(self):
        try:
            df = self.spark_util.spark.read.format(self.format).options(**self.options).load()
            return df
        except Exception as err:
            print(err)

    def write(self, dataframe: DataFrame):
        try:
            dataframe.write.format(self.format).options(**self.options).mode(self.mode).save()
        except Exception as err:
            print(err)
