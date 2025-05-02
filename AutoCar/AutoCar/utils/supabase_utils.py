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

def ensure_bucket_exists(bucket_name: str):
    """
    Check if a bucket exists, and create it if it doesn't
    """
    try:
        client = get_supabase_client()
        if not client:
            logger.error("No Supabase client available")
            return False
        
        # Debug: Log the Supabase URL (but not the key for security)
        supabase_url = client.supabase_url if hasattr(client, 'supabase_url') else 'Unknown'
        logger.info(f"Using Supabase URL: {supabase_url}")
        
        # List all buckets for debugging
        try:
            all_buckets = client.storage.list_buckets()
            logger.info(f"Existing buckets: {all_buckets}")
        except Exception as list_error:
            logger.error(f"Unable to list buckets: {list_error}")
            
        # Try to get the bucket to check if it exists
        try:
            logger.info(f"Checking if bucket '{bucket_name}' exists...")
            bucket_info = client.storage.get_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' already exists: {bucket_info}")
            return True
        except Exception as get_error:
            logger.error(f"Error checking if bucket exists: {get_error}")
            logger.info(f"Bucket '{bucket_name}' doesn't exist, attempting to create it...")
            
            # Bucket doesn't exist, create it
            try:
                create_result = client.storage.create_bucket(bucket_name, {'public': True})
                logger.info(f"Created bucket '{bucket_name}' result: {create_result}")
                return True
            except Exception as create_error:
                logger.error(f"Failed to create bucket '{bucket_name}': {create_error}")
                
                # Try the alternative API format if applicable
                try:
                    logger.info("Trying alternative bucket creation format...")
                    create_result = client.storage.create_bucket(id=bucket_name, options={'public': True})
                    logger.info(f"Created bucket with alternative format: {create_result}")
                    return True
                except Exception as alt_error:
                    logger.error(f"Alternative bucket creation also failed: {alt_error}")
                    return False
    except Exception as e:
        logger.error(f"Error ensuring bucket exists: {e}")
        return False

def upload_file_to_storage(bucket_name: str, file_path: str, file_content: bytes, content_type: str = None):
    """
    Upload a file to Supabase Storage with comprehensive error handling
    
    Args:
        bucket_name (str): The name of the storage bucket
        file_path (str): The path within the bucket (including filename)
        file_content (bytes): The binary content of the file
        content_type (str, optional): The MIME type of the file
    
    Returns:
        tuple: (success, result_or_error)
            success (bool): True if upload succeeded, False otherwise
            result_or_error: The upload result or error message
    """
    try:
        client = get_supabase_client()
        if not client:
            return False, "No Supabase client available"
        
        # Ensure the bucket exists first
        if not ensure_bucket_exists(bucket_name):
            return False, f"Failed to create or access bucket: {bucket_name}"
        
        # Prepare file options
        file_options = {}
        if content_type:
            # Try both formats that might be supported by the Supabase client version
            file_options = {
                "contentType": content_type,  # Newer format
                "content-type": content_type  # Older format
            }
        
        # Attempt upload using different API formats
        try:
            # Try the newer API format first
            try:
                logger.info(f"Trying upload with newer API format: file_options={file_options}")
                result = client.storage.from_(bucket_name).upload(
                    file_path,
                    file_content,
                    file_options=file_options
                )
                logger.info(f"Upload successful with newer API format: {result}")
            except (TypeError, AttributeError):
                # Fall back to older API format
                logger.info("Falling back to older API format")
                result = client.storage.from_(bucket_name).upload(
                    file_path,
                    file_content,
                    file_options
                )
                logger.info(f"Upload successful with older API format: {result}")
            
            # Get the public URL
            try:
                url = client.storage.from_(bucket_name).get_public_url(file_path)
                if not url:
                    return False, "Failed to get public URL after successful upload"
                
                return True, url
            except Exception as url_error:
                logger.error(f"Error getting public URL: {url_error}")
                return False, f"File uploaded but failed to get public URL: {str(url_error)}"
                
        except Exception as upload_error:
            logger.error(f"Error in upload operation: {upload_error}")
            return False, str(upload_error)
            
    except Exception as e:
        logger.error(f"Unexpected error in upload_file_to_storage: {e}")
        return False, str(e) 