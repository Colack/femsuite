import re

class FemScriptInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def run(self, code):
        lines = code.split("\n")
        self.execute_block(lines)

    def execute_block(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("#"):
                i += 1
                continue

            if line.startswith("sparkle") and "(" in line and line.endswith("{"):
                match = re.search(r"sparkle (\w+)\((.*?)\) \{", line)
                if match:
                    func_name, params = match.groups()
                    block, end_idx = self.get_block(lines, i + 1)
                    self.functions[func_name] = {"params": params.split(","), "block": block}
                    i = end_idx
                else:
                    print("UwU >~< Couldn't understand function declaration!")

            elif "(" in line and ")" in line:
                match = re.search(r"(\w+)\((.*)\)", line)
                if match:
                    func_name, args = match.groups()
                    self.handle_function_call(func_name, args.split(","))
                else:
                    print(f"UwU >~< Couldn't understand function call: {line}")

            elif line.startswith("uwu"):
                self.handle_uwu(line)

            elif line.startswith("sparkle"):
                match = re.search(r"sparkle (\w+) = (.+)", line)
                if match:
                    var_name, value = match.groups()
                    self.variables[var_name] = self.eval_expression(value)
                else:
                    print("UwU >~< Couldn't understand sparkle declaration!")

            elif line.startswith("blush"):
                match = re.search(r"blush (.+) \{", line)
                if match:
                    condition = self.eval_expression(match.group(1))
                    if condition:
                        block, end_idx = self.get_block(lines, i + 1)
                        self.execute_block(block)
                        i = end_idx
                else:
                    print("UwU >~< Couldn't understand blush condition!")

            elif line.startswith("kawaii"):
                match = re.search(r"kawaii (.+) \{", line)
                if match:
                    condition_expr = match.group(1)
                    block, end_idx = self.get_block(lines, i + 1)
                    while self.eval_expression(condition_expr):
                        self.execute_block(block)
                    i = end_idx
                else:
                    print("UwU >~< Couldn't understand kawaii loop!")

            else:
                print(f"UwU >~< Unknown command: {line}")
            
            i += 1

    def handle_uwu(self, line):
        match = re.search(r'uwu (.+)', line)
        if match:
            content = match.group(1)
            try:
                parts = content.split("💕")
                evaluated_parts = [str(self.eval_expression(part.strip())) for part in parts]
                print("".join(evaluated_parts))
            except Exception as e:
                print(f"UwU >~< Something went wrong with uwu! {e}")
        else:
            print("UwU >~< Couldn't understand uwu!")

    def handle_function_call(self, func_name, args):
        if func_name in self.functions:
            func = self.functions[func_name]
            params = [p.strip() for p in func["params"] if p.strip()]
            if len(params) != len(args):
                print(f"UwU >~< Argument mismatch for function '{func_name}'!")
                return

            prev_vars = self.variables.copy()

            for param, arg in zip(params, args):
                self.variables[param] = self.eval_expression(arg.strip())

            self.execute_block(func["block"])

            return_value = self.variables.get("return", None)

            self.variables = prev_vars

            return return_value
        else:
            print(f"UwU >~< Undefined function '{func_name}'!")

    def get_block(self, lines, start_idx):
        block = []
        brace_count = 1
        i = start_idx
        while i < len(lines):
            line = lines[i].strip()
            if line.endswith("{"):
                brace_count += 1
            elif line == "}":
                brace_count -= 1
                if brace_count == 0:
                    break
            block.append(line)
            i += 1
        return block, i

    def eval_expression(self, expr):
        expr = expr.replace("💕", "+").replace("💔", "-")
        expr = expr.replace("💖", "*").replace("✨", "/")
        try:
            return eval(expr, {}, self.variables)
        except Exception as e:
            print(f"UwU >~< Evaluation error: {e}")
            return expr.strip('"')

interpreter = FemScriptInterpreter()