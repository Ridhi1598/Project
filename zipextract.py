import zipfile
with zipfile.ZipFile('email.zip', 'r') as zip_ref:
    zip_ref.extractall()