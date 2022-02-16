import ast
import networkx as nx
import matplotlib.pyplot as plt
import abc

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List, Type, Iterable


__all__ = [
    'visualize_ast',
    'visualize_from_source',
    'visualize_from_file',
]


@dataclass
class GraphNodeProps:
    color: Optional[str]
    label: Optional[str]


@dataclass
class AstGraph:
    graph: nx.DiGraph
    node_properties: Dict[ast.AST, GraphNodeProps]
    edge_labels: Dict[Tuple[ast.AST, ast.AST], Optional[str]]
    ast_to_graph_node: Dict[ast.AST, int]
    graph_node_to_ast: List[ast.AST]

    def draw(self):
        layout = nx.drawing.nx_pydot.graphviz_layout(self.graph, prog="dot")

        nx_node_labels = {
            self.get_node_id(node): self.node_properties[node].label
            for node in self.node_properties
            if self.node_properties[node].label
        }

        nx_node_colors = [
            self.node_properties[node].color
            for node in self.graph_node_to_ast
        ]

        nx_edge_labels = {
            (self.ast_to_graph_node[edge[0]], self.ast_to_graph_node[edge[1]]): self.edge_labels[edge]
            for edge in self.edge_labels
            if self.edge_labels[edge]
        }

        base_size = 500

        nx.draw(self.graph,
                layout,
                labels=nx_node_labels,
                node_color=nx_node_colors,
                node_shape='s',
                font_size=8,
                node_size=base_size,
                with_labels=True)
        nx.draw_networkx_edge_labels(self.graph,
                                     layout,
                                     nx_edge_labels)

    def get_node_id(self, node: ast.AST) -> int:
        if node not in self.ast_to_graph_node:
            new_id = len(self.ast_to_graph_node)
            self.ast_to_graph_node[node] = new_id
            self.graph_node_to_ast.append(node)
        return self.ast_to_graph_node[node]

    def add_edge(self, child_node: ast.AST, parent: Optional[Tuple[ast.AST, Optional[str]]]):
        if parent is None:
            return
        parent_node, label = parent
        if label is not None:
            self.edge_labels[(parent_node, child_node)] = label
        self.graph.add_edge(self.get_node_id(parent_node),
                            self.get_node_id(child_node))

    def add_node(self, ast_node: ast.AST, properties: GraphNodeProps):
        self.graph.add_node(self.get_node_id(ast_node))
        self.node_properties[ast_node] = properties


class AstNodeVisualizer(abc.ABC):
    visualizers: Dict[Any, Any] = {}

    def __init__(self, acceptible_nodes: List[Type]):
        self.acceptible_nodes = acceptible_nodes

    @abc.abstractmethod
    def visualize_node(self, node: ast.AST, graph: AstGraph) -> Optional[Iterable[ast.AST]]:
        pass

    def register(self):
        AstNodeVisualizer.visualizers.update(
            {node_t: self for node_t in self.acceptible_nodes})

    def get_visualier(node: Any) -> Optional[Any]:
        node_type = type(node)
        if not issubclass(node_type, ast.AST):
            return None
        if type(node) in AstNodeVisualizer.visualizers:
            return AstNodeVisualizer.visualizers[type(node)]
        for vis_type, visualizer in AstNodeVisualizer.visualizers.items():
            if issubclass(node_type, vis_type):
                return visualizer
        return None

    def can_visualize(node: Any) -> bool:
        return AstNodeVisualizer.get_visualier(node) is not None

    def visualize_ast(node: ast.AST, graph: AstGraph):
        visualizer: AstNodeVisualizer = AstNodeVisualizer.get_visualier(node)
        if visualizer is None:
            return
        children_nodes = visualizer.visualize_node(node, graph)
        if children_nodes is None:
            return
        for children_node in children_nodes:
            AstNodeVisualizer.visualize_ast(children_node, graph)


class DefaultVisualizer(AstNodeVisualizer):
    def __init__(self):
        super().__init__([ast.expr, ast.stmt, ast.mod])

    def default_description(field: str, value: Any) -> Optional[str]:
        easy_descriptible_types = [int, float, str, bool]
        if type(value) in easy_descriptible_types:
            return f'{field}={value}'
        return None

    def build_default_name(node: ast.AST, desc: Optional[str]) -> str:
        node_type = type(node).__name__
        if desc is None:
            return node_type
        return f'{node_type}\n{desc}'

    def visualize_node(self, node: ast.AST, graph: AstGraph) -> Optional[Iterable[ast.AST]]:
        node_desc = None
        for field, field_value in ast.iter_fields(node):
            if node_desc is None:
                node_desc = DefaultVisualizer.default_description(field,
                                                                  field_value)
            if isinstance(field_value, List):
                for elem_i, element in enumerate(field_value):
                    if AstNodeVisualizer.can_visualize(element):
                        graph.add_edge(element, (node, f'{field} #{elem_i}'))
                        yield element
            elif AstNodeVisualizer.can_visualize(field_value):
                graph.add_edge(field_value, (node, field))
                yield field_value

        graph.add_node(node,
                       GraphNodeProps(
                           color='#abc7ed',
                           label=DefaultVisualizer.build_default_name(node, node_desc)))


