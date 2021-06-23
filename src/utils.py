import urllib.request
from botocore.exceptions import ClientError
import boto3
import os
import zipfile
from lxml import etree


def upload_s3(local_file_path, s3_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")

    try:
        s3.upload_file(local_file_path, bucket_name, s3_key)
    except ClientError as e:
        print(f"failed uploading to s3 {e}")
        return False
    return True


def get_safe_value_from_dict(data, key):
    if key in data:
        return data[key]
    else:
        return None


def download(url: str, filename: str, folder: str):
    filepath = f'{folder}/{filename}'
    print(f"downloading: {url}")
    filepath, headers = urllib.request.urlretrieve(url, filename=filepath)
    print("download file location: ", filepath)
    return filepath


def get_epub_cover(epub_path):
    namespaces = {
        "calibre": "http://calibre.kovidgoyal.net/2009/metadata",
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcterms": "http://purl.org/dc/terms/",
        "opf": "http://www.idpf.org/2007/opf",
        "u": "urn:oasis:names:tc:opendocument:xmlns:container",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }
    ''' Return the cover image file from an epub archive. '''

    # We open the epub archive using zipfile.ZipFile():
    with zipfile.ZipFile(epub_path) as z:
        t = etree.fromstring(z.read("META-INF/container.xml"))
        rootfile_path = t.xpath("/u:container/u:rootfiles/u:rootfile",
                                namespaces=namespaces)[0].get("full-path")
        # print("Path of root file found: " + rootfile_path)

        t = etree.fromstring(z.read(rootfile_path))
        cover_id = t.xpath("//opf:metadata/opf:meta[@name='cover']",
                           namespaces=namespaces)[0].get("content")
        # print("ID of cover image found: " + cover_id)

        cover_href = t.xpath("//opf:manifest/opf:item[@id='" + cover_id + "']",
                             namespaces=namespaces)[0].get("href")
        cover_path = os.path.join(os.path.dirname(rootfile_path), cover_href)
        print("Path of cover image found: " + cover_path)

        return z.open(cover_path)


def write_file(filepath, contents):
    f = open(filepath, "w")
    f.write(contents)
    f.close()
