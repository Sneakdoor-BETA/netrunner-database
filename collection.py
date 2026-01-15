import csv
import os
from typing import Type, TypeVar, Optional
from pydantic import BaseModel, ConfigDict, TypeAdapter
from transformer import (
    ResultBase, ResultSide, ResultFaction,
    ResultType, ResultSubtype,
    ResultCycle, ResultSet, ResultSettype,
    ResultCard, ResultPrinting
)

class CollectionRow(BaseModel):
    """《矩阵潜袭》卡牌完整数据结构"""

    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    id: str
    """卡图唯一标识符"""

    cycle_enUS: str
    """循环英文名称"""

    cycle_zhCN: str
    """循环中文名称"""

    cycle_position: int
    """循环序号"""

    set_enUS: str
    """卡包英文名称"""

    set_zhCN: str
    """卡包中文名称"""

    set_position: int
    """卡包在循环中位置"""

    settype_enUS: str
    """卡包类型英文名称"""

    settype_zhCN: str
    """卡包类型中文名称"""

    set_size: int
    """卡包卡牌数量"""

    position: int
    """卡图序号"""

    title_enUS: str
    """卡牌英文名称"""

    title_zhCN: str
    """卡牌中文名称"""

    stripped_title: str
    """卡牌英文名称（ASCII）"""

    text_enUS: str
    """卡牌英文文本"""

    text_zhCN: str
    """卡牌中文文本"""

    stripped_text: str
    """卡牌英文文本（ASCII）"""

    type_enUS: str
    """类型英文名称"""

    type_zhCN: str
    """类型中文名称"""

    subtype_enUS: str
    """子类型英文名称"""

    subtype_zhCN: str
    """子类型中文名称"""

    side_enUS: str
    """阵营英文名称"""

    side_zhCN: str
    """阵营中文名称"""

    faction_enUS: str
    """派系英文名称"""

    faction_zhCN: str
    """派系中文名称"""

    is_unique: str
    """卡牌是否独有"""

    deck_limit: Optional[int]
    """卡牌牌组限制"""

    advancement_requirement: Optional[int]
    """卡牌推进需求"""

    agenda_point: Optional[int]
    """卡牌议案分数"""

    base_link: Optional[int]
    """卡牌基础中转"""

    minimum_deck_size: Optional[int]
    """卡牌牌组最小张数"""

    influence_limit: Optional[int]
    """卡牌牌组影响力上限"""

    influence_cost: Optional[int]
    """卡牌影响力费用"""

    cost: Optional[int]
    """卡牌费用"""

    strength: Optional[int]
    """卡牌强度"""

    memory_cost: Optional[int]
    """卡牌内存费用"""

    trash_cost: Optional[int]
    """卡牌销毁费用"""

    flavor_enUS: str
    """卡图英文风味文字"""

    flavor_zhCN: str
    """卡图本地化风味文字"""

    quantity: int
    """卡图在卡包中数量"""

    extra_printing: int
    """卡牌额外牌面数"""

    illustrator: str
    """卡图插画作者"""

    attribution: str
    """卡牌冠名"""

    pronouns: str
    """卡牌人称代词"""

    pronunciation_ipa: str
    """卡牌读音（国际音标）"""

    pronunciation_approx: str
    """卡牌读音（英文音标）"""

    extra_face: int
    """卡牌额外牌面数"""

    narrative_enUS: str
    """卡牌英文背景文字"""

    designed_by: str
    """卡牌设计组"""

    release_date: str
    """卡包发行日期"""

    released_by: str
    """卡图发行组"""


TResult = TypeVar("TResult", bound=ResultBase)


def load_sources(constraint: Type[TResult], filename: str) -> dict[str, TResult]:
    location = os.path.join("result", filename + ".json")
    with open(location, "r", encoding="utf-8") as file:
        text = file.read()
        validator = TypeAdapter(list[constraint])
        entries = validator.validate_json(text, strict=True)
        result: dict[str, TResult] = dict()
        for entry in entries:
            result[entry.codename] = entry
        return result


def load_printings() -> list[ResultPrinting]:
    table = load_sources(ResultPrinting, "printings")
    result = list(table.values())
    result.sort(key=lambda x: x.codename)
    return result


