import unittest
import erie_server
import numpy as np

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
#        test_data = np.array([[[21.21320344, 21.21320344, 21.21320344, 21.21320344],
#                               [21.21320344, 21.21320344, 21.21320344, 21.21320344],
#                               [21.21320344, 21.21320344, 21.21320344, 21.21320344],
#                               [21.21320344, 21.21320344, 21.21320344, 21.21320344],
#                               [17.67766953, 17.67766953, 17.67766953, 17.67766953],
#                               [17.67766953, 17.67766953, 17.67766953, 17.67766953],
#                               [17.67766953, 17.67766953, 17.67766953, 17.67766953],
#                               [17.67766953, 17.67766953, 17.67766953, 17.67766953],
#                               [14.14213562, 14.14213562, 14.14213562, 14.14213562]]])
#        prediction = erie_server.erie_model.predict(test_data)
#        self.assertAlmostEqual(prediction[0,0], 2.633, places=3)  #Station 45005 
#        self.assertAlmostEqual(prediction[0,1], 2.973, places=3)  #Station 45142

if __name__ == '__main__':
   unittest.main()
