# -*- coding: utf-8 -*-
"""Unique content for each location page of the draft site.
Each page picks its own layout ("tpl") and accent colour so no two feel the same.
Personal notes are written in Kat's voice; ones marked KAT-CHECK are drafted and Kat should confirm."""

PAGES = {

"face-painter-horsham.html": dict(
 tpl="letter", acc="#FF4FA3", hero=("../img/v2-hero.webp", "60% 30%"),
 kicker="Home turf", eyebrow="Horsham, West Sussex",
 letter=[
  "Horsham is home. I live here, my daughter grew up running round Horsham Park, and it's where The Painting Pixie started: painting a butterfly on her cheek at a birthday party because nobody else was free that day.",
  "So when I pack the car for a Horsham booking it doesn't feel like work. I know which halls have good light, where to park near the Carfax on a Saturday, and which parks get busy on a sunny Sunday. I recently painted at the Eats & Beats Festival at New House Farm on the edge of town, and half the queue were families I'd met at school gates and birthday parties.",
  "If you're planning something in Horsham, I'd love to be part of it.",
 ],
 signoff="Kat x",
 quote="There's something special about bringing a bit of magic to celebrations in my own home town.",
 venues_title="My Horsham party map",
 venues=[
  ("Horsham Park", "Picnic parties by the pond, with The Pavilions in the Park next door if the weather turns."),
  ("Denne Park & Hills Farm", "Garden parties and family get-togethers on the south side of town."),
  ("Broadbridge Heath", "The leisure centre and community halls for bigger, rain-proof birthdays."),
  ("Southwater Country Park", "Lake, beach and play areas, a favourite for summer parties."),
  ("Chesworth Farm", "A lovely green spot for relaxed family celebrations."),
  ("The Carfax", "Right in the centre, where the town's fêtes and markets come together."),
 ],
 events_title="Where you'll find me in Horsham",
 events=[
  ("Eats & Beats Festival", "New House Farm", "Food, music and a very long face-painting queue. I loved it."),
  ("School summer fairs", "June & July", "Roffey, Holbrook, Southwater, Broadbridge Heath and more."),
  ("Halloween & bonfire parties", "October & November", "Pumpkins, skulls and glittery bats."),
  ("Christmas fairs", "December", "Snowflakes, reindeer and sparkly elves."),
 ],
 hoods=["Roffey", "Holbrook", "Broadbridge Heath", "Southwater", "Warnham", "Mannings Heath", "Christ's Hospital", "Littlehaven", "Kilnwood Vale", "Colgate", "Rusper", "Barns Green"],
 designs=["Unicorns", "Tigers", "Spider-webs & superheroes", "Glitter butterflies"],
 gallery=["unicorn-birthday-face-paint-girl-horsham-festival.webp", "tiger-face-paint-boy-laughing-horsham-festival.webp", "leopard-print-face-paint-girl-horsham-festival.webp", "blue-dragon-face-paint-girl-laughing-horsham.webp"],
 faqs=[
  ("Do you charge travel within Horsham?", "No. Horsham is home, so there's no travel charge anywhere in town or the surrounding villages."),
  ("Can you paint at a party in Horsham Park?", "Yes. Outdoor parties are lovely. I bring a gazebo-friendly set-up and just need a table, two chairs and a bit of shade."),
  ("How quickly can you confirm a Horsham date?", "Usually the same day. Message me with the date and roughly how many children and I'll tell you straight away."),
  ("Do you do school fairs in Horsham?", "Yes, school and PTA summer fairs are some of my favourite bookings. Book early, as June weekends go first."),
 ],
),

"face-painter-crawley.html": dict(
 tpl="guide", acc="#2FD4C4", hero=("../img/n-tiger-boy-party.webp", "50% 22%"),
 kicker="A familiar face", eyebrow="Crawley, West Sussex",
 intro=[
  "Crawley isn't just somewhere I cover. It's where I am four or five days every week: I teach GCSE and A level here, so I've spent years getting to know Crawley families, and there's a good chance I already know someone at your party.",
  "What I love about Crawley is how much happens in its neighbourhoods. Every area has its own parade, its own community centre and its own crowd, and the parties are big, busy and brilliant fun. A long queue of excited children is exactly my kind of afternoon.",
  "It's only about 10 minutes from my home in Horsham, so there's no travel charge anywhere in Crawley.",
 ],
 quote="I'm in Crawley four or five days a week. It isn't a new patch for me. It's home turf.",
 tiles=[
  ("Where", "Tilgate Park on a sunny weekend, neighbourhood community centres for rain-proof birthdays, and K2 Crawley for big sports-hall parties."),
  ("When", "Spring birthdays, summer fun days in Goffs Park, events like Eats & Beats near Crawley, school fairs, Halloween discos and Christmas parties."),
  ("What", "Fast, bold designs for big groups: tigers, superheroes, footballs and unicorns that keep the queue moving."),
 ],
 venues=[
  ("Tilgate Park", "Lake walks, the nature centre and plenty of picnic space."),
  ("Goffs Park", "The lake and miniature railway make it a family favourite."),
  ("K2 Crawley", "Sports halls that suit big, busy birthday parties."),
  ("Worth Park", "Restored gardens in Pound Hill, lovely for summer gatherings."),
  ("Memorial Gardens", "Right by the town centre and County Mall."),
  ("Neighbourhood community centres", "Every area has one, and they're perfect for winter parties."),
 ],
 hoods=["Three Bridges", "Pound Hill", "Maidenbower", "Furnace Green", "Tilgate", "Broadfield", "Bewbush", "Ifield", "Langley Green", "Northgate", "Southgate", "Forge Wood", "Copthorne", "Ifield Green"],
 faqs=[
  ("Is there a travel charge for Crawley?", "No. Crawley is about 10 minutes from my home in Horsham, so there's no travel charge anywhere in the town, from Ifield and Bewbush to Three Bridges, Pound Hill and Maidenbower."),
  ("Can you handle a big class party in Crawley?", "Yes. Whole-class parties are common in Crawley. For 25 or more children I'd suggest the 3-hour Ultimate Sparkle so nobody misses out."),
  ("Do you paint at Tilgate Park or Goffs Park?", "Yes. I paint at outdoor parties all over Crawley; I just need a table, two chairs and a little shade."),
  ("Are you DBS checked?", "Yes. I hold the same DBS clearance I need for teaching, plus full public liability insurance."),
  ("Do you cover hen parties in Crawley too?", "Absolutely. Glitter, gems and grown-up designs start from £150."),
 ],
),

"face-painter-haywards-heath.html": dict(
 tpl="seasons", acc="#A77BFF", hero=("../img/n-unicorn-girl-party-hall.webp", "50% 22%"),
 kicker="One of my regulars", eyebrow="Haywards Heath, Mid Sussex",
 intro=[
  "Haywards Heath is one of my most regular areas. It has that lovely mix of town and village: busy birthday parties in the centre, then ten minutes later I'm on Lindfield Common or tucked away in a Cuckfield garden.",
  "What I love most is the countryside on the doorstep. Driving in past the fields towards Borde Hill or out to the showground at Ardingly always feels like the start of a good day.",
 ],
 quote="Ten minutes from a town-centre party to a village green. That's Haywards Heath for me.",
 photo="../img/n-crown-girl-blue-sky.webp",
 seasons=[
  ("Spring", "Easter fairs, spring birthdays and the first garden parties of the year around Victoria Park."),
  ("Summer", "School summer fairs, village fêtes in Lindfield and Cuckfield, and big family days near Ardingly."),
  ("Autumn", "Back-to-school birthdays, then pumpkins, skulls and spooky Halloween parties."),
  ("Winter", "Christmas fairs, festive class parties and sparkly snowflake designs."),
 ],
 venues=[
  ("Victoria Park", "Right in the middle of town and great for summer parties."),
  ("Beech Hurst Gardens", "Gardens with a miniature railway that children love."),
  ("Lindfield Common", "The pond and the green make it a picture-perfect setting."),
  ("Cuckfield", "Village halls and gardens, a short hop from town."),
  ("Borde Hill Garden", "A beautiful setting for family events and celebrations."),
  ("The Dolphin Leisure Centre", "A dry, roomy option for bigger birthdays."),
 ],
 hoods=["Lindfield", "Cuckfield", "Ardingly", "Scaynes Hill", "Wivelsfield", "Bolney", "Ansty", "Balcombe", "Lindfield Common", "Franklands Village"],
 faqs=[
  ("Do you travel to Lindfield and Cuckfield?", "Yes, all the time. There's no extra charge for the villages around Haywards Heath."),
  ("Can you paint at a village fête?", "Yes. Fêtes are some of my favourite bookings. I can work as a paid stall or for a set fee, whichever suits your committee."),
  ("What do I need to provide?", "A table, two chairs and somewhere with good light. Outdoors, a little shade helps the paint and the children."),
  ("How far ahead should I book?", "Summer weekends in Mid Sussex go weeks ahead, so get in touch as soon as you have a date."),
 ],
),

"face-painter-burgess-hill.html": dict(
 tpl="story", acc="#FF9A3C", hero=("LIVE:burgess-hill.webp", "50% 50%"),
 kicker="Down the road", eyebrow="Burgess Hill, Mid Sussex",
 story=[
  "Burgess Hill always feels like a proper community town to me. Everyone seems to know everyone, and word travels fast. More than one of my bookings here has come from a mum who saw her friend's child walk out of a party with a tiger face.",
  "I've recently been out at Macs Farm near Ditchling, just down the road, and I love that you can be at a town-centre birthday in the morning and out under the South Downs by the afternoon.",
  "Whether it's a party at The Triangle, a garden do in Keymer or a school fair in Hassocks, I'll bring the same fast, careful painting I'd want at my own daughter's party.",
 ],
 quote="One tiger face at a Burgess Hill party, and three more bookings by the end of the week.",
 places_title="Places I love round here",
 places=[
  ("The Triangle", "Big, dry and made for birthday parties when the weather's against you.", "../img/n-tiger-girl-closeup.webp"),
  ("St John's Park", "Right in the middle of town, perfect for summer picnics and fun days.", "../img/v2-fairy.webp"),
  ("Ditchling & the Downs", "Macs Farm, Ditchling Common and the hills on the skyline.", "../img/n-crown-girl-blue-sky.webp"),
 ],
 hoods=["Hassocks", "Keymer", "Ditchling", "Wivelsfield", "Hurstpierpoint", "Sayers Common", "Albourne", "World's End", "Victoria", "Hammonds Ridge"],
 faqs=[
  ("Do you cover Hassocks, Keymer and Ditchling?", "Yes. They're all close by and there's no extra travel charge."),
  ("Can you come to a party at The Triangle?", "Yes. Leisure centre parties work brilliantly. I just need a table near a plug-free corner with good light."),
  ("How many children can you paint in two hours?", "Up to 15 with the Classic Party. For bigger groups the 3-hour Ultimate Sparkle covers up to 25."),
  ("Do you paint grown-ups too?", "Yes. Hen dos, birthdays and festivals get glitter, gems and grown-up designs from £150."),
 ],
),

"face-painter-east-grinstead.html": dict(
 tpl="letter", acc="#4FB6FF", hero=("../img/v2-leopard-girl.webp", "50% 30%"),
 kicker="A town I fell for", eyebrow="East Grinstead, West Sussex",
 letter=[
  "I painted faces at an event in East Grinstead recently and came home completely charmed. The high street is a picture, with that long run of old timber-framed buildings, and the families were so friendly.",
  "It's a town with a lot of history, from the Bluebell Railway steaming in at the station to Ashdown Forest just down the road, and I love that a party here can feel like part of a story.",
  "If you're planning something in East Grinstead or the villages around it, I'd love to come back.",
 ],
 signoff="Kat x",
 quote="Old timber-framed streets, steam trains and the forest on the doorstep. East Grinstead has a bit of magic built in.",
 venues_title="Party spots around East Grinstead",
 venues=[
  ("East Court", "Lovely grounds and a classic spot for town events."),
  ("Mount Noddy", "The recreation ground for summer fun days and picnics."),
  ("Chequer Mead", "The arts centre, right in town."),
  ("Weir Wood Reservoir", "A beautiful backdrop on the edge of town."),
  ("Ashdown Forest", "Home of the Hundred Acre Wood, a short drive away."),
  ("Village halls", "Forest Row, Felbridge and Sharpthorne all have great ones."),
 ],
 events_title="When East Grinstead gets busy",
 events=[
  ("Spring & summer fairs", "May to July", "School and community fairs across town."),
  ("Family fun days", "Summer holidays", "Parks and village greens at their best."),
  ("Halloween parties", "October", "Spooky designs for the half-term crowd."),
  ("Christmas events", "December", "Festive fairs and class parties."),
 ],
 hoods=["Forest Row", "Felbridge", "Lingfield", "Dormansland", "Sharpthorne", "West Hoathly", "Turners Hill", "Crawley Down", "Ashurst Wood", "Dormans Park"],
 designs=["Steam-train cheeks", "Woodland animals", "Butterflies", "Dragons"],
 gallery=["green-dragon-face-paint-for-kids.webp", "butterfly-tiger-face-paint-for-sisters.webp", "pink-princess-crown-face-paint-with-butterfly-wing-cheek-design.webp", "gold-tiger-face-paint-for-boys.webp"],
 faqs=[
  ("Do you travel to East Grinstead from Horsham?", "Yes, it's an easy drive and I'm happy to come over for parties, fairs and events."),
  ("Do you cover Forest Row and Lingfield?", "Yes, along with Felbridge, Dormansland and the villages around Ashdown Forest."),
  ("Can you paint at a school fair?", "Yes. I can work as a paid stall or for a set fee, and I keep designs quick so the queue keeps moving."),
  ("Is the paint safe for sensitive skin?", "Yes. I use professional, cosmetic-grade face paints made for skin."),
 ],
),

"face-painter-worthing.html": dict(
 tpl="seasons", acc="#2FD4C4", hero=("LIVE:worthing-beach.webp", "50% 55%"),
 kicker="By the sea", eyebrow="Worthing, West Sussex",
 intro=[
  "Worthing bookings are the ones I secretly hope go on a bit, because it means I get to finish with a walk along the seafront. There's something about the pier, the beach huts and that big open sky that puts everyone in a good mood.",
  "From back-garden birthdays in Goring to seafront events and school fairs in Broadwater, Worthing parties have a lovely, relaxed seaside feel, and I bring designs to match: mermaids, sea creatures and sparkly scales go down a storm here.",
 ],
 quote="A party in Worthing, then chips on the seafront. That's a good Saturday.",
 photo="../img/n-lilac-flower-eye.webp",
 seasons=[
  ("Spring", "Easter fairs and the first seafront birthdays of the year."),
  ("Summer", "Beach-side parties, seafront events and school summer fairs across town."),
  ("Autumn", "Half-term parties and spooky Halloween designs."),
  ("Winter", "Christmas fairs, festive parties and sparkly snowflakes."),
 ],
 venues=[
  ("Worthing Pier & seafront", "Summer events with the sea as the backdrop."),
  ("Beach House Park", "Green space a stone's throw from the beach."),
  ("Splashpoint", "The seafront leisure centre for rain-proof parties."),
  ("Highdown Gardens", "Chalk gardens on the hill above Goring."),
  ("Steyne Gardens", "A classic spot right in the middle of town."),
  ("Community halls", "Broadwater, Durrington and Tarring all have lovely ones."),
 ],
 hoods=["Goring-by-Sea", "Ferring", "Broadwater", "Durrington", "Tarring", "Findon", "Lancing", "Sompting", "East Preston", "Angmering", "High Salvington"],
 faqs=[
  ("Do you travel to Worthing?", "Yes. I regularly come down to Worthing and the coast for parties and events."),
  ("Can you paint at a beach or seafront party?", "Yes. I just need a table, two chairs and a little shelter from sun and wind."),
  ("What designs are popular in Worthing?", "Mermaids, sea creatures and sparkly scales, plus all the classics: tigers, unicorns and superheroes."),
  ("Do you cover Goring, Ferring and Lancing?", "Yes, along with Findon, Durrington and the villages along the coast."),
 ],
),

"face-painter-brighton.html": dict(
 tpl="guide", acc="#FF4FA3", hero=("LIVE:brighton-palace-pier.webp", "50% 50%"), events_only=True,
 kicker="Bright lights", eyebrow="Brighton & Hove",
 title="Face Painter in Brighton &amp; Hove | Events, Hens &amp; Weddings | The Painting Pixie",
 desc="Insured, DBS-checked face painter and glitter artist for Brighton & Hove events: hen dos, weddings, festivals, Pride and corporate days. Get a quote from Kat.",
 sub="Glitter, face and body art for hen dos, weddings, festivals, Pride and corporate events across Brighton and Hove.",
 intro=[
  "Brighton is the place where nobody thinks a grown-up with a glittery face is unusual, and I love that. Some of my most creative bookings have been here, from rainbow designs at big celebrations to full glitter looks at hen dos.",
  "In Brighton I focus on events: hen weekends, weddings, festival and Pride days, brand launches and bigger family celebrations where there's a real crowd to paint. Smaller birthday parties are welcome too, so just get in touch and I'll let you know if I can fit yours in. I've recently been out at Macs Farm near Ditchling too, just a short drive away.",
 ],
 quote="In Brighton, the grown-ups queue for glitter as fast as the kids queue for tigers.",
 tiles=[
  ("Where", "Hotels and seafront venues, wedding venues across the city and the Downs, festival sites, parks and corporate spaces."),
  ("When", "Brighton Festival in May, summer on the seafront, Pride in August, then Halloween and Christmas events."),
  ("What", "Hen-do glitter, festival looks, body art, glitter tattoos and a glitter bar, plus a kids' corner for weddings and family events."),
 ],
 venues=[
  ("The seafront hotels", "Glitter and gems for hen dos before a big night out."),
  ("Brighton Pride", "Rainbow glitter and festival looks in August."),
  ("Preston Park", "Big summer events and community days."),
  ("Stanmer Park", "Festivals, fairs and outdoor celebrations on the edge of the city."),
  ("Hove Lawns", "Seafront events with a view of the West Pier."),
  ("Wedding venues on the Downs", "A kids' corner, or glitter for the whole wedding party."),
 ],
 hoods=["Hove", "Kemptown", "Hanover", "Preston Park", "Withdean", "Patcham", "Rottingdean", "Saltdean", "Portslade", "Moulsecoomb", "Woodingdean", "Ovingdean"],
 faqs=[
  ("Do you do hen parties in Brighton?", "Yes, lots. Glitter, gems and grown-up designs start from £150, and I can come to your house, Airbnb, venue or hotel."),
  ("Do you do children's birthday parties in Brighton?", "Yes, get in touch. In Brighton I mainly focus on events, weddings, hen dos and larger celebrations, but I'm happy to do parties when I can fit them in."),
  ("Can you paint at Pride or festival events?", "Yes. Rainbow designs, glitter and body art are a big part of what I do. Get in touch early for event dates."),
  ("Do you do corporate and brand events in Brighton?", "Yes. Staff days, launches and brand activations, with a glitter bar or glitter tattoos that look great in photos. Ask for a quote."),
 ],
),

"face-painter-lewes.html": dict(
 tpl="story", acc="#FF9A3C", hero=("../img/n-tiger-girl-closeup.webp", "50% 30%"),
 kicker="A town with a spark", eyebrow="Lewes, East Sussex",
 story=[
  "Lewes is a town that takes its celebrations seriously. Anywhere with a bonfire night famous across the country is a place that knows how to throw a party, and you can feel that everywhere: in the castle on the hill, the twisting lanes and the independent shops.",
  "I love bringing colour to celebrations here, whether that's a birthday near Landport Recreation Ground, a family day near Pells Pool or a special event in the shadow of Lewes Castle. I've recently been out at Macs Farm near Ditchling too, not far from Lewes at all.",
  "And come autumn, a Lewes Halloween party is one of the best bookings of my year.",
 ],
 quote="Any town with a bonfire night that famous knows how to throw a party.",
 places_title="Places I love in Lewes",
 places=[
  ("Lewes Castle", "Standing over the town since Norman times. A party view like no other.", "../img/n-adult-skull.webp"),
  ("Pells Pool", "The old lido, packed with families every summer.", "../img/n-lilac-flower-eye.webp"),
  ("Southover Grange Gardens", "Beautiful gardens in the middle of town for summer gatherings.", "../img/v2-sisters.webp"),
 ],
 hoods=["Kingston", "Barcombe", "Ringmer", "Glynde", "Iford", "Offham", "Newick", "Cooksbridge", "Southover", "Cliffe"],
 faqs=[
  ("Do you travel to Lewes?", "Yes. I regularly paint in Lewes and the villages around it."),
  ("Do you do Halloween and bonfire parties in Lewes?", "Yes. October and early November are very busy here, so book early."),
  ("Can you paint at a wedding near Lewes?", "Yes. Face painting and glitter keep little guests happy and grown-ups love it too."),
  ("Do you cover Ringmer and Barcombe?", "Yes, plus Kingston, Glynde and Newick."),
 ],
),

"face-painter-south-downs.html": dict(
 tpl="letter", acc="#9BE15D", hero=("../img/v2-sisters.webp", "50% 30%"),
 kicker="Worth the drive", eyebrow="Midhurst & Petworth", short="Midhurst & Petworth",
 letter=[
  "Midhurst and Petworth are a little further out for me, but I genuinely love the drive. Once you're through the lanes and the Downs open up around you, it feels like a day out before I've even unpacked my brushes.",
  "Both towns have a lovely, old-fashioned community feel. Petworth with its antique shops and the great house and park on the edge of town, Midhurst with the Cowdray ruins by the river. Village fêtes and garden parties out here are some of the prettiest I get to paint at.",
  "If you're planning something in the South Downs, I'll happily make the trip.",
 ],
 signoff="Kat x",
 quote="Once the Downs open up around me, it already feels like a day out.",
 venues_title="Party spots in the South Downs",
 venues=[
  ("Petworth Park", "Deer park and grand views on the edge of town."),
  ("Cowdray", "The Tudor ruins and parkland by Midhurst."),
  ("The Leconfield Hall, Petworth", "The town hall at the heart of Petworth."),
  ("The Grange Centre, Midhurst", "Midhurst's community hub."),
  ("Village greens", "Fittleworth, Easebourne and Graffham are all lovely."),
  ("Goodwood", "Big event days a short drive south."),
 ],
 events_title="When I'm out that way",
 events=[
  ("Summer fêtes", "June to August", "Village fêtes and flower shows across the Downs."),
  ("Petworth Festival", "Summer", "The town's arts festival brings everyone out."),
  ("Garden parties", "All summer", "Birthdays and weddings in beautiful gardens."),
  ("Christmas fairs", "December", "Festive designs for village fairs."),
 ],
 hoods=["Easebourne", "Fernhurst", "Cocking", "Graffham", "Tillington", "Fittleworth", "Duncton", "Lodsworth", "Stedham", "Byworth"],
 designs=["Woodland animals", "Fairies", "Floral cheeks", "Tigers"],
 gallery=["rainbow-butterfly-face-paint-for-sisters.webp", "unicorn-rainbow-face-paint-for-girls.webp", "tiger-eye-face-paint-design.webp", "pink-leopard-print-face-paint.webp"],
 faqs=[
  ("Do you travel as far as Midhurst and Petworth?", "Yes. It's a little further from Horsham, but I'm happy to make the trip for parties, fêtes and weddings."),
  ("Is there a travel charge?", "For longer trips I may add a small travel charge, and I'll always tell you up front."),
  ("Can you paint at a village fête?", "Yes, I can work as a paid stall or for a set fee."),
  ("Do you cover the villages around Midhurst?", "Yes, including Easebourne, Fernhurst, Cocking and Stedham."),
 ],
),

"face-painter-west-sussex-villages.html": dict(
 tpl="villages", acc="#E2BE7A", hero=("../img/v2-fairy.webp", "50% 25%"),
 kicker="Village life", eyebrow="The villages around Horsham", short="the villages around Horsham",
 intro=[
  "Some of my favourite bookings are in the villages around Horsham. Village parties have a different feel: the whole street turns up, grandparents come and sit by my table, and the children who've had their faces done run off to show everyone at the fête.",
  "Because I live in Horsham, these villages are on my doorstep. I know the halls, the greens and the fêtes, and I love driving out through the lanes on a summer Saturday.",
 ],
 quote="At a village party the whole street turns up, and grandparents pull up a chair by my table.",
 villages=[
  ("Billingshurst", "A busy village with a great community feel. Parties in the village halls and summer fun on the recreation ground."),
  ("Henfield", "A proper Sussex village, with fêtes on the common and garden parties all summer."),
  ("Steyning", "An old market town under the Downs, with a lovely high street and plenty of community events."),
  ("Storrington", "Village halls and greens at the foot of the Downs, great for summer birthdays."),
  ("Pulborough", "On the river Arun, close to Fishers Farm Park and the Brooks."),
  ("Southwater", "Right next to Horsham, with the country park lake for summer parties."),
 ],
 hoods=["Partridge Green", "West Chiltington", "Cowfold", "Ashington", "Bramber", "Upper Beeding", "Slinfold", "Rudgwick", "Barns Green", "Wisborough Green"],
 faqs=[
  ("Do you charge travel to the villages?", "No travel charge for the villages around Horsham. I'm only down the road."),
  ("Can you paint at our village fête?", "Yes. I can work as a paid stall or for a set fee, whichever suits your committee."),
  ("Do you work in village halls?", "Yes. I just need a table, two chairs and good light."),
  ("How early should we book a summer fête?", "As soon as you have the date. June and July Saturdays go first."),
 ],
),

"face-painter-guildford.html": dict(
 tpl="story", acc="#4FB6FF", hero=("../img/n-blue-monster-roar.webp", "50% 28%"),
 kicker="Art-trail memories", eyebrow="Guildford, Surrey",
 story=[
  "Guildford is somewhere I know well. You'll often find me painting at birthday parties near Stoke Park or in the town centre, as well as school fêtes, weddings and community events nearby.",
  "My favourite Guildford memory is joining the last Guildford Festival of the Arts on North Street. Painting in the middle of an art trail, with artists all around and families wandering from stall to stall, felt like the perfect fit for what I do.",
  "Guildford parties tend to be creative ones. Children here love choosing something a bit different, and I love being asked to invent a design on the spot.",
 ],
 quote="Painting in the middle of an art trail felt like the perfect fit for what I do.",
 places_title="Places I love in Guildford",
 places=[
  ("Stoke Park", "Huge open space and the lido, perfect for summer birthdays.", "../img/n-unicorn-girl-party.webp"),
  ("North Street", "Where I painted at the Guildford Festival of the Arts.", "../img/n-arm-glitter-swirl.webp"),
  ("The Castle grounds", "Gardens on the hill above the cobbled High Street.", "../img/n-crown-girl-blue-sky.webp"),
 ],
 hoods=["Merrow", "Burpham", "Onslow Village", "Stoughton", "Shalford", "Bramley", "Chilworth", "Wonersh", "Send", "Godalming"],
 faqs=[
  ("Do you travel to Guildford from Horsham?", "Yes. Guildford is one of my regular areas."),
  ("Can you paint at an arts or community festival?", "Yes. I've painted at the Guildford Festival of the Arts and love event days like that."),
  ("Do you cover Godalming and Shalford?", "Yes, plus Merrow, Burpham, Bramley and the villages around."),
  ("Do you paint adults at weddings?", "Yes. Glitter and gems are a big hit with grown-up guests."),
 ],
),

"face-painter-reigate.html": dict(
 tpl="seasons", acc="#A77BFF", hero=("../img/n-crown-girl-blue-sky.webp", "50% 22%"),
 kicker="Busy all year", eyebrow="Reigate & Redhill, Surrey",
 intro=[
  "Families around Reigate and Redhill keep me busy all year round. It's one of those areas where a booking at a birthday in Priory Park leads to a school fair in Redhill, then a christening in Merstham.",
  "I love the views here. Standing on Reigate Hill and looking out across the Weald, you can almost see all the way home to Horsham, and it always reminds me how close these towns really are.",
 ],
 quote="From the top of Reigate Hill you can almost see all the way home to Horsham.",
 photo="../img/n-tiger-boy-party.webp",
 seasons=[
  ("Spring", "Spring birthdays and Easter fairs, with Priory Park coming into its own."),
  ("Summer", "School fairs, garden parties and fun days across Reigate, Redhill and Merstham."),
  ("Autumn", "Half-term parties and Halloween discos."),
  ("Winter", "Christmas fairs and festive parties in town."),
 ],
 venues=[
  ("Priory Park", "The lake, the gardens and lots of space for summer parties."),
  ("Memorial Park, Redhill", "A central park with plenty of room for families."),
  ("Earlswood Lakes", "A peaceful spot just south of Redhill."),
  ("Reigate Hill & Colley Hill", "Big views over the Weald."),
  ("The Harlequin, Redhill", "The town's theatre and arts hub."),
  ("Community halls", "Merstham, Woodhatch and Salfords all have good ones."),
 ],
 hoods=["Redhill", "Merstham", "Woodhatch", "Earlswood", "Salfords", "South Park", "Meadvale", "Nutfield", "Kingswood", "Betchworth"],
 faqs=[
  ("Do you cover both Reigate and Redhill?", "Yes, plus Merstham, Earlswood and the villages around."),
  ("Can you paint at a party in Priory Park?", "Yes. Outdoor parties are lovely; I just need a table, two chairs and a bit of shade."),
  ("Can you do a 3-hour booking?", "Yes. The Ultimate Sparkle is 3 hours of face painting, with glitter and gems."),
  ("How far ahead should I book?", "Weekends go weeks ahead, so message me as soon as you have a date."),
 ],
),

"face-painter-dorking.html": dict(
 tpl="guide", acc="#9BE15D", hero=("../img/v2-tiger-boy.webp", "50% 22%"),
 kicker="Hills and vineyards", eyebrow="Dorking, Surrey",
 intro=[
  "Dorking is one of the prettiest places I paint. The drive in under Box Hill, the vineyards on the slopes and the old high street make every booking feel a little bit like a holiday.",
  "Parties here range from cosy garden birthdays in Westcott to big village events in Brockham, and I love that so many families make the most of the countryside right on their doorstep.",
 ],
 quote="The drive in under Box Hill makes every Dorking booking feel a little bit like a holiday.",
 tiles=[
  ("Where", "Garden parties under Box Hill, community halls in town, and village greens in Brockham, Westcott and Mickleham."),
  ("When", "Spring birthdays, summer fêtes and fun days, the famous Brockham bonfire season and Christmas fairs."),
  ("What", "Woodland animals, tigers and butterflies outdoors, plus glitter for the grown-ups."),
 ],
 venues=[
  ("Box Hill", "The famous viewpoint and endless picnic space."),
  ("Denbies Wine Estate", "Vineyards on the hillside for grown-up celebrations."),
  ("Cotmandene", "The green in town for summer gatherings."),
  ("Meadowbank", "Park space by the Pipp Brook."),
  ("Brockham Green", "A village green straight out of a postcard."),
  ("Dorking Halls", "The town's big venue for events."),
 ],
 hoods=["Westcott", "Brockham", "Mickleham", "Betchworth", "Capel", "Holmwood", "Ranmore", "Beare Green", "North Holmwood", "Abinger"],
 faqs=[
  ("Do you travel to Dorking?", "Yes. It's an easy drive from Horsham up the A24."),
  ("Do you cover Brockham and Westcott?", "Yes, plus Mickleham, Capel and the villages around."),
  ("Can you paint at a vineyard or garden wedding?", "Yes. Glitter and face painting are lovely for wedding guests of all ages."),
  ("Do you paint at village fêtes?", "Yes, as a paid stall or for a set fee."),
 ],
),

"face-painter-surrey-villages.html": dict(
 tpl="villages", acc="#4FB6FF", hero=("../img/n-unicorn-girl-party.webp", "50% 25%"),
 kicker="Surrey's southern villages", eyebrow="Cranleigh, Leatherhead & Horley", short="Cranleigh, Leatherhead & Horley",
 intro=[
  "The towns and villages on the Surrey side of the border are some of my closest neighbours. I regularly head up to Cranleigh, Leatherhead and Horley for birthdays, school fairs and community events.",
  "I painted at the last Guildford Festival of the Arts, just up the road, and it's always lovely to bring the sparkle to Surrey's smaller events, where everyone knows everyone and the queue is full of familiar faces by the end of the day.",
 ],
 quote="By the end of a village event, the queue is full of familiar faces.",
 villages=[
  ("Cranleigh", "Often called the biggest village in England, with a lovely common and plenty of community events."),
  ("Leatherhead", "A historic market town by the River Mole, close to Norbury Park and Ashtead Common."),
  ("Horley", "Next door to Gatwick and only a short hop from Crawley, with busy family parties."),
  ("Ewhurst & Ockley", "Village greens and halls deep in the Surrey Hills."),
  ("Ashtead & Fetcham", "Family parties near Leatherhead, with the common close by."),
  ("Smallfield & Charlwood", "Villages on the border, easy for me to reach."),
 ],
 hoods=["Cranleigh", "Ewhurst", "Bramley", "Leatherhead", "Ashtead", "Fetcham", "Bookham", "Horley", "Smallfield", "Charlwood"],
 faqs=[
  ("Do you travel to Cranleigh, Leatherhead and Horley?", "Yes. They're all within easy reach of Horsham."),
  ("Do you cover the smaller villages too?", "Yes, from Ewhurst and Ockley to Charlwood and Smallfield."),
  ("Can you paint at a school fair?", "Yes. I keep designs quick so the queue keeps moving."),
  ("Do you paint grown-ups?", "Yes. Hen dos and adult parties start from £150."),
 ],
),

"face-painter-sussex.html": dict(
 tpl="county", acc="#FF4FA3", hero=("../img/v2-hero.webp", "60% 30%"),
 kicker="All of Sussex", eyebrow="Sussex",
 intro=[
  "I'm Kat, I live in Horsham, and Sussex is where I paint most. From Horsham and Haywards Heath to the coast at Brighton and Worthing, I work with families, schools and event organisers right across the county.",
  "I recently painted at the Eats & Beats Festival at New House Farm near Horsham, and I was out at Macs Farm near Ditchling too. Whether you need a children's entertainer for a garden party or professional face painters for a big event, I cover towns across Sussex and I'm happy to travel further for the right booking.",
 ],
 quote="From the Weald to the coast, Sussex is where I paint most.",
 towns=[
  ("face-painter-horsham.html", "Horsham", "Home. No travel charge in town."),
  ("face-painter-crawley.html", "Crawley", "Where I teach, and know so many families."),
  ("face-painter-haywards-heath.html", "Haywards Heath", "One of my most regular areas."),
  ("face-painter-burgess-hill.html", "Burgess Hill", "Down the road from Ditchling."),
  ("face-painter-east-grinstead.html", "East Grinstead", "A town I fell for."),
  ("face-painter-worthing.html", "Worthing", "Parties by the sea."),
  ("face-painter-brighton.html", "Brighton & Hove", "Hens, weddings, Pride and festivals."),
  ("face-painter-lewes.html", "Lewes", "Bonfire town."),
  ("face-painter-south-downs.html", "Midhurst & Petworth", "Worth the drive."),
  ("face-painter-west-sussex-villages.html", "Villages around Horsham", "Billingshurst, Henfield, Steyning and more."),
 ],
 faqs=[
  ("Which parts of Sussex do you cover?", "West Sussex, Brighton & Hove and much of East Sussex, from Horsham and Crawley to Worthing, Brighton and Lewes."),
  ("Do you charge for travel?", "Not in and around Horsham. For longer trips I may add a small travel charge, always agreed up front."),
  ("Can you bring more than one artist?", "Yes, for big events and festivals I can bring extra artists."),
  ("Do you do corporate and festival events in Sussex?", "Yes. I've painted at festivals and corporate family days across the county."),
 ],
),

"face-painter-surrey.html": dict(
 tpl="county", acc="#2FD4C4", hero=("../img/v2-adult-tiger.webp", "50% 30%"),
 kicker="Across the border", eyebrow="Surrey",
 intro=[
  "Surrey is right on my doorstep. Horsham sits on the border, so towns like Dorking, Reigate and Guildford are an easy drive for parties, weddings and events.",
  "I've painted at the Guildford Festival of the Arts, and lately I've been heading north too: Croydon and Baker Street recently, with Putney, Sutton and the Good Hotel in London coming up. From a garden party in Cranleigh to a big London event, longer trips are no problem for the right booking further for the right booking.",
 ],
 quote="Horsham sits right on the border, so Surrey is on my doorstep.",
 towns=[
  ("face-painter-guildford.html", "Guildford", "Art-trail memories."),
  ("face-painter-reigate.html", "Reigate & Redhill", "Busy all year round."),
  ("face-painter-dorking.html", "Dorking", "Hills and vineyards."),
  ("face-painter-surrey-villages.html", "Cranleigh, Leatherhead & Horley", "Surrey's southern villages."),
 ],
 faqs=[
  ("Which parts of Surrey do you cover?", "Mainly south and central Surrey: Guildford, Reigate, Redhill, Dorking, Cranleigh, Leatherhead and Horley."),
  ("Do you charge for travel to Surrey?", "Most of south and central Surrey is within about 40 minutes of my home in Horsham. For anything further, such as London, I may add a small travel cost, which we'll agree before you book."),
  ("Can you paint at a Surrey wedding?", "Yes. Face painting and glitter are lovely for guests of all ages."),
  ("Can you cover a big Surrey event?", "Yes. For festivals and large corporate days I can bring extra face painters so the queue keeps moving."),
 ],
),
}
