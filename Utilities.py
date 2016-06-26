def is_con_to_int(test_string):
    try:
        int(test_string)
    except ValueError:
        return False
    return True
