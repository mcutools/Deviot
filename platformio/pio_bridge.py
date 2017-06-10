#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

from .run_command import run_command
from ..libraries import paths
from ..libraries.file import File
from ..libraries.tools import get_setting
from .project_recognition import ProjectRecognition

class PioBridge(ProjectRecognition):
    def __init__(self):
        super(PioBridge, self).__init__()

    def save_boards_list(self):
        """PlatformIO Board List
        
        Gets the list of all boards availables in platformIO and
        stores it in a json file
        """
        cmd = ['boards', '--json-output']
        boards = run_command(cmd, set_return=True)

        board_file_path = paths.getBoardsFileDataPath()
        File(board_file_path).write(boards)

    def get_boards_list(self):
        """Board List
        
        Get the json file with the list of boards and return it.
        The location of the json file is defined in paths.py in the
        function getBoardsFileDataPath
        
        Returns:
            json -- list of boards
        """
        board_file_path = paths.getBoardsFileDataPath()

        file = File(board_file_path)
        boards_list = file.read_json(boards)

        return boards_list

    def remove_ini_environment(self, board_id):
        """Remove Environment
        
        Removes the environments from the platformio.ini file.
        It happens each time a environment/board is removed selecting it
        from the list of boards (Select Board). The behavior of this
        option is; if the board isn't in the configs, it will be added
        if not, removed.
        
        Arguments:
            board_id {[type]} -- [description]
        """
        if(self.is_initialized):

            key = 'env:' + board_id
            pio_file = self.get_config(full=True)

            if(key in pio_file):
                pio_file.pop(key, None)

            self.save_config(pio_file, full=True)

    def get_config(self, key=None, default=None, full=False):
        """Gets platformio.ini Configs
        
        Gets the platformio.ini file of the project loaded in the
        current view and return the value of the key requested.
        You can use the full parameter to retrieve the full file
        
        Keyword Arguments:
            key {str} -- key of the option (default: {None})
            default {str} -- default value if the key value
                             is not found (default: {None})
            full {bool} -- to return the full file (default: {False})
        
        Returns:
            str -- found or default value
        """
        from ..libraries.configobj.configobj import ConfigObj

        file_config = self.get_ini_path()
        config = ConfigObj(file_config)

        if(full):
            return config

        if(key in config):
            return config[key]
        return default


    def save_config(self, key=None, value=None, full=False):
        """Save in platformio.ini
        
        Stores the key and value in platfirmio.ini file, this
        file is the one asociated with current open sketch
        
        Keyword Arguments:
            key {str} -- key of the option/config (default: {None})
            value {str} -- value of the option/config (default: {None})
            full {bool} -- when is true write key in the file (default: {False})
        
        Returns:
            bool -- True if the file was write, False if not
        """
        from ..libraries.configobj.configobj import ConfigObj

        file_config = self.get_ini_path()
        config = ConfigObj(file_config)

        if(full):
            key.write()
            return True

        config[key] = value
        
        config.write()
        return True

