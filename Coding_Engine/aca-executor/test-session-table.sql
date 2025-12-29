-- Create test_session table
-- This table tracks candidate test sessions with timing, status, and activity monitoring

CREATE TABLE test_session (
    candidate_id VARCHAR(36) NOT NULL PRIMARY KEY,
    test_start_time TIMESTAMP NOT NULL,
    test_duration_minutes INTEGER NOT NULL DEFAULT 60,
    last_heartbeat TIMESTAMP NULL,
    last_activity TIMESTAMP NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    completion_method VARCHAR(50) NULL,
    completed_at TIMESTAMP NULL,
    sections_completed JSONB NULL,
    pending_answers JSONB NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    CONSTRAINT fk_test_session_candidate 
        FOREIGN KEY (candidate_id) 
        REFERENCES candidate(candidate_id) 
        ON DELETE CASCADE,
    
    -- Check constraints
    CONSTRAINT test_session_status_check 
        CHECK (status IN ('active', 'completed', 'abandoned')),
    
    CONSTRAINT test_session_completion_method_check 
        CHECK (completion_method IN ('manual', 'tab_close', 'timer_expired', 'heartbeat_timeout', 'auto') 
               OR completion_method IS NULL)
);

-- Create indexes for better query performance
CREATE INDEX idx_test_session_status ON test_session(status);
CREATE INDEX idx_test_session_last_heartbeat ON test_session(last_heartbeat);
CREATE INDEX idx_test_session_test_start_time ON test_session(test_start_time);

-- Create function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_test_session_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at on row update
CREATE TRIGGER trigger_update_test_session_updated_at
    BEFORE UPDATE ON test_session
    FOR EACH ROW
    EXECUTE FUNCTION update_test_session_updated_at();

