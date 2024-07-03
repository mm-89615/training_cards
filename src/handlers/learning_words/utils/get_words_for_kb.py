def get_words_for_kb(data: dict[str, str]):
    kb = {data["en_correct"]: data["ru_correct"], **data["incorrect"]}
    return kb
