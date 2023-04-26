from unittest import TestCase, main
import client
import datetime


arguments = client.client_arguments()
message = {
    "action": "presence",
    "time": str(datetime.date.today()),
    "type": "status",
    "user": {
        "account_name": "C0deMaver1ck",
        "status": "Yep, I am here!"
    }
}


class TestArgument(TestCase):

    def test_host_argument(self):
        self.assertIs(arguments.a, 'localhost')

    def test_port_type_argument(self):
        self.assertIsInstance(arguments.p, int)

    def test_port_argument(self):
        self.assertEqual(arguments.p, 8000)


class TestConnectClient(TestCase):

    def test_crash_server(self):
        with self.assertRaises(OverflowError):
            client.connect_to_server('sadasdasd', 111111111111)


class TestRequestsServer(TestCase):

    def test_crash_request(self):
        with self.assertRaises(AttributeError):
            client.requests_client('sdfsdf', message)

    def test_crash_server_connection_error(self):
        with self.assertRaises(ConnectionRefusedError):
            server = client.connect_to_server(arguments.a, arguments.p)
            client.requests_client(server, message)


if __name__ == '__main__':
    main()
