def strip_comments_and_spaces(arg: str) -> str:
    return arg.split("#")[0].strip()