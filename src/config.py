"""
Configuration module for loading environment variables.

This module uses python-dotenv to load environment variables from a .env file
and provides easy access to configuration values throughout the application.

Usage:
    from src.config import Config
    
    # Access configuration values
    bucket_name = Config.S3_BUCKET_NAME
    region = Config.AWS_REGION
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Find the .env file in the project root (research_assistant directory)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Central configuration class for all environment variables."""
    
    # AWS Configuration
    AWS_PROFILE = os.getenv('AWS_PROFILE', 'default')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # AWS S3 Bucket
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    S3_INDEX_KEY = os.getenv('S3_INDEX_KEY', 'faiss/claims.index')
    S3_METADATA_KEY = os.getenv('S3_METADATA_KEY', 'faiss/claims_meta.pkl')
    
    # AWS Bedrock Models
    EMBED_MODEL_ID = os.getenv('EMBED_MODEL_ID', 'amazon.titan-embed-text-v2:0')
    SEARCH_MODEL_ID = os.getenv('SEARCH_MODEL_ID', 'meta.llama3-8b-instruct-v1:0')
    MODEL_ID = os.getenv('MODEL_ID', 'global.anthropic.claude-haiku-4-5-20251001-v1:0')
    
    # Local Paths
    DOWNLOADS_DIR = os.getenv('DOWNLOADS_DIR', 'downloads')
    INDEX_FILENAME = os.getenv('INDEX_FILENAME', 'faiss_claims.index')
    METADATA_FILENAME = os.getenv('METADATA_FILENAME', 'metadata.pkl')
    
    # Model Configuration
    EMBEDDING_DIMENSIONS = int(os.getenv('EMBEDDING_DIMENSIONS', '256'))
    MAX_OUTPUT_TOKENS = int(os.getenv('MAX_OUTPUT_TOKENS', '900'))
    TOP_K_RESULTS = int(os.getenv('TOP_K_RESULTS', '2'))
    FRESH_CLAIMS_LIMIT = int(os.getenv('FRESH_CLAIMS_LIMIT', '10'))
    
    # Cache Directory
    CACHE_DIR = os.getenv('CACHE_DIR', 'cache/semantic_scholar')
    
    @classmethod
    def validate(cls):
        """Validate that required environment variables are set."""
        required_vars = ['S3_BUCKET_NAME']
        missing = [var for var in required_vars if not getattr(cls, var)]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please check your .env file."
            )
    
    @classmethod
    def get_aws_session(cls):
        """Create and return a boto3 session with configured profile and region."""
        import boto3
        return boto3.Session(
            profile_name=cls.AWS_PROFILE,
            region_name=cls.AWS_REGION
        )
    
    @classmethod
    def get_bedrock_client(cls):
        """Create and return a Bedrock runtime client."""
        session = cls.get_aws_session()
        return session.client(
            service_name='bedrock-runtime',
            region_name=cls.AWS_REGION
        )
    
    @classmethod
    def get_s3_client(cls):
        """Create and return an S3 client."""
        session = cls.get_aws_session()
        return session.client('s3', region_name=cls.AWS_REGION)
