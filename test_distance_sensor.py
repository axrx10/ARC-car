# You don't need to modify the imports; leave them as they are.
import unittest
from unittest.mock import patch
from distance_sensor import DistanceSensor
import time

class TestDistanceSensor(unittest.TestCase):

    @patch('RPi.GPIO.setup')
    @patch('RPi.GPIO.setmode')
    def setUp(self, mock_setmode, mock_setup):
        self.sensor = DistanceSensor(trig_pin=23, echo_pin=24)

    @patch('RPi.GPIO.output')
    @patch('RPi.GPIO.input')
    @patch('time.time')
    def test_read(self, mock_time, mock_input, mock_output):
        mock_time.side_effect = [0, 0, 0.002]  # 0.002 seconds to indicate 34.3 cm distance
        mock_input.side_effect = [0, 1]
        distance = self.sensor.read()
        self.assertAlmostEqual(distance, 34.3, places=1)

    def tearDown(self):
        self.sensor.cleanup()

if __name__ == '__main__':
    unittest.main()
