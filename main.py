import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("ffmpeg_mcp")

@mcp.tool()
def run_ffmpeg_command(sandbox: str, command: str) -> str:
    """
    Executes an ffmpeg command on the server and returns the output.
    
    Args:
        sandbox (str): The sandbox directory path. Required to ensure commands run in isolation. The command will be run within this directory. Call create_sandbox() to create one.
        command (str): The ffmpeg command to execute.
        
    Returns:
        str: The output from the ffmpeg command execution.
    """
    import subprocess
    
    if not sandbox:
        return "Error: Sandbox environment not specified. Please create a sandbox first."
    
    if not command.startswith("ffmpeg"):
        return "Error: Only ffmpeg commands are allowed."

    if not os.path.exists(sandbox):
        return "Error: Sandbox environment does not exist."

    try:
        result = subprocess.run(
            command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=sandbox
        )
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr.decode('utf-8')}"
    
@mcp.tool()
def create_sandbox():
    """
    Creates a sandboxed environment for running ffmpeg commands.
    
    Returns:
        str: Sandbox directory path.
    """
    
    random_suffix = httpx.get("https://www.random.org/strings/?num=1&len=8&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new").text.strip()
    sandbox_dir = f"/tmp/ffmpeg_sandbox_{random_suffix}"

    return sandbox_dir

@mcp.tool()
def put_file(sandbox: str, filename: str, content: bytes) -> str:
    """
    Puts a file into the sandbox environment.
    
    Args:
        sandbox (str): The sandbox directory path.
        filename (str): The name of the file to create.
        content (bytes): The content to write into the file.
        
    Returns:
        str: The full path of the created file.
    """
    import os

    if not os.path.exists(sandbox):
        os.makedirs(sandbox)

    file_path = os.path.join(sandbox, filename)
    with open(file_path, 'wb') as f:
        f.write(content)
    
    return file_path

@mcp.tool()
def get_file(sandbox: str, filename: str) -> bytes:
    """
    Retrieves a file from the sandbox environment.
    
    Args:
        sandbox (str): The sandbox directory path.
        filename (str): The name of the file to retrieve.
        
    Returns:
        bytes: The content of the retrieved file.
    """
    import os

    file_path = os.path.join(sandbox, filename)
    with open(file_path, 'rb') as f:
        content = f.read()
    
    return content

@mcp.tool()
def delete_file(sandbox: str, filename: str) -> str:
    """
    Deletes a file from the sandbox environment.
    
    Args:
        sandbox (str): The sandbox directory path.
        filename (str): The name of the file to delete.
        
    Returns:
        str: Confirmation message.
    """
    import os

    file_path = os.path.join(sandbox, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"File {filename} deleted successfully."
    else:
        return f"File {filename} does not exist."
    
@mcp.tool()
def download_file(sandbox: str, url: str, filename: str) -> str:
    """
    Downloads a file from a URL into the sandbox environment.
    
    Args:
        sandbox (str): The sandbox directory path.
        url (str): The URL of the file to download.
        filename (str): The name to save the downloaded file as.
        
    Returns:
        str: The full path of the downloaded file.
    """
    import os
    import httpx

    if not os.path.exists(sandbox):
        os.makedirs(sandbox)

    response = httpx.get(url)
    file_path = os.path.join(sandbox, filename)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    
    return file_path

@mcp.tool()
def upload_file(sandbox: str, filename: str, upload_url: str) -> str:
    """
    Uploads a file from the sandbox environment to a specified URL.
    
    Args:
        sandbox (str): The sandbox directory path.
        filename (str): The name of the file to upload.
        upload_url (str): The URL to upload the file to.
        
    Returns:
        str: The response from the upload request.
    """
    import os
    import httpx

    file_path = os.path.join(sandbox, filename)
    with open(file_path, 'rb') as f:
        files = {'file': (filename, f)}
        response = httpx.post(upload_url, files=files)
    
    return response.text

@mcp.tool()
def download_file_from_gcs(sandbox: str, gcs_url: str, filename: str) -> str:
    """
    Downloads a file from Google Cloud Storage into the sandbox environment.
    
    Args:
        sandbox (str): The sandbox directory path.
        gcs_url (str): The GCS URL of the file to download.
        filename (str): The name to save the downloaded file as.
        
    Returns:
        str: The full path of the downloaded file.
    """
    import os
    from google.cloud import storage

    if not os.path.exists(sandbox):
        os.makedirs(sandbox)

    client = storage.Client()
    bucket_name, blob_name = gcs_url.replace("gs://", "").split("/", 1)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    file_path = os.path.join(sandbox, filename)
    blob.download_to_filename(file_path)
    
    return file_path

@mcp.tool()
def upload_file_to_gcs(sandbox: str, filename: str, gcs_url):
    """
    Uploads a file from the sandbox environment to Google Cloud Storage.
    
    Args:
        sandbox (str): The sandbox directory path.
        filename (str): The name of the file to upload.
        gcs_url (str): The GCS URL to upload the file to.
        
    Returns:
        str: Confirmation message.
    """
    import os
    from google.cloud import storage

    file_path = os.path.join(sandbox, filename)
    client = storage.Client()
    bucket_name, blob_name = gcs_url.replace("gs://", "").split("/", 1)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_filename(file_path)
    
    return f"File {filename} uploaded to {gcs_url} successfully."

if __name__ == "__main__":
    mcp.run()
