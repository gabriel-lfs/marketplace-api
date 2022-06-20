from typing import Optional

import boto3
from botocore.exceptions import ClientError
from botocore.response import StreamingBody
from pydantic import AnyHttpUrl
from starlette.datastructures import State
from starlette.requests import Request

from core.settings import settings


class StorageProvider:
    state_name = 'storage_provider'

    def __init__(
            self,
            endpoint_url: Optional[AnyHttpUrl] = None,
    ):
        self._endpoint_url = endpoint_url or settings.endpoint_url

    @property
    def _client(self):
        if not hasattr(self, '__client'):
            self.__client = boto3.client(
                's3',
                endpoint_url=self._endpoint_url or settings.endpoint_url
            )
        return self.__client

    def file_exists(
            self, key: str, bucket_name: Optional[str] = None
    ) -> bool:
        bucket_name = bucket_name or settings.bucket_name
        try:
            self._client.head_object(Bucket=bucket_name, Key=key)
        except ClientError as e:
            if e.response.get('Error', {}).get('Code', '') == 404:
                return False
            else:
                raise
        else:
            return True

    def get_file(
            self, key: str, bucket_name: Optional[str] = None
    ) -> Optional[StreamingBody]:
        bucket_name = bucket_name or settings.bucket_name

        if not self.file_exists(key, bucket_name):
            return None

        payload = self._client.get_object(Bucket=bucket_name, Key=key)
        return payload['Body']


def setup_storage(enpoint_url: AnyHttpUrl = None):
    async def _setup_storage(state: State):
        provider = StorageProvider(endpoint_url=enpoint_url)
        setattr(state, StorageProvider.state_name, provider)

    return _setup_storage


def get_storage(request: Request):
    return getattr(request.app.state, StorageProvider.state_name)
