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
status, json_data, text_data = magento.get(method='products',
                                           entity_id='41416')
print('get', status, len(text_data), json_data)
# Post a record
json_data['price'] += 100.11
status, json_data, text_data = magento.post(method='products',
                                            data={'product': json_data})
print('post', status, len(text_data), json_data)
# Filter by SKU
filters = [[Filter(field='sku',
                   compare_type=CompareType.CONTAINS,
                   value='414%')],
           [Filter(field='sku',
                   compare_type=CompareType.NOT_EQUAL,
                   value='41416')]
           ]
# Search some records
status, json_data, text_data = magento.search(method='products',
                                              filters=filters,
                                              page_size=10,
                                              current_page=1)
print('search', len(text_data), json_data)
# Search some records using simple filter
status, json_data, text_data = magento.search_simple(
    method='products',
    simple_filter=Filter(field='sku',
                         compare_type=CompareType.EQUAL,
                         value='41416'),
    page_size=10,
    current_page=1)
print('search_simple', len(text_data), json_data)
# Show all products
status, json_data, text_data = magento.all(method='products',
                                           page_size=100,
                                           current_page=1)
print('all', len(text_data), json_data)
