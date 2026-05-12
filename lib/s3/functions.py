import os
from fastapi import UploadFile, HTTPException
import aioboto3
from botocore.client import Config
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION")

session = aioboto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

async def upload_cv(userId: str, cv: UploadFile):
    s3_key = f"cvs/{userId}.pdf"
    
    try:
        file_content = await cv.read()

        async with session.client("s3") as s3: # type: ignore
            await s3.put_object(
                Bucket=AWS_S3_BUCKET,
                Key=s3_key,
                Body=file_content,
                ContentType="application/pdf"
            )
        
        return s3_key

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

async def delete_cv(s3_key: str):
    try:
        async with session.client("s3") as s3: # type: ignore
            await s3.delete_object(
                Bucket=AWS_S3_BUCKET,
                Key=s3_key
            )
        return True
    except Exception as e:
        print(f"Error eliminando de S3: {e}")
        raise HTTPException(status_code=500, detail=f"No se pudo eliminar el archivo: {str(e)}")

async def get_presigned_url(s3_key: str, expires_in: int = 3600):
    try:
        # Añadimos la configuración para forzar Signature Version 4
        s3_config = Config(signature_version='s3v4')

        async with session.client(
            "s3", 
            region_name=AWS_REGION,
            config=s3_config
        ) as s3: # type: ignore
            url = await s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': AWS_S3_BUCKET,
                    'Key': s3_key
                },
                ExpiresIn=expires_in
            )
            return url
        
    except Exception as e:
        print(f"Error generando URL firmada: {e}")
        raise HTTPException(status_code=500, detail="No se pudo generar el enlace de acceso.")