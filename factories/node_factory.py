from nodes.connection_node import ConnectionNode
from nodes.console_connection_node import ConsoleConnectionNode
from nodes.jdbc_connection_node import JDBCConnectionNode
from nodes.process_node import ProcessingNode
from nodes.query_processing_node import QueryProcessingNode
from utils.spark_util import SparkUtil


class NodeFactory:
    spark_util: SparkUtil

    def __init__(self, spark: SparkUtil):
        self.spark_util = spark

    def make_connection_node(self, name: str, node_property: dict) -> ConnectionNode:
        format = node_property['format']
        if format == 'jdbc':
            node = JDBCConnectionNode(
                name=name,
                type=node_property['type'],
                format=format,
                stream=node_property['stream'],
                options=node_property['options'],
                spark_util=self.spark_util,
                mode=node_property.get("mode"),
                parent=node_property.get("parent")
            )
        elif format == 'console':
            node = ConsoleConnectionNode(
                name=name,
                type=node_property['type'],
                format=format,
                stream=node_property['stream'],
                options=node_property['options'],
                spark_util=self.spark_util,
                mode=node_property.get('mode'),
                parent=node_property.get('parent')
            )
        return node

    def make_processing_node(self, name: str, node_property: dict) -> ProcessingNode:
        format = node_property['format']
        if format == 'query':
            node = QueryProcessingNode(
                name=name,
                format=format,
                options=node_property['options'],
                type=node_property['type'],
                spark_util=self.spark_util,
            )
            return node
