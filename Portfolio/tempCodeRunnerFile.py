from google.cloud import bigquery
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file(
'"C:\Users\matta\Documents\Mattan\Visual Code Studio\pdm-reporting-team-c4d3091b302d.json"')

project_id = 'pdm-reporting-team'
client = bigquery.Client(credentials= credentials,project=project_id)




query_job = client.query("""
   SELECT *
   FROM `Mattan.Shopify_Customer_Purchase_History`
   LIMIT 1000 """)

results = query_job.result() # Wait for the job to complete.