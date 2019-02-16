import re
import sys
import xml.etree.ElementTree as ET

import requests

try:
    api_key = sys.argv[1]
    domain_name = sys.argv[2]
except:
    print("Invalid arguments. Usage: export-bind.py ZONOMI-API-KEY domain.name")
    exit(13)

# noinspection PyUnboundLocalVariable
f = open(domain_name + ".zone.txt", "w")
r = requests.get("https://zonomi.com/app/dns/dyndns.jsp?action=QUERY&name=**.%s&api_key=%s" % (domain_name, api_key))

root = ET.fromstring(r.content)
actions = root.find("actions")
action = actions.find("action")


def isIpAddress(target):
    if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', target):
        return True
    else:
        return False


def get_content_fqn(target):
    if isIpAddress(target):
        return target
    else:
        return target + "."


for record in action.iter("record"):
    source_name = record.attrib.get("name")
    type = record.attrib.get("type")
    source_content = record.attrib.get("content")

    if source_name == domain_name:
        name = "        "
    elif "." + domain_name in source_name:
        name = source_name.replace("." + domain_name, "")
    else:
        name = source_name + "."

    if type == "NS" or type == "SOA": continue

    if type == "CNAME":
        content = get_content_fqn(source_content)
    elif type == "MX":
        content = "%s\t%s" % (record.attrib.get("prio"), get_content_fqn(source_content))
    elif type == "TXT":
        content = "\"%s\"" % source_content
    else:
        content = get_content_fqn(source_content)

    f.write(
        "%s\t%s\t%s\t%s\t%s\n" % (
            name,
            record.attrib.get("ttl").replace(" seconds", ""),
            "IN",
            type,
            content
        )
    )
    print("Exporting record: %s " % record.attrib)
