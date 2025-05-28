#!/usr/bin/env python
import os
import sys
import subprocess

def start_server():
    """Start the WoofWorld backend server with proper environment"""
    
    backend_dir = r"C:\Project\Pemograman Web\WoofWorld\woofworld_backend"
    
    print("Starting WoofWorld Backend Server with CORS fixes...")
    print(f"Working directory: {backend_dir}")
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    try:
        # Try to activate conda environment and start server
        cmd = [
            "conda", "run", "-n", "woofworld", 
            "pserve", "development.ini", "--reload"
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        
        # Start the server
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print("Server starting... Press Ctrl+C to stop")
        
        # Print output in real-time
        for line in process.stdout:
            print(line.rstrip())
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
        process.terminate()
    except Exception as e:
        print(f"Error starting server: {e}")
        # Try alternative method
        print("Trying alternative start method...")
        try:
            cmd = ["python", "-m", "pserve", "development.ini", "--reload"]
            subprocess.run(cmd)
        except Exception as e2:
            print(f"Alternative method also failed: {e2}")

if __name__ == "__main__":
    start_server()
