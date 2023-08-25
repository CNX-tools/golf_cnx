# Activate the virtual environment
$venvPath = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
}

# Run the Python script
Start-Process powershell -ArgumentList "-NoExit -Command ""python -m RealTimeCrawler""" -WindowStyle Normal

# Set the window title
$Host.UI.RawUI.WindowTitle = "RealTimeCrawler - Golf TeeTime"
