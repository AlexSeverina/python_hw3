from functools import wraps


class ContractError(Exception):
    """We use this error when someone breaks our contract."""


#: Special value, that indicates that validation for this type is not required.
Any = object()


def contract(arg_types=None, return_type=None, raises=None):
    """Contract for checking input and output types of function.
        Some arguments may be omitted.

        :param arg_types: tuple of arguments allowed in corresponding positions
        :param return_type: type of allowed return type
        :param raises: types of allowed exceptions"""
    def factory(function):
        @wraps(function)
        def decorator(*args):
            for i, arg in enumerate(args):
                if (arg_types is not None
                        and type(arg) is not arg_types[i]
                        and Any is not arg_types[i]):
                    raise ContractError
                try:
                    return_value = function(*args)
                except Exception as ex:
                    if (type(ex) not in raises
                            and Any not in raises):
                        raise ContractError from ex
                    else:
                        raise ex
                if (return_type is not None
                        and type(return_value) is not return_type):
                    raise ContractError
        return decorator
    return factory


@contract(arg_types=(int, Any))
def add_two_numbers(first, second):
    return first + second


@contract(arg_types=(int, int), return_type=float, raises=(ZeroDivisionError,))
def div(first, second):
    return first / second


if __name__ == '__main__':
    add_two_numbers(1, 2)
    add_two_numbers(1, 3.4)
    # add_two_numbers(2.1, 1)

    div(1, 2)
    div(1, 0)  # raises ZeroDisionError
    div(1, None)

