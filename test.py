import subprocess

# Run the modified PowerShell script using subprocess
subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "RealTimeCrawler.ps1"], shell=True)
