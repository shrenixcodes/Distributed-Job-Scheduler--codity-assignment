
# ER Diagram (Textual Representation)

```
+----------------+      +-------------------------+      +-------------------+
| Users          |      | Organization Members    |      | Organizations     |
+----------------+      +-------------------------+      +-------------------+
| id (PK, UUID)  |<-----| id (PK, UUID)          |----->| id (PK, UUID)     |
| email (UNIQUE) |      | organization_id (FK)    |      | name (TEXT)       |
| full_name (TEXT)|     | user_id (FK)            |      | created_at (TIME) |
| created_at (TIME)     | role (TEXT)              |      +-------------------+
| updated_at (TIME)     +-------------------------+
+----------------+               |
                                 |
+------------------+             |
| Projects         |<------------+
+------------------+
| id (PK, UUID)    |
| org_id (FK)      |
| name (TEXT)      |
| description (TEXT)|
+------------------+
         |
         |
+-----------------+
| Queues          |
+-----------------+
| id (PK, UUID)   |
| project_id (FK) |
| name (TEXT)     |
| priority (INT)  |
| concurrency (INT)|
| is_paused (BOOL)|
+-----------------+
         |
         |
         |--------------------------------------------------
         |                                                 |
+------------------+   +---------------+   +-------------------+
| Jobs             |   | RetryPolicies |   | Scheduled Jobs    |
+------------------+   +---------------+   +-------------------+
| id (PK, UUID)    |   | id (PK, UUID) |   | id (PK, UUID)     |
| queue_id (FK)    |---| queue_id (FK) |   | queue_id (FK)     |
| status (TEXT)    |   | ...           |   | cron (TEXT)       |
| payload (JSON)   |   +---------------+   | ...               |
| priority (INT)   |                       +-------------------+
| ...              |
+------------------+
         |
         |
+--------------------+
| Job Executions     |
+--------------------+
| id (PK, UUID)      |
| job_id (FK)        |
| worker_id (FK)     |
| ...                |
+--------------------+

+---------------------+   +-------------------------+
| Workers             |   | Worker Heartbeats       |
+---------------------+   +-------------------------+
| id (PK, UUID)       |<--| id (PK, UUID)           |
| name (TEXT)         |   | worker_id (FK)          |
| status (TEXT)       |   | timestamp (TIME)        |
| last_heartbeat (TIME)|  +-------------------------+
+---------------------+

+---------------------------+
| Dead Letter Queue         |
+---------------------------+
| id (PK, UUID)             |
| original_job_id (FK)      |
| queue_id (FK)             |
| ...                       |
+---------------------------+
```

