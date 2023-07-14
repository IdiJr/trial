#!/usr/bin/python3
""" Import modules and packages for storage """
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
