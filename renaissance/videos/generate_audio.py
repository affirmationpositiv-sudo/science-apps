#!/usr/bin/env python3
"""Generate TTS audio for Renaissance videos"""
import subprocess, os, sys

voice = "de-DE-FlorianMultilingualNeural"
out_dir = os.path.dirname(os.path.abspath(__file__))

scripts = {
    "01_renaissance_intro": """Stell dir vor, du wachst morgens auf und fühlst dich nicht mehr wie ein Gefangener deiner eigenen Gewohnheiten. Stell dir vor, du hast etwas gefunden, das dich nicht bremst, sondern trägt. Das ist Renaissance.

Die meisten Ansätze gegen Pornografie-Sucht funktionieren nicht. Blocker-Apps? Du findest immer einen Weg drum herum. Scham und Schuld? Die machen alles nur schlimmer. Reine Enthaltsamkeit? Das ist wie eine Diät zu machen, ohne zu lernen, wie man kocht. Irgendwann fällst du zurück.

Renaissance ist anders. Wir sagen nicht: Hör auf damit. Wir sagen: Werde zu jemandem, für den das kein Thema mehr ist. Der Unterschied ist fundamental. Wir ersetzen die Leere nicht mit Verboten, sondern mit echtem Wachstum. Mit Skills, die dich stärker machen. Mit einem KI-Coach, der immer für dich da ist. Mit einer Community, die dich trägt.

Du startest mit einem kostenlosen Kennenlerngespräch. Dann bekommst du Zugang zu unserem 12-Wochen-Programm. Jede Woche ein neues Modul. Skills, die du wirklich lernen kannst. Egal ob Musik, Sport, Programmieren oder eine Sprache. Du baust etwas auf, während die Sucht von alleine verschwindet.

Dein persönlicher KI-Coach ist 24 Stunden am Tag, 7 Tage die Woche für dich da. Er kennt deine Fortschritte, erinnert dich an deine Ziele und gibt dir genau den Push, den du brauchst. Ohne zu verurteilen. Dazu kritisches Feedback von Jason, unserem Qualitäts-Chef. Und Motivation von Yesar, deinem persönlichen Coach.

Das alles beginnt mit einem einzigen Schritt: Einem kostenlosen Gespräch. Keine Verpflichtung. Kein Druck. Nur ein ehrliches Gespräch darüber, wo du stehst und wo du hinwillst. 30 Minuten, die dein Leben verändern können. Buche jetzt deinen Termin auf unserer Seite.""",

    "02_warum_dieser_ansatz": """Lass mich dir eine ehrliche Frage stellen: Wie oft hast du schon versucht, mit Pornografie aufzuhören? Wie viele Methoden hast du ausprobiert? Wie oft hast du dir geschworen: Dieses Mal schaffe ich es. Und bist dann doch wieder zurückgefallen?

Weißt du, warum das passiert? Weil die meisten Methoden von außen kommen. Sie sagen dir, was du NICHT tun sollst. Aber das Gehirn funktioniert nicht so. Wenn ich dir sage: Denk nicht an einen rosa Elefanten, woran denkst du dann? Genau. Verbot erzeugt Widerstand. Widerstand erzeugt Scham. Scham erzeugt noch mehr Konsum. Es ist eine Abwärtsspirale.

Renaissance dreht die Spirale um. Statt zu fragen: Was muss ich aufgeben, fragen wir: Was willst du werden? Wir haben die besten Erkenntnisse aus 34 Büchern über Psychologie, Gewohnheiten, Disziplin und persönliches Wachstum in ein System gegossen, das für dich arbeitet. Nicht gegen dich.

Cialdini, Kahneman, James Clear, Cal Newport. Die klügsten Köpfe der Verhaltenspsychologie. Wir haben ihre Erkenntnisse mit modernster KI-Technologie kombiniert. Dein persönlicher KI-Coach kennt dich besser als jede App. Jason, unser Qualitäts-Chef, lässt keine Ausreden durchgehen. Und Yesar sorgt dafür, dass du am Ball bleibst.

12 Wochen. Ein Programm, das dich fordert, aber nicht überfordert. Skills, die du wirklich lernen kannst. Eine Community, die genau weiß, wie du dich fühlst. Und ein Coach, der nur eines will: Dass du es schaffst.

Buche jetzt dein kostenloses Erstgespräch. 30 Minuten. Kein Druck. Nur ein ehrliches Gespräch darüber, ob Renaissance das Richtige für dich ist. Der Link wartet unten.""",

    "03_so_startest_du": """Du hast dich entschieden. Du willst etwas ändern. Aber du fragst dich: Wie genau läuft das jetzt ab? Hier ist dein Fahrplan für die ersten 7 Tage.

Alles beginnt mit deinem kostenlosen Erstgespräch. 30 Minuten mit einem echten Coach. Du erzählst deine Geschichte. Wir hören zu. Und dann schauen wir gemeinsam, ob Renaissance zu dir passt. Wenn ja, bekommst du sofort Zugang zur Plattform.

Du wählst deinen ersten Skill. Gitarre, Calisthenics, Programmieren, eine Sprache. Was immer dich antreibt. Dein KI-Coach hilft dir, den perfekten Einstieg zu finden. Keine Angst vor Fehlern. Jeder Meister war mal Anfänger.

Tägliche Quests. Kurze, machbare Aufgaben. 10 Minuten Meditation. 15 Minuten am Skill arbeiten. Dankbarkeitstagebuch. Der KI-Coach erinnert dich, Jason fordert dich, Yesar feiert dich. Das System trägt dich durch die ersten Tage.

Nach einer Woche hast du schon mehr geschafft als viele in einem Monat. Du hast eine neue Gewohnheit aufgebaut. Du hast deinen ersten richtigen Skill gelernt. Und das Beste: Der Drang, in alte Muster zurückzufallen, wird schon schwächer. Nicht weil du kämpfst, sondern weil du wächst.

Der erste Schritt ist immer der schwerste. Aber du musst ihn nicht alleine gehen. Klick auf den Link, buche dein Gespräch, und lass uns loslegen."""
}

for name, text in scripts.items():
    out_path = os.path.join(out_dir, f"{name}.mp3")
    print(f"Generating {name}...", end=" ", flush=True)
    subprocess.run([
        "edge-tts", "--voice", voice,
        "--rate", "+5%",
        "--pitch", "+0Hz",
        "--text", text,
        "--write-media", out_path
    ], capture_output=True, timeout=120)
    size = os.path.getsize(out_path)
    print(f"✅ {size/1024:.0f} KB")

print("\n✅ ALLE 3 AUDIOS FERTIG")
