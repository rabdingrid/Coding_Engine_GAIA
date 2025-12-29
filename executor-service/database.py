"""Database connection and operations"""
import json
import uuid
import logging
import asyncpg
import asyncio
from typing import List, Dict, Optional
from executor_service.config import DATABASE_URL

logger = logging.getLogger(__name__)

# Database connection pool (lazy initialization - only when needed)
db_pool = None
_db_pool_lock = asyncio.Lock()

async def get_db_pool():
    """Lazy initialization of database connection pool - SECURITY FIX: No hardcoded credentials"""
    global db_pool
    if db_pool is None:
        async with _db_pool_lock:
            if db_pool is None:  # Double-check after acquiring lock
                try:
                    # SECURITY FIX: DATABASE_URL is required from environment (no fallback)
                    if not DATABASE_URL:
                        raise ValueError("DATABASE_URL environment variable is required. Set it in Azure Container Apps environment variables.")
                    db_pool = await asyncpg.create_pool(
                        DATABASE_URL,
                        min_size=1,
                        max_size=5,  # Reduced pool size
                        command_timeout=30  # Reduced timeout
                    )
                    logger.info("✅ Database connection pool created (lazy init)")
                except Exception as e:
                    logger.error(f"❌ Database connection failed: {e}")
                    db_pool = None
    return db_pool

async def save_submission_to_db(
    user_id: str,
    question_id: str,
    language: str,
    code: str,
    test_results: List[Dict],
    summary: Dict,
    execution_id: str
) -> Optional[str]:
    """Save submission results to database"""
    pool = await get_db_pool()
    if not pool:
        logger.warning("Database pool not available, skipping save")
        return None
    
    try:
        async with pool.acquire() as conn:
            # Create submissions table if it doesn't exist
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS submissions (
                    id SERIAL PRIMARY KEY,
                    submission_id VARCHAR(255) UNIQUE,
                    user_id VARCHAR(255) NOT NULL,
                    question_id VARCHAR(255) NOT NULL,
                    language VARCHAR(50) NOT NULL,
                    code TEXT NOT NULL,
                    test_results JSONB NOT NULL,
                    summary JSONB NOT NULL,
                    execution_id VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert submission
            submission_id = str(uuid.uuid4())
            await conn.execute("""
                INSERT INTO submissions (
                    submission_id, user_id, question_id, language, code,
                    test_results, summary, execution_id
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, submission_id, user_id, question_id, language, code,
                json.dumps(test_results), json.dumps(summary), execution_id)
            
            logger.info(f"✅ Submission saved: {submission_id}")
            return submission_id
    except Exception as e:
        logger.error(f"❌ Error saving submission: {e}")
        raise

