# -*- coding: utf-8 -*-
"""Party venue guides on the town pages: halls and venues parents can hire, with a link to each venue's own site.
Researched 10 Oct 2026 (sources in the "Venue outreach emails" doc). Outreach emails ask each venue to confirm face
painting is welcome and to recommend Kat back.

Each venue: (name, where, one practical fact, link or None, flags)
  flags: 'painted' = Kat has painted here (only when Kat has said so)
         'partner' = the venue recommends Kat / links back (set when they reply; shows a badge)
Only add a link we have seen on the venue's or council's own site. Facts must come from the venue's own pages."""

HIRE = {
    'face-painter-crawley.html': dict(
        h='Halls and party venues to book in Crawley',
        lede='Need somewhere to hold it? These are places Crawley families book for birthdays.',
        venues=[
            ('Neighbourhood community centres', 'Across Crawley', 'Every neighbourhood has one, run by the council and booked online.',
             'https://crawley.gov.uk/culture/sport-and-leisure/community-centres/community-centre-information', ''),
            ('Friary Hall', 'Town centre', 'Church hall hire right in the middle of town.',
             'https://www.crawleycatholic.church/church-and-hall-hire-1', ''),
            ("Clip 'n Climb Crawley", 'Climbing centre', 'Climbing parties, with exclusive hire of the whole centre for bigger groups.',
             'https://crawley.clipnclimb.co.uk/exclusivehire/', ''),
            ('Crawley Town Community Foundation', 'Broadfield Stadium', 'Birthday parties at the town’s football stadium.',
             'https://www.ctcommunityfoundation.com/other-services-1', ''),
        ]),
    'face-painter-haywards-heath.html': dict(
        h='Village halls around Haywards Heath',
        lede='Mid Sussex is full of good halls. A few within easy reach of town:',
        venues=[
            ("Queen's Hall, Cuckfield", 'Cuckfield', 'A council hall with a children’s party rate.',
             'https://cuckfield.gov.uk/hall-hire/queens-hall', ''),
            ('Cuckfield Village Hall', 'Cuckfield', 'Has a secure garden, handy for outdoor games in summer.',
             'https://www.cuckfield.gov.uk/hall-hire/cuckfield-village-hall', ''),
            ('King Edward Hall', 'Lindfield', 'The village hall in the middle of Lindfield.', None, ''),
            ('Scaynes Hill Millennium Village Centre', 'Scaynes Hill', 'A village centre a few minutes east of town.', None, ''),
            ('Haywards Heath Town Hall', 'Town centre', 'Rooms for hire in the middle of town.',
             'https://www.haywardsheath.gov.uk/town-hall', ''),
        ]),
    'face-painter-burgess-hill.html': dict(
        h='Somewhere to hold a Burgess Hill party',
        lede='The Town Council runs several halls, and there are good options in the villages too.',
        venues=[
            ('Cyprus Hall', 'Town centre', 'Room for 150, so whole-class parties fit easily.',
             'https://www.burgesshill.gov.uk/leisure-tourism/leisure-facilities/halls-for-hire/', ''),
            ("St Andrew's Community Centre", 'Burgess Hill', 'Two halls, the Rider Hall and the Youth Centre Hall, so you can pick the size.',
             'https://www.burgesshill.gov.uk/leisure-tourism/leisure-facilities/halls-for-hire/', ''),
            ('Sidney West Sports & Community Centre', 'Burgess Hill', 'A Town Council sports and community centre.',
             'https://www.burgesshill.gov.uk/leisure-tourism/leisure-facilities/halls-for-hire/', ''),
            ('Adastra Hall', 'Hassocks', 'The village hall in Hassocks, just south of town.', None, ''),
            ('The Macs Farm', 'Ditchling', 'A farm with open days and family events below the Downs.', None, 'painted'),
        ]),
    'face-painter-reigate.html': dict(
        h='Halls to hire in Reigate and Redhill',
        lede='Booking a room is usually the first job. Three to start with:',
        venues=[
            ('Woodhatch Community Centre', 'Woodhatch, Reigate', 'Rooms for up to 100, with a kitchen for self-catering.',
             'https://surreyca.org.uk/community-halls/woodhatch-community-centre/', ''),
            ('Reigate & Redhill YMCA Sport & Community Centre', 'Princes Road, Redhill', 'Halls and an activity room with plenty of space.',
             'https://surreyca.org.uk/community-halls/reigate-and-redhill-ymca-sport-and-community-centre/', ''),
            ('Reigate Hill Golf Club', 'Reigate Hill', 'Function suites and a terrace for family parties and christenings.',
             'https://www.reigatehillgolfclub.co.uk/events/parties-events.html', ''),
        ]),
    'face-painter-worthing.html': dict(
        h='Worthing venues for parties and celebrations',
        lede='From a manor house with barns to the local community halls:',
        venues=[
            ('Field Place Manor House & Barns', 'Durrington', 'Barns, gardens, a children’s play area and free parking.',
             'https://www.southdownsleisure.co.uk/?p=536', ''),
            ('Durrington Community Centre', 'Romany Road', 'The community centre for Durrington.', 'https://durringtoncc.wordpress.com/', ''),
            ('Findon Village Hall', 'Findon', 'The village hall just north of Worthing, booked through the parish council.',
             'https://findonparishcouncil.gov.uk/i-want-to/book-the-village-hall/', ''),
            ("West Tarring Young People's Club", 'Tarring High Street', 'A community building in the old village of Tarring.', 'https://wtyphub.org/', ''),
        ]),
}

NOTE = ('Links go to each venue’s own website. When you book, check the venue’s rules for entertainers. Kat brings her own '
        'table and skin-safe paints and packs everything away within your hire time.')

CSS = '''
.loc-hire .hire{list-style:none;padding:0;margin:18px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.loc-hire .hire li{background:rgba(255,255,255,.06);border:1px solid rgba(201,162,77,.35);border-radius:12px;padding:16px 18px;text-align:left}
.loc-hire.band-light .hire li{background:#fff;border-color:rgba(0,0,0,.08)}
.loc-hire .hire b{display:block;font-family:Fraunces,serif;font-weight:400;font-size:19px}
.loc-hire .hire i{display:block;font-style:normal;font-size:13px;opacity:.75;margin:2px 0 6px}
.loc-hire .hire a{display:block;margin-top:6px;font-weight:800;white-space:nowrap}
.loc-hire .tag{display:inline-block;font-size:12px;font-weight:800;padding:2px 8px;border-radius:20px;background:var(--gold,#c9a24d);color:#1a1420;margin:0 6px 6px 0}
.loc-hire .tag.partner{background:#2f8f5b;color:#fff}
.loc-hire .vnote{font-size:14px;opacity:.8;max-width:760px;margin:16px 0 0}
'''
