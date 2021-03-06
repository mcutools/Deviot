#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os

from ..api import deviot
from .file import File
from ..platformio.pio_bridge import PioBridge
from .I18n import I18n


class MenuFiles(PioBridge):
    def __init__(self):
        super(MenuFiles, self).__init__()
        self.translate = I18n().translate

    def get_template_menu(self, file_name):
        """Template Menu

        Get a JSON template file and return it.
        To this option works, the file must be located
        in the Deviot/presets folder

        Arguments:
            file_name {str} -- name of the file

        Returns:
            json -- data of the file
        """
        file_path = deviot.preset_file(file_name)
        preset_file = File(file_path)
        preset_data = preset_file.read_json()

        return preset_data

    def create_sublime_menu(self, data, menu_name, path):
        """Sublime Menu

        Generate a .sublime-menu file who is used by sublime text
        to generate the menu in the menu bar.

        Arguments:
            data {json} -- data with the structure of the menu
            menu_name {str} -- the file will be called menu_name.sublime-menu
            path {str} -- where the menu will be located
        """
        from json import dumps

        menu_name = menu_name + '.sublime-menu'
        menu_path = os.path.join(path, menu_name)

        file = File(menu_path)
        data = dumps(data, sort_keys=True, indent=4)
        file.write(data)

    def create_quick_commands(self):
        """Quick Commands

        Makes the quick command file and translate it
        to the current language selected
        """
        quick_path = deviot.quick_path()
        plugin_path = deviot.plugin_path()
        output_path = os.path.join(plugin_path, 'Default.sublime-commands')

        quick_json = File(quick_path)
        quick_json = quick_json.read_json()

        for items in quick_json:
            items['caption'] = "Deviot: " + self.translate(items['caption'])

        quick_file = File(output_path)
        quick_file.save_json(quick_json)

    def create_context_menu(self):
        """Quick Commands

        Makes the quick command file and translate it
        to the current language selected
        """
        context_path = deviot.context_path()
        plugin_path = deviot.plugin_path()
        output_path = os.path.join(plugin_path, 'Context.sublime-menu')

        context_json = File(context_path)
        context_json = context_json.read_json()

        for items in context_json:
            items['caption'] = self.translate(items['caption'])

        context_file = File(output_path)
        context_file.save_json(context_json)
