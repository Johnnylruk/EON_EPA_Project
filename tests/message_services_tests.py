import unittest
from app.services.message_services import MessageServices  # Import your class

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.message_service = MessageServices()  

    def test_create_message_returns_list(self):
        predictions = {
            
        }
        result = self.message_service.create_message()
        self.assertEqual(result, 5)

    
if __name__ == '__main__':
    unittest.main()