from flask import Flask, render_template, request, redirect, url_for
from helper import A_star, BFS
import numpy as np
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/input", methods=["GET", "POST"])
def input():
    if request.method == "GET":
        return render_template("input.html")
    elif request.method == "POST":
        # Redirect to the result page after processing the form
        return redirect(
            url_for(
                "result",
                initial_1=int(request.form.get("initial_1")),
                initial_2=int(request.form.get("initial_2")),
                initial_3=int(request.form.get("initial_3")),
                initial_4=int(request.form.get("initial_4")),
                initial_5=int(request.form.get("initial_5")),
                initial_6=int(request.form.get("initial_6")),
                initial_7=int(request.form.get("initial_7")),
                initial_8=int(request.form.get("initial_8")),
                initial_9=int(request.form.get("initial_9")),
                goal_1=int(request.form.get("goal_1")),
                goal_2=int(request.form.get("goal_2")),
                goal_3=int(request.form.get("goal_3")),
                goal_4=int(request.form.get("goal_4")),
                goal_5=int(request.form.get("goal_5")),
                goal_6=int(request.form.get("goal_6")),
                goal_7=int(request.form.get("goal_7")),
                goal_8=int(request.form.get("goal_8")),
                goal_9=int(request.form.get("goal_9")),
                search_method=request.form.get("search_method", "a_star"),
                heuristics=request.form.get("heuristics", "manhattan"),
            )
        )


@app.route("/output", methods=["GET"])
def result():
    initial_1 = request.args.get("initial_1", type=int)
    initial_2 = request.args.get("initial_2", type=int)
    initial_3 = request.args.get("initial_3", type=int)
    initial_4 = request.args.get("initial_4", type=int)
    initial_5 = request.args.get("initial_5", type=int)
    initial_6 = request.args.get("initial_6", type=int)
    initial_7 = request.args.get("initial_7", type=int)
    initial_8 = request.args.get("initial_8", type=int)
    initial_9 = request.args.get("initial_9", type=int)

    goal_1 = request.args.get("goal_1", type=int)
    goal_2 = request.args.get("goal_2", type=int)
    goal_3 = request.args.get("goal_3", type=int)
    goal_4 = request.args.get("goal_4", type=int)
    goal_5 = request.args.get("goal_5", type=int)
    goal_6 = request.args.get("goal_6", type=int)
    goal_7 = request.args.get("goal_7", type=int)
    goal_8 = request.args.get("goal_8", type=int)
    goal_9 = request.args.get("goal_9", type=int)

    # Create a list with these variables
    initial_state_list = [
        initial_1,
        initial_2,
        initial_3,
        initial_4,
        initial_5,
        initial_6,
        initial_7,
        initial_8,
        initial_9,
    ]
    goal_state_list = [
        goal_1,
        goal_2,
        goal_3,
        goal_4,
        goal_5,
        goal_6,
        goal_7,
        goal_8,
        goal_9,
    ]
    search_method = request.form.get("search_method", "a_star")
    heuristics = request.form.get("heuristics", "manhattan")

    initial_state = np.array(initial_state_list).reshape(3, 3)
    goal_state = np.array(goal_state_list).reshape(3, 3)

    if search_method == "a_star":
        result = A_star(
            initial_state, goal_state, max_iter=1000000, heuristic=heuristics
        )
    else:
        result = BFS(initial_state, goal_state, max_iter=1000000, heuristic=heuristics)

    result_dict = json.loads(result)

    return render_template(
        "output.html",
        # initial_state=initial_state,
        # goal_state=goal_state,
        # search_method=search_method,
        # heuristics=heuristics,
        result=result_dict,
        search_method=search_method,
        heuristics=heuristics,
    )


if __name__ == "__main__":
    app.run(debug=True)
