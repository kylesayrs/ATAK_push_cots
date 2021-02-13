from zipPackage import zipPackage
from pushCoT import pushCoT

# Don't forget to start serveFiles.py first!
if __name__ == '__main__':
    UID = 'asdf-1234'
    zip_path = zipPackage(UID)
    pushCoT(UID,                # Uid of CoT message
            34.850132,          # Lat of CoT
            137.120065,         # Lon of Cot
            file_path=zip_path) # Omit for no file