def create_collections(printings: list[ResultPrinting]) -> list[CollectionRow]:
    cycles = load_sources(ResultCycle, "cycles")
    sets = load_sources(ResultSet, "sets")
    settypes = load_sources(ResultSettype, "settypes")
    cards = load_sources(ResultCard, "cards")
    sides = load_sources(ResultSide, "sides")
    factions = load_sources(ResultFaction, "factions")
    types = load_sources(ResultType, "types")
    subtypes = load_sources(ResultSubtype, "subtypes")
    result: list[CollectionRow] = list()
    for printing in printings:
        set = sets[printing.set_codename]
        cycle = cycles[set.cycle_codename]
        settype = settypes[set.settype_codename]
        card = cards[printing.card_codename]
        side = sides[card.side_codename]
        faction = factions[card.faction_codename]
        type = types[card.type_codename]
        subtype_enUS = list()
        subtype_zhCN = list()
        for s in card.subtype_codenames:
            subtype = subtypes[s]
            subtype_enUS.append(subtype.oracle_name)
            subtype_zhCN.append(subtype.locale_name)

        row = CollectionRow(
            id=printing.codename,
            cycle_enUS=cycle.oracle_name,
            cycle_zhCN=cycle.locale_name,
            cycle_position=cycle.position,
            set_enUS=set.oracle_name,
            set_zhCN=set.locale_name,
            set_position=set.position,
            settype_enUS=settype.oracle_name,
            settype_zhCN=settype.locale_name,
            set_size=set.size,
            position=printing.position,
            title_enUS=card.oracle_title,
            title_zhCN=card.locale_title,
            stripped_title=card.stripped_title,
            text_enUS=card.oracle_text,
            text_zhCN=card.locale_text,
            stripped_text=card.stripped_text,
            type_enUS=type.oracle_name,
            type_zhCN=type.locale_name,
            subtype_enUS=",".join(subtype_enUS),
            subtype_zhCN=",".join(subtype_zhCN),
            side_enUS=side.oracle_name,
            side_zhCN=side.locale_name,
            faction_enUS=faction.oracle_name,
            faction_zhCN=faction.locale_name,
            is_unique=("♦" if card.is_unique else ""),
            deck_limit=card.deck_limit,
            advancement_requirement=card.advancement_requirement,
            agenda_point=card.agenda_point,
            base_link=card.base_link,
            minimum_deck_size=card.minimum_deck_size,
            influence_limit=card.influence_limit,
            influence_cost=card.influence_cost,
            cost=card.cost,
            strength=card.strength,
            memory_cost=card.memory_cost,
            trash_cost=card.trash_cost,
            flavor_enUS=printing.oracle_flavor,
            flavor_zhCN=printing.locale_flavor,
            quantity=printing.quantity,
            extra_printing=printing.extra_face,
            illustrator=printing.illustrator,
            attribution=card.attribution,
            pronouns=card.pronouns,
            pronunciation_ipa=card.pronunciation_ipa,
            pronunciation_approx=card.pronunciation_approx,
            extra_face=card.extra_face,
            narrative_enUS=card.oracle_narrative,
            designed_by=card.designed_by,
            released_by=printing.released_by,
            release_date=set.release_date,
        )
        result.append(row)

    return result


def save_collections(entries: list[CollectionRow]) -> None:
    headers = [
        "id",
        "cycle_enUS", "cycle_zhCN", "cycle_position",
        "set_enUS", "set_zhCN", "set_position",
        "settype_enUS", "settype_zhCN", "set_size", "position",
        "title_enUS", "title_zhCN", "stripped_title",
        "text_enUS", "text_zhCN", "stripped_text",
        "type_enUS", "type_zhCN", "subtype_enUS", "subtype_zhCN",
        "side_enUS", "side_zhCN", "faction_enUS", "faction_zhCN",
        "is_unique", "deck_limit", "advancement_requirement", "agenda_point",
        "base_link", "minimum_deck_size", "influence_limit", "influence_cost",
        "cost", "strength", "memory_cost", "trash_cost",
        "flavor_enUS", "flavor_zhCN",
        "quantity", "extra_printing",
        "illustrator", "attribution",
        "pronouns", "pronunciation_ipa", "pronunciation_approx",
        "extra_face", "narrative_enUS",
        "designed_by", "released_by", "release_date"
    ]

    with open("derivatives/collections.csv", "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        for e in entries:
            writer.writerow(e.model_dump())


def main():
    printings = load_printings()
    collections = create_collections(printings)
    save_collections(collections)
    print(f"Save {len(collections)} Cards!")


if __name__ == "__main__":
    main()
