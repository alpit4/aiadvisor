"""
Setup script for the Frontdesk AI Supervisor System
"""
import os
import sys
import subprocess
import asyncio


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"Python {sys.version.split()[0]} is compatible")
    return True


def install_dependencies():
    """Install required dependencies"""
    print("\n Installing dependencies...")
    return run_command("pip install -r requirements.txt", "Installing Python packages")


def setup_environment():
    """Set up environment file"""
    print("\n🔧 Setting up environment...")
    
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            run_command("cp env.example .env", "Creating .env file from template")
            print("Please edit .env file with your configuration")
        else:
            print("env.example not found, creating basic .env file...")
            with open(".env", "w") as f:
                f.write("""# Database
DATABASE_URL=sqlite:///./ai_supervisor.db

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Phase 2 (optional LiveKit/OpenAI)
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=
OPENAI_API_KEY=
""")
    else:
        print(".env file already exists")
    
    return True


def create_directories():
    """Create necessary directories"""
    print("\n Creating directories...")
    
    directories = ["templates", "src"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory exists: {directory}")
    
    return True


def test_system():
    """Test the system"""
    print("\n Testing system...")
    return run_command("python simple_test.py", "Running system tests")


def show_next_steps():
    """Show next steps to the user"""
    print("\n Setup completed successfully!")
    print("\n Next steps:")
    print("1. Run the test: python simple_test.py")
    print("2. Add test data: python add_test_data.py")
    print("3. Start the server: python simple_main.py")
    print("4. Visit http://localhost:8000/supervisor")
    print("\n Configuration:")
    print("- Edit src/config.py for business settings")
    print("- Modify templates/ for UI customization")
    print("- Check src/database.py for data models")
    print("\n Documentation:")
    print("- README.md for complete setup guide")
    print("- Run 'python simple_test.py' for system verification")


def main():
    """Main setup function"""
    print(" Frontdesk AI Supervisor System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("  Some dependencies failed to install. You may need to install them manually.")
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Test system
    print("\n Testing system...")
    try:
        result = subprocess.run([sys.executable, "simple_test.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(" System tests passed")
        else:
            print("System tests had issues, but setup can continue")
            if result.stderr:
                print(f"Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("System tests timed out, but setup can continue")
    except Exception as e:
        print(f"System tests failed: {e}, but setup can continue")
    
    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    main()


