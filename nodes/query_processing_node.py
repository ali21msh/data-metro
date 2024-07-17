from typing import Dict

from pyspark.sql import DataFrame

from nodes.process_node import ProcessingNode
from utils.spark_util import SparkUtil


class QueryProcessingNode(ProcessingNode):

    def __init__(self, name: str, format: str, options: dict, type: str, spark_util: SparkUtil):
        super().__init__(
            name=name,
            format=format,
            type=type,
            options=options,
            spark_util=spark_util
        )

    def process(self, dfs: Dict[str, DataFrame]):
        try:
            for parent in self.options['parents']:
                dfs[parent].createOrReplaceTempView(parent)
            df = self.spark_util.spark.sql(self.options['query'])
            return df
        except Exception as err:
            print(err)
