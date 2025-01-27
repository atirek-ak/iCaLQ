def pr_blue(text):
    print(f"\033[94m{text}\033[00m")


def pr_blue_no_new_line(text):
    print(f"\033[94m{text}\033[00m", end="")


def pr_red(text):
    print(f"\033[91m{text}\033[00m")


def pr_red_no_new_line(text):
    print(f"\033[91m{text}\033[00m", end="")

def raise_error_or_print_warning(error_msg: str, raise_error: bool):
    if raise_error:
        raise ValueError(error_msg)
    else:
        pr_red(error_msg)