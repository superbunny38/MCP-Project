import subprocess
import sys
import importlib

def install_and_import(package_name):
    """
    Attempts to import a package. If ImportError occurs,
    it tries to install the package using pip and then import it again.

    Args:
        package_name (str): The name of the package to import and install.

    Returns:
        module: The imported module if successful, None otherwise.
    """
    try:
        # Try to import the package
        module = importlib.import_module(package_name)
        print(f"'{package_name}' is already installed and imported.")
        return module
    except ImportError:
        print(f"'{package_name}' not found. Attempting to install it...")
        
        try:
            # Use sys.executable to ensure pip is called for the correct Python interpreter
            # This runs 'python -m pip install <package_name>'
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"'{package_name}' installed successfully using pip.")
            
            # Try to import again after installation
            module = importlib.import_module(package_name)
            print(f"'{package_name}' is now imported.")
            return module
        except subprocess.CalledProcessError as e:
            print(f"Error during 'pip install {package_name}': {e}")
            print(f"Please make sure pip is working and you have an internet connection.")
            print(f"You might need to install '{package_name}' manually: pip install {package_name}")
            return None
        except FileNotFoundError:
            # This would happen if sys.executable is somehow not found, which is unlikely
            # or if pip is not found and sys.executable -m pip isn't used.
            print("Error: Python executable or pip command not found.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during installation or import of '{package_name}': {e}")
            return None

if __name__ == "__main__":
    print("--------------------------------------------------------------------")
    print("WARNING: Installing packages directly from a Python script is")
    print("generally not recommended for production or shared projects.")
    print("It's better to manage dependencies using a requirements.txt file")
    print("and installing them via 'pip install -r requirements.txt' in the terminal.")
    print("This script is for demonstration or specific automation purposes.")
    print("--------------------------------------------------------------------\n")

    # Attempt to install and import 'requests'
    requests_module = install_and_import("requests")

    if requests_module:
        print("\nSuccessfully ensured 'requests' is available.")
        # Now you can use the requests_module (which is the imported requests library)
        try:
            print("Attempting a test GET request to httpbin.org...")
            response = requests_module.get('https://httpbin.org/get')
            response.raise_for_status() # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            print(f"Test request successful! Origin IP: {data.get('origin')}")
        except Exception as e:
            print(f"An error occurred while trying to use 'requests': {e}")
    else:
        print("\nCould not make 'requests' module available. Please install it manually.")