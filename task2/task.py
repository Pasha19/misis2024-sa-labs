import csv
import io


class TreeNode:
    def __init__(self, value: int):
        self.value: int = value
        self.children: list[TreeNode] = []
        self.parent: TreeNode|None = None
        self.level: int = -1
        self.children_count: int = -1


def build_tree(edges: list[tuple[int, int]]) -> dict[int, TreeNode]:
    nodes = {}
    for parent_val, child_val in edges:
        if parent_val not in nodes:
            nodes[parent_val] = TreeNode(parent_val)
        if child_val not in nodes:
            nodes[child_val] = TreeNode(child_val)
        parent_node = nodes[parent_val]
        child_node = nodes[child_val]
        child_node.parent = parent_node
        parent_node.children.append(child_node)
    return nodes


def find_root(tree: dict[int, TreeNode]) -> int:
    for key, node in tree.items():
        if node.parent is None:
            return key
    raise Exception("Root not found")


def count_children_and_level(tree: dict[int, TreeNode]) -> None:
    root = find_root(tree)
    def count(node: TreeNode, level: int) -> int:
        total_count = 0
        node.level = level
        for child in node.children:
            total_count += 1 + count(child, level + 1)
        node.children_count = total_count
        return total_count
    count(tree[root], 1)


def main(var: str) -> str:
    input_rows = [tuple(map(int, r)) for r in csv.reader(var.split(), delimiter=",")]
    tree = build_tree(input_rows)
    count_children_and_level(tree)
    rows: list[tuple[int, list[int]]] = []
    for key, node in tree.items():
        r1 = len(node.children)
        r2 = 0 if node.parent is None else 1
        r3 = node.children_count - r1
        r4 = max(node.level - 2, 0)
        r5 = 0 if node.parent is None else (len(node.parent.children) - 1)
        rows.append((key, [r1, r2, r3, r4, r5]))
    output = io.StringIO()
    csv_writer = csv.writer(output, delimiter=",")
    for _, row in sorted(rows, key=lambda x: x[0]):
        csv_writer.writerow(row)
    res_str = output.getvalue()
    output.close()
    return res_str
