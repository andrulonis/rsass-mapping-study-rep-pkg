REM This script was generate by ChatGPT based on the everything.sh script and corrected by the authors.



set PYTHON_CMD=
if "%~1" == "--python3" (
    echo "Using Python 3"
    set PYTHON_CMD=python
) else if "%~1" == "--python" (
    echo "Using Python (assumed to be Python 3)"
    set PYTHON_CMD=python
) else (
    echo "Invalid argument. Please specify "--python3" or "--python"."
    exit /b 1
)

if "%PYTHON_CMD%" == "" (
    echo "Python is not installed or an invalid argument was provided."
    exit /b 1
)

%PYTHON_CMD% -m venv rsas_venv
call rsas_venv\Scripts\activate

%PYTHON_CMD% -m pip install -r requirements.txt

%PYTHON_CMD% src\proceedings_collection.py
%PYTHON_CMD% src\proceedings_collection.py --pilot
%PYTHON_CMD% src\pilots_and_final.py
%PYTHON_CMD% src\generate_plots.py

call deactivate
