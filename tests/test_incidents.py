import io
import os
import unittest
from incidents_analyze import incidents

from unittest.mock import patch


class GlobalEngineTest(unittest.TestCase):
    TEST_DATA = io.StringIO('id,feature1,feature2,time\n'
                            '0,1,0,0.206520219143\n'
                            '1,0,0,0.233725001118\n'
                            '2,0,1,0.760992754734\n'
                            '3,1,1,0.92776979943\n'
                            '4,1,0,0.569711498585\n'
                            '5,0,1,0.99224586863\n'
                            '6,0,0,0.593264390713\n'
                            '7,1,0,0.694181201747\n'
                            '8,1,1,0.823812651856\n'
                            '9,0,1,0.906011017725')

    def setUp(self):
        print(f'Вызван {self.shortDescription()}', flush=True)

    def tearDown(self):
        print(f'Оттестировано. \n', flush=True)

    @patch('incidents_analyze.pd.Series.to_csv')
    @patch('os.makedirs')
    @patch('sys.stdout')
    def test_get_incidents(self, mock_print, mock_dirs, mock_to_csv):
        """Тест подсчёта инцидентов"""
        test_dt = 0.3

        test_func = incidents(2, test_dt, self.TEST_DATA, 'test', console=True)
        self.assertEqual(4, sum(test_func > 0))

    @patch('incidents_analyze.pd.Series.to_csv')
    @patch('os.makedirs')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_runtime_incidents(self, mock_time_dec_print, mock_dirs, mock_to_csv):
        """Тест времени работы функции при больших данных
        M=100, N=1000000"""
        test_dt = 0.3
        incidents(100, test_dt,
                  os.path.join(os.path.abspath(__file__), '../../files/big_incidents.csv'),
                  'test', console=True)
        self.assertTrue(float(mock_time_dec_print.getvalue().split()[2]) < 60)


if __name__ == '__main__':
    unittest.main()
