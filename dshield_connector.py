# File: dshield_connector.py
#
# Copyright (c) 2017-2021 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
""" Code that implements calls made to the dshield web API"""

import ipaddress

# Phantom imports
import phantom.app as phantom
import requests
import simplejson as json
from bs4 import UnicodeDammit
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

# THIS Connector imports
from dshield_consts import *


class CertlyConnector(BaseConnector):
    # actions supported by this script
    ACTION_ID_LOOKUP_IP = "lookup_ip"

    def _make_rest_call(self, endpoint, action_result):
        """ Function that makes the REST call to the device, generic function that can be called from various action handlers"""

        resp_json = None

        # Make the call
        try:
            r = requests.get(DSHIELD_LOOKUP_URL + endpoint + '?json')
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, DSHIELD_ERR_SERVER_CONNECTION, e), resp_json

        action_result.add_debug_data({'r_text': r.text if r else 'r is None'})

        try:
            resp_json = r.json()
        except Exception as e:
            # r.text is guaranteed to be NON None, it will be empty, but not None
            msg_string = r.text.replace('{', '').replace('}', '')
            return action_result.set_status(phantom.APP_ERROR, msg_string, e), resp_json

        # Check if there are any errors
        errors = resp_json.get('errors')

        if errors:
            details = json.dumps(resp_json).replace('{', '').replace('}', '')

            return (action_result.set_status(phantom.APP_ERROR,
                                             DSHIELD_ERR_FROM_SERVER.format(status=r.status_code, detail=details)),
                    resp_json)

        # Handle/process any errors that we get back from the device
        if r.status_code == 200:
            # Success
            return phantom.APP_SUCCESS, resp_json

        # Failure
        action_result.add_data(resp_json)

        details = json.dumps(resp_json).replace('{', '').replace('}', '')

        return (action_result.set_status(phantom.APP_ERROR,
                                         DSHIELD_ERR_FROM_SERVER.format(status=r.status_code, detail=details)),
                resp_json)

    def _is_ip(self, input_ip_address):
        """ Function that checks given address and return True if address is valid IPv4 or IPV6 address.
        :param input_ip_address: IP address
        :return: status (success/failure)
        """
        ip_address_input = input_ip_address
        try:
            ipaddress.ip_address(UnicodeDammit(ip_address_input).unicode_markup)
        except:
            return False
        return True

    def _test_connectivity(self, param):
        """ Function that handles the test connectivity action, it is much simpler than other action handlers."""

        config = self.get_config()

        ip = config.get(DSHIELD_JSON_IP, DSHIELD_TC_IP)

        if not ip:
            self.save_progress("Please specify an IP to lookup")
            return self.set_status(phantom.APP_ERROR)

        if not self._is_ip(ip):
            self.save_progress("Please specify a valid IP to lookup")
            return self.set_status(phantom.APP_ERROR)

        # Progress
        self.save_progress(DSHIELD_USING_BASE_URL.format(DSHIELD_LOOKUP_URL))

        # Action result to represent the call
        action_result = ActionResult()

        # Progress message, since it is test connectivity, it pays to be verbose
        self.save_progress("Looking up the IP to check connectivity")

        # Make the rest endpoint call
        ret_val, response = self._make_rest_call('/ip/{0}'.format(ip), action_result)

        # Process errors
        if phantom.is_fail(ret_val):
            # Dump error messages in the log
            self.debug_print(action_result.get_message())

            # Set the status of the complete connector result
            self.set_status(phantom.APP_ERROR, action_result.get_message())

            # Append the message to display
            self.append_to_message(DSHIELD_ERR_CONNECTIVITY_TEST)

            # return error
            return phantom.APP_ERROR

        # Set the status of the connector result
        return self.set_status_save_progress(phantom.APP_SUCCESS, DSHIELD_SUCC_CONNECTIVITY_TEST)

    def _handle_lookup_ip(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        # Progress
        self.save_progress(DSHIELD_USING_BASE_URL.format(DSHIELD_LOOKUP_URL))

        # Make the rest call
        ret_val, response = self._make_rest_call('/ip/{0}'.format(param[DSHIELD_JSON_IP]), action_result)

        # Process/parse the errors encountered while making the REST call.
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        try:
            data = response['ip']
        except:
            return action_result.set_status(phantom.APP_ERROR, "Response not in the expected format")

        # set the data
        action_result.add_data(data)
        action_result.update_summary(
            {'attacks': data.get('attacks'),
             'count': data.get('count'),
             'maxdate': data.get('maxdate'),
             'mindate': data.get('mindate')})

        # set the status
        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        """Function that handles all the actions"""

        # Get the action that we are supposed to carry out, set it in the connection result object
        action = self.get_action_identifier()

        # Intialize it to success
        ret_val = phantom.APP_SUCCESS

        # Bunch if if..elif to process actions
        if action == self.ACTION_ID_LOOKUP_IP:
            ret_val = self._handle_lookup_ip(param)
        elif action == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY:
            ret_val = self._test_connectivity(param)

        return ret_val


if __name__ == '__main__':
    """ Code that is executed when run in standalone debug mode
    for .e.g:
        """

    # Imports
    import sys

    import pudb

    # Breakpoint at runtime
    pudb.set_trace()

    # The first param is the input json file
    with open(sys.argv[1]) as f:
        # Load the input json file
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=' ' * 4))

        # Create the connector class object
        connector = CertlyConnector()

        # Se the member vars
        connector.print_progress_message = True

        # Call BaseConnector::_handle_action(...) to kickoff action handling.
        ret_val = connector._handle_action(json.dumps(in_json), None)

        # Dump the return value
        print(ret_val)

    exit(0)
