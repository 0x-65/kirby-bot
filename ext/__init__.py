from pkgutil import iter_modules

#iterates through the current directory's files
EXTENSIONS: list = [
    module.name for module in iter_modules(__path__, f'{__package__}.')
    ]
