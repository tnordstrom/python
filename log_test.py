import logging
import logging.handlers
import unittest

def add(a, b):
    return int(a) + int(b)

def mult(a, b):
    return int(a) * int(b)

class Test(unittest.TestCase):

    def test_add(self):
        logging.debug('Testing %s begins', self.id())
        logging.info('The quick brown fox jumped over a lazy dog')
        self.assertEqual(5, add(2, 3))
        self.assertEqual(15, add(-6, 21))
        self.assertEqual(10, add('4', '6'))
        self.assertEqual(20, add('16', 4))
        self.assertEqual(14, add(4, '10'))
        self.assertEqual(9, add(4.0, 5.0))
        logging.debug('Testing %s completed', self.id())

    def test_mult(self):
        logging.debug('Testing %s begins', self.id())
        self.assertEqual(25, mult(5, 5))
        self.assertEqual(20, mult('2', 10))
        logging.debug('Testing %s completed', self.id())
        
    def test_add_exceptions(self):
        logging.debug('Testing %s begins', self.id())
        self.assertRaises(Exception, add, 'banana', 'apple')
        self.assertRaises(Exception, add, (2, 3), 5)
        logging.debug('Testing %s completed', self.id())

    def test_mult_exceptions(self):
        logging.debug('Testing %s begins', self.id())
        self.assertRaises(Exception, mult, 'banana', 'apple')
        self.assertRaises(Exception, mult, (2, 3), 5)
        logging.debug('Testing %s completed', self.id())
        
# Set up logging system

LOG_FILENAME = 'log_test.log'
LOG_SIZE = 64  # In kB
LOG_NUM = 5 # How many log files to keep around

handler_list = [logging.handlers.RotatingFileHandler(   LOG_FILENAME,
                                                        maxBytes=1024*LOG_SIZE,
                                                        backupCount=LOG_NUM)]

logging.basicConfig(format='%(asctime)s %(filename)s@%(lineno)d in %(funcName)s %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    handlers=handler_list)

# Log some messages
logging.info('It Begins')

unittest.main(verbosity=2, exit=False)
#logging.info('Result %d' % unittest.result.TestResult.wasSuccessful)

logging.info('All done')

# Clean up logging system

logging.shutdown()

