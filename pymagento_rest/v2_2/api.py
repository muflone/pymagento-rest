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

import requests


class Api(object):
    """
    Magento v2.2 REST API
    """
    def __init__(self, endpoint, secret):
        self.__endpoint = endpoint
        self.__secret = secret

    def request(self,
                method,
                verb='GET',
                store=None,
                data=None) -> tuple[int, dict]:
        """
        Send a remote request to the endpoint using the specified method
        and arguments
        """
        # Build the remote endpoint URL
        endpoint = '{ENDPOINT}{STORE}V1/{METHOD}'.format(
            ENDPOINT=self.__endpoint,
            STORE='%s/' % store if store else '',
            METHOD=method)
        # Build headers
        headers = {
            'Authorization': 'Bearer {SECRET}'.format(SECRET=self.__secret),
            'Content-Type': 'application/json'
        }
        # Send request
        response = requests.request(method=verb,
                                    url=endpoint,
                                    headers=headers,
                                    json=data)
        # Get response
        return response.status_code, response.json()

    def get(self,
            method: str,
            entity_id: str,
            store=None) -> tuple[int, dict]:
        """
        Get data from a Magento object

        :param method: method name to query
        :param entity_id: entity ID to query
        :param store: store codename
        :return:
        """
        status, response = self.request(
            method=f'{method}/{entity_id}',
            verb='GET',
            store=store)
        return status, response
