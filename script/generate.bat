@echo off
setlocal enabledelayedexpansion

cd ..
set "protoDir=.\proto\api"

for /r "%protoDir%" %%f in (*.proto) do (
    set "filePath=%%f"
    set "fileDir=%%~dpf"
    set "relativePath=!fileDir:%CD%\proto%=!"


    echo Command: protoc --proto_path=. --proto_path=%CD%\proto --proto_path=%CD%\proto\third_party --pyi_out=%CD% --http_python_out=%CD%\ !filePath!
    protoc --proto_path=. --proto_path=%CD%\proto --proto_path=%CD%\proto\third_party --python_out=. --http_python_out=. !filePath!
    python -m grpc.tools.protoc --proto_path=%CD%\proto --proto_path=%CD%\proto\third_party --pyi_out=. !filePath!
    echo.
)
