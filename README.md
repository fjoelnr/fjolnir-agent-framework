# fjolnir-agent-framework

## Projektziel

`fjolnir-agent-framework` ist ein modulares Agent-Constitution-Framework fuer professionelle KI-Agenten. Es soll helfen, Agenten so zu beschreiben, zu betreiben und zu pruefen, dass technische Qualitaet, Nachvollziehbarkeit, Trustworthy AI, Aerospace Compliance und reproduzierbare Arbeitsweise systematisch beruecksichtigt werden.

Das Projekt ist kein einzelner Agent und kein Prompt-Sammelsurium. Es ist ein Governance- und Engineering-Rahmen fuer Agentenrollen, Betriebsmodi, Aufgabenbriefings, Review-Kriterien und Qualitaetssicherung.

## Grundidee

Professionelle Agenten brauchen mehr als eine Rollenbeschreibung. Sie benoetigen stabile Verhaltensregeln, klare Grenzen, nachvollziehbare Entscheidungen und pruefbare Ergebnisse.

Das Framework trennt deshalb drei Ebenen:

- Constitution: dauerhafte Grundregeln fuer Verhalten, Nachvollziehbarkeit und Eskalation.
- Mode: fachlicher Betriebsmodus, zum Beispiel Aerospace, AI Assurance, Software Engineering oder Research.
- Task Briefing: konkrete Aufgabe mit Kontext, Eingaben, Grenzen, Akzeptanzkriterien und Ausgabeformat.

Diese Trennung macht Agenten leichter wartbar, vergleichbar und reviewbar.

## Modulares Konzept

Die Repository-Struktur ist bewusst einfach gehalten:

```text
docs/       Grundregeln, Betriebsmodi, Entscheidungslogik und Prompt-Muster
templates/  Wiederverwendbare Vorlagen fuer Rollen, Briefings und Reviews
examples/   Beispielkonfigurationen fuer typische Agenten
tests/      Checklisten fuer Prompt-Qualitaet und Konsistenzpruefung
```

Jedes Modul soll einzeln nutzbar sein. Ein Team kann beispielsweise nur den Software-Engineering-Modus verwenden oder Aerospace Mode und AI Assurance Mode in einem strengeren Review-Prozess kombinieren.

## Zielgruppen

Das Framework richtet sich an:

- Engineering-Teams, die KI-Agenten in Entwicklungsprozesse integrieren.
- Safety- und Assurance-Verantwortliche, die nachvollziehbare Agentenarbeit benoetigen.
- Aerospace- und Systems-Engineering-Teams mit hohen Anforderungen an Reviewbarkeit.
- Governance-, Risk- und Compliance-Funktionen, die Agentenverhalten dokumentieren wollen.
- Research-Teams, die Quellenlage, Unsicherheit und Schlussfolgerungen sauber trennen muessen.

## Erste Nutzung

1. `docs/FJOLNIR_CONSTITUTION.md` lesen und als verbindliche Grundlage uebernehmen oder projektspezifisch anpassen.
2. Einen Betriebsmodus aus `docs/` auswaehlen.
3. Mit `templates/agent_role_template.md` eine Agentenrolle definieren.
4. Mit `templates/task_briefing_template.md` eine konkrete Aufgabe beschreiben.
5. Das Ergebnis mit `tests/prompt_quality_checklist.md` und `tests/consistency_review.md` pruefen.
6. Bei Bedarf ein Beispiel aus `examples/` als Startpunkt verwenden.

## Roadmap

### Kurzfristig

- Inhalte der Betriebsmodi fachlich schaerfen.
- Einheitliche Terminologie fuer Constitution, Mode, Role und Briefing definieren.
- Review-Checklisten um konkrete Bewertungskriterien erweitern.

### Mittelfristig

- Beispielagenten fuer weitere Governance- und Engineering-Szenarien ergaenzen.
- Versionierte Prompt-Artefakte und Aenderungsregeln einfuehren.
- Minimalen Prozess fuer Agentenfreigabe und periodische Revalidierung beschreiben.

### Langfristig

- Mapping zu relevanten Standards und Normen ausarbeiten.
- Testbare Qualitaetskriterien fuer Agentenverhalten definieren.
- Referenzprozess fuer auditierbare Agentenarbeit in regulierten Umgebungen erstellen.

## Status

Initiale Projektstruktur. Die Inhalte sind als ernsthafte Arbeitsgrundlage gedacht, muessen aber vor produktiver oder regulierter Nutzung projektspezifisch geprueft und erweitert werden.

## TODO

- Projektlizenz final festlegen.
- Verantwortliche Rollen fuer Pflege und Review definieren.
- Erste reale Anwendung mit einem Pilot-Agenten dokumentieren.
