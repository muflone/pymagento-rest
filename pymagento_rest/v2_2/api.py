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

import json
import requests
from typing import Optional

from pymagento_rest import Filter


class Api(object):
    """
    Magento v2.2 REST API
    """
    def __init__(self,
                 endpoint: str,
                 secret: str):
        self.__endpoint = endpoint
        self.__secret = secret

    def request(self,
                method: str,
                verb: str = 'GET',
                store: str = None,
                data: dict = None) -> tuple[int, dict]:
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
        try:
            json_results = response.json()
        except json.decoder.JSONDecodeError:
            json_results = None
        return response.status_code, json_results

    def all(self,
            method: str,
            store: str = None,
            page_size: int = 0,
            current_page: int = 0) -> tuple[int, dict]:
        """
        Get all the rows from a Magento object

        :param method: method name to query
        :param store: store codename
        :return:
        """
        search_filters = ''
        # Add page size
        if page_size:
            search_filters += f'searchCriteria[pageSize]={page_size}'
        # Add current_page
        if current_page:
            if search_filters:
                search_filters += '&'
            search_filters += f'searchCriteria[currentPage]={current_page}'
        status, response = self.request(
            method=f'{method}?{search_filters}',
            verb='GET',
            store=store)
        return status, response

    def get(self,
            method: str,
            entity_id: str,
            store: str = None) -> tuple[int, dict]:
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

    def post(self,
             method: str,
             data: dict,
             store: str = None) -> tuple[int, dict]:
        """
        Post data for a Magento object

        :param method: method name to query
        :param data: JSON data to send to the request
        :param store: store codename
        :return:
        """
        status, response = self.request(
            method=f'{method}',
            verb='POST',
            store=store,
            data=data)
        return status, response

    def put(self,
            method: str,
            data: dict,
            store: str = None) -> tuple[int, dict]:
        """
        Send data via PUT for a Magento object

        :param method: method name to query
        :param data: JSON data to send to the request
        :param store: store codename
        :return:
        """
        status, response = self.request(
            method=f'{method}',
            verb='PUT',
            store=store,
            data=data)
        return status, response

    def search(self,
               method: str,
               filters: list[list[Filter]],
               page_size: int = 0,
               current_page: int = 0,
               store: str = None) -> tuple[int, dict]:
        """
        Search data from a Magento method

        :param method: method name to query
        :param filters: list of lists of filters
        :param page_size: pagination size
        :param current_page: current page number
        :param store: store codename
        :return:
        """
        def search_criteria(group_id: int,
                            filter_id: int,
                            field: str,
                            condition: str,
                            value: str) -> str:
            """
            Build a Magento search criteria for the filter and field using
            a specific field name, condition and value
            :param group: index of the group
            :param filter_id: index of the filter
            :param field: field name
            :param condition: field condition
            :param value: field value
            :return: string with the search criteria
            """

            def new_option(group_id: int,
                           filter_id: int,
                           field: str,
                           value: str) -> str:
                """
                Build a Magento search criteria for the filter and field using
                a specific field name
                :param group_id: index of the group
                :param filter_id: index of the filter
                :param field: field name
                :param value: field value
                :return: string with the search criteria
                """
                return (f'searchCriteria[filter_groups][{group_id}]'
                        f'[filters][{filter_id}][{field}]={value}')

            return ('{FIELD}&{CONDITION}&{VALUE}'.format(
                FIELD=new_option(group_id=group_id,
                                 filter_id=filter_id,
                                 field='field',
                                 value=field),
                CONDITION=new_option(group_id=group_id,
                                     filter_id=filter_id,
                                     field='condition_type',
                                     value=condition)
                if condition else '',
                VALUE=new_option(group_id=group_id,
                                 filter_id=filter_id,
                                 field='value',
                                 value=value)
            ))
        # Build search filters chain
        search_filters = ''
        for group_id, subfilters in enumerate(filters):
            for filter_id, filter in enumerate(subfilters):
                if search_filters:
                    search_filters += '&'
                search_filters += search_criteria(
                    group_id=group_id,
                    filter_id=filter_id,
                    field=filter.field,
                    condition=filter.compare_type,
                    value=filter.value)
        # Add page size
        if page_size:
            if search_filters:
                search_filters += '&'
            search_filters += f'searchCriteria[pageSize]={page_size}'
        # Add current_page
        if current_page:
            if search_filters:
                search_filters += '&'
            search_filters += f'searchCriteria[currentPage]={current_page}'
        status, response = self.request(
            method=f'{method}?{search_filters}',
            verb='GET',
            store=store)
        return status, response

    def search_simple(self,
                      method: str,
                      simple_filter: Filter,
                      page_size: int = 0,
                      current_page: int = 0,
                      store: str = None) -> tuple[int, dict]:
        """
        Search data from a Magento method using a single filter

        :param method: method name to query
        :param filter: filter for querying the data
        :param page_size: pagination size
        :param current_page: current page number
        :param store: store codename
        :return:
        """
        return self.search(method=method,
                           filters=[[simple_filter]],
                           page_size=page_size,
                           current_page=current_page,
                           store=store)

    def new_attribute(self,
                      attribute_name: str,
                      value: str):
        """
        Return a new attribute

        :param attribute_name: new attribute name
        :param value: new value for the attribute
        :return: dictionary with attribute and value
        """
        return {'attribute_code': attribute_name,
                'value': value}

    def find_custom_attribute(self,
                              data: dict[str],
                              attribute_name: str) -> Optional[dict[str]]:
        """
        Find an attribute into the custom_attributes from a Magento response

        :param data: Magento response data dictionary
        :param attribute_name: attribute name to lookup
        :return: dictionary item for found value or None
        """
        results = None
        for attribute in data['custom_attributes']:
            if attribute['attribute_code'] == attribute_name:
                results = attribute
                break
        return results

    def find_custom_attribute_value(self,
                                    data: dict[str],
                                    attribute_name: str) -> Optional[str]:
        """
        Find an attribute value into the custom_attributes from
        a Magento response

        :param data: Magento response data dictionary
        :param attribute_name: attribute name to lookup
        :return: found value or None
        """
        results = self.find_custom_attribute(data=data,
                                             attribute_name=attribute_name)
        if results:
            results = results['value']
        return results
