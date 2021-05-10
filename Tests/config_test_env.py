"""Configure testing environment

FA has a complex folder structure from where modules are loaded. Moreover, no
concept of Python package is implemented. This means that in order to import
a particular module, we need to add it directly to the sys.path.

To add more complexity, FA also has a dynamic loading of modules by context.
For example, the `sys.path` for a module running in `Standard` context can be
different from the `sys.path` when running in `FX` context. There are several
context available under `Extension contexts`, and we should be able to specify
the target context of our tests.

Given the dynamic nature of the `sys.path` configuration, we opt for copying
the relevant files for a particular context into a temporal directory that will
be loaded to `sys.path`. The reason to do that is to avoid replacing the call
to `tox` and `pytest` commands by custom implementations. This way we'll keep
the automation mechanism in its original version, ready to be upgraded with
each new released version of `pytest` and `tox`, without any extra effort.
"""

import argparse
import os
import shutil


class Configuration(object):
    def __init__(self, working_directory, target_directory, context):
        self.working_directory = working_directory
        self.target_directory = target_directory
        self.context = context
        if not os.path.exists(self.target_directory):
            os.makedirs(self.target_directory)

    def copy_python_sources(self):
        modules = self._get_modules_to_load()
        for m in modules:
            shutil.copy(m, self.target_directory)

    def _get_modules_to_load(self):
        context_stack = self._get_context_stack()
        module_relative_paths = []
        for i in context_stack:
            extension_modules = self._load_extension_module(i)
            module_relative_paths.extend(extension_modules)
        return module_relative_paths

    def _get_context_stack(self):
        context_full_path = os.path.join(self.working_directory, 'Extension contexts', self.context + '.ectx')
        context_stack = []
        with open(context_full_path) as f:
            for line in f:
                stack_element = line.strip()
                if not stack_element.startswith('%'):
                    context_stack.append(stack_element)
        return context_stack

    def _load_extension_module(self, module):
        extension_module_path = os.path.join(self.working_directory, 'Extensions', module, 'FPythonCode')
        all_python_modules = []
        if os.path.exists(extension_module_path):
            for f in os.listdir(extension_module_path):
                full_path_to_python_module = os.path.join(extension_module_path, f)
                if os.path.isfile(full_path_to_python_module):
                    all_python_modules.append(full_path_to_python_module)
        return all_python_modules


if __name__ == '__main__':
    print('Configuring testing environment')

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--working_directory', help='tox working directory')
    parser.add_argument('-t', '--target_directory', help='target directory to copy source files')
    parser.add_argument('-c', '--context', help='FA context')

    arguments = parser.parse_args()

    configuration = Configuration(
        working_directory=arguments.working_directory,
        target_directory=arguments.target_directory,
        context=arguments.context
    )
    configuration.copy_python_sources()
