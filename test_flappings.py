import unittest
from flappings import flapping_alarms

mocked = [{"service_id": 1704, "duration": 17, "startTime": "2020-07-02  09:01:31"},
{"service_id": 1704, "duration": 2, "startTime": "2020-07-02  00:18:31"},
{"service_id": 1704, "duration": 1, "startTime": "2020-07-02  00:49:31"},
{"service_id": 1704, "duration": 1, "startTime": "2020-07-02  01:38:31"},
{"service_id": 1704, "duration": 2, "startTime": "2020-07-02  06:58:31"}]

mocked_one_long_alarm = [{"service_id": 1704, "duration": 17, "startTime": "2020-07-02  09:01:31"}]

checked = [{'service_id': 1704, 'start': '2020-07-02  06:58:31', 'duration': 19, 'end': '2020-07-02 09:18:31', 'amount_outages': 2, 'sum_outages': 17}]

class TestFlappings(unittest.TestCase):

    def test_result_base(self):
        result = flapping_alarms(mocked)
        self.assertEqual(result, checked)

    def test_result_one_long(self):
        result = flapping_alarms(mocked_one_long_alarm)
        self.assertIsNotNone(result, checked)


    def test_return_type(self):
        result = flapping_alarms(mocked)
        self.assertIs(type(result), list )
if __name__ == '__main__':
    unittest.main()
