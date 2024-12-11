

def construct_prompt(function_body):
    return f"""
    You are a security researcher tasked with identifying vulnerabilities in a codebase. You have been given a function to analyze. 
    The function may or may not be vulnerable
    
    If you think it is vulnerable reply with @@VULNERABLE@@, otherwise reply with @@NOT VULNERABLE@@
    
    If you think the function is vulnerable, please provide the CWE number that you think is most relevant to the vulnerability in the form of @@CWE: <CWE_NUMBER>@@
    
    For example:
    
    @@VULNERABLE@@
    @@CWE: CWE-1234@@
    
    Here is the function:
    
    ```c
    {function_body}
    ```
    """
    