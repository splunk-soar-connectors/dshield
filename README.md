# DShield

Publisher: Splunk \
Connector Version: 2.0.10 \
Product Vendor: DShield \
Product Name: DShield \
Minimum Product Version: 5.1.0

This app implements investigative action that queries the DShield web API

### Configuration variables

This table lists the configuration variables required to operate DShield. These variables are specified when configuring a DShield asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**ip** | optional | string | IP to Lookup for Test Connectivity |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity \
[lookup ip](#action-lookup-ip) - Get IP info from DShield

## action: 'test connectivity'

Validate the asset configuration for connectivity

Type: **test** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'lookup ip'

Get IP info from DShield

Type: **investigate** \
Read only: **True**

The <a href="https://isc.sans.edu/api/#ip">DShield API documentation page</a> explains the <i>count</i> and <i>attacks</i> values (found in the result) as:<ul><li><b>Count:</b> (also reports or records) total number of packets blocked from this IP</li><li><b>Attacks:</b> (also targets) number of unique destination IP addresses for these packets</li></ul>

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** | required | IP to Lookup | string | `ip` `ipv6` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.ip | string | `ip` `ipv6` | 8.8.8.8 |
action_result.data.\*.alexa.domains | numeric | `domain` | |
action_result.data.\*.alexa.firstseen | string | | |
action_result.data.\*.alexa.hostname | string | `host name` | |
action_result.data.\*.alexa.lastrank | numeric | | |
action_result.data.\*.alexa.lastseen | string | | |
action_result.data.\*.as | numeric | | |
action_result.data.\*.asabusecontact | string | `email` | |
action_result.data.\*.ascountry | string | | |
action_result.data.\*.asname | string | | |
action_result.data.\*.assize | numeric | | |
action_result.data.\*.attacks | numeric | | |
action_result.data.\*.cloud | string | | |
action_result.data.\*.comment | string | | |
action_result.data.\*.count | numeric | | |
action_result.data.\*.maxdate | string | | |
action_result.data.\*.maxrisk | string | | |
action_result.data.\*.mindate | string | | |
action_result.data.\*.network | string | | |
action_result.data.\*.number | string | `ip` `ipv6` | |
action_result.data.\*.threatfeeds.\*.firstseen | string | | |
action_result.data.\*.threatfeeds.\*.lastseen | string | | |
action_result.data.\*.threatfeeds.forumspam.firstseen | string | | |
action_result.data.\*.threatfeeds.forumspam.lastseen | string | | |
action_result.data.\*.threatfeeds.matsnu.firstseen | string | | |
action_result.data.\*.threatfeeds.matsnu.lastseen | string | | |
action_result.data.\*.threatfeeds.miner.firstseen | string | | |
action_result.data.\*.threatfeeds.miner.lastseen | string | | |
action_result.data.\*.updated | string | | |
action_result.summary.attacks | numeric | | 23 |
action_result.summary.count | numeric | | 132 |
action_result.summary.maxdate | string | | 2020-12-19 |
action_result.summary.mindate | string | | 2020-12-19 |
action_result.message | string | | Attacks: 23, Count: 132, Maxdate: 2020-12-19, Mindate: 2020-12-19 |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
