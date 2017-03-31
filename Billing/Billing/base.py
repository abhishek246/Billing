
from django.db import models
import hashlib
from functools import wraps
from django.utils.decorators import available_attrs
import operator
from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseNotAllowed

class BaseModel(models.Model):
	created_on = models.DateTimeField(auto_now_add = True, db_index=True, \
									verbose_name='created_on', null=True, blank=True)
	updated_on = models.DateTimeField(auto_now = True, db_index=True, \
									verbose_name='updated_on', null=True, blank=True)
	is_deleted = models.BooleanField(default=False, verbose_name='deleted')

	class Meta:
		abstract = True



class decorator_4xx(object):

    ''' request_method_list: allowed HTTP methods.
    reqd_params: parameters reqd for the current api.
    params_type: parameters with their typ(int,str,datetime) and their attributes
    e.g: [(amount,Decimal,0), (from_date,date, "%Y-%m-%d")]'''

    def __init__(self, reqd_params,
                 params_type=None, validateList=None):

        if not params_type:
            params_type = list()
        if not validateList:
            validateList = list()

        self.reqd_params = reqd_params
        self.params_type = params_type
        self.validateList = validateList

    '''Identifies which http method is valid for the curent api
    and gets all incoming parameters into params_dict'''

    def get_all_params(self, request):

        params_dict = dict()

        if request.method == 'GET':
            params_dict = request.GET

        elif request.method == 'POST':
            params_dict = request.POST

        elif request.method == 'PUT':
            params_dict = QueryDict(request.body)

        elif request.method == "DELETE":
            params_dict = QueryDict(request.body)

        elif request.method == 'PATCH':
            params_dict = request.POST

        return params_dict

    '''Parses supplied param value with param type and param attributes
    supplied at view level'''

    def parse_n_validate(self, params_type, params_dict):

        for param in self.params_type:
            key = param[0]
            key_type = param[1]
            key_val = params_dict[key]

            is_valid, res_str = self.validate_params_type(key_type, key_val)
            if not is_valid:
                return False, res_str
        return True, None

    '''Authenticates session token coming in request body and validates
    whether the token is active or not. If not active
    returns  Http status 401'''

    def authenticate_token(self, request):
    	if request.method in ['GET']:
    		params = request.GET
    	else:
    		params = json.loads(request.body)
    	from Areas.models import User

    	cid = params.get('cid')
    	token = params.get('token')
        user = User.objects.get(pk=cid)
        status = (user.token == token)
        return status, None, None

    '''Makes the decorator callable by view.'''

    def __call__(self, func, *args, **kwargs):
        '''Makes the passed view function persists its name, docstring
         instead of being overriden by inner function'''
        @wraps(func, assigned=available_attrs(func))

        def inner(*args, **kwargs):
            request = args[1]
            params_dict = self.get_all_params(request)
            request.params_dict = params_dict
            '''Checks all required parametes are present or not,
            if not return 400 HTTP bad request'''

            is_valid = reduce(operator.and_, ((
                True if param in params_dict else False) for param in self.reqd_params)) if self.reqd_params else True

            if not is_valid:
                missing_params = filter(lambda param: (
                    param if param not in params_dict else ''), self.reqd_params)

                response_text = "Parameters missing: " + \
                    ",".join(missing_params)
                return HttpResponseBadRequest(response_text)

            '''Validates all parameters are in correct format or not
            with the help of helper class functions'''
            is_valid, res_str = self.parse_n_validate(
                self.params_type, params_dict)

            if not is_valid:
                return HttpResponseBadRequest(res_str)

            '''Validates session against incoming cid and token'''

            is_active, res_code, res_str = self.authenticate_token(request)

            if not is_active:
                return HttpResponse('Unauthorized', status=401)

            return func(*args, **kwargs)
        return inner

def gen_password_hash(passwd):
    return str(hashlib.sha256(passwd).hexdigest())