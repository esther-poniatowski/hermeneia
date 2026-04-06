"""Built-in language-pack registry."""

from __future__ import annotations

from hermeneia.language.base import LanguagePack
from hermeneia.language.en import ENGLISH_PACK


class LanguageRegistry:
    def __init__(self) -> None:
        self._packs: dict[str, LanguagePack] = {ENGLISH_PACK.code: ENGLISH_PACK}

    def get(self, code: str) -> LanguagePack:
        try:
            return self._packs[code]
        except KeyError as exc:
            raise KeyError(f"Unknown language pack '{code}'") from exc

    def register(self, pack: LanguagePack) -> None:
        self._packs[pack.code] = pack

    def supported_codes(self) -> tuple[str, ...]:
        return tuple(sorted(self._packs))
