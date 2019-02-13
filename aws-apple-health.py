#! /usr/local/bin/python3

import argparse
import boto3
import xml.etree.ElementTree as ET
import os
from zipfile import ZipFile

parser = argparse.ArgumentParser(description="Example: python aws-apple-health.py -i <file>.zip -o <file>.xml -b <s3-bucket>")
parser.add_argument('-i', '--input', help='Input zip file name', required=True)
parser.add_argument('-o', '--output', help='Output xml file name', required=True)
parser.add_argument('-b', '--bucket', help='AWS s3 bucket name', required=False)
args = parser.parse_args()
#print (args.input)
#print (args.output)
#print (args.bucket)

#Open zip file and extract the export.xml file
with ZipFile(args.input, 'r') as zip:
    #Print contents of the zip file
    #zip.printdir()

    #Extract export.xml
    zip.extract('apple_health_export/export.xml')

#Move the export.xml file and remove dir
os.rename('apple_health_export/export.xml', 'export.xml')
os.rmdir('apple_health_export/')

#Read the export.xml file using ElementTree
tree = ET.parse('export.xml')
root = tree.getroot()

#Create new xml file
file = open(args.output, 'w')

#Store formatted text and write subset of data to new xml file
xmlDoc = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE HealthData [
<!-- HealthKit Export Version -->
<!ELEMENT Workout ((MetadataEntry|WorkoutEvent|WorkoutRoute)*)>
<!ATTLIST Workout
  workoutActivityType   CDATA #REQUIRED
  duration              CDATA #IMPLIED
  durationUnit          CDATA #IMPLIED
  totalDistance         CDATA #IMPLIED
  totalDistanceUnit     CDATA #IMPLIED
  totalEnergyBurned     CDATA #IMPLIED
  totalEnergyBurnedUnit CDATA #IMPLIED
  sourceName            CDATA #REQUIRED
  sourceVersion         CDATA #IMPLIED
  device                CDATA #IMPLIED
  creationDate          CDATA #IMPLIED
  startDate             CDATA #REQUIRED
  endDate               CDATA #REQUIRED
>
]>"""

#print (xmlDoc)
file.write (xmlDoc + "\n")

for Workout in root.iter('Workout'):
    xmlData = str(Workout.attrib)
    #print (xmlData)
    file.write (xmlData + "\n")

file.close()

#Create an S3 client
s3 = boto3.client('s3',
    #Not recommended, use environment variables!
    #aws_access_key_id='XYZ',
    #aws_secret_access_key='XYZ'
)

#Upload output xml file to s3 bucket
s3.upload_file(args.output, args.bucket, args.output)
