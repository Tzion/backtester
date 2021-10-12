from globals import OUTPUT_DIR
from logger import *
import os


def clean_previous_output():
    '''
    DANGROUS - USE WITH CARE
    
    Delete all the files inside {OUTPUT_DIR}
    '''
    files_to_delete = ["html",]
    def clean_dir(path):
        files_deleted = 0
        for blob in [os.path.join(path,f) for f in os.listdir(path)]:
            if os.path.isdir(blob):
                clean_dir(blob)
            else:
                if blob.split('.')[-1] in files_to_delete:
                    os.remove(os.path.abspath(blob))
                    files_deleted += 1
        logdebug(f'{files_deleted} files were deleted in {path}')

    if os.path.abspath(OUTPUT_DIR).endswith('backtester/output'):  ## hardcoded validation
        clean_dir(OUTPUT_DIR)