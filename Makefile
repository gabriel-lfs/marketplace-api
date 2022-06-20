upload_products:
	aws s3api put-object --bucket updated-products --key products.json --body products.json --endpoint-url="http://localhost:4566"

run:
	uvicorn marketplace.main:app --env-file .env