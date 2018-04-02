from fastavro import reader
import boto3
import subprocess

def remove_s3_file(path):
    cmd='aws s3 rm '+ path
    subprocess.call(cmd.split(" "))

def remove_empty_avro_file(path):
    """Get a list of keys in an S3 bucket."""
    bucket_name = path.split('/')[2]
    prefix = '/'.join(path.split('/')[3:])
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=prefix):
        file='s3://{0}/{1}'.format(bucket.name, obj.key)
        file_stream= read_s3_data(file)
        is_empty=is_empty_avro_file(file_stream)
        if is_empty:
            remove_s3_file(file)


def read_s3_data(path):
    bucket_name = path.split('/')[2]
    prefix = '/'.join(path.split('/')[3:])
    s3 = boto3.resource("s3")
    response = s3.Object(bucket_name=bucket_name, key=prefix).get()

    return response['Body']

def is_empty_avro_file(file):
    response = True
    avro_reader = reader(file)
    for record in avro_reader:
        response = False
        break

    return response


if __name__ == '__main__':
    remove_empty_avro_file("s3://ash.data/khirul/20180313")
