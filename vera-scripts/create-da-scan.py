#!/usr/bin/env python3
import os
import json  
import sys
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py.dynamic import Analyses, Scans, ScanCapacitySummary, ScanOccurrences, ScannerVariables, DynUtils, Occurrences

#name of Dynamic Analysis will be the same as the name of the Github repository:
analysis_name = "Project: " + os.environ.get("JOB_NAME") + " - Workflow Number: " + os.environ.get("JOB_ID")
dynamic_target = os.getenv("Dynamic_Target")
login_user = os.getenv("Dynamic_User")
login_pass = os.getenv("Dynamic_Pass")
owner_name = os.getenv("Dynamic_Owner")
owner_email = os.getenv("Dynamic_Email")

def main():

    #Payload for creating and scheduling new DA job

    url = DynUtils().setup_url(dynamic_target,'DIRECTORY_AND_SUBDIRECTORY',False)

    allowed_hosts = [url]

    auth = DynUtils().setup_auth('AUTO',login_user,login_pass)

    auth_config = DynUtils().setup_auth_config(auth)

    crawl_config = DynUtils().setup_crawl_configuration([],False)

    scan_setting = DynUtils().setup_scan_setting(blocklist_configs=[],custom_hosts=[],user_agent=None)

    scan_config_request = DynUtils().setup_scan_config_request(url, allowed_hosts,auth_config, crawl_config, scan_setting)

    #scan_contact_info = DynUtils().setup_scan_contact_info('andrzej@example.com','Alan Smithee','800-555-1212')

    scan = DynUtils().setup_scan(scan_config_request)

    start_scan = DynUtils().start_scan(12, "HOUR")

    print("TargetURL Scan Settings: ")
    print(scan)

    #Send configuration to Veracode and initiate Scan

    analysis = Analyses().create(analysis_name,scans=[scan],owner=owner_name,email=owner_email, start_scan=start_scan)

    print("Analysis Settings: ")
    print(analysis)


if __name__ == "__main__":
    main()
