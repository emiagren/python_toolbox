"""
Main script that displays a menu of available tools for the user to select and run. 
The script dynamically loads and executes each tool's main function.
"""

import os
import importlib

def list_tools():
    """List all available tools (subfolders) in the toolbox folder."""
    tools = [f for f in os.listdir(".") if os.path.isdir(f) and os.path.isfile(os.path.join(f, f"{f}.py"))]
    return tools

def display_menu(tools):
    """Display the menu for selecting a tool."""
    print("Python Toolbox")
    print("--------------")
    for i, tool in enumerate(tools):
        print(f"{i + 1}. {tool}")
    print("0. Exit")

def load_tool(tool_name):
    """Import and run the main module inside the selected tool folder."""
    try:
        # Import the tool's main module by the folder and file name
        module = importlib.import_module(f"{tool_name}.{tool_name}")
        if hasattr(module, "main"):
            module.main()
        else:
            print(f"Could not run tool '{tool_name}'.")
    except Exception as e:
        print(f"Error loading tool '{tool_name}': {e}")

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
