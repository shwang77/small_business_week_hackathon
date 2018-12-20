from __future__ import print_function

import sys, os
import base64
import msgpack
import json
import boto3

print('Loading function')

client = boto3.client('comprehend')



def lambda_handler(event, context):
 output = []

 for record in event['records']:
   
   print("**************************ENCODING DATA IS: " + record['data'])   
   
   data = base64.b64decode(record['data']).decode("utf-8")
   # print("DATA IS: " + data)
   jsonObj = json.loads(data)
   
   sentiment=client.detect_sentiment(Text=jsonObj['utterance'],LanguageCode='en')['Sentiment']
   
   
   print("utterance: " + jsonObj['utterance'])
   print("sentiment: " + sentiment)
   
   jsonObj["sentiment"] = sentiment
   
   print( "************************** JSON Payload" + json.dumps(jsonObj, indent=4, sort_keys=True) + "**************************")
 
   encodedPayload = base64.b64encode( str(jsonObj).encode("utf-8") + b'\n' ).decode("utf-8")
   # encodedPayload = base64.b64encode( str(jsonObj).encode("utf-8") ).decode("base64")
   
   # print("^^^^^^^^^^^^^^^^^^^^^ Encoding Record: " + str(encodedPayload) + "^^^^^^^^^^^^^^^^^^^^^^^^^^^")
   
   # record["data"] = str(encodedPayload)
   # record["data"] = encodedPayload
   record["result"] = "Ok"
   
   # print("^^^^^^^^^^^^^^^^^^^^^ Record: " + json.dumps(str(record), indent=4, sort_keys=True) + "^^^^^^^^^^^^^^^^^^^^^^^^^^^")
   
   output.append(record)
   # print("$$$$$$ Added record to output collection $$$$$")
      

 # Do custom processing on the payload here
 #   output_record = {
 #     'recordId': record['recordId'],
 #     'result': 'Ok',
 #     'data': base64.b64encode(json.dumps(payload).encode('utf-8') + b'\n').decode('utf-8')
 #   }
 #   output.append(output_record)

 # print('Successfully processed {} records.'.format(len(event['records'])))

 event['records'] = output
 
 # Call to AWS Comprehend 
 # print("^^^^^^^^^^^^^^^^^^^^^ event: " + json.dumps(str(event), indent=4, sort_keys=True) + "^^^^^^^^^^^^^^^^^^^^^^^^^^^")
 
 
 return event
