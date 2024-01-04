from flask import Flask, render_template, request
from algorithm import *


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dfs', methods=['GET'])
def dfs_route():
    s = Solution()
    s.solve(solve_method="dfs")
    s.show_solution()
    graph_svg = s.return_image("dfs")
    print(graph_svg)
    return render_template('search_tree.html', search_type='dfs')

@app.route('/bfs', methods=['GET'])
def bfs_route():
    s = Solution()
    s.solve(solve_method="bfs")
    s.show_solution()
    graph_svg = s.return_image("bfs")
    return render_template('search_tree.html', search_type='bfs')

@app.route('/space', methods=['GET'])
def space_route():
    s = Solution()
    max_depth = request.args.get('max_depth')
    s.generate_solution_space(int(max_depth))
    graph_svg = s.return_image("space")
    return render_template('space.html',space='space')


if __name__ == '__main__':
    app.run(debug=True)