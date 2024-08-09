@echo off
REM Defina o caminho para o Python, se não estiver no PATH do sistema
set PYTHON_PATH="C:\Users\Luiz Fernando\Desktop\day-price-tracking\.venv\Scripts\python.exe"

REM Defina o caminho para o script Python
set SCRIPT_PATH="C:\Users\Luiz Fernando\Desktop\day-price-tracking\main.py"

REM Executa o script Python
python %SCRIPT_PATH%

REM Pause para manter a janela aberta após a execução
pause
