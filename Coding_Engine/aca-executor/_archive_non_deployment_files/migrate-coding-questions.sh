#!/bin/bash

# Migrate coding_question_bank from Railway to Azure
# This script copies questions from Railway to Azure that don't already exist

set -e

echo "🚀 Migrating coding_question_bank from Railway to Azure..."
echo ""

# Database connections
RAILWAY_DB="postgresql://postgres:LpGWrOQpFdgLxybzTYWdGiAuJbitpizZ@yamanote.proxy.rlwy.net:55115/railway"
AZURE_DB=$(cat .postgres-connection.txt)

if [ -z "$AZURE_DB" ]; then
    echo "❌ Error: Azure database connection string not found in .postgres-connection.txt"
    exit 1
fi

# Use PostgreSQL 17 client tools
export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"

echo "📊 Step 1: Checking Railway database..."
RAILWAY_COUNT=$(psql "$RAILWAY_DB" -t -c "SELECT COUNT(*) FROM coding_question_bank;" | xargs)
echo "   Railway has $RAILWAY_COUNT questions"

echo ""
echo "📊 Step 2: Checking Azure database..."
AZURE_COUNT=$(psql "$AZURE_DB" -t -c "SELECT COUNT(*) FROM coding_question_bank;" | xargs)
echo "   Azure has $AZURE_COUNT questions"

echo ""
echo "📊 Step 3: Finding questions to migrate..."

# Create a SQL file to find UUIDs that need migration
MIGRATE_SQL=$(mktemp)
cat > "$MIGRATE_SQL" << 'SQLEOF'
-- Find UUIDs in Railway that don't exist in Azure
SELECT r.uuid
FROM coding_question_bank r
WHERE NOT EXISTS (
    SELECT 1 
    FROM coding_question_bank a 
    WHERE a.uuid = r.uuid
)
ORDER BY r.uuid;
SQLEOF

# Get list of UUIDs to migrate
MIGRATE_UUIDS=$(psql "$RAILWAY_DB" -t -f "$MIGRATE_SQL" | xargs)

if [ -z "$MIGRATE_UUIDS" ]; then
    echo "✅ All questions already exist in Azure. No migration needed."
    rm "$MIGRATE_SQL"
    exit 0
fi

MIGRATE_COUNT=$(echo "$MIGRATE_UUIDS" | wc -w | xargs)
echo "   Found $MIGRATE_COUNT questions to migrate"

echo ""
echo "📥 Step 4: Exporting and importing questions..."

# Create a migration SQL script
IMPORT_SQL=$(mktemp)
cat > "$IMPORT_SQL" << 'IMPORTSQL'
-- Migration script to copy questions from Railway to Azure
-- This will be executed on Azure database with data from Railway

IMPORTSQL

# For each UUID, create INSERT statement
for uuid in $MIGRATE_UUIDS; do
    echo "  Processing: $uuid..."
    
    # Get question data from Railway
    QUESTION_DATA=$(psql "$RAILWAY_DB" -t -A -F $'\t' -c "
        SELECT 
            uuid,
            question,
            COALESCE(sample_test_cases::text, '[]'),
            COALESCE(test_cases::text, '[]'),
            COALESCE(boiler_plate, ''),
            COALESCE(difficulty, ''),
            COALESCE(tags::text, '[]')
        FROM coding_question_bank
        WHERE uuid = '$uuid';
    ")
    
    # Parse the data (tab-separated)
    IFS=$'\t' read -r uuid_val question sample_tc test_tc boiler difficulty tags <<< "$QUESTION_DATA"
    
    # Escape single quotes in question and boiler_plate
    question_escaped=$(echo "$question" | sed "s/'/''/g")
    boiler_escaped=$(echo "$boiler" | sed "s/'/''/g")
    
    # Create INSERT statement
    cat >> "$IMPORT_SQL" << EOF
INSERT INTO coding_question_bank (uuid, question, sample_test_cases, test_cases, boiler_plate, difficulty, tags)
VALUES (
    '$uuid_val',
    E'$question_escaped',
    '$sample_tc'::jsonb,
    '$test_tc'::jsonb,
    E'$boiler_escaped',
    '$difficulty',
    '$tags'::jsonb
)
ON CONFLICT (uuid) DO NOTHING;

EOF
done

echo ""
echo "📤 Step 5: Executing migration on Azure..."

# Execute the import
psql "$AZURE_DB" -f "$IMPORT_SQL" > /dev/null 2>&1

IMPORTED=$(psql "$AZURE_DB" -t -c "SELECT COUNT(*) FROM coding_question_bank;" | xargs)
echo "   Migration executed"

echo ""
echo "✅ Migration complete!"

# Cleanup
rm "$MIGRATE_SQL" "$IMPORT_SQL" 2>/dev/null || true

echo ""
echo "📊 Final counts:"
FINAL_AZURE_COUNT=$(psql "$AZURE_DB" -t -c "SELECT COUNT(*) FROM coding_question_bank;" | xargs)
echo "   Railway: $RAILWAY_COUNT questions"
echo "   Azure: $FINAL_AZURE_COUNT questions"
echo "   Migrated: $((FINAL_AZURE_COUNT - AZURE_COUNT)) questions"
