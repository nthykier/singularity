#file: code/py3compat.py
#Copyright (C) 2005 Evil Mr Henry, Phil Bordelon, Brian Reid, MestreLion
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
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#A full copy of this license is provided in GPL.txt

# Minimal python3 compatibility layer

try:
    unicode_ = unicode
except NameError:
    def unicode_(x, *args, **kwargs):
        return x

try:
    long_ = long
except NameError:
    long_ = int

try:
    from configparser import RawConfigParser, SafeConfigParser
except ImportError:
    from ConfigParser import RawConfigParser, SafeConfigParser

