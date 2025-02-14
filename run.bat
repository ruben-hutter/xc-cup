@echo off
SETLOCAL

:: Check if virtual environment exists
IF EXIST ".venv" (
    CALL .venv\Scripts\activate.bat
    python main.py %*
    CALL .venv\Scripts\deactivate.bat
    EXIT /B
)

:: Check if Conda environment exists
where conda >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    conda env list | findstr "xc-cup-env" >nul
    IF %ERRORLEVEL% EQU 0 (
        conda run -n xc-cup-env python main.py %*
        EXIT /B
    )
)

:: Fallback if no virtual environment is found
python main.py %*

