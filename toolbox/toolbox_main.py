"""
Main script that displays a menu of available tools for the user to select and run.
The script dynamically loads and executes each tool's main function with command-line arguments.
"""

import os
import sys
import importlib

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

def show_tool_arguments(tool_name):
    """
    Display the unique argument options for a tool, 
    if the tool provides a get_parser function.
    """
    try:
        # Load the tool module and check for a 'get_parser' function
        module = importlib.import_module(f"{tool_name}.{tool_name}")
        if hasattr(module, "get_parser"):
            parser = module.get_parser()
            if parser:
                parser.print_help()
            else:
                print(f"No argument information available for '{tool_name}'.")
        else:
            print(f"No argument information available for '{tool_name}'.")
    except ModuleNotFoundError:
        print(f"Error: Module '{tool_name}.{tool_name}' not found.")
    except ImportError as e:
        print(f"Import error in '{tool_name}': {e}")

def load_tool(tool_name):
    """
    Import and run the main module inside the selected tool folder, 
    with command-line arguments.
    """
    try:
        # Import the tool's main module
        module = importlib.import_module(f"{tool_name}.{tool_name}")

        # Check if the module has a main function
        if hasattr(module, "main"):
            # Display the argument options before prompting for user input
            print(f"\nArgument options for '{tool_name}':")
            show_tool_arguments(tool_name)

            while True:  # Loop to allow retrying arguments or going back
                args_input = input(
                    f"\nEnter arguments for '{tool_name}' (type 'm' to return to menu): "
                )

                if args_input.strip().lower() == 'm':  # Allow the user to return to the menu
                    print("Returning to the main menu...")
                    break

                args_list = args_input.split()  # Split input to pass as argument list

                # Temporarily replace sys.argv to simulate command-line arguments
                original_argv = sys.argv  # Save original sys.argv
                sys.argv = [tool_name] + args_list  # Set sys.argv for this tool

                try:
                    module.main()  # Call main() with simulated command-line args
                finally:
                    sys.argv = original_argv  # Restore original sys.argv

                # Prompt user for action
                next_action = input("\nWould you like to try again? (y/n): ").strip().lower()
                if next_action != 'y':
                    break
        else:
            print(f"Error: Tool '{tool_name}' does not have a 'main' function to run.")
    except ModuleNotFoundError:
        print(f"Error: Module '{tool_name}.{tool_name}' not found.")
    except ImportError as e:
        print(f"Import error in '{tool_name}': {e}")

def main():
    """
    Main function that displays the menu of available tools,
    prompts the user to select a tool, then shows its argument help,
    and finally runs the tool with provided command-line arguments.
    """
    tools = list_tools()

    while True:
        display_menu(tools)

        # Prompt user for input
        try:
            choice = input("\nEnter the number of the tool you want to run: ")

            if choice == '0':
                print("Exiting the toolbox. Goodbye!")
                break
            else:
                try:
                    tool_choice = int(choice)
                    if 1 <= tool_choice <= len(tools):
                        tool_name = tools[tool_choice - 1]
                        print(f"\nPreparing to run '{tool_name}'...\n")
                        load_tool(tool_name)
                    else:
                        print("Invalid tool selection. Please try again.")
                except ValueError:
                    print("Invalid selection. Please enter a number.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
