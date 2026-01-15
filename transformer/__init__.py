__version__ = "0.1.0"
__author__ = "Eric03742 <eric03742@foxmail.com>"
__description__ = "《矩阵潜袭》卡牌数据转换/处理/合并工具"


__all__ = [
    "save_side", "save_faction", "save_type", "save_subtype",
    "save_settype", "save_cycle", "save_set",
    "save_format", "save_snapshot", "save_pool", "save_restrictions",
    "save_ruling", "save_card", "save_printing",

    "ResultBase", "ResultSide", "ResultFaction", "ResultType", "ResultSubtype",
    "ResultSettype", "ResultCycle", "ResultSet",
    "ResultFormat", "ResultSnapshot", "ResultPool", "ResultRestriction",
    "ResultRuling", "ResultCard", "ResultPrinting"
]


from .base import ResultBase
from .side import save_side, ResultSide
from .faction import save_faction, ResultFaction
from .type import save_type, ResultType
from .subtype import save_subtype, ResultSubtype
from .settype import save_settype, ResultSettype
from .cycle import save_cycle, ResultCycle
from .set import save_set, ResultSet
from .format import save_format, save_snapshot, ResultFormat, ResultSnapshot
from .pool import save_pool, ResultPool
from .restriction import save_restrictions, ResultRestriction
from .ruling import save_ruling, ResultRuling
from .card import save_card, ResultCard
from .printing import save_printing, ResultPrinting
