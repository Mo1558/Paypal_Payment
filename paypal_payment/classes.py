from decouple import config
import requests

class Login:
    def __init__(self):
        
        self.base_url=config("base_url")                    # from .env file
        self.client_id=config("client_id")                  # from .env file
        self.secret=config("secret")                        # from .env file
        self.token_url=config("token_url")                  # from .env file
        self.auth_url=self.base_url+self.token_url   
        self.auth=(self.client_id,self.secret)               #from paypal website in app section 
        self.params ={'grant_type': 'client_credentials'}    #from paypal website in order section

    def auth_connection(self):
        '''
        for create token from paypal
        '''
        self.data = requests.post(self.auth_url, 
        params=self.params,headers=self.headers,auth=self.auth)
        return self.data

    def create_auht(self):
        '''
        This method for create token forom paypal account by using 
        url that doing this thing and provide things that require
        like (client_id , client_secrt) from paypal app
        and  headers , params and auth 
        '''
        self.headers ={'Content-Type': 
         'application/x-www-form-urlencoded'} 
        try:                                               #from paypal website in order section
            token=self.auth_connection()
        except:
            return "Connection refused"
        if token.status_code==200: 
            self.result = token.json()                     #check if the response is successful
            return (self.result['access_token']) 
            
        else :
            self.result= token.json()
            return self.result['error']

# print(Login().create_auht())

class Order:
    def __init__(self):
        self.base_url=config("base_url")                      # from .env file  
        self.order_url=config("order_url")                    # from .env file
        self.token=Login().create_auht()                      #from Login Class
        self.create_url=self.base_url+self.order_url          #base url + order_url tom create order
        self.headers={'Authorization': f'Bearer {self.token}'}#from paypal website in order section
    

    def create_order(self,price,currency_code):
        '''
        This method for creating a new order in paypal.
        by using token that has been created previously.
        we use some things required like url from paypal 
        to create order , headers and data and return the 
        link to approve order then check fro response
        and validate data
        '''
        self.price=price                                      #price of order 
        self.currency_code=currency_code                      #currency code of order
        self.json_data={                                      #data for order
            "intent": "CAPTURE",                              #to make capture request not authrize
            "purchase_units":[ {
                "amount": 
                    {
                      "currency_code":f"{self.currency_code}",
                      "value": f"{self.price}"
                    }
                    } ] }

        try:
            post_data =Connection().create_connection(self.json_data,self.create_url,self.headers)
        except :
            return "Connection of create order failed"

        if post_data.status_code == 201:                         #check if the response is successful
            self.result=post_data.json()
            return self.result['links'][1]['href']

        elif post_data.status_code == 401:                      #check if the token is valid
            return "invalid_client"

        else:
            self.result= post_data.json()
            return f'''The error is  {self.result['details'][0]['issue']}
            and the description is {self.result['details'][0]['description']}'''

            

    def get_order(self,id):
        '''
        This method returns the order data with 
        the given id. by using url from paypal and give 
        it the id of the order and headers and check for 
        response and validate data
        '''
        self.get_url=f"{self.base_url}{self.order_url}{id}"          #url for get order data 
        try:
            get_data=Connection().get_connection(self.get_url,self.headers)
        except :
            return "Connection of get order Failed"

        if get_data.status_code == 200:                            #check if the response is successfully
            self.result= get_data.json()
            return self.result

        else:
            self.result= get_data.json()
            return f'''The error is  {self.result['details'][0]['issue']}
            and the description is {self.result['details'][0]['description']}'''
    
    
    
    def capture_order(self,id):
        '''
        This method for capturing and complete the order 
        by using url from paypal and given id of order 
        that i want to capture and headers
        check fro response and validate data
        '''
        self.capture_url=f"{self.base_url}{self.order_url}{id}/capture"     #url for capture_order
        self.headers={'Authorization':f'Bearer {self.token}',               #headers needed for capture
        'Content-Type':'application/json','resource_id': 'default'}
        try:
            post_data = Connection().capture_connection(self.capture_url,self.headers)
        except:
            return "Connection of capture failed"

        if post_data.status_code == 201:                                #check if the response is successfully
            self.result=post_data.json()
            if self.result['status']=='COMPLETED':
                return "DONE"

        else:
            self.result=post_data.json()
            return f'''The error is  {self.result['details'][0]['issue']} 
            and the description is {self.result['details'][0]['description']}'''

class Connection(Order):

    def create_connection(self,json_data,url,headers=''):
        '''
        create order from paypal
        '''
        self.json_data = json_data
        self.create_url = url
        self.headers = headers
        self.post_data =requests.post(self.create_url,
        headers=self.headers,json=self.json_data)
        return self.post_data

    def get_connection(self,get_url,headers):
        '''
        get order from paypal
        '''
        self.get_url=get_url
        self.headers=headers
        self.get_data=requests.get(self.get_url,headers=self.headers)
        return self.get_data

    def capture_connection(self,capture_url,headers):
        '''
        capture order from paypal
        '''
        self.capture_url=capture_url
        self.headers=headers
        self.post_data = requests.post(self.capture_url,headers=self.headers)
        return self.post_data



# print(Order().create_order(price=10,currency_code='USD'))
# print(Order().get_order('2CH92983FA7621355'))
print(Order().capture_order('2CH92983FA7621355'))
