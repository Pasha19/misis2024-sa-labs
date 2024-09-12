import json


class Tree:
    def __init__(self, inp: str):
        raw_obj = json.loads(inp)
        self.nodes = list(raw_obj["nodes"].keys())
        self.size = len(self.nodes)
        self.links = {}
        for node in self.nodes:
            self.links[node] = raw_obj["nodes"][node][:]

    def find_root(self):
        for node in self.nodes:
            is_root = True
            for links in self.links[node]:
                if node in links:
                    is_root = False
                    break
            if is_root:
                return node
        raise Exception("Not tree")

    def __get_str(self, node):
        return node + "( " + " ".join([self.__get_str(s) for s in self.links[node]]) + " )"

    def __repr__(self) -> str:
        return self.__get_str(self.find_root())


def main(inp: str):
    return Tree(inp)


st = """
{
    "nodes": {
        "1": ["2"],
        "2": ["3", "4"],
        "3": ["5"],
        "4": [],
        "5": []

    }
}
"""
tree = main(st)
print(tree)
