@echo off
setlocal enabledelayedexpansion

cd ..
set "protoDir=.\proto\thgamejam"

for /r "%protoDir%" %%f in (*.proto) do (
    set "filePath=%%f"
    set "fileDir=%%~dpf"
    set "relativePath=!fileDir:%CD%\proto%=!"
    set "apiPath=%CD%\api!relativePath!"
    set "apiPath=!apiPath:~0,-1!"
    echo proto path: !filePath!
    echo api path: !apiPath!

    if not exist "!apiPath!" (
        echo Creating directory: !apiPath!
        mkdir "!apiPath!"
    )

    echo Command: protoc --proto_path=. --proto_path=%CD%\proto --proto_path=%CD%\proto\third_party --python_out=%CD%\api --http_python_out=%CD%\api !filePath!
    protoc --proto_path=. --proto_path=%CD%\proto --proto_path=%CD%\proto\third_party --python_out=%CD%\api --http_python_out=%CD%\api !filePath!
    echo.
)
