import ast

def ast_analyze_python_code(code: str):
    issues = []

    try:
        tree = ast.parse(code)
        
    except SyntaxError:
        return [{
            "type": "syntax Error",
            "severity": "high",
            "description": "python code no valid!"
        }]
    
    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            # EVAL
            if isinstance(node.func, ast.Name):

                if node.func.id == "eval":

                    issues.append ({
                        "type": "dangerous function",
                        "severity": "high",
                        "description": "eval() use detected!"
                    })

            # EXEC
                elif isinstance(node.func, ast.Name) and node.func.id == "exec":
                    issues.append ({
                        "type": "dangerous function",
                        "severity": "high",
                        "description": "exec() use detected!"
                    })
    return issues