from typing import List, Optional

import paramiko


def list_sftp(url: str, port: int, username: str, password: str, directory: str) -> Optional[List[str]]:
    """
    Connect to an SFTP server and list files in the specified directory.

    Args:
        url (str): The hostname or IP of the SFTP server.
        port (int): The port number (usually 22 for SFTP).
        username (str): Username for authentication.
        password (str): Password for authentication.
        directory (str): Remote directory to list files from.

    Returns:
        Optional[List[str]]: List of filenames in the directory, or None if connection fails.
    """
    try:
        transport = paramiko.Transport((url, port))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        assert sftp is not None  # Inform type checker that sftp is not None
        files = sftp.listdir(directory)

        sftp.close()
        transport.close()
        return files

    except Exception as e:
        print(f"SFTP error: {e}")
        return None
