### Renaissance File Uploader
### Script to upload files to
### Renaissance SFTP server

def ren_sftp_uploader(file_list):
    ###Import Modules###
    import pysftp
    from os import getenv
    from dotenv import load_dotenv
    #######

    ###Variables###
    #Load .ENV File
    load_dotenv('/config_files/env_file/.env')
    #Renaissance SFTP Vars
    renaissance_hostname = getenv('renaissance_hostname')
    renaissance_username = getenv('renaissance_username')
    renaissance_pass = getenv('renaissance_pass')
    #SFTP Config
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    #######

    ###Upload Files to Renaissance###
    with pysftp.Connection(host=renaissance_hostname, \
                        username=renaissance_username, \
                        password=renaissance_pass,
                        cnopts=cnopts) as sftp:
        for upload_file in file_list:
            sftp.put(upload_file,upload_file.split('/')[-1])
    #######