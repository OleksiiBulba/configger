#  Configger - simple configuration package
#  Copyright (C) 2020-2022  Oleksii Bulba
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  Oleksii Bulba
#  oleksii.bulba+configger@gmail.com

from abc import ABC, abstractmethod
from os import path
from pathlib import Path
from typing import Union, TypeVar


def load_dir_config(dir_path: str):
    return 'config dir: ' + str(dir_path)


def load_file_config(file_path: str):
    return 'config file: ' + str(file_path)


class JsonConfig:
    pass


SourceClass = TypeVar('SourceClass')
TargetClass = TypeVar('TargetClass')


class ConfigConverterInterface(ABC):
    @abstractmethod
    def convert(self, config: SourceClass, target_class: TargetClass) -> TargetClass:
        pass


class ConfigConverter(ConfigConverterInterface):
    def convert(self, config: SourceClass, target_class: TargetClass) -> TargetClass:
        pass


class RecursiveConfigConverter(ConfigConverterInterface):
    def convert(self, config: SourceClass, target_class: TargetClass) -> TargetClass:
        pass


def configger(config_dir_or_path: Union[str, Path], config_class: type = JsonConfig, file_filter: str = '*'):
    def config_loader(decorated):
        def inner():
            config = None
            if not path.exists(config_dir_or_path):
                raise ValueError(f'Path "${config_dir_or_path}" does not exist.')
            if path.isdir(config_dir_or_path):
                config = load_dir_config(config_dir_or_path)
            elif path.isfile(config_dir_or_path):
                config = load_file_config(config_dir_or_path)
            if config is None:
                raise ValueError(f'Cannot load config by path "${config_dir_or_path}": path is not a file nor a '
                                 f'directory.')
            config = ConfigConverter().convert(config, config_class)
            return decorated(config)
        return inner
    return config_loader
