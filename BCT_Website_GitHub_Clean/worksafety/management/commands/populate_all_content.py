from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from worksafety.models import SafetyInfo
from generalinfo.models import InfoPage
from partners.models import Partner
from news.models import NewsArticle
from events.models import Event
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate all new features with realistic BCT content'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate content...\n')
        
        try:
            admin = User.objects.filter(is_superuser=True).first()
            if not admin:
                admin = User.objects.first()
        except:
            admin = None
        
        SafetyInfo.objects.all().delete()
        InfoPage.objects.all().delete()
        Partner.objects.all().delete()
        
        self.populate_safety()
        self.populate_general_info()
        self.populate_partners()
        
        self.stdout.write(self.style.SUCCESS('\n✓ All content populated successfully!'))
        self.stdout.write(self.style.WARNING('\nNote: News and Events are left empty for TeamLeaders to add.'))

    def populate_safety(self):
        self.stdout.write('Populating Work Safety...')
        
        SafetyInfo.objects.create(
            category='first_aid',
            title='First Aid Kit Locations',
            content='''Each BCT bus and ticket booth is equipped with a first aid kit.

Ticket Booth Locations:
- Alexanderplatz: Behind the counter, red box
- Brandenburg Gate: Under the desk
- Kurfürstendamm: In the storage cabinet

Bus Locations:
- First aid kit is located behind the driver's seat in a red box
- All drivers are trained in basic first aid'''
        )
        
        SafetyInfo.objects.create(
            category='first_aid',
            title='Basic First Aid Procedures',
            content='''For Minor Injuries:
1. Assess the situation and ensure safety
2. Wear gloves before treating wounds
3. Clean wounds with sterile wipes
4. Apply bandages as needed
5. Document the incident in the logbook

For Serious Injuries:
1. Call emergency services immediately (112)
2. Do NOT move the injured person
3. Keep them calm and comfortable
4. Wait for professional help
5. Notify your team leader immediately'''
        )
        
        SafetyInfo.objects.create(
            category='emergency',
            title='Emergency Contacts - IMPORTANT',
            content='''Keep these numbers readily available:

Emergency Services (Fire, Police, Ambulance): 112
Police (Non-Emergency): 110

BCT Team Leaders:
- Main Office: +49 30 1234 5678
- Emergency Hotline: +49 170 9876 543 (24/7)

Medical:
- Charité Hospital: +49 30 450 50
- Poison Control: +49 30 19240

Lost & Found:
- BVG (Public Transport): +49 30 19449
- Police Lost Property: +49 30 9027 0'''
        )
        
        SafetyInfo.objects.create(
            category='emergency',
            title='Incident Reporting',
            content='''All incidents MUST be reported within 2 hours:

1. Secure the scene and ensure safety
2. Take photos if possible (injuries, damages)
3. Collect witness information
4. Call your team leader immediately
5. Fill out incident report form
6. Submit report within 24 hours

Incident Report Includes:
- Date, time, and location
- Description of what happened
- Names of people involved
- Witness statements
- Photos/evidence
- Your signature'''
        )
        
        SafetyInfo.objects.create(
            category='procedures',
            title='Weather Emergency Procedures',
            content='''Extreme Heat (30°C+):
- Ensure water bottles are stocked on all buses
- Offer water to customers regularly
- Take breaks in shaded areas
- Watch for heat exhaustion symptoms

Thunderstorms:
- If lightning strikes nearby, seek shelter immediately
- Do not stand under trees
- Open-top buses: close roof or seek covered areas
- Monitor weather forecasts regularly

Snow & Ice:
- Wear appropriate footwear with good grip
- Walk carefully on icy surfaces
- Salt should be applied around ticket booths
- Be extra cautious when boarding/departing buses'''
        )
        
        SafetyInfo.objects.create(
            category='procedures',
            title='Dealing with Difficult Customers',
            content='''Stay Calm and Professional:
1. Listen to the customer's concerns
2. Stay polite and maintain eye contact
3. Never raise your voice or argue
4. Offer solutions within company policy

If Customer Becomes Aggressive:
1. Step back and maintain safe distance
2. Call for backup or security
3. Do NOT engage physically
4. Document the interaction
5. Report to team leader immediately

Remember: Your safety comes first. If you feel threatened, remove yourself from the situation and call for help.'''
        )
        
        SafetyInfo.objects.create(
            category='equipment',
            title='Personal Protective Equipment (PPE)',
            content='''Required PPE for All Sellers:
- BCT uniform vest (high visibility)
- Company ID badge (must be visible)
- Comfortable, closed-toe shoes
- Sun protection (hat, sunscreen) in summer

Available Upon Request:
- Raincoat (waterproof BCT jacket)
- Winter gloves and warm clothing
- Protective masks
- Hand sanitizer

Contact your team leader if you need replacement equipment or additional items.'''
        )
        
        self.stdout.write(self.style.SUCCESS('  ✓ Work Safety populated'))

    def populate_general_info(self):
        self.stdout.write('Populating General Information...')
        
        InfoPage.objects.create(
            category='company',
            title='About BCT Berlin City Tour',
            content='''Welcome to BCT - Berlin City Tour GmbH!

We are Berlin's leading provider of hop-on hop-off bus tours, offering visitors an unforgettable experience exploring Germany's vibrant capital city.

Our Mission:
To provide exceptional sightseeing experiences while showcasing Berlin's rich history, culture, and modern attractions.

Our Values:
- Customer satisfaction is our priority
- Professional and friendly service
- Commitment to quality and safety
- Team collaboration and support

Founded in Berlin, we operate a fleet of modern, comfortable buses serving major attractions including Brandenburg Gate, Checkpoint Charlie, Museum Island, and many more landmarks.

As a BCT seller, you are an ambassador of Berlin and represent our company to thousands of tourists every year. Thank you for being part of our team!''',
            order=1
        )
        
        InfoPage.objects.create(
            category='company',
            title='Working Hours & Breaks',
            content='''Standard Operating Hours:
- Summer Season (Apr-Oct): 09:00 - 20:00
- Winter Season (Nov-Mar): 10:00 - 18:00

Seller Shifts:
- Morning Shift: 08:30 - 14:30
- Afternoon Shift: 14:00 - 20:00
- Full Day: 08:30 - 17:00 (with 1-hour break)

Break Policy:
- 15 minutes for shifts up to 4 hours
- 30 minutes for shifts 4-6 hours
- 1 hour for shifts over 6 hours

Overtime:
Must be approved by team leader in advance. Overtime is compensated at standard rate + 25%.''',
            order=2
        )
        
        InfoPage.objects.create(
            category='vouchers',
            title='Ticket Types & Pricing 2025',
            content='''Classic Tour (24 Hours):
- Adult: €28.00
- Child (6-14): €14.00
- Student/Senior: €25.00
- Family (2 adults + 2 children): €65.00

Premium Tour (48 Hours):
- Adult: €38.00
- Child (6-14): €19.00
- Student/Senior: €34.00

Special Features:
- Free WiFi on all buses
- Audio guides in 20 languages
- Hop-on hop-off at 22 stops
- Valid until midnight on last day

Group Discounts:
Groups of 10+: 10% discount
Groups of 20+: 15% discount
School groups: 20% discount (with confirmation)''',
            order=1
        )
        
        InfoPage.objects.create(
            category='vouchers',
            title='Partner Vouchers & Combo Deals',
            content='''Museum Island Pass:
Bus Tour + Museum Island Entry
Adult: €42.00 (Save €8.00)
Student: €35.00 (Save €6.00)

Berlin TV Tower Combo:
Bus Tour + TV Tower Fast Track
Adult: €48.00 (Save €10.00)

Food Vouchers:
Some tickets include €5 food voucher valid at:
- Hard Rock Cafe Berlin
- Hofbräu Beer Garden
- Selected partner restaurants

Online Booking Discounts:
Customers who book online get 10% off. Always ask if they've booked online before selling full-price tickets.''',
            order=2
        )
        
        InfoPage.objects.create(
            category='tours',
            title='Tour Routes & Stops',
            content='''Classic Route (22 Stops):
1. Kurfürstendamm
2. KaDeWe Department Store
3. Lützowplatz
4. Kulturforum
5. Potsdamer Platz
6. Checkpoint Charlie
7. Gendarmenmarkt
8. Alexanderplatz
9. Red City Hall
10. Museum Island
11. Berlin Cathedral
12. Unter den Linden
13. Brandenburg Gate
14. Reichstag
15. Central Station
16. Victory Column
17. Berlin Zoo
18. And more...

Bus Frequency:
Summer: Every 10-15 minutes
Winter: Every 15-20 minutes

Full Loop Duration: Approx. 2.5 hours without stops

Audio Guide Languages:
German, English, French, Spanish, Italian, Portuguese, Russian, Polish, Turkish, Arabic, Chinese, Japanese, Korean, Hebrew, Dutch, Swedish, Czech, and more.''',
            order=1
        )
        
        InfoPage.objects.create(
            category='tours',
            title='Frequently Asked Questions',
            content='''Q: Do tickets need to be activated?
A: Yes, tickets are valid from the moment of first boarding. Show the ticket to the driver or scan the QR code.

Q: What if it rains?
A: All our buses have covered seating. We also have convertible roofs on open-top buses.

Q: Are buses wheelchair accessible?
A: Yes, all BCT buses are equipped with wheelchair lifts and designated spaces.

Q: Can I bring luggage?
A: Small bags are allowed. Large suitcases must be stored in designated areas.

Q: Where can I buy tickets?
A: At any BCT ticket booth, online at berlin-city-tour.de, or directly on the bus (€2 surcharge).

Q: Are pets allowed?
A: Small pets in carriers are permitted. Service dogs are always welcome.''',
            order=2
        )
        
        InfoPage.objects.create(
            category='policies',
            title='Seller Code of Conduct',
            content='''Professional Appearance:
- Wear full BCT uniform at all times
- ID badge must be visible
- Maintain clean and neat appearance
- No strong perfumes or colognes

Customer Interaction:
- Greet every customer with a smile
- Speak clearly and politely
- Be helpful and informative
- Never use offensive language
- Respect cultural differences

Cash Handling:
- Count money carefully in front of customer
- Never leave cash register unattended
- Reconcile cash at shift end
- Report discrepancies immediately

Mobile Phone Use:
- Personal calls only during breaks
- Keep phone on silent during work
- Emergency calls are exceptions

Attendance:
- Arrive 15 minutes before shift
- Notify team leader if late/absent
- No-shows may result in disciplinary action''',
            order=1
        )
        
        InfoPage.objects.create(
            category='policies',
            title='Payment Methods',
            content='''Accepted Payment Methods:
- Cash (EUR only)
- Credit/Debit Cards (Visa, Mastercard, Maestro)
- Contactless payments (Apple Pay, Google Pay)
- PayPal (online only)

Cash Handling:
- Always count change aloud to customer
- Check large bills for authenticity
- Maximum cash in register: €500
- Request cash pickup when limit reached

Card Payments:
- Customer must be present for PIN entry
- Check card matches name on booking
- Keep receipt until customer boards
- For declined cards, offer alternative payment

Refund Policy:
- Unused tickets: Full refund within 24 hours
- Partially used tickets: No refund
- Online bookings: Contact customer service
- Processing time: 5-7 business days''',
            order=2
        )
        
        InfoPage.objects.create(
            category='benefits',
            title='Employee Benefits',
            content='''Salary & Compensation:
- Competitive hourly wage
- Performance bonuses (Seller of the Month)
- Overtime compensation
- Holiday pay

Time Off:
- 24 vacation days per year
- Paid sick leave (with doctor's note)
- Public holidays off or compensated

Professional Development:
- Free German language courses
- Customer service training
- Sales skills workshops
- Leadership development for top performers

Perks:
- Free BCT bus tours for family/friends (2x per year)
- Discounts at partner restaurants & attractions
- Company events and team building activities
- Free BCT merchandise

Health & Safety:
- Accident insurance
- Regular health & safety training
- Ergonomic equipment provided
- Mental health support available''',
            order=1
        )
        
        self.stdout.write(self.style.SUCCESS('  ✓ General Information populated'))

    def populate_partners(self):
        self.stdout.write('Populating Partners...')
        
        Partner.objects.create(
            name='Hard Rock Cafe Berlin',
            category='restaurant',
            description='American restaurant with rock memorabilia, live music, and classic burgers. BCT customers receive 10% discount on food.',
            address='Kurfürstendamm 224, 10719 Berlin',
            phone='+49 30 884620',
            email='berlin@hardrock.com',
            website='https://hardrock.com/cafes/berlin',
            discount_info='Show your BCT ticket for 10% off food orders. Not valid with other promotions. Valid for ticket holder + 3 guests.'
        )
        
        Partner.objects.create(
            name='Berlin TV Tower (Fernsehturm)',
            category='attraction',
            description='Berlin\'s iconic TV tower with observation deck at 203m height. Skip-the-line access for BCT combo ticket holders.',
            address='Panoramastraße 1A, 10178 Berlin',
            phone='+49 30 247575875',
            email='info@tv-turm.de',
            website='https://tv-turm.de',
            discount_info='Combo ticket available: BCT Tour + TV Tower Fast Track. Save €10 when purchased together. Online booking recommended.'
        )
        
        Partner.objects.create(
            name='DDR Museum',
            category='attraction',
            description='Interactive museum showing everyday life in East Germany. Hands-on exhibits and original GDR artifacts.',
            address='Karl-Liebknecht-Str. 1, 10178 Berlin',
            phone='+49 30 847123731',
            email='info@ddr-museum.de',
            website='https://ddr-museum.de',
            discount_info='€2 discount on entry tickets for BCT customers. Show valid bus ticket at the entrance.'
        )
        
        Partner.objects.create(
            name='Hofbräu Wirtshaus Berlin',
            category='restaurant',
            description='Authentic Bavarian beer hall with traditional German food and beer garden. Groups welcome.',
            address='Karl-Liebknecht-Str. 30, 10178 Berlin',
            phone='+49 30 67962696',
            email='berlin@hofbraeu-wirtshaus.de',
            website='https://hofbraeu-berlin.de',
            discount_info='Free pretzel with any meal for BCT customers. Beer garden open April-October.'
        )
        
        Partner.objects.create(
            name='Hotel Adlon Kempinski',
            category='hotel',
            description='Luxury 5-star hotel next to Brandenburg Gate. Historic hotel rebuilt after reunification.',
            address='Unter den Linden 77, 10117 Berlin',
            phone='+49 30 22610',
            email='reservations.adlon@kempinski.com',
            website='https://kempinski.com/adlon',
            discount_info='Corporate rate for BCT: 15% off best available rate. Use code "BCTBERLIN" when booking.'
        )
        
        Partner.objects.create(
            name='Madame Tussauds Berlin',
            category='attraction',
            description='Famous wax museum with over 120 lifelike figures including celebrities, historical figures, and politicians.',
            address='Unter den Linden 74, 10117 Berlin',
            phone='+49 30 400050840',
            email='info.berlin@madametussauds.com',
            website='https://madametussauds.com/berlin',
            discount_info='Combination ticket available with BCT tour. Save 20% when purchased together.'
        )
        
        Partner.objects.create(
            name='Berlin Dungeon',
            category='attraction',
            description='Interactive horror attraction bringing Berlin\'s dark history to life. Not recommended for children under 10.',
            address='Spandauer Str. 2, 10178 Berlin',
            phone='+49 30 25008230',
            email='info@berlindungeon.com',
            website='https://thedungeons.com/berlin',
            discount_info='€3 discount for BCT customers. Fast-track entry available with combo ticket.'
        )
        
        Partner.objects.create(
            name='Alte Nationalgalerie',
            category='attraction',
            description='National Gallery housing 19th-century art collection on Museum Island. UNESCO World Heritage site.',
            address='Bodestraße, 10178 Berlin',
            phone='+49 30 266424242',
            email='service@smb.museum',
            website='https://smb.museum',
            discount_info='Museum Island Pass: Access to all 5 museums for €18 (regular €24) for BCT customers.'
        )
        
        Partner.objects.create(
            name='Curry 36',
            category='restaurant',
            description='Legendary currywurst stand serving authentic Berlin street food since 1981. A must-try for visitors!',
            address='Mehringdamm 36, 10961 Berlin',
            phone='+49 30 2517368',
            email='info@curry36.de',
            website='https://curry36.de',
            discount_info='Show BCT ticket for a free small drink with any currywurst order.'
        )
        
        Partner.objects.create(
            name='Spree River Cruises',
            category='transport',
            description='Scenic boat tours along the River Spree. See Berlin from the water with live commentary.',
            address='Nikolaiviertel Pier, 10178 Berlin',
            phone='+49 30 53630000',
            email='info@spreerivercruises.de',
            website='https://spreerivercruises.de',
            discount_info='BCT customers get 15% off all cruise tickets. Combo packages available for groups of 10+.'
        )
        
        self.stdout.write(self.style.SUCCESS('  ✓ Partners populated'))

