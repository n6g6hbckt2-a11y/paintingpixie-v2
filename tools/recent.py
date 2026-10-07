# -*- coding: utf-8 -*-
"""Where Kat has painted recently (from her travel log, June to October 2026).
Update PERIOD and the lists as new events happen."""
PERIOD = "June to October 2026"
MACS = ("Macs Farm, near Ditchling", 4)
RECENT = {
 "face-painter-brighton.html": [("Brighton", 4), MACS],
 "face-painter-crawley.html": [("Crawley", 2)],
 "face-painter-guildford.html": [("Guildford", 2)],
 "face-painter-worthing.html": [("Worthing", 2)],
 "face-painter-haywards-heath.html": [("Haywards Heath", 1), MACS],
 "face-painter-burgess-hill.html": [MACS],
 "face-painter-lewes.html": [("Lewes", 1), MACS],
 "face-painter-west-sussex-villages.html": [("Henfield", 1), ("Upper Beeding", 1), ("Small Dole", 1)],
 "face-painter-south-downs.html": [("Petworth", 2)],
 "face-painter-horsham.html": [("New House Farm, Horsham", 1)],
 "face-painter-sussex.html": [("Brighton", 4), MACS, ("Crawley", 2), ("Worthing", 2), ("Petworth", 2), ("Haywards Heath", 1), ("Lewes", 1),
                              ("Eastbourne", 1), ("Henfield", 1), ("Upper Beeding", 1), ("Small Dole", 1), ("New House Farm, Horsham", 1)],
 "face-painter-surrey.html": [("Guildford", 2), ("Croydon", 1), ("Baker Street, London", 1)],
}

# Booked events still to come, from Kat's travel log (updated 7 Oct 2026). (place, date, local page it also shows on)
COMING_UP = [
 ("Portslade", "10 October", "face-painter-brighton.html"),
 ("Putney, London", "18 October", "face-painter-surrey.html"),
 ("Sutton", "24 October", "face-painter-surrey.html"),
 ("Good Hotel, London", "30 October", None),   # same booking as "Putney 30.10" in Kat's log
 ("Kingswood", "31 October", "face-painter-surrey.html"),
 ("Kingsfold, near Horsham", "31 October", "face-painter-horsham.html"),
]
