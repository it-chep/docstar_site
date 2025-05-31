from typing import Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

DEFAULT_DOCTOR_IMAGE = 'https://storage.yandexcloud.net/medblogers-photos/images/zag.png'


class S3Client:
    def __init__(
            self,
            bucket_name: str,
            access_key: str,
            secret_key: str,
            region: str = "ru-central1",
            endpoint_url: str = "https://storage.yandexcloud.net",
    ):
        """
        Инициализация клиента для S3-совместимого хранилища или Yandex Object Storage.

        :param bucket_name: Название бакета
        :param access_key: Access Key ID
        :param secret_key: Secret Access Key
        :param region: Регион
        :param endpoint_url: Эндпоинт
        """
        self.bucket_name = bucket_name
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            config=boto3.session.Config(signature_version="s3v4"),
        )

    def upload_file(self, file_name: str, s3_key: str) -> bool:
        """Загружает файл в S3."""
        try:
            self.client.upload_file(file_name, self.bucket_name, s3_key)
            return True
        except (ClientError, NoCredentialsError, FileNotFoundError) as e:
            return False

    def put_object(self, file, s3_key: str) -> bool:
        """Загружает файл в S3."""
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file,
            )
            return True
        except (ClientError, NoCredentialsError, FileNotFoundError) as e:
            return False

    def download_file(self, s3_key: str, local_path: str) -> bool:
        """Скачивает файл из S3."""
        try:
            self.client.download_file(self.bucket_name, s3_key, local_path)
            return True
        except (ClientError, NoCredentialsError) as e:
            return False

    def _list_files(self, prefix: str) -> list:
        """Возвращает список файлов в бакете с указанным префиксом."""
        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
            )
            objects = response.get("Contents", [])
            sorted_objects = sorted(objects, key=lambda x: x["LastModified"])
            return [obj["Key"] for obj in sorted_objects]
        except ClientError as e:
            return []

    def get_user_photos(self) -> dict:
        files = self._list_files("images/user_")
        files_map = dict()
        for file in files:
            user_slug = file.split("_")[1]
            files_map[user_slug] = f"https://storage.yandexcloud.net/medblogers-photos/{file}"
        return files_map

    def delete_file(self, s3_key: str) -> bool:
        """Удаляет файл из S3."""
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            return False

    def check_connection(self) -> bool:
        """Проверяет подключение к бакету."""
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError as e:
            return False

    def generate_presigned_url(self, s3_key: str, expires_in=3600) -> str:
        """Генерирует временную ссылку на файл"""
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            return ""

    def get(self, s3_key: str) -> Optional[str]:
        """Получение фотографии по ключу"""
        try:
            url = self.client.get_object(Bucket=self.bucket_name, Key=s3_key)
            if url == "":
                return None
            return url
        except ClientError as e:
            return None
