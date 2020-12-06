# python-product-importer

Imports products data into AWS Cloudsearch provided in a xml file.

# Todo

* make configuration external
* add unit tests
* convert current code to lambda
* add appropriate code either SAM or Cloudformation
* add local testing (integration tests) with localstack
* add upload mechanism to S3 bucket
  1. extra Lambda that fetches XML data from Opacc and uploads to S3 bucket (add current date and time to file name)
  2. on upload event a second lambda imports data into cloudsearch
* add documentation
