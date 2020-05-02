import unittest
import erie_server

# From tutorial: https://www.youtube.com/watch?v=6tNS--WetLI

class TestErie(unittest.TestCase):
# For list of inherited methods see: https://docs.python.org/3/library/unittest.html#test-cases

    def test_model_load(self):
        self.assertNotEqual(erie_server.erie_model.summary(), '')

    def test_create_vectors(self):
        val1, val2 = erie_server.create_vectors(30., 180.)
        self.assertEqual(round(val1, 2), 0.00)
        self.assertEqual(round(val2, 2), 30.00)

        val1, val2 = erie_server.create_vectors(30., 270.)
        self.assertEqual(round(val1, 2), 30.00)
        self.assertEqual(round(val2, 2), 0.00)

        val1, val2 = erie_server.create_vectors(30., 225.)
        self.assertEqual(round(val1, 2), 21.21)
        self.assertEqual(round(val2, 2), 21.21)

        val1, val2 = erie_server.create_vectors(30., 45.)
        self.assertEqual(round(val1, 2), -21.21)
        self.assertEqual(round(val2, 2), -21.21) 

#    def test_model_output(self):
#        test_data = np.reshape(test_data.to_numpy(), (1, 9, 4), order='C')
#        val1, val2 = erie_model.predict(test_data)
#        self.assertEqual(round(val1, 3), 2.633)
#        self.assertEqual(round(val2, 3), 2.973) 
#        #Station 45005	2.633
#        #Station 45142	2.973

if __name__ == '__main__':
   unittest.main()
