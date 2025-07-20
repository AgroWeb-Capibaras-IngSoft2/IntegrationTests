import requests
import json
import logging
from typing import Dict,Any,Optional,List
from datetime import datetime

PORT=5003

logger=logging.getLogger()
class CarritoApiClient: #Cliente http para interctuar con el API de Carrito
    def __init__(self,session:requests.Session,base_url:str=f"http://localhost:{PORT}"):
        self.session=session
        self.base_url=base_url.rstrip('/')
        self.headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'AgroWeb-CarritoIntegrationTest/1.0'
        }
    
    def _make_request(self,method:str,endpoint:str,**kwargs)->requests.Response:
        url=f"{self.base_url}{endpoint}"
        if 'headers' not in kwargs:
            kwargs['headers']=self.headers.copy()
        else:
            merged_headers=self.headers.copy()
            merged_headers.update(kwargs['headers'])
            kwargs['headers']=merged_headers
        
        logger.info(f"{method.upper()}{url}")
        if 'json' in kwargs:
            logger.debug(f"Request body:{json.dumps(kwargs['json'],indent=2)}")

        try:
            response=self.session.request(method,url,**kwargs)
            logger.info(f"Response: {response.status_code}({len(response.content)} bytes )")

            if len(response.content)<1000:
                try:
                    response_data=response.json()
                    logger.debug(f"Response body: {json.dumps(response_data,indent=2)}")
                except:
                    logger.debug(f"Response body: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    #Escribimos los endpoints principales de nuestra API de carrito

    #Endpoint de crear carrito POST "/carrito/create"
    def create_carrito(self,user_info:dict)->requests.Response:
        return self._make_request("POST",'/carrito/create',json=user_info)


    #Endpoint de añadir producto
    def add_product(self,prod_info:dict)->requests.Response:
        """prod_info:{
                    id_carrito,
                    product_id,
                    cantidad}"""
        return self._make_request("POST","/carrito/addProduct",json=prod_info)


    #Endpoint de cambiar cantidad
    def change_quantity(self,prod_info:dict)->requests.Response:
        """prod_info:{
                    id_carrito,
                    product_id,
                    cantidad
                    }
        """
        return self._make_request("PUT","/carrito/changeQuantity",json=prod_info)

    #Endpoint de elimnar producto
    def delete_product(self,delete_info:dict)->requests.Response:
        """delete_info:{
                        carrito_id,
                        product_id
        }"""
        return self._make_request("DELETE","/carrito/deleteProduct",json=delete_info)

    #Endpoint de vaciar carrito
    def vaciar_carrito(self,carrito_info:dict)->requests.Response:
        """
            carrito_info:{
                        id_carrito
            }
        """
        return self._make_request("DELETE","/carrito/vaciar",json=carrito_info)

    #Endpoint de obtener carrito
    def get_carrito(self,id_carrito:str)->requests.Response:
        return self._make_request("GET",f"/carrito/getCarrito/{id_carrito}")



