from unittest import TestCase, main
import server
from socket import *

arguments = server.server_arguments()
main_server = server.server_init(arguments.a, int(arguments.p))
message = {
    "response": 200,
    "alert": "Необязательное сообщение/уведомление"
}

class TestArgument(TestCase):

    def test_host_argument(self):
        self.assertIs(arguments.a, 'localhost')

    def test_port_type_argument(self):
        self.assertIsInstance(arguments.p, int)

    def test_port_argument(self):
        self.assertEqual(arguments.p, 8000)


class TestInitServer(TestCase):

    def test_crash_init_server(self):
        with self.assertRaises((Exception)):
            server.server_init('sadafsdfsdasd', 1112111111111)


class TestRequestsServer(TestCase):

    def test_crash_server(self):
        with self.assertRaises(Exception):
            server.requests_server('sdfsdf', message)


if __name__ == '__main__':
    main()
