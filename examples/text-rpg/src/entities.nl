# Entity Definitions

@module entities
@target python

@type Entity {
  name: string
  hp: number
  max_hp: number
  attack: number
  defense: number
}

[create-hero]
PURPOSE: Initialize a new hero with starting stats
INPUTS:
  - name: string
RETURNS: Entity(name, 100, 100, 15, 5)

[create-monster]
PURPOSE: Initialize a new monster
INPUTS:
  - name: string
  - difficulty: number
LOGIC:
  1. hp = 20 * difficulty
  2. atk = 3 * difficulty
RETURNS: Entity(name, hp, hp, atk, 0)
