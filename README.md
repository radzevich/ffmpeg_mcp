# FFmpeg MCP Server

A Model Context Protocol (MCP) server that provides secure FFmpeg functionality through a sandboxed environment. This server allows AI assistants and other MCP clients to perform video/audio processing tasks using FFmpeg in an isolated environment.

## Features

- **Sandboxed Execution**: All FFmpeg commands run in isolated temporary directories for security
- **File Management**: Upload, download, and manage files within the sandbox
- **Google Cloud Storage Integration**: Direct integration with GCS for file transfers
- **Security**: Only FFmpeg commands are allowed, preventing arbitrary code execution
- **RESTful API**: Runs as an HTTP server using FastMCP

## Installation

### Prerequisites

- Python 3.11 or higher
- FFmpeg installed on your system
- (Optional) Google Cloud credentials for GCS features

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ffmpeg_mcp
```

2. Install dependencies using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

3. (Optional) Set up Google Cloud credentials for GCS integration:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

## Usage

### Starting the Server

```bash
python main.py
```

The server will start on `localhost:8000` by default.

### Available Tools

#### 1. `create_sandbox()`
Creates a new isolated sandbox environment for FFmpeg operations.

**Returns:** Sandbox directory path

#### 2. `run_ffmpeg_command(sandbox, command)`
Executes FFmpeg commands within the specified sandbox.

**Parameters:**
- `sandbox` (str): Sandbox directory path
- `command` (str): FFmpeg command to execute

**Returns:** Command output or error message

#### 3. `put_file(sandbox, filename, content)`
Puts a file into the sandbox environment.

**Parameters:**
- `sandbox` (str): Sandbox directory path
- `filename` (str): Name of the file to create
- `content` (bytes): File content

**Returns:** Full path of the created file

#### 4. `get_file(sandbox, filename)`
Retrieves a file from the sandbox environment.

**Parameters:**
- `sandbox` (str): Sandbox directory path
- `filename` (str): Name of the file to retrieve

**Returns:** File content as bytes

#### 5. `delete_file(sandbox, filename)`
Deletes a file from the sandbox environment.

**Parameters:**
- `sandbox` (str): Sandbox directory path
- `filename` (str): Name of the file to delete

**Returns:** Confirmation message

#### 6. `download_file(sandbox, url, filename)`
Downloads a file from a URL into the sandbox.

**Parameters:**
- `sandbox` (str): Sandbox directory path
- `url` (str): URL of the file to download
- `filename` (str): Local filename to save as

**Returns:** Full path of the downloaded file

#### 7. `upload_file(sandbox, filename, upload_url)`
Uploads a file from the sandbox to a specified URL.

**Parameters:**
- `sandbox` (str): Sandbox directory path
- `filename` (str): Name of the file to upload
- `upload_url` (str): Destination URL

**Returns:** Upload response

#### 8. `download_file_from_gcs(sandbox, gcs_url, filename)`
Downloads a file from Google Cloud Storage.

**Parameters:**
- `sandbox` (str): Sandbox directory path
- `gcs_url` (str): GCS URL (gs://bucket/path)
- `filename` (str): Local filename to save as

**Returns:** Full path of the downloaded file

#### 9. `upload_file_to_gcs(sandbox, filename, gcs_url)`
Uploads a file to Google Cloud Storage.

**Parameters:**
- `sandbox` (str): Sandbox directory path
- `filename` (str): Name of the file to upload
- `gcs_url` (str): Destination GCS URL

**Returns:** Confirmation message

## Example Workflow

```python
# 1. Create a sandbox
sandbox = create_sandbox()

# 2. Download a video file
download_file(sandbox, "https://example.com/video.mp4", "input.mp4")

# 3. Process with FFmpeg
run_ffmpeg_command(sandbox, "ffmpeg -i input.mp4 -vf scale=720:480 output.mp4")

# 4. Retrieve the processed file
processed_video = get_file(sandbox, "output.mp4")
```

## Security Features

- **Command Restriction**: Only commands starting with "ffmpeg" are allowed
- **Sandbox Isolation**: All operations are contained within temporary directories
- **Path Validation**: Sandbox directories are validated before operations
- **Error Handling**: Comprehensive error handling for failed operations

## Configuration

The server runs on `localhost:8000` by default. You can modify the host and port in the `main.py` file:

```python
if __name__ == "__main__":
    mcp.run(transport="httpx", host="your-host", port=your-port)
```

## Dependencies

- `httpx`: HTTP client for file downloads and uploads
- `mcp[cli]`: Model Context Protocol server framework
- `google-cloud-storage`: Google Cloud Storage integration (optional)
