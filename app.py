from flask import Flask, render_template, jsonify, request
import random
import copy

app = Flask(__name__)

# Classe représentant un arbre dans la forêt
class Tree:
    def __init__(self, state=0):
        self.state = state  # 0: vide, 1: arbre sain, 2: arbre en feu, 3: arbre brûlé

    # Met à jour l'état de l'arbre en fonction de la présence d'un voisin en feu
    def update_state(self, has_burning_neighbor):
        if self.state == 1 and has_burning_neighbor:
            self.state = 2
        elif self.state == 2:
            self.state = 3

# Classe représentant la forêt
class Forest:
    def __init__(self, rows, cols, prob_tree, prob_empty):
        self.rows = rows
        self.cols = cols
        self.prob_tree = prob_tree
        self.prob_empty = prob_empty
        self.grid = [[self._generate_tree() for _ in range(cols)] for _ in range(rows)]
        self._ignite_random_tree()
        self.initial_trees = sum(tree.state == 1 for row in self.grid for tree in row)
        self.total_trees = self.initial_trees
        self.initial_burning_trees = 1
        self.burnt_trees = 0

    # Génère un arbre en fonction des probabilités définies
    def _generate_tree(self):
        if random.random() < self.prob_empty:
            return Tree(0)
        elif random.random() < self.prob_tree:
            return Tree(1)
        else:
            return Tree(0)

    # Allume un arbre aléatoire pour commencer l'incendie
    def _ignite_random_tree(self):
        while True:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.grid[row][col].state == 1:
                self.grid[row][col].state = 2
                break

    # Affiche la grille sous forme de liste de listes représentant les états des arbres
    def display_grid(self):
        return [[tree.state for tree in row] for row in self.grid]

    # Vérifie si un arbre a un voisin en feu
    def has_burning_neighbor(self, row, col):
        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        for r, c in neighbors:
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c].state == 2:
                return True
        return False

    # Met à jour la grille en propageant le feu
    def update_grid(self):
        new_grid = copy.deepcopy(self.grid)
        for row in range(self.rows):
            for col in range(self.cols):
                new_grid[row][col].update_state(self.has_burning_neighbor(row, col))
        self.grid = new_grid
        self.burnt_trees = sum(tree.state == 3 for row in self.grid for tree in row)

    # Retourne les statistiques actuelles de la forêt
    def get_statistics(self):
        surface = self.rows * self.cols
        burning_trees = sum(tree.state == 2 for row in self.grid for tree in row)
        return {
            "total_trees": self.total_trees,
            "surface": surface,
            "burnt_trees": self.burnt_trees,
            "damage_percentage": (self.burnt_trees / self.total_trees) * 100 if self.total_trees > 0 else 0
        }

forest = None  # Variable globale pour contenir l'objet forêt

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/index')
def index():
    return render_template('index.html')

# Initialiser la forêt avec les paramètres donnés
@app.route('/initialize', methods=['POST'])
def initialize():
    rows = int(request.json.get('rows', 20))
    cols = int(request.json.get('cols', 20))
    prob_tree = float(request.json.get('prob_tree', 0.7))
    prob_empty = float(request.json.get('prob_empty', 0.3))
    global forest  # Utiliser le mot-clé global pour modifier la variable globale
    forest = Forest(rows, cols, prob_tree, prob_empty)
    return jsonify(forest.display_grid())

# Met à jour l'état de la forêt
@app.route('/update', methods=['POST'])
def update():
    global forest  # Utiliser le mot-clé global pour accéder à la variable globale
    if forest is None:
        return jsonify({"error": "Forest not initialized"}), 400
    forest.update_grid()
    return jsonify(forest.display_grid())

# Retourne les statistiques actuelles de la forêt
@app.route('/statistics', methods=['GET'])
def statistics():
    global forest
    if forest is None:
        return jsonify({"error": "Forest not initialized"}), 400
    return jsonify(forest.get_statistics())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
