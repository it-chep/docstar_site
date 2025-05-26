import boto3
import os
from botocore.exceptions import ClientError, NoCredentialsError


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

            # https: // storage.yandexcloud.net / medblogers - photos / images / user_trutneva - nataliya - konstantinovna_ % D0 % A1 % D0 % BD % D0 % B8 % D0 % BC % D0 % BE % D0 % BA % 20 % D1 % 8
            # D % D0 % BA % D1 % 80 % D0 % B0 % D0 % BD % D0 % B0 % 202025 - 05 - 16 % 20 % D0 % B2 % 2023.29
            # .20.png?X - Amz - Algorithm = AWS4 - HMAC - SHA256 & X - Amz - Credential = YCAJE0dbB1ceTT28e9UHQE3fM % 2
            # F20250525 % 2
            # Fru - central1 % 2
            # Fs3 % 2
            # Faws4_request & X - Amz - Date = 20250525
            # T205226Z & X - Amz - Expires = 3600 & X - Amz - SignedHeaders = host & X - Amz - Signature = 238229
            # d9192e198975209bcbdc3fa744014483d1be856d3152db26d21dc9b1b2
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
