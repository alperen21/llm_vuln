from langchain_core.tools import tool
from langchain.tools import Tool
import json


def load_json_file(file_path: str) -> dict:
    """
    Loads a JSON file and returns its contents as a dictionary.

    Parameters:
        file_path (str): The path to the JSON file to be loaded.
    Returns:
        dict: The contents of the JSON file as a dictionary.
    Example:
        >>> data = load_json_file('/path/to/file.json')
        >>> print(data)
        {'key': 'value'}
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def get_call_graph():
    current_session = load_json_file("current_session.json")
    call_graph_file = current_session["call_graph_file"]
    call_graph = load_json_file(call_graph_file)
    
    return call_graph
    

@tool
def get_callers(function_name : str) -> list:
    """
    Returns the list of functions that call the given function.

    Parameters:
        function_name (str): The name of the function to find callers for.
    Returns:
        list[str]: A list of function names that call the given function.
    Example:
        >>> callers = get_callers('my_function')
        >>> print(callers)
        ['caller_function1', 'caller_function2']
    """
    call_graph = get_call_graph()
    
    if function_name not in call_graph:
        print(f"Function {function_name} not found in call graph.")
        return []
    else:
        return call_graph[function_name]["callers"]

@tool
def get_function_body(function_name : str) -> str:
    """
    Retrieves the body of a function as a string.
        Args:
            function_name (str): The name of the function whose body is to be retrieved.
        Returns:
            str: A string representing the function body.
        Example:
            >>> body = get_function_body('my_function')
            >>> print(body)
            def my_function():
                # function body
                pass
    """ 
    
    call_graph = get_call_graph()
    
    return call_graph[function_name.replace("'","").strip()]["function_body"]
    


REACT_TOOLS = [
    Tool(
        name="get_callers",
        func=get_callers,
        description=(
            """
            Returns the list of functions that call the given function.

            Parameters:
                function_name (str): The name of the function to find callers for.
            Returns:
                list[str]: A list of function names that call the given function.
            Example:
                >>> callers = get_callers('my_function')
                >>> print(callers)
                ['caller_function1', 'caller_function2']
            """
        )
    ),
    
    Tool(
        name="get_function_body",
        func=get_function_body,
        description=(
            """
            Retrieves the body of a function as a string.
                Args:
                    function_name (str): The name of the function whose body is to be retrieved.
                Returns:
                    str: A string representing the function body.
                Example:
                    >>> body = get_function_body('my_function')
                    >>> print(body)
                    def my_function():
                        # function body
                        pass
            """ 
        )
    )
]