### Renaissance File Uploader
### Script to upload files to
### Classlink SFTP server for 
### Created Renaissance Classes

def ren_sftp_uploader(env_file, file_list):
    ###Import Modules###
    import pysftp
    from os import getenv
    from dotenv import load_dotenv
    #######

    ###Variables###
    #Load .ENV File
    load_dotenv(env_file)
    #Classlink SFTP Vars
    classlink_hostname = getenv('classlink_hostname')
    classlink_username = getenv('classlink_username')
    classlink_key = getenv('classlink_key')
    #SFTP Config
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    #######

    ###Upload Files to Classlink###
    with pysftp.Connection(host=classlink_hostname, \
                        username=classlink_username, \
                        password=classlink_key,
                        cnopts=cnopts) as sftp:
        for upload_file in file_list:
            sftp.put(upload_file,upload_file.split('/')[-1])
    #######