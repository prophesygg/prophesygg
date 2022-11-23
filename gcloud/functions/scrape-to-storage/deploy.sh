FUNCTION_NAME="scrape-to-storage"
ENTRYPOINT="scrape_to_storage"
RUNTIME="python39"

cp -rf ../../../prophesygg/ prophesygg/
cp -rf ../../../requirements.txt .
gcloud functions deploy $FUNCTION_NAME --region us-east1 --memory 256M --entry-point $ENTRYPOINT --runtime $RUNTIME --timeout 540 --trigger-http

rm -rf prophesygg
rm requirements.txt
rm -rf .git