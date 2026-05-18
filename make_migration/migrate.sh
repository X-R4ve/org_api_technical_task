docker compose up -d
sleep 7
cd ..
$(poetry env info --path)/bin/python -m alembic revision --autogenerate
cd make_migration
docker compose down
