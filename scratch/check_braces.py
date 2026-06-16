def check_braces(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    line_num = 1
    col_num = 1
    stack = []
    
    for i, char in enumerate(content):
        if char == '\n':
            line_num += 1
            col_num = 1
        else:
            col_num += 1
            
        if char == '{':
            stack.append((line_num, col_num))
        elif char == '}':
            if not stack:
                print(f"Error: Unmatched closing brace '}}' at line {line_num}, column {col_num}")
                return False
            stack.pop()
            
    if stack:
        for line, col in stack:
            print(f"Error: Unmatched opening brace '{{' at line {line}, column {col}")
        return False
        
    print("All braces are correctly matched!")
    return True

if __name__ == "__main__":
    check_braces("/Users/lap/Code/css/css.css")
