if [ -z "$(docker images -f 'reference=org-api-app' -q)" ]; then
  chmod +x ./build.sh
  ./build.sh
fi
docker compose -p org-api-app up -d