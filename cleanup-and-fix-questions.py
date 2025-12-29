#!/usr/bin/env python3
"""
Clean up database and keep only correct questions, then add remaining ones properly
"""

import json
import os
import asyncpg
import asyncio
import uuid
from pathlib import Path

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

async def cleanup():
    """Clean up database - keep only 3 correct questions"""
    conn = await asyncpg.connect(DB_URL)
    try:
        # Keep only these correct questions
        keep_uuids = [
            'd69847e4-e253-4400-9e44-febff93aeb3a',  # Warehouse Box Removal
            'eaec23b4-be2c-4b65-8745-15c265a56f75',  # Endpoint Inspection
            '22c620aa-b462-4ca5-adee-74ef95598862'   # Count Between
        ]
        
        # Delete all others
        result = await conn.execute('''
            DELETE FROM coding_question_bank 
            WHERE uuid NOT IN ($1, $2, $3)
        ''', keep_uuids[0], keep_uuids[1], keep_uuids[2])
        
        count = await conn.fetchval('SELECT COUNT(*) FROM coding_question_bank')
        print(f'✅ Cleaned database - kept 3 correct questions')
        print(f'   Total questions now: {count}')
        
    finally:
        await conn.close()

if __name__ == "__main__":
    print("🧹 Cleaning up database...")
    asyncio.run(cleanup())
    print("✅ Done!")




