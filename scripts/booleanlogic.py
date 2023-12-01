from pyparsing import infixNotation, opAssoc, Keyword, Word, alphas
import re
"""
Boolean Logic Evaluator

This Python file defines classes and functions for evaluating boolean logic expressions. It includes classes for representing boolean operands, binary operations (AND, OR, NOT), and methods for parsing and evaluating logical expressions.

Classes:
- BoolOperand: Represents a boolean operand with a label and value.
- BoolBinOp: Base class for binary boolean operations.
- BoolAnd: Represents a boolean AND operation.
- BoolOr: Represents a boolean OR operation.
- BoolNot: Represents a boolean NOT operation.

Functions:
- check_exclusion: Evaluates course exclusion based on a given rule.
- extract_courses: Extracts course codes from a string using regular expressions.
- replace_variables: Replaces variables in an expression with their associated values.

Author: [Hayden Jenkins]
Date: [11/01/23]

Example usage:
- Use check_exclusion to evaluate course exclusion rules.
"""

class BoolOperand:
    """
    Represents a boolean operand.

    Attributes:
    - label (str): The label of the operand.
    - value (bool): The boolean value of the operand.
    """

    def __init__(self, t):
        """
        Initializes a BoolOperand.

        Args:
        - t (str): The input operand.
        """
        self.label = t[0]
        self.value = t[0] == "True"

    def __bool__(self):
        """
        Converts the operand to a boolean value.

        Returns:
        - bool: The boolean value of the operand.
        """
        return self.value

    def __str__(self):
        """
        Returns a string representation of the operand.

        Returns:
        - str: String representation of the operand.
        """
        return self.label

    __repr__ = __str__
    __nonzero__ = __bool__

class BoolBinOp:
    """
    Represents a boolean binary operation.

    Attributes:
    - args (list): The list of arguments for the binary operation.
    - reprsymbol (str): The string representation of the binary operation.
    - evalop (function): The function used to evaluate the binary operation.
    """

    def __init__(self, t):
        """
        Initializes a BoolBinOp.

        Args:
        - t (str): The input binary operation.
        """
        self.args = t[0][0::2]

    def __str__(self):
        """
        Returns a string representation of the binary operation.

        Returns:
        - str: String representation of the binary operation.
        """
        sep = f" {self.reprsymbol} "
        return "(" + sep.join(map(str, self.args)) + ")"

    def __bool__(self):
        """
        Converts the binary operation to a boolean value.

        Returns:
        - bool: The boolean value of the binary operation.
        """
        return self.evalop(bool(a) for a in self.args)

    __nonzero__ = __bool__
    __repr__ = __str__

class BoolAnd(BoolBinOp):
    """
    Represents a boolean AND operation.

    Inherits from BoolBinOp.
    """
    reprsymbol = '&'
    evalop = all

class BoolOr(BoolBinOp):
    """
    Represents a boolean OR operation.

    Inherits from BoolBinOp.
    """
    reprsymbol = '|'
    evalop = any

class BoolNot:
    """
    Represents a boolean NOT operation.

    Attributes:
    - arg: The argument of the NOT operation.
    """

    def __init__(self, t):
        """
        Initializes a BoolNot.

        Args:
        - t (str): The input NOT operation.
        """
        self.arg = t[0][1]

    def __bool__(self):
        """
        Converts the NOT operation to a boolean value.

        Returns:
        - bool: The boolean value of the NOT operation.
        """
        v = bool(self.arg)
        return not v

    def __str__(self):
        """
        Returns a string representation of the NOT operation.

        Returns:
        - str: String representation of the NOT operation.
        """
        return "~" + str(self.arg)

    __repr__ = __str__
    __nonzero__ = __bool__

def extract_courses(course_string):
    """
    Extracts course codes from a string using a regular expression.

    Args:
    - course_string (str): The input string containing course codes.

    Returns:
    - list: List of extracted course codes.
    """
    pattern = r'\b[A-Z]{4}-\d{3}\b'
    return re.findall(pattern, course_string)

def extract_programs(program_string):
    """
    Extracts program codes from a string using a regular expression.

    Args:
    - program_string (str): The input string containing program codes.

    Returns:
    - list: List of extracted program codes.
    """
    pattern = r'\b[A-Z]{4}\b'
    return re.findall(pattern, program_string)

def replace_variables(expression, variable_dict):
    """
    Replaces variables in an expression with their associated values.

    Args:
    - expression (str): The expression with variables.
    - variable_dict (dict): A dictionary mapping variables to values.

    Returns:
    - str: The expression with variables replaced by values.
    """
    for variable, value in variable_dict.items():
        expression = expression.replace(variable, str(value))
    return expression

