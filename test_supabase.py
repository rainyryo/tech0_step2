from supabase import create_client
url = "https://pszefvosagdpzilocerq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzemVmdm9zYWdkcHppbG9jZXJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ4ODU1NTIsImV4cCI6MjA2MDQ2MTU1Mn0.nRw_Ev8VGVf_PvnQZ5Lk10JPYg3jaJwUWkGCmNO03fA"
supabase = create_client(url, key)
# テスト挿入
res = supabase.table("place_duplicate").insert({"name":"テスト","url":"","lat":0,"lon":0,"mood":"テスト","time":None}).execute()
print(res)
# テスト取得
print(supabase.table("place_duplicate").select("*").eq("mood","テスト").execute())