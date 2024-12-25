import urllib.parse
import hashlib
from datetime import datetime
from django.conf import settings

class ECPayPayment:
    def __init__(self):
        self.merchant_id = settings.ECPAY_MERCHANT_ID
        self.hash_key = settings.ECPAY_HASH_KEY
        self.hash_iv = settings.ECPAY_HASH_IV
        self.payment_url = settings.ECPAY_PAYMENT_URL

    def create_order(self, order_id, amount, description):
        order_params = {
            'MerchantID': self.merchant_id,
            'MerchantTradeNo': order_id,
            'MerchantTradeDate': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'PaymentType': 'aio',
            'TotalAmount': str(amount),
            'TradeDesc': urllib.parse.quote(description),
            'ItemName': description,
            'ReturnURL': 'https://df2b-61-220-182-115.ngrok-free.app/notify/',
            'ClientBackURL': 'https://df2b-61-220-182-115.ngrok-free.app/payments/complete/',
            'ChoosePayment': 'ALL',
            'EncryptType': '1',
        }
        
        check_mac = self._generate_check_mac(order_params)
        order_params['CheckMacValue'] = check_mac
        
        return order_params
    
    def _generate_check_mac(self, params):
        sorted_params = sorted(params.items())
        
        param_str = f"HashKey={self.hash_key}"
        for key, value in sorted_params:
            param_str += f"&{key}={value}"
        param_str += f"&HashIV={self.hash_iv}"
        
        encoded_str = urllib.parse.quote_plus(param_str).lower()
        
        check_mac = hashlib.sha256(encoded_str.encode('utf-8')).hexdigest().upper()
        
        return check_mac