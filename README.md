# aws-apple-health
This python script processes the export.zip file from the Apple Health app, extracting the export.xml file and selecting the Workout element line items and generats a new xml file containing the subset of data.  The bucket argument enables optional upload of the output file to AWS s3. 

## Export Apple Health Data
1. Navigate to the Apple Health app on your iPhone
2. Select your profile in the upper right corner
3. Select 'Export Health Data' from the bottom, and when prompted select Export
4. This will generate a export.zip archive file
4. When prompted AirDrop to a local host or upload to another location

The file generated will be a zip archive. Within the zip archive is an export.xml file with several hundred thousand... or more rows of data.  The script will take care of unzipping the file, extracting the export.xml file and parsing for the workout summary data.  A new much smaller xml file is generated using the summary data and can be easily uploaded to s3 for further analysis.

Enjoy!
