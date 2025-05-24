def create_test_file():
    """
    Creates a Python test file with a simple testing function
    """
    test_content = '''
def testing():
    """
    A simple test function that does nothing and just passes
    """
    pass


if __name__ == "__main__":
    print("Running testing function...")
    testing()
    print("Testing complete!")
'''
    
    with open("test/tester.py", "w") as f:
        f.write(test_content)
    
    print("Test file created successfully at code/tester.py")

if __name__ == "__main__":
    create_test_file()