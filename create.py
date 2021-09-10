import reader, os, random, uuid
import argparse
import glob
from typing import Set
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator
from eventstreams_sdk.adminrest_v1 import *
import ast
from http import HTTPStatus

SERVICE_NAME = 'adminrest_v1'
KAFKA_ADMIN_URL = os.getenv('KAFKA_ADMIN_URL')
BEARER_TOKEN= os.getenv('BEARER_TOKEN')
API_KEY= os.getenv('API_KEY')

# End Code Setup

# Create Authenticator
if not KAFKA_ADMIN_URL:
    print("Please set env KAFKA_ADMIN_URL")
    exit(1)

if not API_KEY and not BEARER_TOKEN:
    print("Please set either an API_KEY or a BEARER_TOKEN")
    exit(1)

if API_KEY and BEARER_TOKEN:
    print("Please set either an API_KEY or a BEARER_TOKEN not both")
    exit(1)

if API_KEY:
    # Create an Basic IAM authenticator.
    authenticator = BasicAuthenticator('token', API_KEY)
else :
    # Create an IAM Bearer Token authenticator.
    authenticator = BasicAuthenticator('token', BEARER_TOKEN)

service = AdminrestV1(
    authenticator = authenticator
    )
# End Authenticator

# Create Service
base_url = KAFKA_ADMIN_URL
service.set_service_url(base_url)
# End Create Service

def create_topic(service,topic_name,config):
    # Set up parameter values
    partition_count = 1
    configs = []

    # Invoke create method.
    try:
        response = service.create_topic(
            name=topic_name,
            partition_count=partition_count,
            configs=configs,
        )
        if response.status_code == HTTPStatus.ACCEPTED :  
            print("\ttopic created: " + topic_name)
    except:
        print("\tError Creating Topic: " + topic_name)
    # func.End

def create_config(args):
  """
  bankid, allFctId = [], admin=True, provision=True, audit=True 
  """
  #print('------')
  #print(args[])
  retention = args['retention'] * 86400000
  topic_config = f'''
  "cleanup.policy": {args['cleanup_policy']}, "min.insync.replicas": 2, "retention.ms": {retention}, "segment.bytes": 536870912, "compression.type: {args["compression_type"]}'''
  #topic_new_config = ast.literal_eval(topic_config)
  return topic_config

def getcrqlist(filelist):
    ids = []
   # print(filelist)
    for file in filelist:
        print("Processing " + file)
        ymldata = reader.YamlReader(file).data
        ids.append([{ 'owner_name': ymldata['name'], 'CRQ': ymldata['CRQ'], 'userdata': ymldata['users'], 'topicdata' : ymldata['topics'] }])
    return ids

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="IBM Eventstream topic creator tool")

    parser.add_argument("-d", "--directory", dest="directory", required=True, help='yml directory')
    parser.add_argument("-t", "--token", dest="token", required=False, help='vault token for provisioner')
    parser.add_argument("-u", "--url", dest="url", required=False, help='vault_url')
    parser.add_argument("-v", "--verbose", dest="verbose", required=False, help="verbose output if set to True")
    parser.add_argument("-e", "--env", dest="environment", required=True, help='environment: dev, uat or prod')
    parser.add_argument("-f", "--fixed", dest="fixed_policies_glob", required=False, help='Fixed policies files glob')

    args = parser.parse_args()
    """client = hvac.Client(url=args.url, token=args.token, verify=False)

    if 'fixed_policies_glob' in args and args.fixed_policies_glob:
        upload_fixed_policies(client, args.fixed_policies_glob)
    """
    ymlfilelist = glob.glob(args.directory + os.sep + "**" + "*.yaml")
    """
    env_code = {
        'dev': 'b',
        'sit': 'b',
        'uat': 's',
        'prod': 'g'
    }[args.environment]
    """
    crqlist = getcrqlist(ymlfilelist)
    for crq in crqlist:
        for dic in crq:
             for topic in (dic['topicdata']):
                topic_name = topic['name']
                #topic_config = create_config(topic)
                topic.pop('name')
                topic_config = topic
                print(topic_name)
                print(topic_config)
                #create_topic(service, topic_name, topic_config)
             


                
       #for each in crq['userdata']:
        #       print(each['user_name'])

       # config = create_config(topic)
       # print(config)

"""
    for eachidlist in identities:
        for userdatalist in eachidlist:
            for each in userdatalist['userdata']:
                # bankids_lvl = f1bankids_{args.environment}
                if bankids_lvl in each:
                    for eachid in each[bankids_lvl]:
                        # Replace the env_code
                        fctid = each['name'].format(env_code=env_code)
                        if eachid in ids.keys():
                            ids[eachid].append(fctid)
                        else:
                            ids.update({eachid: [fctid]})

    #print(f"===={ids}====")
    createusers(ids, client)
"""
