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

import os

from pymagento_rest import CompareType, Filter
from pymagento_rest.v2_2 import Api


# Instance model object
magento = Api(endpoint=os.environ['MAGENTO_ENDPOINT'],
              secret=os.environ['MAGENTO_SECRET'])
# Get a record by ID
status, results = magento.get(method='products',
                              entity_id='41416')
print('get', status, results)
# Filter by SKU
filters = [[Filter(field='sku',
                   compare_type=CompareType.CONTAINS,
                   value='414%')],
           [Filter(field='sku',
                   compare_type=CompareType.NOT_EQUAL,
                   value='41416')]
           ]
# Search some records
results = magento.search(method='products',
                         filters=filters,
                         page_size=10,
                         current_page=1)
print('search', len(results), results)
# Search some records using simple filter
results = magento.search_simple(method='products',
                                simple_filter=Filter(
                                    field='sku',
                                    compare_type=CompareType.EQUAL,
                                    value='41416'),
                                page_size=10,
                                current_page=1)
print('search_simple', len(results), results)
