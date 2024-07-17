from typing import Optional

from pyspark import SparkConf
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import SparkSession

from config.settings import Settings


class SparkUtil:
    def __init__(self,log_level: str, dynamic_settings: dict, settings: Settings):
        spark_settings = dict(settings.settings.SPARK)
        configs = {**spark_settings, **dynamic_settings}
        spark_conf = SparkConf().setAll([(k, v) for k, v in configs.items()])
        print(spark_conf.getAll())
        self.spark = SparkSession.builder.config(
            conf=spark_conf).getOrCreate()
        self.spark.sparkContext.setLogLevel(log_level)

    def load_dataframe(self, read_format: str, path: str = None, options: dict = None,
                       where_clause: str = None) -> Optional[SparkDataFrame]:
        try:
            spark_reader = self.spark.read.format(read_format)
            if options:
                spark_reader.options(**options)
            if path:
                dataframe = spark_reader.load(path)
            else:
                dataframe = spark_reader.load()
            if where_clause:
                dataframe = dataframe.where(where_clause)
            return dataframe
        except Exception as err:
            print(err)
            return None

    def save_dataframe(self, dataframe: SparkDataFrame, format: str = "delta", mode: str = "append",
                       path: str = None, partition_by: str = None, options: dict = None):
        try:
            writer = dataframe.write.format(format)
            if options:
                writer = writer.options(**options)
            if partition_by:
                writer = writer.partitionBy(partition_by)
            if path:
                writer.mode(mode).save(path)
            else:
                writer.mode(mode).save()
        except Exception as err:
            print(err)
