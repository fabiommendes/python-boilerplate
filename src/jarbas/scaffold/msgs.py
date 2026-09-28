PRE_GEN_PROJECT_DATA = '''
import {package_name} as mod

try:
    method = mod.pre_gen_project
except AttributeError:
    pass
else:
    method()
'''

POST_GEN_PROJECT_DATA = '''
import {package_name} as mod

try:
    method = mod.post_gen_project
except AttributeError:
    pass
else:
    method()
'''