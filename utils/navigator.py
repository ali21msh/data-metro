from typing import List, Dict, Optional

from pyspark.sql import DataFrame

from config.settings import Settings
from factories.node_factory import NodeFactory
from nodes.connection_node import ConnectionNode
from nodes.process_node import ProcessingNode
from utils.spark_util import SparkUtil


class Navigator:
    pipeline: dict
    node_factory: NodeFactory
    nodes: List[ConnectionNode | ProcessingNode]
    dfs: Dict[str, DataFrame]

    def __init__(self,pipeline: dict, settings: Settings):
        self.pipeline = pipeline
        self.dynamic_settings = self.export_dynamic_settings()
        self.node_factory = NodeFactory(SparkUtil("info", self.dynamic_settings, settings))
        self.dfs = {}
        self.export_nodes()

    def export_nodes(self):
        exported_nodes: List[ConnectionNode] = list()
        nodes = self.pipeline["nodes"]
        for key, val in nodes.items():
            if val['type'] in ('source', 'sink'):
                exported_nodes.append(self.node_factory.make_connection_node(key, val))
            if val['type'] == 'processor':
                exported_nodes.append(self.node_factory.make_processing_node(key, val))
        self.nodes = exported_nodes

    def export_dynamic_settings(self) -> Optional[dict]:
        try:
            settings = self.pipeline['settings']
            return settings
        except Exception as err:
            print(err)
            return None

    def navigate(self):
        for node in self.nodes:
            if node.type == 'source':
                df: DataFrame = node.read()
                self.dfs.update({node.name: df})
            if node.type == 'processor':
                df: DataFrame = node.process(self.dfs)
                self.dfs.update({node.name: df})
            if node.type == 'sink':
                node.write(self.dfs[node.parent])
