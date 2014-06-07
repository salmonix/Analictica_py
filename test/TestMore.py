from pprint import pprint

_operators = {
              'is_ok'   : lambda x,y: ( x is y ),
              'isnt_ok' : lambda x,y: ( x is not y ),
              'isa'     : lambda x,y: ( type(x,y) ),
              'same'    :  
}


def _print_ok(message, **kwargs):
    print('Test %s ok. %s' % str(message, pprint(**kwargs)))
    return True

def _print_notok(message,**kwargs):
    print('Failed test : %s %s'% str(message, pprint(**kwargs)) )
    return False

def the_same(value1,value2, message,**kwargs):
    
    if value1 == value2:
        return _print_ok(message, **kwargs)
    else:
        return _print_notok(message,**kwargs)


#def can(obj,what,message,**kwargs):
#    if callable(object):
#        if object."what":
#            _print_ok(message,**kwargs)
#        else:
#            _print_notok(message,**kwargs)
#    else:
#       _print_notok(_'object not callable %s' % str(obj),**kwargs)            