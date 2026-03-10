from ftplib import FTP


def list_ftp(url: str, port: int, username: str, password: str, dir: str) -> list[str]:
    """
    Connect to an FTP server and list files in the specified directory.

    Args:
        url (str): The hostname or IP of the SFTP server.
        port (int): The port number (usually 22 for SFTP).
        username (str): Username for authentication.
        password (str): Password for authentication.
        directory (str): Remote directory to list files from.

    Returns:
        list[str]: List of filenames.
    """
    ftp = FTP()
    ftp.connect("example.com", 21)
    ftp.login("user", "pass")
    files = ftp.nlst()
    ftp.quit()

    return files
