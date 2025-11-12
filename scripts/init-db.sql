-- Initialize databases for each service
CREATE DATABASE IF NOT EXISTS user_service_db;
CREATE DATABASE IF NOT EXISTS email_service_db;
CREATE DATABASE IF NOT EXISTS push_service_db;
CREATE DATABASE IF NOT EXISTS template_service_db;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE user_service_db TO notification_user;
GRANT ALL PRIVILEGES ON DATABASE email_service_db TO notification_user;
GRANT ALL PRIVILEGES ON DATABASE push_service_db TO notification_user;
GRANT ALL PRIVILEGES ON DATABASE template_service_db TO notification_user;
