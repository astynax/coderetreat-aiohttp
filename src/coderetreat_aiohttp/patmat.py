from dataclasses import dataclass
from enum import Enum
import uuid
from typing import TypedDict


class PetKind(Enum):
    CAT = 'cat'
    DOG = 'dog'
    LIZARD = 'lizard'


@dataclass
class Chip:
    uuid: uuid.UUID


@dataclass
class Pet:
    kind: PetKind
    name: str
    chip: Chip | None = None


class PetDict(TypedDict):
    kind: PetKind
    name: str
    chip: Chip | None


@dataclass
class User:
    name: str
    age: int
    pets: list[Pet | PetDict]


if __name__ == '__main__':
    users = [
        User(name="Bob", age=42, pets=[
            Pet(name="Thomas", kind=PetKind.CAT, chip=Chip(uuid.uuid4())),
            Pet(name="Godzilla", kind=PetKind.LIZARD),
            Pet(name="Spike", kind=PetKind.DOG, chip=Chip(uuid.uuid4()))
        ]),
        User(name="Alice", age=32, pets=[
            Pet(name="Spot", kind=PetKind.DOG, chip=Chip(uuid.uuid4())),
            {"name": "Skippy", "kind": PetKind.DOG},
        ])
    ]

    for user in users:
        match user:
            case User(pets=ps, name=user_name) if user.age > 0:
                for pet in user.pets:
                    match pet:
                        case (
                            Pet(kind=PetKind.DOG, name=n) | Pet(kind=PetKind.LIZARD, name=n)
                            | {"kind": PetKind.DOG, "name": n}
                        ):
                            print(f"{n} ({user_name})")
                        case Pet(kind=kind, chip=Chip() as chip):
                            print(f"non-dog ({kind.value}) with chip {chip.uuid}")
