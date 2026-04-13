"""Built-in language-pack registry."""

from __future__ import annotations

from hermeneia.language.base import LanguagePack
from hermeneia.language.en import ENGLISH_PACK


class LanguageRegistry:
    """Languageregistry."""

    def __init__(self) -> None:
        """Initialize the instance."""
        self._packs: dict[str, LanguagePack] = {ENGLISH_PACK.code: ENGLISH_PACK}

    def get(self, code: str) -> LanguagePack:
        """Get.

        Parameters
        ----------
        code : str
            Input value for ``code``.

        Returns
        -------
        LanguagePack
            Resulting value produced by this call.
        """
        try:
            return self._packs[code]
        except KeyError as exc:
            raise KeyError(f"Unknown language pack '{code}'") from exc

    def register(self, pack: LanguagePack) -> None:
        """Register.

        Parameters
        ----------
        pack : LanguagePack
            Input value for ``pack``.
        """
        self._packs[pack.code] = pack

    def supported_codes(self) -> tuple[str, ...]:
        """Supported codes.

        Returns
        -------
        tuple[str, ...]
            Resulting value produced by this call.
        """
        return tuple(sorted(self._packs))
