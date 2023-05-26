import json
import os

# The variables are defined in /.env, and Docker inserts
# those values into the fastapi container. We use the os
# module to retrieve the values
dot_env = {
    **os.environ,
}

data = {
    "admin_email": dot_env["ADMIN_EMAIL"],
    "admin_password": dot_env["ADMIN_PASSWORD"],
    "celery_broker_url": dot_env["CELERY_BROKER_URL"],
    "cors": json.loads(dot_env["BACKEND_CORS_ORIGINS"]),
    "db_host": dot_env["POSTGRES_SERVER"],
    "db_name": dot_env["POSTGRES_DB"],
    "db_password": dot_env["POSTGRES_PASSWORD"],
    "db_port": dot_env["POSTGRES_PORT"],
    "db_user": dot_env["POSTGRES_USER"],
    "default_email": dot_env["EMAILS_FROM_EMAIL"],
    "default_reply_to": dot_env["EMAILS_REPLY_TO"],
    "default_test_user": dot_env["EMAIL_TEST_USER"],
    "dev_email": dot_env["DEV_EMAIL"],
    "dev_email_enabled": dot_env["SEND_DEV_EMAILS"] == "True",
    "domain": dot_env["DOMAIN"],
    "env": dot_env["ENVIRONMENT"],
    "jwt_secret": dot_env["JWT_SECRET"],
    "hash_value": dot_env["HASH_VALUE"],
    "maintenance_mode": dot_env["MAINTENANCE_MODE"] == "True",
    "postgres_url": f"postgresql+psycopg2://{dot_env['POSTGRES_USER']}:{dot_env['POSTGRES_PASSWORD']}@{dot_env['POSTGRES_SERVER']}:{dot_env['POSTGRES_PORT']}/{dot_env['POSTGRES_DB']}",
    "postgres_test_url": f"postgresql+psycopg2://{dot_env['POSTGRES_USER']}:{dot_env['POSTGRES_PASSWORD']}@{dot_env['POSTGRES_SERVER']}:{dot_env['POSTGRES_PORT']}/test",
    "rabbit_mq_password": dot_env["RABBITMQ_DEFAULT_PASS"],
    "rabbit_mq_user": dot_env["RABBITMQ_DEFAULT_USER"],
    "sendgrid_api_key": dot_env["SENDGRID_API_KEY"],
    "stripe_publishable_key": dot_env["STRIPE_PUBLISHABLE_KEY"],
    "stripe_secret_key": dot_env["STRIPE_SECRET_KEY"],
    "stripe_webhook_secret": dot_env["STRIPE_WEBHOOK_SECRET"],
    "support_email": dot_env["SUPPORT_EMAIL"],
}