class BinOpVisualizer(AstNodeVisualizer):
    def __init__(self, operators: Dict[Type, str] = {}):
        super().__init__([ast.BinOp])
        self.operators = operators

    def visualize_node(self, node: ast.BinOp, graph: AstGraph) -> Iterable[ast.AST]:
        op_str = self.operators.get(
            type(node.op), f'binop: {type(node.op).__name__}')
        graph.add_node(node, GraphNodeProps(color='#abedd3', label=op_str))
        graph.add_edge(node.left, (node, 'left'))
        graph.add_edge(node.right, (node, 'right'))
        yield node.left
        yield node.right


class CallVisualizer(AstNodeVisualizer):
    def __init__(self):
        super().__init__([ast.Call])

    def visualize_node(self, node: ast.Call, graph: AstGraph) -> Iterable[ast.AST]:
        def make_arg_repr(arg_i: int):
            return f'#{arg_i}'

        graph.add_edge(node.func, (node, '$func'))
        yield node.func

        for i, arg in enumerate(node.args):
            graph.add_edge(arg, (node, make_arg_repr(i)))
            yield arg
        args_repr = '' if node.args == [] else ','.join(
            map(make_arg_repr, range(len(node.args))))
        graph.add_node(node,
                       GraphNodeProps(
                           color='yellow',
                           label=f'$func ({args_repr})'))


class NameVisualizer(AstNodeVisualizer):
    def __init__(self):
        super().__init__([ast.Name])

    def visualize_node(self, node: ast.Name, graph: AstGraph) -> None:
        graph.add_node(node, GraphNodeProps(color='green', label=node.id))


class ConstantVisualizer(AstNodeVisualizer):
    def __init__(self):
        super().__init__([ast.Constant])

    def visualize_node(self, node: ast.Constant, graph: AstGraph) -> None:
        graph.add_node(node, GraphNodeProps(color='purple', label=node.value))


class CompareVisualizer(AstNodeVisualizer):
    def __init__(self, operators: Dict[Type, str] = {}):
        super().__init__([ast.Compare])
        self.operators = operators

    def print_comparator(self, comp: ast.cmpop) -> str:
        return self.operators.get(type(comp), f'cmp: {type(comp).__name__}')

    def visualize_node(self, node: ast.Compare, graph: AstGraph) -> Iterable[ast.AST]:
        graph.add_node(node, GraphNodeProps(color='#eddeab', label='compare'))
        graph.add_edge(node.left, (node, None))
        yield node.left

        for right_op, right in zip(node.ops, node.comparators):
            graph.add_edge(right, (node, self.print_comparator(right_op)))
            yield right


def visualize_ast(node: ast.AST,
                  output_file_path: Optional[Path],
                  no_show: bool
                  ):

    DefaultVisualizer().register()
    BinOpVisualizer({
        ast.Add: '+',
        ast.Sub: '-',
        ast.Div: '/',
        ast.Mult: '*'
    }).register()
    CallVisualizer().register()
    NameVisualizer().register()
    ConstantVisualizer().register()
    CompareVisualizer({
        ast.Lt: '<',
        ast.Gt: '>',
        ast.LtE: '<=',
        ast.GtE: '>=',
        ast.NotEq: '!=',
        ast.Eq: '==',
    }).register()

    graph = AstGraph(nx.DiGraph(), {}, {}, {}, [])
    AstNodeVisualizer.visualize_ast(node, graph)
    graph.draw()
    if output_file_path is not None:
        plt.savefig(output_file_path)
    if not no_show:
        plt.show()


def visualize_from_source(source: str,
                          output_file_path: Optional[Path],
                          no_show: bool
                          ):
    visualize_ast(ast.parse(source), output_file_path, no_show)


def visualize_from_file(source_file_path: Path,
                        output_file_path: Optional[Path],
                        no_show: bool
                        ):
    with source_file_path.open('r') as source_file:
        return visualize_from_source(source_file.read(), output_file_path, no_show)
