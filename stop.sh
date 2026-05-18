if [ -e "app_config/.test" ]; then
  docker compose -p org-api-app down -v
  rm -r app_config
else
  docker compose -p org-api-app down
fi