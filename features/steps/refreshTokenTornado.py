# import tornado.web
# from cryptography.fernet import Fernet
# import base64
# import calendar
# import json
# from cgitb import handler
# from datetime import datetime
# from os import urandom
# import requests
# import tornado.web
# from cryptography.fernet import Fernet
#
#
# def username_get_secure_cookies(self):
#     """
#     Returns the given signed cookie if it validates, or None
#     Returns
#     -------
#     byte string
#         decoded cookie value
#     """
#     print("dhsaggdsahg", self.get_secure_cookie('username'))
#     return self.get_secure_cookie('username')
#
#
# def refresh_token_get_secure_cookies(self):
#     """
#     Get the refresh token secure cookies
#     Returns
#     -------
#     byte string
#         The decoded cookie value is returned
#     """
#     return self.get_secure_cookie('refresh_token')
#
#
# def set_refresh_cookies(self, token, expire_in, key):
#     """
#     Set Refresh token in cookie.
#     Parameters
#     ----------
#     self : object
#         handler instance
#     token : str
#         refresh token
#     expire_in : int
#         expire time
#     key : str
#         secret key
#     Returns:
#         None
#     """
#     self.set_secure_cookie("refresh_token", Fernet(str.encode(key)).encrypt(str.encode(str(token))).decode(),
#                            expires=calendar.timegm(
#                                (datetime.datetime.utcnow() + datetime.timedelta(seconds=expire_in)).timetuple()))
#
#
# def cookies_handler_using_access_token(self, code, refresh_access_token, expire_in, refresh_expire_in, key, resource):
#     """
#     Set the cookies access token after login.
#     Parameters
#     ---------
#     code: str
#         decoded access token
#     refresh_access_token: str
#         decoded refresh access token
#     expire_in: str
#         decoded access token expiring time
#     refresh_expire_in: str
#         decoded refresh access token expiring time
#     key: str
#         secret key for encoding and decoding the cookies data
#     resource: str
#         keyclock client id
#     Returns
#     -------
#     str
#         Only set the cookies for user and refresh_token.
#     """
#     try:
#         timeduration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expire_in)  # expire_in
#         cookies_expire = calendar.timegm(timeduration.timetuple())
#         cookies_setup = json.dumps({'code': code, 'time_set': str(cookies_expire)})
#         self.set_secure_cookie("username", Fernet(str.encode(key)).encrypt(str.encode(str(cookies_setup))).decode(),
#                                expires=cookies_expire)
#         set_refresh_cookies(self, refresh_access_token, refresh_expire_in, key)
#     except Exception as e:
#         self.logger.info(str(e))
#
#
# def refresh_token_cookies_upgrade(self, refresh_token, keycloak_logout_flage=False):
#         """
#         Getting the keycloak cookie details.
#         Parameters
#         ----------
#         refresh_token : str
#             refresh token for keycloak url
#         keycloak_logout_flage : bool
#             keycloak flag set as False default.
#         Returns
#         -------
#         bool
#             True if success, else False
#         json object
#             Returns cookie setup json details
#         """
#         try:
#             access_token_resp = requests.post(self.key_cloak_url, data={'client_id': self.key_client_id,
#                                                                         'client_secret': self.key_client_secret,
#                                                                         'grant_type': 'refresh_token',
#                                                                         'refresh_token': refresh_token},
#                                               verify=False,
#                                               timeout=30)
#             if access_token_resp.json()['access_token']:
#                 access_token = access_token_resp.json()['access_token']
#                 headers = {'Authorization': 'Bearer ' + access_token,
#                            'refresh_access_token': access_token_resp.json()['refresh_token'],
#                            'expires_in': access_token_resp.json()['expires_in'],
#                            'refresh_expires_in': access_token_resp.json()['refresh_expires_in']}
#                 access_token = headers.get("Authorization")
#                 refresh_access_token = headers.get("refresh_access_token")
#                 self.logger.info(str(self.key_cloak_url + " \n method: GET"))
#                 cookies_handler_using_access_token(self, access_token, refresh_access_token, headers.get("expires_in"),
#                                                    headers.get("refresh_expires_in"), self.secret_key,
#                                                    self.key_client_id)
#                 timeduration = datetime.datetime.utcnow() + datetime.timedelta(
#                     seconds=headers.get("expires_in"))  # expire_in
#                 cookies_expire = calendar.timegm(timeduration.timetuple())
#                 cookies_setup = json.dumps({'code': access_token, 'time_set': str(cookies_expire)})
#                 return True, cookies_setup
#             else:
#                 self.clear_cookie("username")
#                 self.clear_cookie("refresh_token")
#                 self.clear_all_cookies()
#                 return False
#         except Exception as e:
#             self.clear_cookie("username")
#             self.clear_cookie("refresh_token")
#             self.clear_all_cookies()
#             self.logger.info(str('Failed to refresh access token, Please try again!'))
#             self.logger.info(str(e))
#             return False
#
#
# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#             """
#             Retrieve username cookie from storage if not available then
#             user refresh_token from cookie and fetch updated access token and
#             update username cookie
#             Returns
#             -------
#             str
#                 username cookie
#             """
#             username = username_get_secure_cookies(self)
#             if username is None:
#                 # call refresh cookies based on refresh token
#                 if refresh_token_get_secure_cookies(self) is not None:
#                     refresh_flage, username = refresh_token_cookies_upgrade(self,
#                                                                             Fernet(str.encode(self.secret_key)).decrypt(
#                                                                                 self.refresh_token_get_secure_cookies()).decode())
#                     if refresh_flage:
#                         return username if username else None
#                     else:
#                         return None
#             else:
#                 refresh_flage, username = refresh_token_cookies_upgrade(self, Fernet(str.encode(self.secret_key)).decrypt(
#                     self.refresh_token_get_secure_cookies()).decode(), True)
#                 if refresh_flage:
#                     return username if username else None
#                 else:
#                     return None
#
# application = tornado.web.Application([
#     (r"/", MainHandler),
# ], cookie_secret=str(urandom(16)))
# if __name__ == "__main__":
#     application.listen(8888)
#     tornado.ioloop.IOLoop.instance().start()
#
#
#
#
