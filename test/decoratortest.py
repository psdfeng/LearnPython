from functools import wraps


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging


@logit
def addition_func(x):
   """Do some math."""
   return x + x


result = addition_func(4)
# Output: addition_func was called

# from functools import wraps
# import pdb


# def decorator_name(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if not can_run:
#             return "Function will not run"
#         return f(*args, **kwargs)
#     return decorated


# @decorator_name
# def func():
#     return("Function is running")


# can_run = True
# print(func())
# # Output: Function is running

# can_run = False
# print(func())
pdb.set_trace()
# Output: Function will not run


# from functools import wraps


# def a_new_decorator(a_func):
#     @wraps(a_func)
#     def wrapTheFunction():
#         print("I am doing some boring work before executing a_func()")
#         a_func()
#         print("I am doing some boring work after executing a_func()")
#     return wrapTheFunction


# @a_new_decorator
# def a_function_requiring_decoration():
#     """Hey yo! Decorate me!"""
#     print("I am the function which needs some decoration to "
#           "remove my foul smell")


# print(a_function_requiring_decoration.__name__)
# Output: a_function_requiring_decoration


# def a_new_decorator(a_func):

#     def wrapTheFunction():
#         print("I am doing some boring work before executing a_func()")

#         a_func()

#         print("I am doing some boring work after executing a_func()")

#     return wrapTheFunction


# # def a_function_requiring_decoration():
# #     print("I am the function which needs some decoration to remove my foul smell")


# # a_function_requiring_decoration()
# # #outputs: "I am the function which needs some decoration to remove my foul smell"

# # a_function_requiring_decoration = a_new_decorator(
# #     a_function_requiring_decoration)
# # #now a_function_requiring_decoration is wrapped by wrapTheFunction()

# # a_function_requiring_decoration()
# # #outputs:I am doing some boring work before executing a_func()
# # #        I am the function which needs some decoration to remove my foul smell
# # #        I am doing some boring work after executing a_func()


# @a_new_decorator
# def a_function_requiring_decoration():
#     """Hey you! Decorate me!"""
#     print("I am the function which needs some decoration to "
#           "remove my foul smell")


# a_function_requiring_decoration()
# #outputs: I am doing some boring work before executing a_func()
# #         I am the function which needs some decoration to remove my foul smell
# #         I am doing some boring work after executing a_func()

# #the @a_new_decorator is just a short way of saying:
# a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
