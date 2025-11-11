#!/bin/bash

# cd into the folder which contains your sandbox dir
cd ~/src
# mirror your sandbox dir
drives mirror --live sandbox PASTE_YOUR_HYPERDRIVE_HASH_HERE --filter "/venv/**" --filter "**/__pycache/**" --filter "/.idea/**" --filter "*.pyc" --filter "*.dylib" --filter "/.mypy_cache/**" --filter ".aider*" --filter "/.aider.tags.cache.v3/cache.db" --filter "**/node_modules/**" --verbose
