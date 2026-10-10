# -*- coding: utf-8 -*-
"""Per-town headings and block order for the town pages, so no two pages share the same structure or headings.
Keys: order (list of blocks), and headings for venues, tiles, seasons, places, events, gallery, villages, towns,
reviews, hoods, faq, prices. Check with tools/check_unique.py (target: no pair of town pages shares over 20%)."""

HEADS = {
    'face-painter-horsham.html': dict(
        gallery='What Horsham children ask for', reviews='Horsham parents on Kat', prices='Horsham party prices:',
        hoods='Roffey, Southwater, Warnham and the rest of Horsham', faq='Horsham party questions'),
    'face-painter-crawley.html': dict(
        venues='Where Crawley parties happen', reviews='What Crawley families say', prices='Crawley prices:',
        hoods='From Ifield to Maidenbower', faq='Crawley questions'),
    'face-painter-haywards-heath.html': dict(
        seasons='Haywards Heath through the year', venues='Halls, parks and gardens in Haywards Heath',
        reviews='Mid Sussex mums and dads on Kat', prices='Haywards Heath prices:',
        hoods='Lindfield, Cuckfield, Ardingly and more', faq='Before you book in Haywards Heath'),
    'face-painter-burgess-hill.html': dict(
        reviews='Burgess Hill reviews', prices='Prices for Burgess Hill parties:',
        hoods='Hassocks, Ditchling, Hurstpierpoint and around', faq='Burgess Hill: your questions answered'),
    'face-painter-east-grinstead.html': dict(
        order=['letter', 'events', 'venues:list', 'postcard', 'gallery', 'recent', 'prices', 'hoods', 'reviews', 'faq'],
        gallery='Designs East Grinstead loves', reviews='Families near East Grinstead', prices='East Grinstead prices:',
        hoods='Forest Row, Felbridge, Lingfield and beyond', faq='East Grinstead FAQs'),
    # seaside layout: postcard first, venue list, then the year
    'face-painter-worthing.html': dict(
        order=['intro:quote', 'postcard', 'venues:list', 'seasons', 'reviews', 'recent', 'prices', 'hoods', 'faq'],
        venues='By the sea and in the halls: Worthing spots', seasons='Worthing, season by season',
        reviews='Kind words from the coast', prices='Worthing prices:',
        hoods='Goring, Ferring, Durrington and along the coast', faq='Worthing party FAQs'),
    'face-painter-brighton.html': dict(
        order=['intro:quote', 'venues:chips', 'tiles', 'reviews', 'postcard', 'recent', 'prices', 'hoods', 'faq'],
        tiles='How a Brighton event comes together', venues='Brighton venues Kat loves', reviews='Brighton guests on Kat',
        prices='Brighton prices:', hoods='Hove, Kemptown, Rottingdean and the rest of the city', faq='Brighton & Hove questions'),
    'face-painter-lewes.html': dict(
        order=['story', 'postcard', 'places', 'recent', 'prices', 'reviews', 'hoods', 'faq'],
        reviews='What people say in and around Lewes', prices='Lewes prices:',
        hoods='Lewes and the villages below the Downs', faq='Lewes questions, answered'),
    'face-painter-south-downs.html': dict(
        order=['letter', 'venues:list', 'postcard', 'gallery', 'events', 'reviews', 'recent', 'prices', 'hoods', 'faq'],
        gallery='Favourites in Midhurst and Petworth', reviews='Reviews from the South Downs', prices='South Downs prices:',
        hoods='Easebourne, Fernhurst, Graffham and more', faq='Midhurst & Petworth questions'),
    'face-painter-west-sussex-villages.html': dict(
        order=['intro:quote', 'villages', 'reviews', 'postcard', 'recent', 'prices', 'hoods', 'faq'],
        villages='West Sussex villages I visit', reviews='Village families on Kat', prices='Village party prices:',
        hoods='Partridge Green, Cowfold, Slinfold and more', faq='Village party questions'),
    'face-painter-guildford.html': dict(
        order=['story', 'places', 'reviews', 'postcard', 'recent', 'prices', 'faq', 'hoods'],
        reviews='Guildford reviews', prices='Guildford prices:',
        hoods='Merrow, Burpham, Shalford and around Guildford', faq='Guildford questions'),
    # planner layout: practical first (where, questions), the year later
    'face-painter-reigate.html': dict(
        order=['intro:split', 'venues:chips', 'faq', 'reviews', 'seasons', 'recent', 'prices', 'hoods', 'postcard'],
        venues='Planning a Reigate party: where to hold it', faq='Reigate & Redhill planning questions',
        seasons='When Reigate books Kat', reviews='Reigate and Redhill reviews', prices='Reigate prices:',
        hoods='Redhill, Merstham, Earlswood and nearby'),
    'face-painter-dorking.html': dict(
        order=['intro:quote', 'venues:cards', 'tiles', 'postcard', 'faq', 'recent', 'prices', 'reviews', 'hoods'],
        tiles='The Dorking party guide', venues="Dorking's best party spots", faq='Dorking questions',
        reviews='Dorking reviews', prices='Dorking prices:', hoods='Westcott, Brockham, Capel and the Mole Valley'),
    'face-painter-surrey-villages.html': dict(
        order=['intro:quote', 'postcard', 'villages', 'faq', 'recent', 'prices', 'reviews', 'hoods'],
        villages='Surrey villages Kat visits', faq='Surrey village questions', reviews='Surrey village reviews',
        prices='Surrey village prices:', hoods='Ewhurst, Ashtead, Bookham and more'),
    'face-painter-sussex.html': dict(
        order=['intro:quote', 'towns', 'reviews', 'recent', 'prices', 'postcard', 'faq'],
        towns='Sussex towns with their own page', reviews='Sussex reviews', faq='Sussex questions', prices='Sussex prices:'),
    'face-painter-surrey.html': dict(
        order=['intro:quote', 'postcard', 'towns', 'recent', 'prices', 'faq', 'reviews'],
        towns='Surrey towns Kat covers', reviews='Surrey reviews', faq='Surrey questions', prices='Surrey prices:'),
}
