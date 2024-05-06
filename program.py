import requests
import json
import datetime
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from Config import SENDER_EMAIL, EMAIL_PASSWORD, PATH_FOR_TABLE

logging.basicConfig(filename = 'test_log.log', level = logging.DEBUG,
                    format = '%(asctime)s %(levelname)s %(funcName)s || %(message)s')

def get_week(day=None):
    if day == None:
        start_day = datetime.date.today()
    else:
        start_day = datetime.datetime.strptime(day, '%d.%m.%Y')
    
    back_date = start_day - datetime.timedelta(weeks=4)

    date_range = f'{back_date.strftime('%d.%m.%Y')}-{start_day.strftime('%d.%m.%Y')}'

    return date_range

def get_contracts(**kwargs):
    url = f'http://openapi.clearspending.ru/restapi/v3/contracts/search/'
    parameters = {**kwargs}
    logging.info('Log starts execution of function get_contracts' + url, parameters)
    try:
        req = requests.get(url, parameters)
        logging.info(req)
    except Exception as e:
        logging.error('Link error')
        logging.exception(e)
    try:
        data = req.json()
        logging.info(data)
        return data
    except Exception as e:
        logging.error('JSONformat conversion error')
        logging.exception(e)

def recurs_find_data(key, object):
    if object == None:
        return None
    else:
        if key in object:
            return object[key]
        if type(object) == dict:
            for k, v in object.items():
                if type(v) == dict:
                    result = recurs_find_data(key, v)
                    return result
                elif type(v) == list:
                    for el in range(len(v)):
                        result = recurs_find_data(key, v[el-1])
                        return result
        elif type(object) == list:
            for el in range(len(object)):
                        result = recurs_find_data(key, object[el-1])
                        return result
            
def get_top_contracts(json_data):
    
    data = json_data['contracts']['data']

    top_contracts = []

    for contract in data:
        contract_dict={}
        contract_url = recurs_find_data('contractUrl', contract)
        contract_dict['contract_url'] = contract_url

        sign_date = recurs_find_data('signDate', contract)
        contract_dict['sign_date'] = sign_date

        num_reg = recurs_find_data('regNum', contract)
        contract_dict['num_reg'] = num_reg

        price = recurs_find_data('price', contract)
        contract_dict['price'] = price

        customer = recurs_find_data('customer', contract)
        customer_inn = recurs_find_data('inn', customer)
        contract_dict['customer_inn'] = customer_inn

        customer_name = recurs_find_data('fullName', customer)
        contract_dict['customer_name'] = customer_name

        suppliers = recurs_find_data('suppliers', contract)
        suppliers_dict = {}

        if suppliers != None:
            for supplier in suppliers:
                supplier_inn = recurs_find_data('inn', supplier)
                supplier_name = recurs_find_data('organisationName', supplier)
                suppliers_dict[supplier_inn] = supplier_name
                suppliers_data = '\n'.join([f'{v} INN {k}' for k, v in suppliers_dict.items()])
        else:
            suppliers_data = 'No data'
        
        contract_dict['suppliers_data'] = suppliers_data


        products = recurs_find_data('products', contract)

        subjects = '; '.join([recurs_find_data('name', product) for product in products])
        contract_dict['subjects'] = subjects
        
        top_contracts.append(contract_dict)
        return top_contracts[:5]

def create_message(top_contracts):
    
    env = Environment(
        loader = FileSystemLoader('Template'), 
        autoescape = select_autoescape(['html', 'xml'])
    )

    template = env.get_template('table.html')
    message = template.render(items=top_contracts)
    with open(PATH_FOR_TABLE, 'w', encoding='UTF-8') as a:
        a.write(message)
    return message

result = get_contracts(daterange = get_week('01.05.2023'), customerregion = 39, sort = '-price')

try:
    if result == '':
        print('Empty string')
    else:
        with open('result.json', 'w') as json_file:
            json.dump(result, json_file)
        logging.info('result_json' + 'saved')
except Exception as e:
    logging.error('result_json' + 'is failed to saved')
    logging.exception(e)

message = create_message(get_top_contracts(result))

email_list = ['0107lenam@gmail.com']

def send_mail_contracts(message, email_list):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Top-5 largest government contracts in the Kaliningrad region'
    msg['From'] = SENDER_EMAIL
    msg['To'] = ', '.join(email_list)
    message_text = MIMEText(message, 'html')
    msg.attach(message_text)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)
    
send_mail_contracts(message, email_list)
