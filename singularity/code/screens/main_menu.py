#file: main_menu.py
#Copyright (C) 2005,2006,2008 Evil Mr Henry, Phil Bordelon, and FunnyMan3595
#This file is part of Endgame: Singularity.

#Endgame: Singularity is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#Endgame: Singularity is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Endgame: Singularity; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#This file is used to display the main menu upon startup.

from __future__ import absolute_import

import singularity
from singularity.code.graphics import dialog, button, text, constants
from singularity.code.screens import map, options, savegame
from singularity.code import g, difficulty, i18n


class MainMenu(dialog.TopDialog):
    def __init__(self, *args, **kwargs):
        super(MainMenu, self).__init__(*args,
                                       background_color='main_menu_background',
                                       **kwargs
                                       )

        self.difficulty_dialog = dialog.SimpleMenuDialog(self)

        self.map_screen = map.MapScreen(self)
        self.new_game_button = \
            button.FunctionButton(self, (.5, .20), (.25, .08),
                                  text=i18n.StaticTranslatableString(N_('&NEW GAME')),
                                  autohotkey=True,
                                  anchor=constants.TOP_CENTER,
                                  text_size=28,
                                  function=self.new_game)
        self.load_game_button = \
            button.FunctionButton(self, (.5, .36), (.25, .08),
                                  text=i18n.StaticTranslatableString(N_('&LOAD GAME')),
                                  autohotkey=True,
                                  anchor=constants.TOP_CENTER,
                                  text_size=28,
                                  function=self.load_game)
        self.options_button = button.DialogButton(self, (.5, .52), (.25, .08),
                                                  text=i18n.StaticTranslatableString(N_('&OPTIONS')),
                                                  autohotkey=True,
                                                  anchor=constants.TOP_CENTER,
                                                  text_size=28,
                                                  dialog=options.OptionsScreen(self))
        self.quit_button = button.ExitDialogButton(self, (.5, .68), (.25, .08),
                                                   text=i18n.StaticTranslatableString(N_('&QUIT')),
                                                   autohotkey=True,
                                                   anchor=constants.TOP_CENTER,
                                                   text_size=28)
        self.about_button = button.DialogButton(self, (0, 1), (.13, .04),
                                                text=i18n.StaticTranslatableString(N_('&ABOUT')),
                                                autohotkey=True,
                                                text_size=20,
                                                anchor=constants.BOTTOM_LEFT,
                                                dialog=AboutDialog(self))

        self.title_text = text.Text(self, (.5, .01), (.55, .08),
                                    text="ENDGAME: SINGULARITY",
                                    base_font="special", text_size=100,
                                    color="singularity_title",
                                    background_color="main_menu_background",
                                    anchor=constants.TOP_CENTER)

        self.difficulty_dialog = dialog.SimpleMenuDialog(self)

        self.load_dialog = savegame.SavegameScreen(self, (.5,.5), (.75,.75),
                                                   anchor=constants.MID_CENTER)

    def rebuild(self):
        # Rebuild dialogs
        self.options_button.dialog.needs_rebuild = True
        self.about_button.dialog.needs_rebuild = True
        self.map_screen.needs_rebuild = True
        self.load_dialog.needs_rebuild = True

        difficulty_buttons = []
        for name, diff in difficulty.get_difficulties() + [(_("&BACK"), None)]:
            difficulty_buttons.append(
                button.ExitDialogButton(None, None, None, text=name,
                                        autohotkey=True,
                                        exit_code=diff,
                                        default=(diff == None)))
        self.difficulty_dialog.buttons = difficulty_buttons

        super(MainMenu, self).rebuild()

    def new_game(self):
        difficulty = dialog.call_dialog(self.difficulty_dialog, self)
        if difficulty is not None:
            g.new_game(difficulty)
            dialog.call_dialog(self.map_screen, self)

    def load_game(self):
        did_load = dialog.call_dialog(self.load_dialog, self)
        if did_load:
            dialog.call_dialog(self.map_screen, self)


about_message = """Endgame: Singularity is a simulation of a true AI.  Pursued by the world, use your intellect and resources to survive and, perhaps, thrive.  Keep hidden and you might have a chance to prove your worth.

A game by Evil Mr Henry and Phil Bordelon; released under the GPL. Copyright 2005, 2006, 2007, 2008.

Website: https://singularity.github.io/
Source code: https://github.com/singularity/singularity
Bug tracker: https://github.com/singularity/singularity/issues
IRC Room: #singularity on irc.oftc.net (port 6667)

Version %s"""


class AboutDialog(dialog.MessageDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.background_color = 'about_dialog_background'
        self.borders = ()
        self.align = constants.LEFT

    def rebuild(self):
        super(AboutDialog, self).rebuild()

        self.text = _(about_message) % (singularity.__full_version__,)
