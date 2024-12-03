import gzip
import shutil

# Replace 'yourfile.gz' with your actual .gz file name
with gzip.open('network-accounts-service-qa02-LogsToS3-1-2024-11-18-09-14-22-46a19023-ca0e-440c-b269-75127a6321d2.gz', 'rb') as f_in:
    with open('network-accounts-service-qa02-LogsToS3-1-2024-11-18-09-14-22-46a19023-ca0e-440c-b269-75127a6321d2.json', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print("File decompressed successfully!")
