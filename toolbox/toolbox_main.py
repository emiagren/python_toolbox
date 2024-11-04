"""
Main script that displays a menu of available tools for the user to select and run. 
The script dynamically loads and executes each tool's main function.
"""

import os
import sys
import importlib
import inspect

def list_tools():
    """List all available tools (subfolders) in the toolbox folder."""
    tools = [f for f in os.listdir(".") if os.path.isdir(f) and os.path.isfile(os.path.join(f, f"{f}.py"))]
    return tools

def display_menu(tools):
    """Display the menu for selecting a tool, formatting names nicely."""
    print("\nPython Toolbox")
    print("--------------")
    for i, tool in enumerate(tools):
        # Replace underscores with spaces and capitalize each word
        formatted_tool_name = tool.replace("_", " ").title()
        print(f"{i + 1}. {formatted_tool_name}")
    print("0. Exit")

def load_tool(tool_name):
    """
    Import and run the main module inside the selected tool folder, 
    with support for command-line arguments.
    """
    try:
        # Import the tool's main module
        module = importlib.import_module(f"{tool_name}.{tool_name}")

        # Check if the module has a main function
        if hasattr(module, "main"):
            # Get the main function
            main_func = module.main

            # Check if main expects arguments
            main_signature = inspect.signature(main_func)
            if len(main_signature.parameters) > 0:
                # Prompt user for arguments if main() has parameters
                args_input = input(
                    f"Enter arguments for '{tool_name}' (e.g., 'generate_key' or 'encrypt filename secret.key'): "
                    )
                args_list = args_input.split()  # Split user input to pass as argument list

                # Simulate command-line arguments by setting sys.argv
                sys.argv = [tool_name] + args_list
                main_func()  # Call main() with simulated command-line args
            else:
                # Call main() without arguments if none are expected
                main_func()
        else:
            print(f"Error: Tool '{tool_name}' does not have a 'main' function to run.")
    except ModuleNotFoundError:
        print(f"Error: Module '{tool_name}.{tool_name}' not found. Check folder and file names.")
    except AttributeError:
        print(f"Error: '{tool_name}' does not have a callable 'main' function.")
    except ImportError as e:
        print(f"Import error in '{tool_name}': {e}")


def main():
    """ 
    Main function that displays the menu of available tools,
    prompts the user to select a tool, then loads and runs the 
    selected tool's main function.
    """
    tools = list_tools()

    while True:
        display_menu(tools)

        # Prompt user for input
        try:
            choice = int(input("\nEnter the number of the tool you want to run: "))
            if choice == 0:
                print("Exiting the toolbox. Goodbye!")
                break
            elif 1 <= choice <= len(tools):
                tool_name = tools[choice - 1]
                print(f"\nRunning '{tool_name}'...\n")
                load_tool(tool_name)
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
