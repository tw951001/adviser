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

from tools.regextemplates.rules.data.commands.command import Command
from tools.regextemplates.rules.data.memory import Memory


class Probability(Command):
    def __init__(self, arguments: str):
        Command.__init__(self, arguments)
        self.value = float(arguments)

    def are_arguments_valid(self) -> bool:
        return self.value >= 0

    def add_inner_command(self, command):
        raise BaseException('Probability does not take any inner commands')

    def are_inner_commands_valid(self) -> bool:
        return not self.inner_commands
