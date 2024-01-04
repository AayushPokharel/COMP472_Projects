from flask import Flask, render_template, request
import pydot

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solution")
def solution():
    search_method = request.args.get("sol", "bfs")
    if search_method == "bfs":
        tree_data = generate_search_tree("bfs")
    elif search_method == "dfs":
        tree_data = generate_search_tree("dfs")
    else:
        tree_data = generate_search_tree("bfs")

    graph = pydot.Dot(graph_type="graph")
    add_edges(graph, tree_data)
    svg_string = graph.create_svg().decode("utf-8")

    return render_template(
        "solution.html",
        svg_string=svg_string,
        search_method=search_method,
    )


def add_edges(graph, node):
    for child in node.get("children", []):
        graph.add_edge(pydot.Edge(node["name"], child["name"]))
        add_edges(graph, child)


def generate_search_tree(search_method):
    root = {"name": "(0,0)", "id": "0,0"}
    visited_states = set()
    queue = [root]
    visited_states.add("(0,0)")

    while queue:
        current_node = queue.pop(0) if search_method == "bfs" else queue.pop()
        current_state = current_node["name"]
        x, y = map(int, current_state.strip("()").split(","))

        if x == 4:
            continue

        child_nodes = generate_child_nodes(current_state)

        for child in child_nodes:
            child_state = child["name"]
            if child_state not in visited_states:
                current_node.setdefault("children", []).append(child)
                queue.append(child)
                visited_states.add(child_state)

    return root


def generate_child_nodes(state):
    x, y = map(int, state.strip("()").split(","))
    operators = [
        {"name": f"Fill 5L Jug: (5, {y})", "operation": (5, y)},
        {"name": f"Fill 3L Jug: ({x}, 3)", "operation": (x, 3)},
        {"name": f"Empty 5L Jug: (0, {y})", "operation": (0, y)},
        {"name": f"Empty 3L Jug: ({x}, 0)", "operation": (x, 0)},
        {
            "name": f"Transfer from 5L to 3L: ({x - min(x, 3 - y)}, {y + min(x, 3 - y)})",
            "operation": (x - min(x, 3 - y), y + min(x, 3 - y)),
        },
        {
            "name": f"Transfer from 3L to 5L: ({x + min(y, 5 - x)}, {y - min(y, 5 - x)})",
            "operation": (x + min(y, 5 - x), y - min(y, 5 - x)),
        },
    ]

    child_nodes = []
    for op in operators:
        next_state = op["operation"]
        if 0 <= next_state[0] <= 5 and 0 <= next_state[1] <= 3:
            child_nodes.append({"name": str(next_state), "children": []})

    return child_nodes


if __name__ == "__main__":
    app.run(debug=True)
