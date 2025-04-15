# Add these imports at the top
from django.conf import settings
import supabase

def get_supabase_client():
    """
    Returns the Supabase client instance or None if not configured
    """
    return settings.supabase

def fetch_data(table_name, query=None):
    """
    Fetch data from a Supabase table
    """
    client = get_supabase_client()
    if not client:
        return None
    
    data = client.table(table_name).select("*")
    if query:
        data = query(data)
    
    return data.execute()

def insert_data(table_name, data):
    """
    Insert data into a Supabase table
    """
    client = get_supabase_client()
    if not client:
        return None
    
    return client.table(table_name).insert(data).execute()

def update_data(table_name, data, match_column, match_value):
    """
    Update data in a Supabase table
    """
    client = get_supabase_client()
    if not client:
        return None
    
    return client.table(table_name).update(data).eq(match_column, match_value).execute()

def delete_data(table_name, match_column, match_value):
    """
    Delete data from a Supabase table
    """
    client = get_supabase_client()
    if not client:
        return None
    
    return client.table(table_name).delete().eq(match_column, match_value).execute()