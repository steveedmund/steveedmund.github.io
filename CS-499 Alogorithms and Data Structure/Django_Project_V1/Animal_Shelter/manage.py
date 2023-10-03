#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""



# Importing necessary modules
import os  # Module for operating system functionality
import sys  # Module for system-specific parameters and functions

def main():
    """Run administrative tasks."""
    # Set the DJANGO_SETTINGS_MODULE environment variable to 'Animal_Shelter.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Animal_Shelter.settings')

    try:
        # Import the execute_from_command_line function from django.core.management
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Handle the case where Django is not installed or not available
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Execute the command-line utility with the command-line arguments passed to the script
    execute_from_command_line(sys.argv)

# Check if this script is the main entry point
if __name__ == '__main__':
    main()  # Run the main function if this script is executed directly
