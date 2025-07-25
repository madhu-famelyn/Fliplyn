import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Add your project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'admin')))  # <- Update 'admin' if needed

# ✅ Load .env variables
from dotenv import load_dotenv
load_dotenv()

# Alembic Config object
config = context.config

# ✅ Set DB URL from .env
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Import Base AFTER sys.path is set
from models.base import Base

# ✅ Set metadata for autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
