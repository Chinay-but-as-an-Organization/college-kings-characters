from __future__ import annotations

from renpy import store
import renpy.exports as renpy


from game.characters.Relationship_ren import Relationship
from game.characters.Moods_ren import Moods
from game.characters.NonPlayableCharacter_ren import NonPlayableCharacter
from game.characters.PlayableCharacters_ren import PlayableCharacter


"""renpy
init python:
"""


class CharacterService:
    @staticmethod
    def get_relationship(
        character: NonPlayableCharacter, target: PlayableCharacter
    ) -> Relationship:
        if not hasattr(character, "relationships"):
            character.relationships = {}

        return character.relationships.setdefault(target.name, Relationship.FRIEND)

    @staticmethod
    def has_relationship(
        character: NonPlayableCharacter,
        relationship: Relationship,
        target: PlayableCharacter = None,
    ) -> bool:
        if target is None:
            target = store.mc

        return CharacterService.get_relationship(character, target) == relationship

    @staticmethod
    def set_relationship(
        character: NonPlayableCharacter,
        relationship: Relationship,
        target: PlayableCharacter = None,
    ) -> None:
        if target is None:
            target = store.mc

        if not hasattr(character, "relationships"):
            character.relationships = {}

        if not hasattr(target, "relationships"):
            target.relationships = {}

        if (
            character.relationships.setdefault(target.name, Relationship.FRIEND)
            == relationship
        ):
            return

        character.relationships[target.name] = relationship
        target.relationships[character.name] = relationship

    @staticmethod
    def get_mood(character: NonPlayableCharacter) -> Moods:
        return character.mood

    @staticmethod
    def set_mood(character: NonPlayableCharacter, mood: Moods) -> None:
        if mood == character.mood:
            return

        character.mood = mood

    @staticmethod
    def reset_mood(character: NonPlayableCharacter) -> None:
        character.mood = Moods.NORMAL

    @staticmethod
    def add_mood(character: NonPlayableCharacter, mood: Moods) -> None:
        if mood == character.mood:
            return

        if character.mood == Moods.NORMAL:
            character.mood = mood
            return

        character.mood = character.mood | mood

    @staticmethod
    def remove_mood(character: NonPlayableCharacter, mood: Moods) -> None:
        character.mood = character.mood & ~mood

    @staticmethod
    def get_profile_pictures(character_name: str) -> list[str]:
        directory: str = f"images/characters/{character_name.lower()}"

        try:
            return [file for file in renpy.list_files() if file.startswith(directory)]
        except OSError:
            return [
                file
                for file in renpy.list_files()
                if file.startswith("images/characters/chloe")
            ]

    @staticmethod
    def is_girlfriend(
        character: NonPlayableCharacter, target: PlayableCharacter = None
    ) -> bool:
        if target is None:
            target = store.mc

        return CharacterService.has_relationship(
            target.name, Relationship.GIRLFRIEND, store.mc
        )

    @staticmethod
    def is_fwb(
        character: NonPlayableCharacter, target: PlayableCharacter = None
    ) -> bool:
        if target is None:
            target = store.mc

        return CharacterService.has_relationship(
            target.name, Relationship.FWB, store.mc
        )

    @staticmethod
    def is_dating(
        character: NonPlayableCharacter, target: PlayableCharacter = None
    ) -> bool:
        if target is None:
            target = store.mc

        return CharacterService.has_relationship(
            target.name, Relationship.DATING, store.mc
        )

    @staticmethod
    def is_kissed(
        character: NonPlayableCharacter, target: PlayableCharacter = None
    ) -> bool:
        if target is None:
            target = store.mc

        return CharacterService.has_relationship(
            target.name, Relationship.KISSED, store.mc
        )

    @staticmethod
    def is_friend(
        character: NonPlayableCharacter, target: PlayableCharacter = None
    ) -> bool:
        if target is None:
            target = store.mc

        return CharacterService.has_relationship(
            target.name, Relationship.FRIEND, store.mc
        )

    @staticmethod
    def is_ex(
        character: NonPlayableCharacter, target: PlayableCharacter = None
    ) -> bool:
        if target is None:
            target = store.mc

        return CharacterService.has_relationship(target.name, Relationship.EX, store.mc)

    @staticmethod
    def is_mad(character: NonPlayableCharacter) -> bool:
        return Moods.MAD in character.mood
