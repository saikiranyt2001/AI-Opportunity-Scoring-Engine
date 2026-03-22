# PowerShell script to run pytest with the correct PYTHONPATH
$env:PYTHONPATH = "$(Resolve-Path ./ai-opportunity-engine)"
& "c:/Users/saiki/OneDrive/Documents/AI Opportunity Scoring Engine/.venv/Scripts/python.exe" -m pytest ai-opportunity-engine/tests
