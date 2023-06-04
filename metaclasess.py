import dis


class ServerVerifier(type):
    """
    Метакласс для обработки функций используемых при создании сервера
    """

    def __init__(cls, name, bases, namespace):

        allow_methods = []
        attrs = []
        for method in namespace:
            try:
                ret = dis.get_instructions(namespace[method])
                for i in ret:
                    if i.opname == 'LOAD_METHOD':
                        if i.argval not in allow_methods:
                            allow_methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
            except TypeError:
                pass
        if 'connect' in allow_methods:
            raise TypeError
        if 'sock' not in attrs:
            raise TypeError('Socket Error')
        super().__init__(name, bases, namespace)


class ClientVerifier(type):
    """
    Метакласс для обработки функций используемых при создании клиента
    """

    def __init__(cls, name, bases, namespace):
        allow_methods = []
        for method in namespace:
            try:
                ret = dis.get_instructions(namespace[method])
                for i in ret:
                    if i.opname == 'LOAD_METHOD':
                        if i.argval not in allow_methods:
                            allow_methods.append(i.argval)
            except TypeError:
                pass

        if 'accept' in allow_methods:
            raise TypeError('Method accept error')
        elif 'listen' in allow_methods:
            raise TypeError('Method listen error')

        if 'get_message' not in allow_methods and 'send_message' not in allow_methods:
            raise TypeError('Sockets error')

        super().__init__(name, bases, namespace)
