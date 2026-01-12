from pydantic import TypeAdapter

from .base import OracleBase, LocaleBase, ResultBase


class OracleType(OracleBase):
    """英文「类型」数据结构"""

    name: str
    """类型名称"""

    side_id: str
    """类型所属阵营"""


class LocaleType(LocaleBase):
    """中文「类型」数据结构"""

    name: str
    """类型名称"""


class ResultType(ResultBase):
    """最终「类型」数据结构"""

    oracle_name: str
    """类型英文名称"""

    locale_name: str
    """类型中文名称"""

    side_codename: str
    """类型所属阵营"""


oracle_validator = TypeAdapter(list[OracleType])
locale_validator = TypeAdapter(list[LocaleType])
result_validator = TypeAdapter(list[ResultType])


ORACLE_FILE = "source/enUS/v2/card_types.json"
LOCALE_FILE = "source/zhCN/data/json/types.json"
RESULT_FILE = "result/types.json"


def load_oracle() -> list[OracleType]:
    with open(ORACLE_FILE, "r", encoding="utf-8") as file:
        text = file.read()
        entries = oracle_validator.validate_json(text, strict=True)
        return entries


def load_locale() -> dict[str, LocaleType]:
    with open(LOCALE_FILE, "r", encoding="utf-8") as file:
        text = file.read()
        entries = locale_validator.validate_json(text, strict=True)
        result: dict[str, LocaleType] = dict()
        for e in entries:
            result[e.id] = e

        return result


def load_result() -> list[ResultType]:
    oracles = load_oracle()
    locales = load_locale()
    results: list[ResultType] = list()
    for oracle in oracles:
        locale = locales.get(oracle.id, None)
        if locale is None:
            raise Exception(f"ID = {oracle.id}：缺少中文数据!")

        result = ResultType(
            codename=oracle.id,
            oracle_name=oracle.name,
            locale_name=locale.name,
            side_codename=oracle.side_id
        )

        results.append(result)

    return results


def save_type() -> None:
    results = load_result()
    raw = result_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
