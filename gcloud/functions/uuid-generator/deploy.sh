FUNCTION_NAME="uuid-generator"
ENTRYPOINT="generate_uuid"
RUNTIME="python39"

cp -rf ../../../prophesygg/ prophesygg/
cp -rf ../../../requirements.txt .
gcloud functions deploy $FUNCTION_NAME --region us-east1 --memory 128M --entry-point $ENTRYPOINT --runtime $RUNTIME --timeout 10 --trigger-http --min-instances 1

rm -rf prophesygg
rm requirements.txt
rm .gcloudignore
rm .gitignore
rm -rf .git