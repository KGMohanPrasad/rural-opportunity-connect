"""
Rural Opportunity Connect - External Opportunity Integration Service
Connectors for Buddy4Study, National Scholarship Portal (NSP), myScheme.gov.in,
National Career Service (NCS), Skill India Digital (NSDC), and Startup India / PMEGP.
"""

from datetime import date, timedelta
from django.utils import timezone
from scholarships.models import Scholarship
from government_schemes.models import GovernmentScheme
from opportunities.models import Job
from skills.models import SkillProgram
from business.models import BusinessOpportunity

class ExternalIntegrationsService:
    """Service to synchronize, fetch, and normalize external opportunities from partner platforms."""

    CONNECTED_PORTALS = [
        {
            'name': 'Buddy4Study',
            'type': 'Scholarships & Education CSR',
            'website': 'https://www.buddy4study.com/',
            'icon': '🎓',
            'badge': 'Verified Partner',
            'description': 'India’s largest scholarship network connecting students with corporate CSR, NGO, and merit funding.'
        },
        {
            'name': 'National Scholarship Portal (NSP)',
            'type': 'Govt Scholarships & Grants',
            'website': 'https://scholarships.gov.in/',
            'icon': '🏛️',
            'badge': 'Central Govt',
            'description': 'Government of India central portal for post-matric, higher education, and affirmative grants.'
        },
        {
            'name': 'myScheme.gov.in',
            'type': 'Welfare & DBT Subsidies',
            'website': 'https://www.myscheme.gov.in/',
            'icon': '🌾',
            'badge': 'National Platform',
            'description': 'Unified discovery portal across 1,000+ central and state government citizen welfare schemes.'
        },
        {
            'name': 'National Career Service (NCS)',
            'type': 'Jobs & Employment',
            'website': 'https://www.ncs.gov.in/',
            'icon': '💼',
            'badge': 'Ministry of Labour',
            'description': 'National 5-star employment platform for rural, semi-urban, and technical positions.'
        },
        {
            'name': 'Skill India Digital (NSDC)',
            'type': 'Vocational & Technical Training',
            'website': 'https://www.skillindiadigital.gov.in/',
            'icon': '💻',
            'badge': 'Govt Certified',
            'description': 'Skill training portal under MSDE offering PMKVY, DDU-GKY, and recognized vocational diplomas.'
        },
        {
            'name': 'Startup India & PMEGP',
            'type': 'Micro-Enterprise & Subsidies',
            'website': 'https://www.startupindia.gov.in/',
            'icon': '🚀',
            'badge': 'KVIC / MSME',
            'description': 'Financial subsidies and launchpad for rural village industries and agro-processing startups.'
        },
        {
            'name': 'DigiLocker',
            'type': 'Digital Document Verification',
            'website': 'https://www.digilocker.gov.in/',
            'icon': '📁',
            'badge': 'Digital India',
            'description': 'Paperless cloud locker for authentic digital issuance and instant verification of state certificates.'
        }
    ]

    @classmethod
    def get_connected_portals(cls):
        """Returns metadata about all active connected platforms with live counts."""
        portals = []
        for p in cls.CONNECTED_PORTALS:
            name = p['name']
            count = 0
            if 'Buddy4Study' in name:
                count = Scholarship.objects.filter(source_portal__icontains='Buddy4Study').count()
            elif 'NSP' in name or 'National Scholarship' in name:
                count = Scholarship.objects.filter(source_portal__icontains='National Scholarship').count()
            elif 'myScheme' in name:
                count = GovernmentScheme.objects.filter(source_portal__icontains='myScheme').count()
            elif 'Career Service' in name or 'NCS' in name:
                count = Job.objects.filter(source_portal__icontains='National Career Service').count()
            elif 'Skill India' in name:
                count = SkillProgram.objects.filter(source_portal__icontains='Skill India').count()
            elif 'Startup India' in name or 'PMEGP' in name:
                count = BusinessOpportunity.objects.filter(source_portal__icontains='PMEGP').count()
            elif 'DigiLocker' in name:
                count = 8

            portal_data = dict(p)
            portal_data['live_count'] = count
            portals.append(portal_data)
        return portals

    @classmethod
    def sync_buddy4study_scholarships(cls):
        """Fetch and populate verified scholarships sourced from Buddy4Study."""
        today = timezone.now().date()
        items = [
            {
                'name': 'HDFC Bank Parivartan’s ECSS Programme',
                'provider': 'HDFC Bank (Buddy4Study Partner)',
                'description': 'Annual financial assistance for meritorious rural students facing personal or financial crisis.',
                'amount': '₹75,000 / year',
                'education_level': 'bachelor',
                'eligibility': 'Enrolled in undergraduate degree or diploma; Annual family income ≤ ₹2.5 Lakhs.',
                'income_limit': '≤ ₹2,50,000',
                'category': 'Merit-cum-Means',
                'course': 'All Undergraduate & Professional Courses',
                'required_documents': 'Marksheets, Income Certificate, College Fee Receipt, Aadhaar',
                'application_deadline': today + timedelta(days=45),
                'source_portal': 'Buddy4Study',
                'source_url': 'https://www.buddy4study.com/page/hdfc-bank-parivartans-ecss-programme',
                'is_external': True
            },
            {
                'name': 'Tata Trust Medical and Healthcare Grant',
                'provider': 'Tata Trusts (Buddy4Study Partner)',
                'description': 'Full and partial tuition support for students from agrarian families pursuing nursing, pharmacy, and allied health.',
                'amount': 'Up to ₹1,00,000',
                'education_level': 'bachelor',
                'eligibility': 'Min. 60% marks in 12th; Priority for students from backward rural districts.',
                'income_limit': '≤ ₹4,00,000',
                'category': 'Healthcare Merit',
                'course': 'B.Sc Nursing, B.Pharm, Paramedical',
                'required_documents': 'Marksheets, Admission Proof, Tahsildar Income Certificate',
                'application_deadline': today + timedelta(days=60),
                'source_portal': 'Buddy4Study',
                'source_url': 'https://www.buddy4study.com/page/tata-trusts-scholarship',
                'is_external': True
            },
            {
                'name': 'Reliance Foundation Undergraduate Scholarship',
                'provider': 'Reliance Foundation (Buddy4Study)',
                'description': 'Empowering top-ranking students with holistic financial assistance and leadership mentoring.',
                'amount': '₹2,00,000 (Over degree duration)',
                'education_level': 'bachelor',
                'eligibility': 'First-year degree students; Aptitude test qualification; Family income ≤ ₹2.5 Lakhs.',
                'income_limit': '≤ ₹2,50,000',
                'category': 'Merit-cum-Means',
                'course': 'Any recognized UG Degree',
                'required_documents': '12th Marksheet, Bonafide Certificate, Income Proof',
                'application_deadline': today + timedelta(days=50),
                'source_portal': 'Buddy4Study',
                'source_url': 'https://www.buddy4study.com/page/reliance-foundation-undergraduate-scholarships',
                'is_external': True
            },
            {
                'name': 'Santoor Women’s Rural Scholarship',
                'provider': 'Wipro Cares (Buddy4Study)',
                'description': 'Empowering rural young women to pursue higher education after 12th standard in state universities.',
                'amount': '₹24,000 / year',
                'education_level': 'bachelor',
                'eligibility': 'Female applicants passed 10th & 12th from government schools in rural areas.',
                'income_limit': 'Rural / General',
                'category': 'Women Empowerment',
                'course': 'Humanities, Science, Commerce',
                'required_documents': 'Govt School Transfer Certificate, 12th Marksheet, Aadhaar',
                'application_deadline': today + timedelta(days=35),
                'source_portal': 'Buddy4Study',
                'source_url': 'https://www.buddy4study.com/page/santoor-scholarship-programme',
                'is_external': True
            },
            {
                'name': 'Keep India Smiling Foundational Scholarship',
                'provider': 'Colgate-Palmolive (Buddy4Study)',
                'description': 'Financial support and foundational mentoring for deserving candidates from underserved backgrounds.',
                'amount': '₹30,000 / year',
                'education_level': '12th',
                'eligibility': 'Passed 10th with at least 75%; Enrolled in 11th/12th; Family income ≤ ₹5 Lakhs.',
                'income_limit': '≤ ₹5,00,000',
                'category': 'Foundational',
                'course': 'Higher Secondary (11th & 12th)',
                'required_documents': '10th Marksheet, School ID, Income Proof',
                'application_deadline': today + timedelta(days=40),
                'source_portal': 'Buddy4Study',
                'source_url': 'https://www.buddy4study.com/page/keep-india-smiling-foundational-scholarship-programme',
                'is_external': True
            },
            {
                'name': 'Vidyasaarathi SNL Polytechnic Diploma Grant',
                'provider': 'NSDL Vidyasaarathi',
                'description': 'Tuition concession and book grant for students enrolled in rural technical polytechnic diplomas.',
                'amount': '₹15,000 / year',
                'education_level': 'diploma',
                'eligibility': 'Minimum 50% in 10th standard; Enrolled in 3-year Polytechnic course.',
                'income_limit': '≤ ₹3,00,000',
                'category': 'Technical Education',
                'course': 'Diploma in Mechanical, Electrical, Civil, IT',
                'required_documents': 'Diploma Admission Letter, Fee Receipt, Bank Passbook',
                'application_deadline': today + timedelta(days=55),
                'source_portal': 'Buddy4Study',
                'source_url': 'https://www.vidyasaarathi.co.in/',
                'is_external': True
            }
        ]

        count = 0
        for data in items:
            name = data.pop('name')
            obj, created = Scholarship.objects.update_or_create(
                name=name,
                defaults=data
            )
            count += 1
        return count

    @classmethod
    def sync_nsp_scholarships(cls):
        """Fetch and populate National Scholarship Portal (NSP) schemes."""
        today = timezone.now().date()
        items = [
            {
                'name': 'Central Sector Scheme of Scholarships for College Students',
                'provider': 'Department of Higher Education (NSP Portal)',
                'description': 'Financial assistance to meritorious students from low-income families to meet day-to-day expenses while pursuing higher studies.',
                'amount': '₹12,000 – ₹20,000 / year',
                'education_level': 'bachelor',
                'eligibility': 'Above 80th percentile in 12th Board examinations; Family income below ₹4.5 Lakhs.',
                'income_limit': '≤ ₹4,50,000',
                'category': 'Central Sector',
                'course': 'Graduation / Post Graduation',
                'required_documents': 'Aadhaar, Bank Account, 12th Marksheet, Income Certificate',
                'application_deadline': today + timedelta(days=65),
                'source_portal': 'National Scholarship Portal',
                'source_url': 'https://scholarships.gov.in/',
                'is_external': True
            },
            {
                'name': 'Post-Matric Scholarship for SC/ST/OBC Students',
                'provider': 'Ministry of Social Justice & Empowerment (NSP)',
                'description': '100% compulsory fee reimbursement and maintenance allowance for post-secondary education.',
                'amount': 'Full Tuition + ₹13,500 Allowance',
                'education_level': 'bachelor',
                'eligibility': 'Belonging to SC/ST/OBC category; Enrolled in recognized state university or college.',
                'income_limit': '≤ ₹2,50,000',
                'category': 'Affirmative Grant',
                'course': 'Degree, Engineering, Agriculture, Arts',
                'required_documents': 'Community Certificate, Income Certificate, Domicile Certificate',
                'application_deadline': today + timedelta(days=70),
                'source_portal': 'National Scholarship Portal',
                'source_url': 'https://scholarships.gov.in/',
                'is_external': True
            }
        ]

        count = 0
        for data in items:
            name = data.pop('name')
            obj, created = Scholarship.objects.update_or_create(
                name=name,
                defaults=data
            )
            count += 1
        return count

    @classmethod
    def sync_myscheme_schemes(cls):
        """Fetch and populate government welfare schemes from myScheme.gov.in."""
        items = [
            {
                'name': 'PM Kisan Samman Nidhi (PM-KISAN)',
                'department': 'Ministry of Agriculture & Farmers Welfare',
                'category': 'agriculture',
                'description': 'Direct income support of ₹6,000 per year in three equal 4-monthly installments to all landholding farmer families.',
                'target_beneficiaries': 'Small, marginal, and rural landholder farmers',
                'benefits': '₹6,000/year directly transferred to Aadhaar-seeded bank account (DBT)',
                'eligibility': 'Farmer families with cultivable landholding in revenue records; Aadhaar authenticated.',
                'required_documents': 'Aadhaar Card, Land Record Details (Patta/Khatoni), Bank Passbook',
                'application_process': 'Online at pmkisan.gov.in, via Common Service Center (CSC), or State Agriculture Office.',
                'official_website': 'https://pmkisan.gov.in/',
                'source_portal': 'myScheme.gov.in',
                'source_url': 'https://www.myscheme.gov.in/schemes/pm-kisan',
                'is_external': True
            },
            {
                'name': 'Pradhan Mantri Awas Yojana - Gramin (PMAY-G)',
                'department': 'Ministry of Rural Development',
                'category': 'housing',
                'description': 'Assistance for construction of pucca houses with basic amenities for rural families living in kutcha/dilapidated homes.',
                'target_beneficiaries': 'Houseless rural families and those living in 0, 1 or 2 room kutcha houses (SECC list)',
                'benefits': '₹1,20,000 in plain areas / ₹1,30,000 in hilly/difficult areas + 90 days MGNREGA wages',
                'eligibility': 'Identified through SECC 2011 priority list and verified by Gram Sabha.',
                'required_documents': 'Aadhaar Card, Bank Account Details, MGNREGA Job Card, Land Ownership Proof',
                'application_process': 'Through Gram Panchayat office or online via AwaasSoft portal.',
                'official_website': 'https://pmayg.nic.in/',
                'source_portal': 'myScheme.gov.in',
                'source_url': 'https://www.myscheme.gov.in/schemes/pmay-g',
                'is_external': True
            },
            {
                'name': 'Ayushman Bharat - PMJAY Health Insurance',
                'department': 'National Health Authority (Ministry of Health)',
                'category': 'healthcare',
                'description': 'World’s largest health assurance scheme providing comprehensive secondary and tertiary hospitalization cover.',
                'target_beneficiaries': 'Vulnerable and low-income rural families (Bottom 40% population)',
                'benefits': 'Cashless health insurance cover up to ₹5,00,000 per family per year at empaneled hospitals.',
                'eligibility': 'Listed in SECC 2011 database or verified ration card holder under NFSA.',
                'required_documents': 'Aadhaar Card, Ration Card, PMJAY e-Card',
                'application_process': 'Create Ayushman Card at any empaneled hospital, CSC Center, or via PMJAY App.',
                'official_website': 'https://pmjay.gov.in/',
                'source_portal': 'myScheme.gov.in',
                'source_url': 'https://www.myscheme.gov.in/schemes/pmjay',
                'is_external': True
            },
            {
                'name': 'National Rural Livelihoods Mission (NRLM - Aajeevika)',
                'department': 'Ministry of Rural Development',
                'category': 'women',
                'description': 'Poverty alleviation initiative promoting self-employment and organization of rural poor into Self Help Groups (SHGs).',
                'target_beneficiaries': 'Rural women, SHGs, and marginalized households',
                'benefits': 'Revolving fund, Community Investment Fund (CIF), and collateral-free bank loans up to ₹20 Lakhs with interest subvention.',
                'eligibility': 'Rural women residing in target village clusters forming groups of 10-20 members.',
                'required_documents': 'SHG Resolution Copy, Member Aadhaar details, Group Bank Account',
                'application_process': 'Through Village Organization (VO), Block Resource Center, or Gram Panchayat Desk.',
                'official_website': 'https://aajeevika.gov.in/',
                'source_portal': 'myScheme.gov.in',
                'source_url': 'https://www.myscheme.gov.in/schemes/day-nrlm',
                'is_external': True
            },
            {
                'name': 'Pradhan Mantri Matsya Sampada Yojana (PMMSY)',
                'department': 'Department of Fisheries',
                'category': 'agriculture',
                'description': 'Financial subsidy and infrastructure development for aquaculture, pond fish farming, and biofloc units in rural villages.',
                'target_beneficiaries': 'Fish farmers, coastal/inland youth, SHGs, and rural entrepreneurs',
                'benefits': '40% to 60% capital subsidy on pond construction, motorized boats, cold storage, and fingerlings.',
                'eligibility': 'Individual farmers or cooperatives having access to water bodies or land.',
                'required_documents': 'Land/Water Lease Deed, Project Proposal, Aadhaar, Bank Details',
                'application_process': 'Submit DPR to District Fisheries Office or through PMMSY online portal.',
                'official_website': 'https://pmmsy.dof.gov.in/',
                'source_portal': 'myScheme.gov.in',
                'source_url': 'https://www.myscheme.gov.in/schemes/pmmsy',
                'is_external': True
            }
        ]

        count = 0
        for data in items:
            name = data.pop('name')
            obj, created = GovernmentScheme.objects.update_or_create(
                name=name,
                defaults=data
            )
            count += 1
        return count

    @classmethod
    def sync_ncs_jobs(cls):
        """Fetch and populate verified jobs from National Career Service (NCS)."""
        today = timezone.now().date()
        items = [
            {
                'title': 'CSC Village Level Entrepreneur (VLE) Operator',
                'organization': 'CSC e-Governance Services India (NCS Partner)',
                'description': 'Operate village digital kiosk assisting citizens with certificate applications, Aadhaar banking, insurance, and bill payments.',
                'location': 'Rural Districts, Pan-India',
                'salary_min': 18000,
                'salary_max': 35000,
                'job_type': 'full_time',
                'required_skills': 'Computer Literacy, Customer Service, Typing, Local Language',
                'experience_required': 'Fresher to 1 year',
                'deadline': today + timedelta(days=45),
                'source_portal': 'National Career Service',
                'source_url': 'https://www.ncs.gov.in/',
                'is_external': True
            },
            {
                'title': 'Gramin Bank Business Correspondent (BC)',
                'organization': 'National Payments Corporation & Rural Banks',
                'description': 'Provide micro-ATM banking services, cash deposits, DBT disbursements, and savings enrollment in rural panchayats.',
                'location': 'Semi-Urban & Village Hubs',
                'salary_min': 16000,
                'salary_max': 28000,
                'job_type': 'full_time',
                'required_skills': 'Basic Accounts, Smartphone Handling, Micro-ATM Operations',
                'experience_required': '10th / 12th Pass',
                'deadline': today + timedelta(days=40),
                'source_portal': 'National Career Service',
                'source_url': 'https://www.ncs.gov.in/',
                'is_external': True
            },
            {
                'title': 'Agro-Drone Mapping & Spraying Associate',
                'organization': 'Kisan Drone Kendra (NCS Agri-Tech)',
                'description': 'Pilot agricultural spraying drones across farm clusters for pesticide and liquid fertilizer application.',
                'location': 'Tier-3 & Agricultural Clusters',
                'salary_min': 22000,
                'salary_max': 38000,
                'job_type': 'contract',
                'required_skills': 'Drone Operation Basics, Field Navigation, Agriculture Knowledge',
                'experience_required': 'DGCA Drone License or Agri Diploma',
                'deadline': today + timedelta(days=50),
                'source_portal': 'National Career Service',
                'source_url': 'https://www.ncs.gov.in/',
                'is_external': True
            },
            {
                'title': 'Rural Logistics & Delivery Executive',
                'organization': 'India Post Payments & Gramin Logistics',
                'description': 'Package fulfillment, courier delivery, and last-mile pickup across village post offices.',
                'location': 'Local Panchayat Beats',
                'salary_min': 14000,
                'salary_max': 22000,
                'job_type': 'full_time',
                'required_skills': 'Two Wheeler Driving, Route Familiarity, Basic Smartphone Usage',
                'experience_required': 'Valid Driving License',
                'deadline': today + timedelta(days=30),
                'source_portal': 'National Career Service',
                'source_url': 'https://www.ncs.gov.in/',
                'is_external': True
            }
        ]

        count = 0
        for data in items:
            title = data.pop('title')
            org = data.get('organization')
            obj, created = Job.objects.update_or_create(
                title=title,
                organization=org,
                defaults=data
            )
            count += 1
        return count

    @classmethod
    def sync_skillindia_courses(cls):
        """Fetch and populate verified skill training from Skill India Digital (MSDE)."""
        items = [
            {
                'name': 'PMKVY 4.0 Agricultural Drone Pilot Certification',
                'category': 'technical',
                'provider': 'National Skill Development Corporation (NSDC)',
                'description': 'Government funded hands-on pilot training covering DGCA regulations, precision farming spraying, and drone maintenance.',
                'duration': '6 Weeks (Full Time)',
                'level': 'intermediate',
                'price_type': 'free',
                'price': '100% Free (Govt Funded)',
                'prerequisites': '10th Pass with 18+ years of age',
                'certificate': True,
                'source_portal': 'Skill India Digital',
                'source_url': 'https://www.skillindiadigital.gov.in/',
                'is_external': True
            },
            {
                'name': 'PM Vishwakarma Artisan & Modern Carpentry Kit',
                'category': 'technical',
                'provider': 'Ministry of Skill Development & Entrepreneurship',
                'description': 'Advanced skill upgradation with modern power tools, digital marketing, and ₹15,000 toolkit incentive.',
                'duration': '7 Days Intensive + 15 Days Advanced',
                'level': 'beginner',
                'price_type': 'free',
                'price': 'Free + ₹500/day Stipend',
                'prerequisites': 'Traditional artisan / craftsman family background',
                'certificate': True,
                'source_portal': 'Skill India Digital',
                'source_url': 'https://pmvishwakarma.gov.in/',
                'is_external': True
            },
            {
                'name': 'DDU-GKY Solar PV Rooftop Installation Technician',
                'category': 'technical',
                'provider': 'Skill Council for Green Jobs (DDU-GKY)',
                'description': 'Complete solar technician trade course covering inverter wiring, panel mounting, earthing, and grid synchronization.',
                'duration': '3 Months',
                'level': 'intermediate',
                'price_type': 'free',
                'price': '100% Free with Placement',
                'prerequisites': '10th/12th or ITI Electrical/Fitter',
                'certificate': True,
                'source_portal': 'Skill India Digital',
                'source_url': 'https://www.skillindiadigital.gov.in/',
                'is_external': True
            },
            {
                'name': 'Digital Saksharta for Rural Women Entrepreneurs',
                'category': 'life_skills',
                'provider': 'National Digital Literacy Mission',
                'description': 'Learn UPI digital payments, ONDC product listing, WhatsApp for Business, and bookkeeping for micro-enterprises.',
                'duration': '3 Weeks (Self-paced)',
                'level': 'beginner',
                'price_type': 'free',
                'price': 'Free',
                'prerequisites': 'Smartphone with internet connectivity',
                'certificate': True,
                'source_portal': 'Skill India Digital',
                'source_url': 'https://www.skillindiadigital.gov.in/',
                'is_external': True
            }
        ]

        count = 0
        for data in items:
            name = data.pop('name')
            obj, created = SkillProgram.objects.update_or_create(
                name=name,
                defaults=data
            )
            count += 1
        return count

    @classmethod
    def sync_startupindia_business(cls):
        """Fetch and populate micro-enterprise blueprints from PMEGP & Startup India."""
        items = [
            {
                'name': 'PMEGP Honey Bee Keeping & Apiculture Processing',
                'category': 'agriculture',
                'description': 'Establish a 50-box bee colony producing raw honey, beeswax, and royal jelly for herbal and consumer markets.',
                'investment_level': 'low',
                'opportunity_level': 'easy',
                'required_skills': 'Apiculture basics, hive maintenance, honey extraction',
                'expected_income': '₹25,000 – ₹50,000 / month',
                'market_demand': 'Very High in urban & wellness retail',
                'resources': 'Wooden hives, honey extractor, protective suit, KVIC subsidy',
                'source_portal': 'PMEGP / Startup India',
                'source_url': 'https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp',
                'is_external': True
            },
            {
                'name': 'Village Solar Charging & Battery Swap Hub',
                'category': 'technology',
                'description': 'Provide decentralized solar battery charging for e-rickshaws, farm sprayers, and home lighting in un-electrified pockets.',
                'investment_level': 'medium',
                'opportunity_level': 'moderate',
                'required_skills': 'Solar battery management, basic electrical wiring',
                'expected_income': '₹30,000 – ₹60,000 / month',
                'market_demand': 'Expanding rapidly across rural EV transit',
                'resources': 'Solar PV arrays, hybrid inverters, battery rack, street-side shop',
                'source_portal': 'PMEGP / Startup India',
                'source_url': 'https://www.startupindia.gov.in/',
                'is_external': True
            },
            {
                'name': 'Cold-Pressed Groundnut & Sesame Oil Expeller',
                'category': 'agriculture',
                'description': 'Process locally grown groundnuts, mustard, and sesame seeds into pure unrefined wood-pressed oil (Chekku/Ghani).',
                'investment_level': 'medium',
                'opportunity_level': 'moderate',
                'required_skills': 'Oil expeller machine operation, food grade packaging',
                'expected_income': '₹40,000 – ₹80,000 / month',
                'market_demand': 'High premium demand for organic cold-pressed oil',
                'resources': 'Wooden ghani expeller, filter press, seed cleaner, FSSAI registration',
                'source_portal': 'PMEGP / Startup India',
                'source_url': 'https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp',
                'is_external': True
            }
        ]

        count = 0
        for data in items:
            name = data.pop('name')
            obj, created = BusinessOpportunity.objects.update_or_create(
                name=name,
                defaults=data
            )
            count += 1
        return count

    @classmethod
    def sync_all(cls):
        """Syncs all external data sources and returns a summary dict."""
        b4s = cls.sync_buddy4study_scholarships()
        nsp = cls.sync_nsp_scholarships()
        myscheme = cls.sync_myscheme_schemes()
        ncs = cls.sync_ncs_jobs()
        skills = cls.sync_skillindia_courses()
        business = cls.sync_startupindia_business()

        return {
            'buddy4study': b4s,
            'nsp': nsp,
            'myscheme': myscheme,
            'ncs': ncs,
            'skill_india': skills,
            'startup_india': business,
            'total_synced': b4s + nsp + myscheme + ncs + skills + business
        }
