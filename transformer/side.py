from pydantic import TypeAdapter

from .base import OracleBase, LocaleBase, ResultBase


class OracleSide(OracleBase):
    """英文「阵营」数据结构"""

    name: str
    """阵营名称"""


class LocaleSide(LocaleBase):
    """中文「阵营」数据结构"""

    name: str
    """阵营名称"""


class ResultSide(ResultBase):
    """最终「阵营」数据结构"""

    oracle_name: str
    """阵营英文名称"""

    locale_name: str
    """阵营中文名称"""


oracle_validator = TypeAdapter(list[OracleSide])
locale_validator = TypeAdapter(list[LocaleSide])
result_validator = TypeAdapter(list[ResultSide])


ORACLE_FILE = "source/enUS/v2/sides.json"
LOCALE_FILE = "source/zhCN/data/json/sides.json"
RESULT_FILE = "result/sides.json"


def load_oracle() -> list[OracleSide]:
    with open(ORACLE_FILE, "r", encoding="utf-8") as file:
        text = file.read()
        entries = oracle_validator.validate_json(text, strict=True)
        return entries


def load_locale() -> dict[str, LocaleSide]:
    with open(LOCALE_FILE, "r", encoding="utf-8") as file:
        text = file.read()
        entries = locale_validator.validate_json(text, strict=True)
        result: dict[str, LocaleSide] = dict()
        for e in entries:
            result[e.id] = e

        return result


def load_result() -> list[ResultSide]:
    oracles = load_oracle()
    locales = load_locale()
    results: list[ResultSide] = list()
    for oracle in oracles:
        locale = locales.get(oracle.id, None)
        if locale is None:
            raise Exception(f"ID = {oracle.id}：缺少中文数据!")

        result = ResultSide(
            codename=oracle.id,
            oracle_name=oracle.name,
            locale_name=locale.name
        )

        results.append(result)

    return results


def save_side() -> None:
    results = load_result()
    raw = result_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
