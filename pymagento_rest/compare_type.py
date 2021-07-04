##
#     Project: PyMagento REST
# Description: REST API for Magento
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021 Fabio Castelli
#     License: GPL-3+
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
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

class CompareType(object):
    """
    Comparison types used in Magento filters
    """
    EQUAL = 'eq'
    MORE_EQUAL = 'moreq'
    NOT_EQUAL = 'neq'
    GREATER = 'gt'
    GREATER_EQ = 'gteq'
    LOWER = 'lt'
    LOWER_EQ = 'lteq'
    IN = 'in'
    NOT_IN = 'nin'
    IN_SET = 'finset'
    NOT_IN_SET = 'nfinset'
    FROM = 'from'
    TO = 'to'
    CONTAINS = 'like'
    NULL = 'null'
    NOT_NULL = 'notnull'
