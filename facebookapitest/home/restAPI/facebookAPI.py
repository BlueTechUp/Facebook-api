import json
import sys

sys.path.append(
    '/home/bluetechup/virtual-env/env-facebook-api/lib/python3.5/site-packages')  # Replace this with the place you installed facebookads using pip
sys.path.append(
    '/home/bluetechup/virtual-env/env-facebook-api/lib/python3.5/site-packages/facebook_business-3.0.0-py2.7.egg-info')  # same as above

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adaccountuser import AdAccountUser
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative

import logging

log = logging.getLogger('app')

fields = [
    Ad.Field.name, Ad.Field.ad_review_feedback, Ad.Field.effective_status, Ad.Field.status
]
params = {
    Ad.Field.effective_status:
        [Ad.EffectiveStatus.disapproved]
}

disable_reason = [
    'NONE',
    'ADS_INTEGRITY_POLICY',
    'ADS_IP_REVIEW',
    'RISK_PAYMENT',
    'GRAY_ACCOUNT_SHUT_DOWN',
    'ADS_AFC_REVIEW',
    'BUSINESS_INTEGRITY_RAR',
    'PERMANENT_CLOSE',
    'UNUSED_RESELLER_ACCOUNT',
    'UNUSED_ACCOUNT'
]
relevance_score = ['Unknown']


def account_field_format(account_name, disablereason):
    ret = account_name + "<br><span style=\"color: red;\">" + disablereason + "</span>"
    return ret


def image_field_format(img_url):
    ret = "<img src=" + img_url + ">"
    return ret


def check_ad(token):
    FacebookAdsApi.init(access_token=token)

    me = AdAccountUser(fbid='me')
    ad_account_list = list(me.get_ad_accounts(fields={'name', 'disable_reason', 'asset_score'}))
    check_result = []
    for ad_account in ad_account_list:
        try:
            ad_account_dict = json.loads(str(ad_account).replace("<AdAccount> ", "", len('<AdAccount> ')))
            account = AdAccount(ad_account_dict['id'])
            ad_list = account.get_ads(fields=fields, params=params)

            if len(ad_list) > 0:
                tmp_ad = []
                ad_creative_url = account.get_ad_creatives(fields=['thumbnail_url'], params=params)
                tmp_ad_creative_url_dict = json.loads(
                    str(ad_creative_url[1]).replace("<AdCreative> ", "", len('<AdCreative> ')))
                for ad in ad_list:
                    try:
                        tmp_ad.clear()
                        ad_dict = json.loads(str(ad).replace("<Ad> ", "", len("<Ad> ")))

                        tmp_ad.append(account_field_format(ad_account_dict['name'],
                                                           disable_reason[ad_account_dict['disable_reason']]))
                        tmp_ad.append("<img src=" + tmp_ad_creative_url_dict['thumbnail_url'] + ">")
                        tmp_ad.append(ad_dict['name'])
                        tmp_ad.append(relevance_score[ad_account_dict['asset_score']])
                        tmp_ad.append(ad_dict['status'])

                        err_housing = ""
                        if "HOUSING_OR_CREDIT" in ad_dict['ad_review_feedback']['global']:
                            err_housing = "<span style=\"color: red;\"> HOUSING_OR_CREDIT </span><br>" + \
                                          ad_dict['ad_review_feedback']['global']['HOUSING_OR_CREDIT'] + "<br>"

                        err_cloaking = ""
                        if "CLOAKING" in ad_dict['ad_review_feedback']['global']:
                            err_cloaking = "<br><span style=\"color: red;\"> CLOAKING </span><br>" + \
                                           ad_dict['ad_review_feedback']['global']['CLOAKING'] + "<br>"

                        tmp_ad.append(err_housing + err_cloaking)

                        check_result.append(tmp_ad)
                    except Exception as e:
                        log.error("error ads %s", e)
        except Exception as e:
            log.error("error ad account %s", e)

    return check_result
