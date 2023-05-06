from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from game.characters.ICharacter_ren import ICharacter

import renpy.exports as renpy

from game.characters.Relationship_ren import Relationship
from game.characters.Moods_ren import Moods

if TYPE_CHECKING:
    from game.characters.PlayableCharacters_ren import mc

"""renpy
init python:
"""


class CharacterService:
    @staticmethod
    def get_relationship(
        character: ICharacter, target: Optional[ICharacter] = None
    ) -> Relationship:
        if target is None:
            target = mc

        if not hasattr(character, "relationships"):
            character.relationships = {}

        return character.relationships.setdefault(target, Relationship.FRIEND)

    @staticmethod
    def has_relationship(
        character: ICharacter,
        relationship: Relationship,
        target: Optional[ICharacter] = None,
    ) -> bool:
        if target is None:
            target = mc

        return CharacterService.get_relationship(character, target) == relationship

    @staticmethod
    def set_relationship(
        character: ICharacter,
        relationship: Relationship,
        target: Optional[ICharacter] = None,
    ) -> None:
        if target is None:
            target = mc

        if not hasattr(character, "relationships"):
            character.relationships = {}

        if not hasattr(target, "relationships"):
            target.relationships = {}

        if (
            character.relationships.setdefault(target, Relationship.FRIEND)
            == relationship
        ):
            return

        character.relationships[target] = relationship
        target.relationships[character] = relationship

    @staticmethod
    def get_mood(character: ICharacter) -> Moods:
        return character.mood

    @staticmethod
    def has_mood(character: ICharacter, mood: Moods) -> bool:
        return mood == character.mood or character.mood & mood == mood

    @staticmethod
    def set_mood(character: ICharacter, mood: Moods) -> None:
        if mood == character.mood:
            return

        character.mood = mood

    @staticmethod
    def reset_mood(character: ICharacter) -> None:
        character.mood = Moods.NORMAL

    @staticmethod
    def add_mood(character: ICharacter, mood: Moods) -> None:
        if mood == character.mood:
            return

        if character.mood == Moods.NORMAL:
            character.mood = mood
            return

        character.mood = character.mood | mood

    @staticmethod
    def remove_mood(character: ICharacter, mood: Moods) -> None:
        character.mood = character.mood & ~mood

    @staticmethod
    def get_profile_pictures(character_name: str) -> list[str]:
        directory: str = f"characters/images/{character_name.lower()}"

        try:
            return [file for file in renpy.list_files() if file.startswith(directory)]
        except OSError:
            return [
                file
                for file in renpy.list_files()
                if file.startswith("characters/images/chloe")
            ]

    @staticmethod
    def is_girlfriend(
        character: ICharacter, target: Optional[ICharacter] = None
    ) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(
            character, Relationship.GIRLFRIEND, target
        )

    @staticmethod
    def is_fwb(character: ICharacter, target: Optional[ICharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(character, Relationship.FWB, target)

    @staticmethod
    def is_dating(character: ICharacter, target: Optional[ICharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(character, Relationship.DATING, target)

    @staticmethod
    def is_kissed(character: ICharacter, target: Optional[ICharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(character, Relationship.KISSED, target)

    @staticmethod
    def is_friend(character: ICharacter, target: Optional[ICharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(character, Relationship.FRIEND, target)

    @staticmethod
    def is_ex(character: ICharacter, target: Optional[ICharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(character, Relationship.EX, target)

    @staticmethod
    def is_mad(character: ICharacter) -> bool:
        return CharacterService.has_mood(character, Moods.MAD)

    @staticmethod
    def is_threatened(character: ICharacter) -> bool:
        return CharacterService.has_mood(character, Moods.THREATENED)
