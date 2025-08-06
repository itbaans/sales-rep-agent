import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the Streamlit application"""
    
    # Ensure we're in the correct directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if required directories exist
    required_dirs = ['ui', 'ui/components', 'ui/utils', 'data']
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Check if required files exist
    required_files = [
        'data/leads.json',
        'data/long_term_memory.json'
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"Warning: {file_path} not found. Creating empty file...")
            if file_path.endswith('.json'):
                Path(file_path).write_text('{}')
    
    # Set environment variables if needed
    if not os.getenv('GOOGLE_API_KEY'):
        print("Warning: GOOGLE_API_KEY not set. Please set it in your .env file.")
    
    # Run Streamlit
    try:
        print("Starting Streamlit application...")
        print("Access the app at: http://localhost:8501")
        subprocess.run([
            sys.executable, 
            "-m", "streamlit", "run", 
            "streamlit_app.py",
            "--server.port=8501",
            "--server.address=localhost"
        ])
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error running Streamlit: {e}")

if __name__ == "__main__":
    main()