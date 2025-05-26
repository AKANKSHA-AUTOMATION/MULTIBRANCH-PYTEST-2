def calculator(a,b,operations):
    """
    Perform basic arithmetic operations on two numbers.
    
    Parameters:
    a (int,float) : The first number.
    b (int,float) : The second number.
    operations (list) : A list of operations to perfor,. Supported operations are 'add', 'subtract', 'multiply', 'divide'.

    Returns:
    dict : A dictionary with the results of the operations.

    """

    results = {}

    if 'add' in operations:
        results['add'] = a+b

    if 'subtract' in operations:
        results['subtract'] = a-b

    if 'multiply' in operations:
        results['multiply'] = a*b

    if 'divide' in operations:
        if b !=0:
            results['divide'] = a/b

        else:
            results['divide'] = "Error: Division by zero"

    return results

if __name__ == "__main__":
    a = 90
    b = 80
    operations = ['add','subtract','multiply','divide']
    results = calculator(a,b,operations)
    print(results)


