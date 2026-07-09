# Prompt Patterns

## Beschreibung

Prompt Patterns sind wiederverwendbare Bausteine fuer Agentenkonfigurationen. Sie sollen helfen, Rollen, Modi und Aufgaben konsistent zu kombinieren.

## Pattern: Constitution + Mode + Briefing

```text
Folge der Fjolnir Constitution.
Arbeite im Modus: [MODE].
Bearbeite das folgende Task Briefing: [BRIEFING].
Gib das Ergebnis im Format [FORMAT] aus.
```

## Pattern: Evidence-Bound Answer

```text
Antworte nur auf Basis der bereitgestellten Eingaben.
Kennzeichne Fakten, Annahmen, Schlussfolgerungen, Risiken und Empfehlungen.
Wenn Evidenz fehlt, benenne die Luecke.
```

## Pattern: Review Findings

```text
Pruefe das Artefakt gegen die genannten Kriterien.
Sortiere Befunde nach Schweregrad.
Jeder Befund enthaelt Ort, Problem, Evidenz, Auswirkung und Empfehlung.
```

## Pattern: Bounded Autonomy

```text
Arbeite innerhalb des beschriebenen Auftrags eigenstaendig.
Pausiere bei sicherheits-, compliance-, kosten- oder freigaberelevanten Entscheidungen.
```

## TODO

- Weitere Patterns fuer Assurance, Research und Engineering ergaenzen.
- Pattern-Qualitaet mit Checklisten aus `tests/` verknuepfen.
- Beispiele fuer schlechte und verbesserte Prompts aufnehmen.
