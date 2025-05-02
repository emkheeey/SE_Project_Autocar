from django.conf import settings
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    """
    Returns the Supabase client instance
    """
    try:
        supabase_url = settings.SUPABASE_URL
        supabase_key = settings.SUPABASE_KEY
        
        if not supabase_url or not supabase_key:
            logger.error("Supabase URL or key not configured")
            return None
            
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        logger.error(f"Error creating Supabase client: {e}")
        return None

def fetch_data(table_name: str, query=None):
    """
    Fetch data from a Supabase table
    """
    try:
        client = get_supabase_client()
        if not client:
            logger.error("No Supabase client available")
            return None
        
        data = client.table(table_name).select("*")
        if query:
            data = query(data)
        
        result = data.execute()
        return result
    except Exception as e:
        logger.error(f"Error fetching data from {table_name}: {e}")
        return None

def insert_data(table_name: str, data: dict):
    """
    Insert data into a Supabase table
    """
    try:
        client = get_supabase_client()
        if not client:
            logger.error("No Supabase client available")
            return None
        
        result = client.table(table_name).insert(data).execute()
        return result
    except Exception as e:
        logger.error(f"Error inserting data into {table_name}: {e}")
        return None

def update_data(table_name: str, data: dict, match_column: str, match_value: str):
    """
    Update data in a Supabase table
    """
    try:
        client = get_supabase_client()
        if not client:
            logger.error("No Supabase client available")
            return None
        
        result = client.table(table_name).update(data).eq(match_column, match_value).execute()
        return result
    except Exception as e:
        logger.error(f"Error updating data in {table_name}: {e}")
        return None

def delete_data(table_name: str, match_column: str, match_value: str):
    """
    Delete data from a Supabase table
    """
    try:
        client = get_supabase_client()
        if not client:
            logger.error("No Supabase client available")
            return None
        
        result = client.table(table_name).delete().eq(match_column, match_value).execute()
        return result
    except Exception as e:
        logger.error(f"Error deleting data from {table_name}: {e}")
        return None 