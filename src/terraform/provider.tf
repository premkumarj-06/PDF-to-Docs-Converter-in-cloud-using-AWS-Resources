# to create bucket from aws cloudshell
# aws s3api create-bucket --bucket doc-converter-03 --region ap-south-1 --create-bucket-configuration LocationConstraint=ap-south-1

# # sync all folders to the bucket
# aws s3 sync folder-path s3://doc-converter-03

# # to copy only one file to s3 from cloudshell
# aws s3 cp /home/cloudshell-user/python.zip s3://doc-converter-03/python/

# # zip all the contents of the file
# zip -r [file.zip] [file]