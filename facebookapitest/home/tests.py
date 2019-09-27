from django.test import TestCase

# Create your tests here.
import sys
sys.path.append('/home/bluetechup/virtual-env/env-facebook-api/lib/python3.5/site-packages') # Replace this with the place you installed facebookads using pip
sys.path.append('/home/bluetechup/virtual-env/env-facebook-api/lib/python3.5/site-packages/facebook_business-3.0.0-py2.7.egg-info') # same as above

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

my_app_id = 'your-app-id'
my_app_secret = 'your-appsecret'
my_access_token = 'your-page-access-token'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount('act_<your-adaccount-id>')
campaigns = my_account.get_campaigns()
print(campaigns)