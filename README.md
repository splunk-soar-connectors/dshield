[comment]: # "Auto-generated SOAR connector documentation"
# DShield

Publisher: Splunk  
Connector Version: 2\.0\.6  
Product Vendor: DShield  
Product Name: DShield  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.1\.0  

This app implements investigative action that queries the DShield web API

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a DShield asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**ip** |  optional  | string | IP to Lookup for Test Connectivity

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity  
[lookup ip](#action-lookup-ip) - Get IP info from DShield  

## action: 'test connectivity'
Validate the asset configuration for connectivity

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'lookup ip'
Get IP info from DShield

Type: **investigate**  
Read only: **True**

The <a href="https\://isc\.sans\.edu/api/\#ip">DShield API documentation page</a> explains the <i>count</i> and <i>attacks</i> values \(found in the result\) as\:<ul><li><b>Count\:</b> \(also reports or records\) total number of packets blocked from this IP</li><li><b>Attacks\:</b> \(also targets\) number of unique destination IP addresses for these packets</li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** |  required  | IP to Lookup | string |  `ip`  `ipv6` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.ip | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.alexa\.domains | numeric |  `domain` 
action\_result\.data\.\*\.alexa\.firstseen | string | 
action\_result\.data\.\*\.alexa\.hostname | string |  `host name` 
action\_result\.data\.\*\.alexa\.lastrank | numeric | 
action\_result\.data\.\*\.alexa\.lastseen | string | 
action\_result\.data\.\*\.as | numeric | 
action\_result\.data\.\*\.asabusecontact | string |  `email` 
action\_result\.data\.\*\.ascountry | string | 
action\_result\.data\.\*\.asname | string | 
action\_result\.data\.\*\.assize | numeric | 
action\_result\.data\.\*\.attacks | numeric | 
action\_result\.data\.\*\.cloud | string | 
action\_result\.data\.\*\.comment | string | 
action\_result\.data\.\*\.count | numeric | 
action\_result\.data\.\*\.maxdate | string | 
action\_result\.data\.\*\.maxrisk | string | 
action\_result\.data\.\*\.mindate | string | 
action\_result\.data\.\*\.network | string | 
action\_result\.data\.\*\.number | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.threatfeeds\.\*\.firstseen | string | 
action\_result\.data\.\*\.threatfeeds\.\*\.lastseen | string | 
action\_result\.data\.\*\.threatfeeds\.forumspam\.firstseen | string | 
action\_result\.data\.\*\.threatfeeds\.forumspam\.lastseen | string | 
action\_result\.data\.\*\.threatfeeds\.matsnu\.firstseen | string | 
action\_result\.data\.\*\.threatfeeds\.matsnu\.lastseen | string | 
action\_result\.data\.\*\.threatfeeds\.miner\.firstseen | string | 
action\_result\.data\.\*\.threatfeeds\.miner\.lastseen | string | 
action\_result\.data\.\*\.updated | string | 
action\_result\.summary\.attacks | numeric | 
action\_result\.summary\.count | numeric | 
action\_result\.summary\.maxdate | string | 
action\_result\.summary\.mindate | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 