def check_exclusion(course_wish_list, completed_courses, rule):
    """
    Check course exclusion based on a given rule.

    Args:
    - course_wish_list (list): List of courses the user wishes to take.
    - completed_courses (list): List of courses the user has completed.
    - rule (str): The exclusion rule to evaluate.

    Returns:
    - bool: The result of the exclusion rule evaluation.
    """

    TRUE = Keyword("True")
    FALSE = Keyword("False")
    boolOperand = TRUE | FALSE | Word(alphas, max=1)
    boolOperand.setParseAction(BoolOperand)

    boolExpr = infixNotation(boolOperand, [
        ("NOT", 1, opAssoc.RIGHT, BoolNot),
        ("AND", 2, opAssoc.LEFT, BoolAnd),
        ("OR", 2, opAssoc.LEFT, BoolOr),
    ])

    all_courses = course_wish_list + completed_courses
    all_courses = list(dict.fromkeys(all_courses)) #remove any duplicates
    exclusions = set(extract_courses(rule))

    premises = {}
    for course in exclusions:
        value = course in all_courses
        premises[course] = value

    expression = replace_variables(rule, premises)
    return not bool(boolExpr.parseString(expression)[0])

def check_prerequisite(course_wish_list, completed_courses, rule):
    """
    Check course prerequisites based on a given rule.

    Args:
    - course_wish_list (list): List of courses the user wishes to take.
    - completed_courses (list): List of courses the user has completed.
    - rule (str): The prerequisite rule to evaluate.

    Returns:
    - bool: The result of the prerequisite rule evaluation.
    """

    TRUE = Keyword("True")
    FALSE = Keyword("False")
    boolOperand = TRUE | FALSE | Word(alphas, max=1)
    boolOperand.setParseAction(BoolOperand)

    boolExpr = infixNotation(boolOperand, [
        ("NOT", 1, opAssoc.RIGHT, BoolNot),
        ("AND", 2, opAssoc.LEFT, BoolAnd),
        ("OR", 2, opAssoc.LEFT, BoolOr),
    ])

    prerequisites = set(extract_courses(rule))

    premises = {}
    for course in prerequisites:
        value = course in completed_courses
        premises[course] = value

    expression = replace_variables(rule, premises)
    return bool(boolExpr.parseString(expression)[0])

def check_corequisite(course_wish_list, completed_courses, rule):
    """
    Check course corequisite based on a given rule.

    Args:
    - course_wish_list (list): List of courses the user wishes to take.
    - completed_courses (list): List of courses the user has completed.
    - rule (str): The corequisite rule to evaluate.

    Returns:
    - bool: The result of the corequisite rule evaluation.
    """

    TRUE = Keyword("True")
    FALSE = Keyword("False")
    boolOperand = TRUE | FALSE | Word(alphas, max=1)
    boolOperand.setParseAction(BoolOperand)

    boolExpr = infixNotation(boolOperand, [
        ("NOT", 1, opAssoc.RIGHT, BoolNot),
        ("AND", 2, opAssoc.LEFT, BoolAnd),
        ("OR", 2, opAssoc.LEFT, BoolOr),
    ])

    all_courses = course_wish_list + completed_courses
    all_courses = list(dict.fromkeys(all_courses)) #remove any duplicates
    corequisites = set(extract_courses(rule))

    premises = {}
    for course in corequisites:
        value = course in all_courses
        premises[course] = value

    expression = replace_variables(rule, premises)
    return bool(boolExpr.parseString(expression)[0])

def check_program(student_program, rule):
    """
    Check course program requirement based on a given rule.

    Args:
    - student_program (string): The program the student is enrolled in.
    - rule (str): The program rule to evaluate.

    Returns:
    - bool: The result of the program rule evaluation.
    """

    TRUE = Keyword("True")
    FALSE = Keyword("False")
    boolOperand = TRUE | FALSE | Word(alphas, max=1)
    boolOperand.setParseAction(BoolOperand)

    boolExpr = infixNotation(boolOperand, [
        ("NOT", 1, opAssoc.RIGHT, BoolNot),
        ("AND", 2, opAssoc.LEFT, BoolAnd),
        ("OR", 2, opAssoc.LEFT, BoolOr),
    ])

    programs = set(extract_programs(rule))

    premises = {}
    for program in programs:
        value = program == student_program 
        premises[program] = value

    expression = replace_variables(rule, premises)
    return bool(boolExpr.parseString(expression)[0])