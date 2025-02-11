# Check for virtual environment and activate it correctly
if (Test-Path ".venv") {
    .\.venv\Scripts\Activate.ps1
    python xc_cup_ranker.py $args
    deactivate
    exit 0
}

# Check if Conda is installed and the environment exists
if (Get-Command conda -ErrorAction SilentlyContinue) {
    if (conda env list | Select-String "xc-cup-env") {
        conda run -n xc-cup-env python xc_cup_ranker.py $args
        exit 0
    }
}

# Fallback if no virtual environment is found
python xc_cup_ranker.py $args

