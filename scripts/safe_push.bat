@echo off
REM Safe push script that prevents conflicts
echo Checking for remote changes...
git fetch origin

echo Pulling latest changes with rebase...
git pull --rebase origin master

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to rebase. Please resolve conflicts manually.
    exit /b 1
)

echo Pushing changes...
git push origin master

if %ERRORLEVEL% EQU 0 (
    echo Push successful!
) else (
    echo Push failed!
    exit /b 1
)