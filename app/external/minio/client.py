from minio import Minio  # pyright: ignore[reportAttributeAccessIssue]
import io

class MinioClient:
    def __init__(self, endpoint: str, access_key: str, secret_key: str) -> None:
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )

    def upload_file(self, file: bytes, bucket: str, key: str) -> None:
        data = io.BytesIO(file)

        self.client.put_object(
            bucket=bucket,
            object_name=key,
            data=data,
            length=len(file)
        )

    def upload_file_path(self, file_path: str, bucket: str, key: str) -> None:
        self.client.fput_object(
            bucket_name=bucket,
            object_name=key,
            file_path=file_path
        )

    def download_file(self, bucket: str, key: str) -> bytes:
        response = None

        try:
            response = self.client.get_object(bucket, key)
            return response.read()
        finally:
            if response:
                response.close()
                response.release_conn()

    def delete_file(self, bucket: str, key: str) -> None:
        self.client.remove_object(bucket, key)

    def list_files(self, bucket: str) -> list[str]:
        objects = self.client.list_objects(bucket)
        return [obj.object_name for obj in objects]