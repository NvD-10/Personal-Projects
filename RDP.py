import tkinter as tk

class ParseNode:
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children or []

class Grammar:
    def __init__(self, grammar, start, logger):
        self.logger = logger
        self.productions = self.getProductions(grammar)
        self.start = start
        self.eliminateLeftRecursion()
    
    def log(self, message):
        self.logger(message)
    
    def getProductions(self, text):
        grammar = {}
        for line in text.strip().split("\n"):
            left, right = line.split("->")
            left = left.strip()
            grammar[left] = []
            for r in right.split("|"):
                symbols = r.strip().split()
                grammar[left].append([] if symbols == ["ε"] else symbols)
        return grammar
    
    def eliminateLeftRecursion(self):
        new_grammar = {}
        for variable in self.productions:
            normal, recursive = [], []
            for production in self.productions[variable]:
                if production and production[0] == variable:
                    recursive.append(production[1:])
                else:
                    normal.append(production)
            if recursive:
                self.log(f"Left Recursion Detected in {variable}")
                prime = variable + "'"
                new_grammar[variable] = []
                for prod in normal:
                    new_grammar[variable].append(prod + [prime])
                new_grammar[prime] = []
                for prod in recursive:
                    new_grammar[prime].append(prod + [prime])
                new_grammar[prime].append([])
            else:
                new_grammar[variable] = self.productions[variable]
        self.productions = new_grammar
    
    def __str__(self):
        output = []
        for variable in self.productions:
            parts = []
            for production in self.productions[variable]:
                parts.append(" ".join(production) if production else "ε")
            output.append(f"{variable} -> {' | '.join(parts)}")
        return "\n".join(output)

class RDP:
    def __init__(self, grammar, logger):
        self.logger = logger
        self.grammar = grammar
        self.input = ""
        self.position = 0
    
    def log(self, message):
        self.logger(message)
    
    def parse(self, input):
        self.input = input
        self.position = 0
        self.log(f"Parsing started from {self.grammar.start}")
        tree = self.parseVariable(self.grammar.start)
        if tree and self.position == len(input):
            self.log("ACCEPT")
            return tree
        self.log("REJECT")
        return None
    
    def parseVariable(self, variable):
        self.log(f"Expand {variable} at position {self.position}")
        for production in self.grammar.productions[variable]:
            saved = self.position
            children = []
            self.log(f"Trying {variable} -> {' '.join(production) if production else 'ε'}")
            succcess = True
            for symbol in production:
                if symbol.isupper() or symbol.endswith("'"):
                    node = self.parseVariable(symbol)
                else:
                    node = self.match(symbol)
                if node is None:
                    succcess = False
                    break
                children.append(node)
            if not production:
                children.append(ParseNode('ε'))
            if succcess:
                return ParseNode(variable, children)
            self.log("Wrong Production")
            self.position = saved
        return None
    
    def match(self, terminal):
        if self.position < len(self.input) and self.input[self.position] == terminal:
            self.log(f"Matched '{terminal}'")
            self.position += 1
            return ParseNode(terminal)
        self.log(f"Failed to match '{terminal}'")
        return None

class TreeDrawer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 20
        self.y_step = 36

    def draw(self, node, x, y):
        box_w = 20
        box_h = 20

        self.canvas.create_rectangle(
            x - box_w//2, y - box_h//2,
            x + box_w//2, y + box_h//2
        )
        self.canvas.create_text(x, y, text=node.symbol)

        if not node.children:
            return x

        child_x = x - (len(node.children) - 1) * 50 // 2
        centers = []

        for child in node.children:
            cx = self.draw(child, child_x, y + self.y_step)
            centers.append(cx)
            child_x += 50

        for cx in centers:
            self.canvas.create_line(x, y + box_h//2, cx, y + self.y_step - box_h//2)

        return sum(centers) // len(centers)


def runGUI():
    root = tk.Tk()
    root.title("Recursive Descent Parser")
    tk.Label(root, text="Grammar").pack()
    grammar_box = tk.Text(root, height=6, width=60)
    grammar_box.pack()
    tk.Label(root, text="Start Symbol").pack()
    start_entry = tk.Entry(root)
    start_entry.pack()
    tk.Label(root, text="Input String").pack()
    input_entry = tk.Entry(root)
    input_entry.pack()
    output = tk.Text(root, height=15, width=80)
    output.pack()
    canvas = tk.Canvas(root, width=800, height=200, bg="white")
    canvas.pack()


    def log(message):
        output.insert("end", message + "\n")
        output.see("end")
    
    def run_parser():
        output.delete("1.0", "end")
        grammar = Grammar(
            grammar_box.get("1.0", "end"),
            start_entry.get(),
            log
        )
        log("Final Grammar:")
        log(str(grammar))
        parser = RDP(grammar, log)
        tree = parser.parse(input_entry.get())
        if tree:
            drawer = TreeDrawer(canvas)
            drawer.draw(tree, 300, 30)
    
    tk.Button(root, text="Parse", command=run_parser).pack()
    root.mainloop()

runGUI()
