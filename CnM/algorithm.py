
import os
import emoji
import pydot
import random
from collections import deque

# Set it to bin folder of graphviz
os.environ["PATH"] += os.pathsep + '/usr/lib/x86_64-linux-gnu/graphviz'


# global variables
Parent, Move, node_list = dict(), dict(), dict()
# i = 0 # To track node


class Solution():

    def __init__(self):
        self.start_state = (3, 3, 1)
        self.goal_state = (0, 0, 0)
        self.options = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]

        self.boat_side = ["right", "left"]

        self.graph = pydot.Dot(graph_type='graph', bgcolor="#ffffff",fontcolor="black", fontsize="24",
                                # label="fig: Missionaries and Cannibal State Space Tree"
                                )      
        self.visited = {}
        self.solved = False

    def is_valid_move(self, number_missionaries, number_cannnibals):
        """
        Checks if number constraints are satisfied
        """
        return (0 <= number_missionaries <= 3) and (0 <= number_cannnibals <= 3)

    def is_goal_state(self, number_missionaries, number_cannnibals, side):
        return (number_missionaries, number_cannnibals, side) == self.goal_state

    def is_start_state(self, number_missionaries, number_cannnibals, side):
        return (number_missionaries, number_cannnibals, side) == self.start_state

    def number_of_cannibals_exceeds(self, number_missionaries, number_cannnibals):
        number_missionaries_right = 3 - number_missionaries
        number_cannnibals_right = 3 - number_cannnibals
        return (number_missionaries > 0 and number_cannnibals > number_missionaries) \
               or (number_missionaries_right > 0 and number_cannnibals_right > number_missionaries_right)

    def solve(self, solve_method="dfs"):
        self.visited = dict()
        Parent[self.start_state] = None
        Move[self.start_state] = None
        node_list[self.start_state] = None

        return self.dfs(*self.start_state, 0) if solve_method == "dfs" else self.bfs()

    def bfs(self):
        q = deque()
        q.append(self.start_state + (0, ))
        self.visited[self.start_state] = True

        while q:
            number_missionaries, number_cannnibals, side, depth_level = q.popleft()
            u, v = self.draw_edge(number_missionaries, number_cannnibals, side, depth_level)    

            
            if self.is_start_state(number_missionaries, number_cannnibals, side):   
                v.set_style("filled")
                v.set_fillcolor("blue")
                v.set_fontcolor("white")
            elif self.is_goal_state(number_missionaries, number_cannnibals, side):
                v.set_style("filled")
                v.set_fillcolor("green")
                return True
            elif self.number_of_cannibals_exceeds(number_missionaries, number_cannnibals):
                v.set_style("filled")
                v.set_fillcolor("red")
                continue
            else:
                v.set_style("filled")
                v.set_fillcolor("orange")

            op = -1 if side == 1 else 1

            can_be_expanded = False

            for x, y in self.options:
                next_m, next_c, next_s = number_missionaries + op * x, number_cannnibals + op * y, int(not side)
                if (next_m, next_c, next_s) not in self.visited:
                    if self.is_valid_move(next_m, next_c):
                        can_be_expanded = True
                        self.visited[(next_m, next_c, next_s)] = True
                        q.append((next_m, next_c, next_s, depth_level + 1))
                        
                        # Keep track of parent and corresponding move
                        Parent[(next_m, next_c, next_s)] = (number_missionaries, number_cannnibals, side)
                        Move[(next_m, next_c, next_s)] = (x, y, side)
                        node_list[(next_m, next_c, next_s)] = v
                
            if not can_be_expanded:
                v.set_style("filled")
                v.set_fillcolor("gray")
        return False

    def dfs(self, number_missionaries, number_cannnibals, side, depth_level):
        self.visited[(number_missionaries, number_cannnibals, side)] = True

        u, v = self.draw_edge(number_missionaries, number_cannnibals, side, depth_level)    

        
        if self.is_start_state(number_missionaries, number_cannnibals, side):
            v.set_style("filled")
            v.set_fillcolor("blue")
        elif self.is_goal_state(number_missionaries, number_cannnibals, side):
            v.set_style("filled")
            v.set_fillcolor("green")    
            return True
        elif self.number_of_cannibals_exceeds(number_missionaries, number_cannnibals):
            v.set_style("filled")
            v.set_fillcolor("red")
            return False
        else:
            v.set_style("filled")
            v.set_fillcolor("orange")

        solution_found = False
        operation = -1 if side == 1 else 1
        
        can_be_expanded = False

        for x, y in self.options:
            next_m, next_c, next_s = number_missionaries + operation * x, number_cannnibals + operation * y, int(not side)

            if (next_m, next_c, next_s) not in self.visited:
                if self.is_valid_move(next_m, next_c):
                    can_be_expanded = True
                    # Keep track of Parent state and corresponding move
                    Parent[(next_m, next_c, next_s)] = (number_missionaries, number_cannnibals, side)
                    Move[(next_m, next_c, next_s)] = (x, y, side)
                    node_list[(next_m, next_c, next_s)] = v

                    solution_found = (solution_found or self.dfs(next_m, next_c, next_s, depth_level + 1))
                
                    if solution_found:
                        return True

        if not can_be_expanded:
            v.set_style("filled")
            v.set_fillcolor("gray")

        self.solved = solution_found
        return solution_found

    def draw(self, *, number_missionaries_left, number_cannnibals_left, number_missionaries_right, number_cannnibals_right):
        """
            Draw state on console using emojis
        """
        left_m = emoji.emojize(f":old_man: " * number_missionaries_left)
        left_c = emoji.emojize(f":ogre: " * number_cannnibals_left)
        right_m = emoji.emojize(f":old_man: " * number_missionaries_right)
        right_c = emoji.emojize(f":ogre: " * number_cannnibals_right)
        
        print('{}{}{}{}{}'.format(left_m, left_c + " " * (14 - len(left_m) - len(left_c)), "_" * 40, " " * (12 - len(right_m) - len(right_c)) + right_m, right_c))
        print("")

    def show_solution(self):
        state = self.goal_state
        path, steps, nodes = [] ,[], []

        while state is not None:
            path.append(state)
            steps.append(Move[state])
            nodes.append(node_list[state])
        
            state = Parent[state]
        
        steps, nodes = steps[::-1], nodes[::-1]

        number_missionaries_left, number_cannnibals_left = 3, 3
        number_missionaries_right, number_cannnibals_right = 0, 0
    
        print("*" * 60)
        self.draw(number_missionaries_left=number_missionaries_left, number_cannnibals_left=number_cannnibals_left, number_missionaries_right=number_missionaries_right, number_cannnibals_right=number_cannnibals_right)
        
        for i, ((number_missionaries, number_cannnibals, side), node) in enumerate(zip(steps[1:], nodes[1:])):
            
            if node.get_label() != str(self.start_state):
                node.set_style("filled")
                node.set_fillcolor("yellow")
        
            print(f"Step {i + 1}: Move {number_missionaries} missionaries  and {number_cannnibals} cannibals from {self.boat_side[side]} to {self.boat_side[int(not side)]}.")

            op = -1 if side == 1 else 1
            
            number_missionaries_left = number_missionaries_left + op * number_missionaries
            number_cannnibals_left = number_cannnibals_left + op * number_cannnibals

            number_missionaries_right = number_missionaries_right - op * number_missionaries
            number_cannnibals_right = number_cannnibals_right - op * number_cannnibals
            
            self.draw(number_missionaries_left=number_missionaries_left, number_cannnibals_left=number_cannnibals_left, number_missionaries_right=number_missionaries_right, number_cannnibals_right=number_cannnibals_right)
        
        print("The problem is solved in {} steps".format(len(steps) - 1))

    def draw_edge(self, number_missionaries, number_cannnibals, side, depth_level):
        u, v = None, None
        if Parent[(number_missionaries, number_cannnibals, side)] is not None:
            u = pydot.Node(str(Parent[(number_missionaries, number_cannnibals, side)] + (depth_level - 1, )), label=str(Parent[((number_missionaries, number_cannnibals, side))]))
            self.graph.add_node(u)

            v = pydot.Node(str((number_missionaries, number_cannnibals, side, depth_level)), label=str((number_missionaries, number_cannnibals, side)))
            self.graph.add_node(v)

            edge = pydot.Edge(str(Parent[(number_missionaries, number_cannnibals, side)] + (depth_level - 1, )), str((number_missionaries, number_cannnibals, side, depth_level) ), dir='forward')
            self.graph.add_edge(edge)
        else:
            # For start node
            v = pydot.Node(str((number_missionaries, number_cannnibals, side, depth_level)), label=str((number_missionaries, number_cannnibals, side)))
            self.graph.add_node(v)        
        return u, v
    
    def draw_edge_sp(self,number_missionaries, number_cannnibals, side, depth_level, node_num):
        u, v = None, None
        if Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)] is not None:
            u = pydot.Node(str(Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)]), label=str(Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)][:3]))
            self.graph.add_node(u)

            v = pydot.Node(str((number_missionaries, number_cannnibals, side, depth_level, node_num)), label=str((number_missionaries, number_cannnibals, side)))
            self.graph.add_node(v)

            edge = pydot.Edge(str(Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)]), str((number_missionaries, number_cannnibals, side, depth_level, node_num) ), dir='forward')
            self.graph.add_edge(edge)
        else:
            # For start node
            v = pydot.Node(str((number_missionaries, number_cannnibals, side, depth_level, node_num)), label=str((number_missionaries, number_cannnibals, side)))
            self.graph.add_node(v)        
        return u, v

    def bfs(self):
        q = deque()
        q.append(self.start_state + (0, ))
        self.visited[self.start_state] = True

        while q:
            number_missionaries, number_cannnibals, side, depth_level = q.popleft()
            # Draw Edge from u -> v
            # Where u = Parent[v]
            # and v = (number_missionaries, number_cannnibals, side, depth_level)
            u, v = self.draw_edge(number_missionaries, number_cannnibals, side, depth_level)    

            
            if self.is_start_state(number_missionaries, number_cannnibals, side):   
                v.set_style("filled")
                v.set_fillcolor("blue")
                v.set_fontcolor("white")
            elif self.is_goal_state(number_missionaries, number_cannnibals, side):
                v.set_style("filled")
                v.set_fillcolor("green")
                return True
            elif self.number_of_cannibals_exceeds(number_missionaries, number_cannnibals):
                v.set_style("filled")
                v.set_fillcolor("red")
                continue
            else:
                v.set_style("filled")
                v.set_fillcolor("orange")

            op = -1 if side == 1 else 1

            can_be_expanded = False

            for x, y in self.options:
                next_m, next_c, next_s = number_missionaries + op * x, number_cannnibals + op * y, int(not side)
                if (next_m, next_c, next_s) not in self.visited:
                    if self.is_valid_move(next_m, next_c):
                        can_be_expanded = True
                        self.visited[(next_m, next_c, next_s)] = True
                        q.append((next_m, next_c, next_s, depth_level + 1))
                        
                        # Keep track of parent and corresponding move
                        Parent[(next_m, next_c, next_s)] = (number_missionaries, number_cannnibals, side)
                        Move[(next_m, next_c, next_s)] = (x, y, side)
                        node_list[(next_m, next_c, next_s)] = v
                
            if not can_be_expanded:
                v.set_style("filled")
                v.set_fillcolor("gray")
        return False

    def generate_solution_space(self, max_depth=10):
        # global i
        i = 0
        q = deque()
        node_num = 0
        q.append((3, 3, 1, 0, node_num))

        
        Parent[(3, 3, 1, 0, node_num)] = None

        while q:

            number_missionaries, number_cannnibals, side, depth_level, node_num = q.popleft()
        
            u, v = self.draw_edge_sp(number_missionaries, number_cannnibals, side, depth_level, node_num)    

            
            if self.is_start_state(number_missionaries, number_cannnibals, side):   
                v.set_style("filled")
                v.set_fillcolor("blue")
                v.set_fontcolor("white")
            elif self.is_goal_state(number_missionaries, number_cannnibals, side):
                v.set_style("filled")
                v.set_fillcolor("green")
                continue
                # return True
            elif self.number_of_cannibals_exceeds(number_missionaries, number_cannnibals):
                v.set_style("filled")
                v.set_fillcolor("red")
                continue
            else:
                v.set_style("filled")
                v.set_fillcolor("orange")

            if depth_level == max_depth:
                return True

            op = -1 if side == 1 else 1

            can_be_expanded = False

            # i = node_num
            for x, y in self.options:
                next_m, next_c, next_s = number_missionaries + op * x, number_cannnibals + op * y, int(not side)
                
               
                if Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)] is None or (next_m, next_c, next_s) != Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)][:3]:
                    if self.is_valid_move(next_m, next_c):
                        can_be_expanded = True
                        i += 1
                        q.append((next_m, next_c, next_s, depth_level + 1, i))
                        
                        # Keep track of parent
                        Parent[(next_m, next_c, next_s, depth_level + 1, i)] = (number_missionaries, number_cannnibals, side, depth_level, node_num)

            if not can_be_expanded:
                v.set_style("filled")
                v.set_fillcolor("gray")
        return False


    
    def write_image(self, name):
        file_name = "{}.svg".format(name)
        try:
            self.graph.write_svg(file_name)
        except Exception as e:
            print("Error while writing file", e)
        print(f"File {file_name} successfully written.")
    
    def return_image(self, name):
        file_name = "static/{}.svg".format(name)
        try:
            graph_svg = self.graph.write_svg(file_name)
            return graph_svg
        except Exception as e:
            print("Error while writing file", e)
            return e


if __name__ == "__main__":
    method = "bfs"
    s = Solution()
    s.solve(solve_method=method)
    s.show_solution()
    s.write_image(method)

    sol = Solution()
    sol.generate_solution_space()
    sol.write_image("full_space_tree")# s.write_image(method)
