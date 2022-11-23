from google.cloud import storage as s
from google.auth.transport.requests import AuthorizedSession
from google.resumable_media import requests, common

PROPHESY_STORAGE_CLIENT = s.Client()


def read_from_bucket(bucket_id, object_id, as_str=True):
    client = s.Client()
    bucket = client.get_bucket(bucket_id)
    blob = bucket.blob(object_id)
    if as_str:
        return blob.download_as_string()
    else:
        return blob


def read_to_disk(bucket_id, object_id, filename):
    client = s.Client()
    bucket = client.get_bucket(bucket_id)
    blob = bucket.blob(object_id)
    blob.download_to_filename(filename)
    return True


def write_to_bucket(bucket_id, object_id, contents, content_type=None):
    client = s.Client()
    bucket = client.get_bucket(bucket_id)
    blob = bucket.blob(object_id)
    if content_type:
        blob.upload_from_string(contents, content_type=content_type)
    else:
        blob.upload_from_string(contents)
    return object_id


def write_to_bucket_from_file(bucket_id, object_id, filename):
    client = s.Client()
    bucket = client.get_bucket(bucket_id)
    blob = bucket.blob(object_id)
    blob.upload_from_filename(filename)
    return object_id


def check_object_exists(bucket_id, object_id):
    client = s.Client()
    bucket = client.get_bucket(bucket_id)
    blob = bucket.blob(object_id)
    return blob.exists()


def remove_object(bucket_id, object_id):
    client = s.Client()
    bucket = client.get_bucket(bucket_id)
    blob = bucket.blob(object_id)
    blob.delete()
    return True


class GCSObjectStreamUpload(object):
    def __init__(
        self,
        client: s.Client,
        bucket: str,
        blob: str,
        content_type: str,
        chunk_size: int = 1024 * 1024,
    ):
        self._client = client
        self._bucket = self._client.bucket(bucket)
        self._blob = self._bucket.blob(blob)
        self._buffer = b""
        self._buffer_size = 0
        self._chunk_size = chunk_size
        self._content_type = content_type
        self._read = 0
        self._transport = AuthorizedSession(credentials=self._client._credentials)
        self._request = None  # type: requests.ResumableUpload

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, *_):
        if exc_type is None:
            self.stop()

    def start(self):
        url = (
            f"https://www.googleapis.com/upload/storage/v1/b/"
            f"{self._bucket.name}/o?uploadType=resumable"
        )
        self._request = requests.ResumableUpload(
            upload_url=url, chunk_size=self._chunk_size
        )
        self._request.initiate(
            transport=self._transport,
            content_type=self._content_type,
            stream=self,
            stream_final=False,
            metadata={"name": self._blob.name},
        )

    def stop(self):
        self._request.transmit_next_chunk(self._transport)

    def write(self, data: bytes) -> int:
        data_len = len(data)
        self._buffer_size += data_len
        self._buffer += data
        del data
        while self._buffer_size >= self._chunk_size:
            try:
                self._request.transmit_next_chunk(self._transport)
            except common.InvalidResponse:
                self._request.recover(self._transport)
        return data_len

    def read(self, chunk_size: int) -> bytes:
        # I'm not good with efficient no-copy buffering so if this is
        # wrong or there's a better way to do this let me know! :-)
        to_read = min(chunk_size, self._buffer_size)
        memview = memoryview(self._buffer)
        self._buffer = memview[to_read:].tobytes()
        self._read += to_read
        self._buffer_size -= to_read
        return memview[:to_read].tobytes()

    def tell(self) -> int:
        return self._read
