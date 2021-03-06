###############################################################################
#
# Copyright 2019, University of Stuttgart: Institute for Natural Language Processing (IMS)
#
# This file is part of Adviser.
# Adviser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3.
#
# Adviser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Adviser.  If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################

import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QWidget, QFileDialog

from tools.crosstickgame.editwidget import EditWidget
from tools.crosstickgame.nlumodules import NLU_MODULES


class TestCaseTask(QWidget):
    """The MinMax game task

    For the MinMax game, the user has to specify a file to save the changes to,
    a domain and an NLU module for that particular domain.
    
    Attributes:
        _callback: the method to call when something inside the form changes
        _domain {Domain}: currently selected domain (as specified in the ontology manager)
        _module {Module}: currently selected NLU module
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._ui = uic.loadUi(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), '..', 'ui', 'testcasetask.ui'), self)

        self._callback = None

        self._domain_objects = list(NLU_MODULES.keys())
        self._ui.choose_dest.clicked.connect(self._on_choose_destination)
        self._ui.domains.addItems([domain.get_domain_name() for domain in self._domain_objects])
        self._ui.domains.setCurrentIndex(-1)
        self._ui.domains.currentIndexChanged.connect(self._on_domain_changed)
        self._ui.modules.currentIndexChanged.connect(self._on_module_changed)

        self._domain = None
        self._module = None

    def _on_choose_destination(self):
        """Callback function when the user clicks the button for the destination file.

        A file dialog is opened, the files should be stored as .json files.
        """
        qfd = QFileDialog(caption='Select a JSON-file', filter='JSON-Files (*.json)')
        qfd.setDefaultSuffix('.json')
        qfd.setFilter(QDir.Files)
        qfd.setFileMode(QFileDialog.AnyFile)
        qfd.setAcceptMode(QFileDialog.AcceptSave)

        if qfd.exec_() == QFileDialog.Accepted:
            dest_file = qfd.selectedFiles()[0]
            if dest_file == '':
                return
            self._ui.dest_file.setText(dest_file)
            self._callback(self)

    def _on_domain_changed(self, domain_idx):
        """Callback function when the user selected a new domain.

        Arguments:
            domain_idx {int} -- index of the domain in the QComboBox
        """
        self._domain = self._domain_objects[domain_idx]

        # when the domain changes, also a new module must be selected!
        self._ui.modules.clear()
        self._ui.modules.addItems([key for key in NLU_MODULES[self._domain]])
        self._ui.modules.setCurrentIndex(-1)  # don't just assume a module

        self._callback(self)
    
    def _on_module_changed(self, _):
        """Callback function when the user selected a new NLU module.
        """
        self._callback(self)  # inform the task creator

    def set_callback(self, callback):
        """
        Arguments:
            callback {function} -- The function to call when something inside the form changes
        """
        self._callback = callback

    def is_valid(self):
        """Required method to specify whether the current configuration is valid.
        
        This method is called to check whether the OK button can be enabled.
        
        Returns:
            bool -- whether the current configuration is valid
        """
        if self._ui.dest_file.text() == '':
            return False
        elif self._ui.dest_file.text().strip() == '':
            return False
        elif self._ui.domains.currentIndex() < 0:
            return False
        elif self._ui.modules.currentIndex() < 0:
            return False
        else:
            return True

    def create_task(self):
        """Required method to create the task-specific widget.

        This method is only called if the current configuration is valid.
        
        For the MinMax game, a new EditWidget is created with the properties
        specified by the user.
        
        Returns:
            QWidget -- the task-specific widget
        """
        filename_write = self._ui.dest_file.text()

        return EditWidget(save_to=filename_write,
                          domain=self._domain,
                          module_name=self._ui.modules.currentText()), filename_write
