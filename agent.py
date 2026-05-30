import os
import subprocess
import json
from openai import OpenAI

# Initialize AI client (Make sure to export OPENAI_API_KEY before running)
#client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")    

)
def run_coral_query(sql_query):
    """Executes a SQL query via the local Coral CLI and returns the JSON output"""
    try:
        result = subprocess.run(
            ["coral", "sql", sql_query, "--format", "json"],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Coral Query Failed: {e}")
        return None

def interpret_incident(service_name):
    print(f"[*] Investigating active incident in {service_name}...")
    
    # 1. Gather the unified cross-source context via Coral
    query = f"""
      SELECT l.timestamp, l.message, g.commit_id, g.author, g.message as commit_msg
      FROM opensearch.logs l
      JOIN git_history.deployments g ON g.repo = '{service_name}'
      WHERE l.level = 'ERROR' AND l.timestamp >= g.committed_at
      ORDER BY l.timestamp DESC LIMIT 1;
    """
    
    data_context = run_coral_query(query)
    if not data_context:
        print("[-] No diagnostic correlation data returned from Coral.")
        return

    print("[+] Diagnostic data gathered from OpenSearch & Git History via Coral.")

    # 2. Feed the correlated dataset to the AI interpreter
    prompt = f"""
    You are an expert Principal Site Reliability Engineer. An incident has occurred in the service: {service_name}.
    Here is the unified data retrieved via Coral cross-source SQL queries (combining cluster logs and deployment metadata):
    
    {json.dumps(data_context, indent=2)}
    
    Analyze the log message against the deployment history timeline. Provide a structured response with:
    1. ROOT CAUSE ANALYSIS: What happened, why it happened, and how the recent commit relates to the log.
    2. SUSPECT COMMIT: Identify the exact commit ID and author responsible.
    3. REMEDIATION ACTION: The exact terminal command or action to resolve the issue right now (e.g., specific rollback commands or config patches).
    """

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[{"role": "user", "content": prompt}]
    )
    
    print("\n==============================================")
    print("         AI SRE REMEDIATION REPORT            ")
    print("==============================================\n")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    interpret_incident("payment-service")
