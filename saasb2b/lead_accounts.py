import random
from saasb2b.utils import environment_utils, snowflake_utils, general_utils
from pathlib import Path

ENV = environment_utils.get_environment_settings(Path.cwd().as_posix())

DB = ENV["DB"]
PATH = ENV["PATH"]

"""
    People table – for leads and contacts
    Accounts table – for account
    1)	Create accounts-leads connection:
        a.	For each lead – randomly select an account
        b.	Join the attributes of the lead and the account (CREATE SF_LEADS)
    2)	Over the list of leads-in-accounts, randomly select x% of them to also become contacts.
    3)	For each lead-in-account that is also a contact, populate attributes for contacts (CREATE SF_CONTACT)
    4)	Randomly generate
        """

with snowflake_utils.get_snowflake_cursor(DB) as sf_cursor:

    sql_script_accounts = "select id from account"
    res_accounts = sf_cursor.execute(command=sql_script_accounts).fetchall()

    accounts_list = [account[0] for account in res_accounts]

    sql_script_leads = "select people_id from people"
    res_leads = sf_cursor.execute(command=sql_script_leads).fetchall()

    leads_accounts_list = []
    for lead in res_leads:
        lead_id = lead[0]
        account_id = accounts_list[random.randint(0, len(accounts_list))]
        leads_accounts_list.append((lead_id, account_id))

    print(leads_accounts_list)






