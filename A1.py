import os
from typing import Union, List, Optional


alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
all_valid_chars = var_chars + ["(", ")", ".", "\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"


def read_lines_from_txt(fp: [str, os.PathLike]) -> List[str]:
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """
    with open(fp) as f:
        lines = f.read().splitlines()
    return lines


def is_valid_var_name(s: str) -> bool:
    """
    Checks if a string is a valid variable name.

    :param s: Input string
    :return: True if the name starts with a letter and contains only letters and digits
    """
    # Check if the first character is a letter
    if (s[0] in alphabet_chars):
        # Check if all characters are letters or digits
        for i in s:
            if not (i in alphabet_chars or i in numeric_chars):
                return False    
        return True
    return False





class Node:
    """
    Nodes in a parse tree
    Attributes:
        elem: a list of strings
        children: a list of child nodes
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem if elem is not None else []
        self.children = []


    def add_child_node(self, node: 'Node') -> None:
        self.children.append(node)




class ParseTree:   # A class to represent a full parse tree.
    
    def __init__(self, root, tokens: Optional[List[str]] = None):
        self.root = root # The root node of the tree
        self.length = len(tokens) if tokens else None  # Length of the tokens list(to know when to stop)
        self.global_counter = 0  # counter for printed elements
        self.stopped = False  # Flag to stop

    def print_tree(self, node: Optional[Node] = None, level: int = -1) -> None:
        """
        Prints the parse tree, respecting the global length limit.

        :param node: The current node being processed (defaults to root).
        :param level: Current level in the tree for indentation (defaults to -1 in order to print root).
        """
        if self.stopped:
            return  # Stop if length is reached

        if node is None:
            node = self.root

        # Loop through each element in the node
        for e in node.elem:
            if self.global_counter == self.length:  # Stop if length limit is reached
                self.stopped = True
                return  
            
            if e == '\\' or e == '(' or (self.global_counter == 0):  # Print '\\' or '(' with correct formatting
                print('----' * level + '_'.join((node.elem[self.global_counter:])))
                level += 1
                print('----' * level + '_'.join(e))
                self.global_counter += 1
            else:
                print('----' * level + '_'.join(e)) # Print regular elements
                self.global_counter += 1
        
        # Recursively print child nodes
        for child in node.children:
            if not self.stopped:
                self.print_tree(child, level + 1)
       



def parse_tokens(s_: str) -> Union[List[str], bool]: 
    """
    Parse input string into tokens for valid syntax.
    :param s_: The input string
    :return: List of tokens or False if invalid
    """
    spaceNum = 0
    if s_[0] == '\\':  # Check for incomplete lambda expression
        if len(s_) == 1 or len(s_) == 2:      
            print(f"Error at position {0}: lambda expression missing parts '{s_[0]}'.")
            return False

    for k in range(len(s_)):  # Loop through s_
        if s_[k] == '.' and s_[k-1] == ' ':  # Check for invalid space before dot
            print(f"Error at position {k-1}: Invalid space before dot '{s_[k-1]}'.")
            return False

        if s_[k] == ' ':  # Multiple spaces check
            spaceNum += 1
            if s_[k-1] == '\\':  # Invalid space after '\\'
                print(f"Error at position {k-1}: Invalid space in lambda expression '{s_[k-1]}'.")
                return False
            else:
                continue
        if spaceNum > 1:  # More than one space
            print(f"Error at position {k}: Invalid spacing.")
            continue
        else:
            spaceNum = 0 #reset spaceNum(dont want more than one space bewteen items)

    s = s_.replace(' ', '_')  # Replace spaces with '_'
    tokens = []
    i = 0
    closePram_ToAdd = 0 # ) needed to add at the end due to . operator
    open_parensExtra = 0 # counter for ( to check for equality in ( and )
    openPranDone = 0 # see if first bracket done is a ) which would be invalid

    while i < len(s):  # Tokenize the string
        char = s[i]
        if char == '\\':  # Lambda token
            tokens.append('\\')
            i += 1
        elif char == '_':  # Skip underscores
            i += 1
        elif char == '(':  # Open parenthesis
            tokens.append('(')
            openPranDone += 1
            open_parensExtra -= 1
            i += 1
        elif char == ')':  # Close parenthesis
            if openPranDone == 0:
                print(f"Error at position {i}: Invalid close parenthesis '{char}'.")
                return False
            tokens.append(')')
            open_parensExtra += 1
            if s[i-1] == '(':
                print(f"Error at position {i}: Empty expression '{char}'.")
                return False
            if s[i-1] == '.':
                print(f"Error at position {i}: Empty expression after dot '{char}'.")
                return False
            i += 1
        elif char == '.':  # Dot represents an open parenthesis
            tokens.append('(')
            closePram_ToAdd += 1
            i += 1
        elif char in alphabet_chars:  # Valid variable names
            var = char
            i += 1
            while i < len(s) and s[i] in var_chars:
                var += s[i]
                i += 1
            if is_valid_var_name(var):
                tokens.append(var)
            else:
                print(f"Error at position {i}: Invalid variable name '{var}'.")
                return False
        else:  # Invalid character
            print(f"Error at position {i}: Invalid character '{char}'.")
            return False

    if closePram_ToAdd != 0:  # Check for unmatched parentheses
        if tokens[-1] == '(':
            print(f"Error at position {i}: Empty expression.")
            return False
        goal = 0
        while goal != closePram_ToAdd:
            tokens.append(')')
            goal += 1

    if open_parensExtra < 0:  # Missing closing parenthesis
        print(f"Error at position {i}: Missing close parenthesis.")
        return False

    if open_parensExtra > 0:  # Missing opening parenthesis
        print(f"Error at position {i}: Missing open parenthesis.")
        return False
   
    for c in range(len(tokens)): #lambda error checking
       
        if(tokens[c] == '\\' and (len(tokens) == 2)):
            print(f"Error at position {c}: Invalid lamda expression '{tokens[c]}'.")
            return False
       
        if len(tokens) - c > 2:
            if (tokens[c] == '\\') and not((is_valid_var_name(tokens[c+1])) and ((is_valid_var_name(tokens[c+2])) or ((tokens[c+2] == '(') and ((tokens[c+3] == '(') or (tokens[c+3] == '\\') or (is_valid_var_name(tokens[c+3]))) and ((tokens[c+4] == '(') or (is_valid_var_name(tokens[c+4])) or (tokens[c+4] == ')'))))):
                print(f"Error at position {c}: Invalid lamda expression '{tokens[c]}'.")
                return False
       
    return tokens




def read_lines_from_txt_check_validity(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string  to yield a tokenized list of strings for printing, joined by _ characters
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string {l} is {'_'.join(tokens)}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")
    else:
        print(f"Not All lines are valid") # Added this to show when there is an atleast one invalid example


def read_lines_from_txt_output_parse_tree(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string to yield a tokenized output string, to be used in constructing a parse tree. The
    parse tree should call print_tree() to print its content to the console.
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()




def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    Recursively build a parse tree from a list of tokens.
    :param tokens: A list of token strings
    :param node: A Node object
    :return: A node with children representing variables, parentheses, or lambdas
    """
    first = False
    if node is None:  # Create root node if not provided
        node = Node()
        first = True

    index = 0
    node.elem = tokens  # set tokens to the node's element list

    # Traverse through the tokens
    while index < len(tokens):
        token = tokens[index]

        if token == '(':  # Handle opening parenthesis(want to print remaining tokens, then resume normally)
            node.add_child_node(Node(node.elem))
            return build_parse_tree_rec(tokens[1:], node)

        if token == ')':  # Handle closing parenthesis
            node.add_child_node(Node([')']))
            index += 1
            return build_parse_tree_rec(tokens[1:], node)

        elif token == '\\':  # Handle lambda expressions(want to print remaining tokens, then resume normally)
            node.add_child_node(Node(node.elem))
            return build_parse_tree_rec(tokens[1:], node)
        
        elif (is_valid_var_name(token)) and (first == True):  # Handle lambda expressions(want to print remaining tokens, then resume normally)
            node.add_child_node(Node(node.elem))
            return build_parse_tree_rec(tokens[1:], node)

        elif is_valid_var_name(token):  # Handle valid variable names
            node.add_child_node(Node([token]))
            index += 1
            return build_parse_tree_rec(tokens[1:], node)
	
    return node 



def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a parse tree from a list of tokens
    :param tokens: List of tokens
    :return: parse tree
    """
    print("\n")
    root_node = build_parse_tree_rec(tokens)
    return ParseTree(root_node, tokens)
    


if __name__ == "__main__":


    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)
    read_lines_from_txt_output_parse_tree(valid_examples_fp)
    print("Checking invalid examples...")
    read_lines_from_txt_check_validity(invalid_examples_fp)