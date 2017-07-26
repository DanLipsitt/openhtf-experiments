from openhtf.util.validators import Equals

assert(Equals('0')('0'))
assert(Equals('0')('0.1') is False)

print('all assertions passed')
