#!/usr/bin/env python

import boto3

#### ---------------- Variables ------------------
ROOT_OU_ID = "ou-y1m8-r7fcpgzz"  #update the root ou id
ORG_UNIT_LIST = [ "Prod", "Dev", "UAT" ]
TARGET_REGION = "us-east-1"
#### ------------------------------------------

def get_active_accounts_in_ou(ou_name):
    """List all the active member accounts under the given organisation unit"""
    org_client = boto3.client('organizations')
    try:
        response = org_client.list_organizational_units_for_parent(ParentId=ROOT_OU_ID)
        ou = next((ou for ou in response['OrganizationalUnits'] if ou['Name'] == ou_name), None)
        if ou:
            response = org_client.list_accounts_for_parent(ParentId=ou['Id'])
            active_accounts_in_ou = [{'id': account['Id'], 'name': account[
                'Name']} for account in response['Accounts'] if account['Status'] == 'ACTIVE']
            return active_accounts_in_ou
        else:
            print(f"Organizational unit '{ou_name}' not found.")
    except org_client.exceptions.InvalidInputException as err:
        return None, f"Invalid input: {str(err)}"
    except org_client.exceptions.ServiceException as err:
        return None, f"An error occurred: {str(err)}"

def get_all_active_accounts():
    """List all the active member accounts under the organisation"""
    try:
        org = boto3.client('organizations')
        response = org.list_accounts()
        results = response["Accounts"]
        while "NextToken" in response:
            response = org.list_accounts(NextToken=response["NextToken"])
            results.extend(response["Accounts"])
        active_accounts = [{'id': account['Id'], 'name': account[
            'Name']} for account in results if account['Status'] == 'ACTIVE']
        return active_accounts
    except org.exceptions.ServiceException as err:
        print(f"An error occurred: {str(err)}")
    except Exception as err:
        print(f"An unexpected error occurred: {str(err)}")

def generate_accounts_yml_file(accounts, file, target_region):
    """Generate custodian accounts yaml file"""
    header_yml = """
accounts:"""

    account_yml = """
- account_id: '{account_id}'
  name: {account_name}
  regions:
  - {account_region}
  role: arn:aws:iam::{account_id}:role/AWSControlTowerExecution
  vars:
    cc1: support@gmail.com
    cc2: ''"""
    with open(file, "w", encoding="utf-8") as account_yml_file:
        print(f"Generating {file} ...")
        account_yml_file.write(header_yml)
        print("Generating custodian accounts yml file")
        for account in accounts:
            print(account)
            account_yml_file.write(
                account_yml.format(
                    account_id=account['id'],
                    account_name=account['name'],
                    account_region=target_region
                )
            )

if __name__ == "__main__":
    generate_accounts_yml_file(get_all_active_accounts(), "all_accounts.yml", TARGET_REGION)
    for ou_name in ORG_UNIT_LIST:
        file_name = f"{ou_name}_ou_accounts.yml"
        generate_accounts_yml_file(
            get_active_accounts_in_ou(ou_name), file_name.lower(), TARGET_REGION)