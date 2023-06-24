#!/usr/bin/env python3

import os
import sys

from grpc_tools import protoc


def generate_proto_api(proto_path: str | list[str]):
    if isinstance(proto_path, str):
        proto_path = [proto_path]

    protoc.main(
        (
            '',
            '--proto_path=./proto',
            '--proto_path=./proto/third_party',
            '--python_out=.',
            '--pyi_out=.',
            '--pyhttp_out=.',
            *proto_path
        )
    )


def generate_proto_all_api():
    directory = f'.{os.sep}proto{os.sep}api'
    proto_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".proto"):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                proto_files.append(relative_path)

    proto_files = [f'{directory}{os.sep}{s}' for s in proto_files]
    generate_proto_api(proto_files)


def generate_proto_config():
    protoc.main(
        (
            '',
            '--proto_path=.',
            '--proto_path=./proto/third_party',
            '--python_out=.',
            '--pyi_out=.',
            './config/conf.proto'
        )
    )


def main(command: str, arguments):
    match command:
        case 'all':
            generate_proto_all_api()
            generate_proto_config()

        case 'api':
            generate_proto_all_api()

        case 'config':
            generate_proto_config()


if __name__ == '__main__':
    arguments = sys.argv[1:]
    command = "all"
    if arguments is not None and len(arguments) > 0:
        command = arguments[0]
        arguments = arguments[1:]

    sys.exit(main(command=command, arguments=arguments))
