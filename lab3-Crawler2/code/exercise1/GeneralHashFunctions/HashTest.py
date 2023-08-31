# SJTU EE208

import GeneralHashFunctions

string = 'HelloWorld!'

print(f'string: {string}')

for func in dir(GeneralHashFunctions):
    if func.endswith('Hash'):
        print(f'{func:10s}:', getattr(GeneralHashFunctions, func)(string))
