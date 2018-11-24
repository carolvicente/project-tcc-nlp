# import pkgutil
# import sys
# import os

# __all__ = [x[1] for x in pkgutil.iter_modules(path='.')]

# # Module directory
# _MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
# _PROJECT_DIR_ROOT = _MODULE_DIR.split('src')[0]

# print(_PROJECT_DIR_ROOT)


# # Add CEDP root dir
# if _PROJECT_DIR_ROOT not in sys.path:
#     sys.path.insert(0, _PROJECT_DIR_ROOT)

# # Get Python code path
# _PYTHONCODE_PATH = '{}source'.format(_MODULE_DIR.split('source')[0])

# if _PYTHONCODE_PATH not in sys.path:
#     sys.path.append(_PYTHONCODE_PATH)

# # Add all modules paths
# for module in __all__:
#     if module != 'source':
#         module_path = '{}/{}'.format(_MODULE_DIR, module)
#         if module_path not in sys.path and os.path.isdir(module_path):
#             sys.path.append(module_path)

# # Debug
# if __name__ == '__main__':
#     print('{}:\n{}'.format(__name__, sys.path))
