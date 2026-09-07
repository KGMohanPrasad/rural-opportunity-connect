import os
import sys
from datetime import date

# Configure UTF-8 for console output
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from government_schemes.models import GovernmentScheme
from scholarships.models import Scholarship

def populate_schemes():
    print("Populating authentic Government Schemes...")
    GovernmentScheme.objects.all().delete()
    
    schemes_data = [
        {
            "name": "PM Surya Ghar: Muft Bijli Yojana",
            "department": "Ministry of New and Renewable Energy (MNRE)",
            "category": "rural",
            "description": "National initiative to provide free electricity up to 300 units per month to 1 crore rural and urban households by installing rooftop solar systems with direct central financial assistance.",
            "target_beneficiaries": "Rural and urban households with residential electricity connections and suitable rooftop space.",
            "benefits": "Direct bank subsidy up to Rs 78,000 for 3kW solar installation, zero electricity bills up to 300 units, and income from selling surplus power back to the grid.",
            "eligibility": "Indian citizen, owns a residential house with suitable roof, existing domestic power connection, has not availed any other rooftop solar subsidy.",
            "required_documents": "Electricity Bill, Aadhaar Card, Bank Passbook, Roof Ownership Document / NOC, Passport Photo",
            "application_process": "Register on pmsuryaghar.gov.in with consumer number, submit rooftop details, choose registered DISCOM vendor, complete net-metering, receive subsidy directly into bank account.",
            "official_website": "https://pmsuryaghar.gov.in/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/pmsgmby",
            "is_external": False
        },
        {
            "name": "PM Vishwakarma Scheme",
            "department": "Ministry of Micro, Small and Medium Enterprises (MSME)",
            "category": "skills",
            "description": "Flagship scheme providing end-to-end support to traditional artisans and craftspeople working with hands and tools across 18 traditional trades in rural and semi-urban India.",
            "target_beneficiaries": "Artisans, carpenters, blacksmiths, potters, cobblers, weavers, tailors, sculptors, and traditional craftsmen.",
            "benefits": "PM Vishwakarma Certificate & ID Card, basic skill training (5-7 days) with Rs 500/day stipend, toolkit incentive of Rs 15,000, collateral-free enterprise credit up to Rs 3,00,000 at 5% concessional interest.",
            "eligibility": "Minimum age 18 years, engaged in one of 18 traditional trades, not availed similar credit loans (PMEGP/Mudra) in last 5 years, restricted to one member per family.",
            "required_documents": "Aadhaar Card, Mobile Linked with Aadhaar, Bank Account Passbook, Ration Card / Family Proof",
            "application_process": "Register through Common Service Centre (CSC) on pmvishwakarma.gov.in, undergo Gram Panchayat verification, complete skill assessment, and apply for loan tranche.",
            "official_website": "https://pmvishwakarma.gov.in/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/pm-vishwakarma",
            "is_external": False
        },
        {
            "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
            "department": "Ministry of Agriculture & Farmers Welfare",
            "category": "agriculture",
            "description": "Central sector scheme providing income support to all landholding farmer families across the country to supplement their financial needs for procuring various agricultural inputs.",
            "target_beneficiaries": "Small, marginal, and all operational landholder farmer families owning cultivable land.",
            "benefits": "Direct cash transfer of Rs 6,000 per annum paid in three equal installments of Rs 2,000 directly into Aadhaar-seeded bank accounts.",
            "eligibility": "Landholding farmer family with cultivable land in land records. Excludes institutional landholders, income-tax payers, and constitutional post holders.",
            "required_documents": "Aadhaar Card, Land Revenue Records (Khata/Khasra/Patta), Aadhaar-seeded Active Bank Account, e-KYC Verification",
            "application_process": "Apply via pmkisan.gov.in portal under 'New Farmer Registration' or visit local Village Revenue Officer (Patwari) / CSC centre. Complete biometric or OTP-based e-KYC.",
            "official_website": "https://pmkisan.gov.in/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/pm-kisan",
            "is_external": False
        },
        {
            "name": "Prime Minister's Employment Generation Programme (PMEGP)",
            "department": "Ministry of MSME / Khadi and Village Industries Commission (KVIC)",
            "category": "entrepreneurship",
            "description": "Credit-linked subsidy programme to generate self-employment opportunities through establishment of micro-enterprises in non-farm rural and urban sectors.",
            "target_beneficiaries": "Rural youth, aspiring entrepreneurs, self-help groups, and cooperative societies setting up new micro-units.",
            "benefits": "Bank-financed project cost up to Rs 50 lakh for manufacturing and Rs 20 lakh for service sector with capital subsidy up to 35% in rural areas for special categories.",
            "eligibility": "Individuals aged 18+ years. For projects above Rs 10 lakh in manufacturing or Rs 5 lakh in services, minimum educational qualification is 8th pass.",
            "required_documents": "Aadhaar Card, Detailed Project Report (DPR), Educational Certificate, Caste/Special Category Certificate, Rural Area Certificate from Panchayat",
            "application_process": "Submit online application with project proposal on kviconline.gov.in/pmegpeportal. Approved projects forwarded to financing bank for sanction and subsidy release.",
            "official_website": "https://www.kviconline.gov.in/pmegpeportal/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/pmegp",
            "is_external": False
        },
        {
            "name": "Pradhan Mantri Awas Yojana - Gramin (PMAY-G)",
            "department": "Ministry of Rural Development",
            "category": "housing",
            "description": "National flagship housing mission providing financial assistance to houseless and people living in dilapidated or kutcha houses to build a pucca dwelling unit with clean energy and sanitation.",
            "target_beneficiaries": "Rural homeless households and families living in kutcha or dilapidated houses identified via SECC/Awas+ lists.",
            "benefits": "Unit financial assistance of Rs 1,20,000 in plain areas and Rs 1,30,000 in hilly/difficult areas, plus 90-95 days of unskilled wage labor under MGNREGA (~Rs 27,000) and Rs 12,000 for toilet under SBM-G.",
            "eligibility": "Rural households without pucca house, verified via Gram Sabha and SECC/Awas+ survey data. Priority to SC/ST, women-headed, and disabled individuals.",
            "required_documents": "Aadhaar Card, Bank Account Details (DBT enabled), MGNREGA Job Card Number, Land/Homestead Right Certificate",
            "application_process": "Beneficiary list prepared by Gram Sabha and verified via Awaas+ app. Geotagged milestone photos at foundation, plinth, and lintel stages trigger direct bank transfers.",
            "official_website": "https://pmayg.nic.in/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/pmay-g",
            "is_external": False
        },
        {
            "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "department": "Ministry of Agriculture & Farmers Welfare",
            "category": "agriculture",
            "description": "Comprehensive agricultural insurance scheme providing financial support to farmers suffering crop loss or damage due to non-preventable natural risks, drought, pests, and unseasonal weather.",
            "target_beneficiaries": "All farmers including sharecroppers and tenant farmers growing notified crops in notified areas.",
            "benefits": "Comprehensive risk coverage from pre-sowing to post-harvest losses. Uniformly low premium: 2% for Kharif crops, 1.5% for Rabi crops, and 5% for commercial/horticultural crops; balance subsidized by Govt.",
            "eligibility": "Farmers cultivating notified crops in defined insurance units. Open to both loanee and non-loanee farmers.",
            "required_documents": "Aadhaar Card, Land Possession Certificate / RoR / Khasra, Sowing Certificate from Village Revenue Officer / Panchayat, Bank Passbook copy",
            "application_process": "Apply through National Crop Insurance Portal (pmfby.gov.in), nearest CSC centre, or local bank branch within the cut-off sowing notification date.",
            "official_website": "https://pmfby.gov.in/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/pmfby",
            "is_external": False
        },
        {
            "name": "Ayushman Bharat - PM Jan Arogya Yojana (AB-PMJAY)",
            "department": "National Health Authority, Ministry of Health & Family Welfare",
            "category": "healthcare",
            "description": "World's largest government-funded health assurance scheme providing cashless secondary and tertiary healthcare coverage to over 12 crore vulnerable rural and urban families.",
            "target_beneficiaries": "Bottom 40% vulnerable and economically weak rural families identified as per SECC deprivation criteria.",
            "benefits": "Cashless and paperless inpatient treatment up to Rs 5,00,000 per family per year across more than 27,000 empaneled public and private hospitals across India.",
            "eligibility": "Families listed in SECC 2011 database or NFSA ration card databases, as well as senior citizens aged 70+ irrespective of income.",
            "required_documents": "Aadhaar Card, Ration Card / Family Identification Document, Active Mobile Number",
            "application_process": "Check eligibility online at beneficiary.nha.gov.in or visit nearest Ayushman Arogya Mandir / CSC / Hospital Helpdesk to generate Ayushman Card instantly.",
            "official_website": "https://beneficiary.nha.gov.in/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/ab-pmjay",
            "is_external": False
        },
        {
            "name": "Mahatma Gandhi NREGA (MGNREGS)",
            "department": "Ministry of Rural Development",
            "category": "employment",
            "description": "Statutory demand-driven wage employment program guaranteeing livelihood security in rural areas by providing at least 100 days of guaranteed wage employment per financial year.",
            "target_beneficiaries": "Every rural household whose adult members volunteer to do unskilled manual work on community and individual infrastructure works.",
            "benefits": "Statutory wage payment deposited directly into Aadhaar-linked bank/post office account within 15 days; creation of durable rural assets (farm ponds, water conservation, road connectivity).",
            "eligibility": "Adult members of rural households willing to do unskilled manual labor. Residing within Gram Panchayat area.",
            "required_documents": "Aadhaar Card, Passport size photographs of all adult members, Bank/Post Office Savings Account details",
            "application_process": "Submit application to local Gram Panchayat for Job Card issuance. Request employment verbally or in writing; Gram Panchayat issues dated receipt and work allocation within 15 days.",
            "official_website": "https://nrega.nic.in/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/mgnrega",
            "is_external": False
        },
        {
            "name": "Lakhpati Didi Initiative (DAY-NRLM)",
            "department": "Ministry of Rural Development",
            "category": "women",
            "description": "Special mission under Deendayal Antyodaya Yojana - National Rural Livelihoods Mission to enable rural women self-help group (SHG) members to earn a sustainable income of at least Rs 1,00,000 per year.",
            "target_beneficiaries": "Rural women organized into Self Help Groups (SHGs) and their Village Organizations.",
            "benefits": "Access to community investment funds, bank credit linkage, business mentoring, market linkages, training in high-value agriculture, livestock, drone piloting (Namo Drone Didi), and local retail.",
            "eligibility": "Active member of a DAY-NRLM registered Self Help Group for at least 6 months with regular attendance, savings, and internal loan repayments.",
            "required_documents": "SHG Member Passbook, Aadhaar Card, Bank Account Details, Livelihood Micro-Plan Copy",
            "application_process": "Coordinate with Community Resource Person (CRP) and Cluster Level Federation (CLF) to prepare an individual livelihood enterprise plan.",
            "official_website": "https://aajeevika.gov.in/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/lakhpatididi",
            "is_external": False
        },
        {
            "name": "Pradhan Mantri Mudra Yojana (PMMY)",
            "department": "Department of Financial Services, Ministry of Finance",
            "category": "financial",
            "description": "Scheme to provide collateral-free institutional credit up to Rs 20 lakh to non-corporate, non-farm small and micro enterprises for manufacturing, trading, services, and allied agricultural activities.",
            "target_beneficiaries": "Small shopkeepers, rural artisans, food processing units, repair shops, transport operators, and aspiring micro-entrepreneurs.",
            "benefits": "Collateral-free loans in 4 categories: Shishu (up to Rs 50,000), Kishore (Rs 50,000 to Rs 5 lakh), Tarun (Rs 5 lakh to Rs 10 lakh), and Tarun Plus (Rs 10 lakh to Rs 20 lakh) at competitive bank rates.",
            "eligibility": "Any Indian citizen with a viable business plan for a non-farm income-generating activity, with no history of default with any financial institution.",
            "required_documents": "Aadhaar Card, PAN Card, Business Address Proof, Quotation of Machinery / Items to be purchased, Bank statement for last 6 months",
            "application_process": "Apply online through JanSamarth portal (jansamarth.in) or visit any Commercial Bank, RRB, Small Finance Bank, or MFI with business project proposal.",
            "official_website": "https://www.mudra.org.in/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/pmmy",
            "is_external": False
        },
        {
            "name": "Pradhan Mantri Matsya Sampada Yojana (PMMSY)",
            "department": "Department of Fisheries, Ministry of Fisheries, Animal Husbandry & Dairying",
            "category": "agriculture",
            "description": "Flagship scheme to bring about ecologically sustainable, economically viable Blue Revolution through focused investment in fish production, hatcheries, cold storage, and aquaculture value chain.",
            "target_beneficiaries": "Fishers, fish farmers, fish workers, SHGs, JLGs, fisheries cooperatives, and rural youth setting up aquaculture projects.",
            "benefits": "Government financial assistance of 40% (general category) and up to 60% (women, SC/ST) on capital investment for new pond construction, biofloc units, recirculatory aquaculture systems (RAS), and refrigerated transport.",
            "eligibility": "Individual fish farmers, groups, or enterprises with suitable land or water bodies, or valid lease agreements.",
            "required_documents": "Aadhaar Card, Land/Water Body Ownership or Lease Agreement (minimum 7-10 years), Detailed Project Report (DPR), Bank Account Details",
            "application_process": "Submit project proposal to the District Fisheries Officer or apply via PMMSY MIS portal (pmmsy.dof.gov.in). Approved proposals receive back-ended subsidy upon project completion.",
            "official_website": "https://pmmsy.dof.gov.in/",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/pmmsy",
            "is_external": False
        },
        {
            "name": "Kisan Credit Card (KCC) Scheme",
            "department": "Ministry of Agriculture & Farmers Welfare / RBI / NABARD",
            "category": "financial",
            "description": "Pioneering financial credit instrument providing adequate and timely credit under a single window to farmers for their cultivation and non-cultivation agricultural requirements, dairy, and fisheries.",
            "target_beneficiaries": "All farmers, individual/joint borrowers, tenant farmers, oral lessees, sharecroppers, SHGs or Joint Liability Groups of farmers.",
            "benefits": "Revolving credit line up to Rs 3,00,000 at an effective interest rate of 4% per annum (standard 7% minus 3% prompt repayment incentive). No collateral required for loans up to Rs 1,60,000.",
            "eligibility": "Owner cultivators or tenant farmers engaged in crop cultivation, dairy farming, poultry, sheep/goat rearing, or fisheries.",
            "required_documents": "Aadhaar Card, PAN Card, Land Records (7/12 extract, Khasra/Khatauni) or crop cultivation certificate, Passport photo",
            "application_process": "Fill one-page KCC application available on pmkisan.gov.in or any public sector/regional rural bank branch. Banks are mandated to issue KCC within 14 working days.",
            "official_website": "https://www.myscheme.gov.in/schemes/kcc",
            "source_portal": "myScheme.gov.in",
            "source_url": "https://www.myscheme.gov.in/schemes/kcc",
            "is_external": False
        }
    ]

    for item in schemes_data:
        GovernmentScheme.objects.create(**item)
    print(f"Successfully populated {len(schemes_data)} Government Schemes.")

def populate_scholarships():
    print("Populating authentic Scholarships...")
    Scholarship.objects.all().delete()

    scholarships_data = [
        {
            "name": "National Means-cum-Merit Scholarship Scheme (NMMSS)",
            "provider": "Department of School Education & Literacy, Ministry of Education, GoI",
            "description": "Centrally sponsored scholarship to provide financial assistance to meritorious students from economically weaker sections to arrest dropouts after class 8 and encourage secondary schooling.",
            "amount": "Rs 12,000 per annum (Rs 1,000 per month)",
            "education_level": "12th",
            "eligibility": "Studying in Class 9 in government, local body, or government-aided schools with at least 55% marks in Class 8. Continued till Class 12 upon passing exams.",
            "income_limit": "Family income not exceeding Rs 3,50,000 per annum",
            "category": "School Education / Merit",
            "course": "Secondary & Higher Secondary Education (Class 9 to 12)",
            "required_documents": "Aadhaar Card, Class 8 Marksheet, Family Income Certificate, Bank Account Details (DBT enabled), School Bonafide Certificate",
            "application_deadline": date(2026, 11, 30),
            "source_portal": "National Scholarship Portal (NSP)",
            "source_url": "https://scholarships.gov.in/",
            "is_external": False
        },
        {
            "name": "PM Young Achievers Scholarship Award Scheme (PM-YASASVI)",
            "provider": "Ministry of Social Justice and Empowerment, Government of India",
            "description": "Comprehensive top-class education scholarship scheme for Other Backward Classes (OBC), Economically Backward Classes (EBC), and De-Notified Nomadic Tribes (DNT).",
            "amount": "Up to Rs 1,25,000 per annum (Full tuition fees + living allowance)",
            "education_level": "bachelor",
            "eligibility": "Belong to OBC/EBC/DNT category, studying in identified top-class schools or recognized higher education institutions/universities.",
            "income_limit": "Annual family income not exceeding Rs 2,50,000 per annum",
            "category": "OBC / EBC / DNT Merit-cum-Means",
            "course": "Class 9 to 12 & Undergraduate Professional Degree Programs",
            "required_documents": "Aadhaar Card, Caste/Category Certificate, Income Certificate from competent authority, Admission Fee Receipt, Bank Passbook",
            "application_deadline": date(2026, 10, 31),
            "source_portal": "National Scholarship Portal (NSP)",
            "source_url": "https://scholarships.gov.in/",
            "is_external": False
        },
        {
            "name": "Central Sector Scheme of Scholarships for College & University Students (CSSS)",
            "provider": "Department of Higher Education, Ministry of Education, GoI",
            "description": "Scholarship awarded to meritorious students from low-income families pursuing regular graduate and post-graduate degree courses in recognized colleges and universities.",
            "amount": "Rs 12,000/yr for Graduation; Rs 20,000/yr for Post-Graduation",
            "education_level": "bachelor",
            "eligibility": "Scored above 80th percentile in relevant stream in Class 12 board exams, pursuing full-time degree program. Not receiving any other central/state scholarship.",
            "income_limit": "Gross family income not exceeding Rs 4,50,000 per annum",
            "category": "Merit-cum-Means (Higher Education)",
            "course": "Full-time Undergraduate & Postgraduate Degree Programs",
            "required_documents": "Class 12 Marksheet, College Admission Proof/Bonafide, Aadhaar Card, Income Certificate, Bank Passbook",
            "application_deadline": date(2026, 11, 15),
            "source_portal": "National Scholarship Portal (NSP)",
            "source_url": "https://scholarships.gov.in/",
            "is_external": False
        },
        {
            "name": "Post-Matric Scholarship Scheme for SC & ST Students",
            "provider": "Ministry of Social Justice & Empowerment & Ministry of Tribal Affairs, GoI",
            "description": "Centrally sponsored scheme providing complete financial support to Scheduled Caste and Scheduled Tribe students studying at post-matriculation or post-secondary stages.",
            "amount": "Full compulsory non-refundable fees + monthly maintenance allowance up to Rs 13,500/yr",
            "education_level": "bachelor",
            "eligibility": "SC or ST community students enrolled in recognized post-matric courses (diploma, degree, master's) in government or accredited private institutions.",
            "income_limit": "Annual family income not exceeding Rs 2,50,000 per annum",
            "category": "SC / ST Welfare",
            "course": "Post-Matric Diploma, Degree, Medical, Engineering, and Professional Courses",
            "required_documents": "Caste Certificate, Income Certificate, Previous Year Marksheets, Current Year Fee Structure, Aadhaar Card, Bank Account Details",
            "application_deadline": date(2026, 12, 15),
            "source_portal": "National Scholarship Portal (NSP)",
            "source_url": "https://scholarships.gov.in/",
            "is_external": False
        },
        {
            "name": "AICTE Pragati Scholarship Scheme for Girl Students",
            "provider": "All India Council for Technical Education (AICTE), Ministry of Education",
            "description": "Empowerment scheme aimed at providing assistance for advancement of girls pursuing technical degree or diploma education in AICTE approved institutions.",
            "amount": "Rs 50,000 per annum for every year of study",
            "education_level": "diploma",
            "eligibility": "Female student admitted to 1st year of Degree or Diploma course (or 2nd year through lateral entry) in an AICTE approved institution. Maximum 2 girls per family.",
            "income_limit": "Family income not exceeding Rs 8,00,000 per annum",
            "category": "Girls in Technical Education",
            "course": "Engineering, Technology, Architecture, Pharmacy, Diploma in Engineering",
            "required_documents": "Class 10 & 12 / ITI Marksheet, AICTE College Allotment Letter, Tuitions Fee Receipt, Family Income Certificate, Aadhaar Card",
            "application_deadline": date(2026, 10, 31),
            "source_portal": "National Scholarship Portal (NSP)",
            "source_url": "https://scholarships.gov.in/",
            "is_external": False
        },
        {
            "name": "HDFC Bank Parivartan's Educational Crisis Support Scholarship (ECSS)",
            "provider": "HDFC Bank CSR Foundation / Buddy4Study",
            "description": "Flagship social initiative to help meritorious students from economically disadvantaged families who are going through personal or financial crises continue their education.",
            "amount": "Up to Rs 75,000 per year (covers institutional fees and books)",
            "education_level": "bachelor",
            "eligibility": "Students enrolled in Class 1 to 12, Diploma, ITI, Undergraduate, or Postgraduate courses who have secured at least 55% marks in prior examinations.",
            "income_limit": "Annual family income less than or equal to Rs 2,50,000",
            "category": "Crisis Support & Merit",
            "course": "General & Professional Degree Courses (BA, BSc, BCom, BTech, MBBS, BCA)",
            "required_documents": "Previous Year Marksheet, Identity Proof (Aadhaar), Current Year Admission Proof, Crisis Document (if applicable) or Income Certificate, Bank Details",
            "application_deadline": date(2026, 9, 30),
            "source_portal": "Buddy4Study",
            "source_url": "https://www.buddy4study.com/page/hdfc-bank-parivartans-ecss-programme",
            "is_external": False
        },
        {
            "name": "Reliance Foundation Undergraduate Scholarship",
            "provider": "Reliance Foundation",
            "description": "Prestigious scholarship program empowering young students with grants to support undergraduate study in any stream of study across recognized colleges in India.",
            "amount": "Up to Rs 2,00,000 for the full duration of undergraduate degree",
            "education_level": "bachelor",
            "eligibility": "First-year full-time undergraduate students who scored minimum 60% in Class 12 board examination. Includes an aptitude test.",
            "income_limit": "Household income up to Rs 15,00,000 (preference given to < Rs 2,50,000)",
            "category": "Undergraduate Merit-cum-Means",
            "course": "All Undergraduate Degree Streams (Arts, Science, Commerce, Engineering, Law)",
            "required_documents": "Class 12 Marksheet, College Bonafide/Admission Letter, Family Income Certificate, Aadhaar Card, Passport Photograph",
            "application_deadline": date(2026, 10, 15),
            "source_portal": "Reliance Foundation Scholarships",
            "source_url": "https://www.scholarships.reliancefoundation.org/",
            "is_external": False
        },
        {
            "name": "Santoor Women's Scholarship",
            "provider": "Wipro Cares & Azim Premji Foundation",
            "description": "Annual scholarship program dedicated to encouraging and assisting young rural women from underprivileged backgrounds in pursuing higher education.",
            "amount": "Rs 24,000 per annum for full 3-year undergraduate course",
            "education_level": "bachelor",
            "eligibility": "Young women who completed Class 10 from local government school and Class 12 from government junior college, enrolled in first year of recognized 3-year degree.",
            "income_limit": "Family income not exceeding Rs 3,00,000 per annum",
            "category": "Rural Women Empowerment",
            "course": "Humanities, Liberal Arts, Sciences, Commerce (B.A., B.Sc., B.Com.)",
            "required_documents": "Class 10 & 12 Government School Pass Certificates, Degree College Bonafide/Fee Receipt, Aadhaar Card, Bank Passbook in student's name",
            "application_deadline": date(2026, 10, 20),
            "source_portal": "Buddy4Study",
            "source_url": "https://www.buddy4study.com/page/santoor-scholarship-programme",
            "is_external": False
        },
        {
            "name": "Kotak Kanya Scholarship",
            "provider": "Kotak Education Foundation",
            "description": "Financial assistance program for meritorious girl students from low-income families to pursue professional graduation courses from premier and accredited institutes.",
            "amount": "Rs 1,50,000 per year until completion of professional degree",
            "education_level": "bachelor",
            "eligibility": "Meritorious girl students who scored 75%+ in Class 12 board exams, enrolled in 1st year of professional degree courses (Engineering, MBBS, Architecture, Design, Integrated LLB).",
            "income_limit": "Annual family income less than or equal to Rs 6,00,000",
            "category": "Professional Education / Girls",
            "course": "B.Tech, B.E., MBBS, B.Arch, Integrated 5-Year Law, Design Degree",
            "required_documents": "Class 12 Marksheet, Entrance Exam Scorecard (JEE/NEET/CLAT), College Admission Letter & Fee Receipt, Aadhaar Card, Parents' Income Certificate",
            "application_deadline": date(2026, 9, 30),
            "source_portal": "Buddy4Study",
            "source_url": "https://www.buddy4study.com/page/kotak-kanya-scholarship",
            "is_external": False
        },
        {
            "name": "SBI Asha Scholarship Programme",
            "provider": "SBI Foundation (CSR arm of State Bank of India)",
            "description": "Scholarship initiative to provide financial assistance to top-performing rural and semi-urban students studying in top NIRF-ranked institutions and premier universities.",
            "amount": "Rs 50,000 to Rs 2,00,000 per academic year",
            "education_level": "master",
            "eligibility": "Students pursuing undergraduate or postgraduate courses in top NIRF-ranked institutions, with minimum 75% marks in previous qualifying examination.",
            "income_limit": "Gross annual family income up to Rs 3,00,000",
            "category": "Higher & Postgraduate Education",
            "course": "Bachelors & Masters in Technology, Science, Management, Medicine",
            "required_documents": "Previous Academic Marksheets, Admission Letter from Institution, Institutional Fee Receipt, Income Certificate, Aadhaar Card, Student Bank Account Proof",
            "application_deadline": date(2026, 11, 5),
            "source_portal": "Buddy4Study",
            "source_url": "https://www.buddy4study.com/page/sbi-asha-scholarship-program",
            "is_external": False
        },
        {
            "name": "Keep India Smiling Foundational Scholarship Programme",
            "provider": "Colgate-Palmolive (India) Limited",
            "description": "Foundational educational scholarship to provide foundational support to meritorious students pursuing secondary education, higher secondary, graduation, or vocational training.",
            "amount": "Rs 30,000 to Rs 50,000 per annum",
            "education_level": "12th",
            "eligibility": "Students who passed Class 10 or 12 with at least 75% marks and enrolled in Class 11, 12, 3-year graduation, or 1-2 year recognized vocational ITI/polytechnic diploma.",
            "income_limit": "Annual household income less than Rs 5,00,000",
            "category": "Vocational & Higher Secondary",
            "course": "Higher Secondary (10+2), ITI Trades, Polytechnic Diploma, General Graduation",
            "required_documents": "Class 10 or 12 Marksheet, Entrance Exam / Admission Letter, Current College/School ID, Income Proof, Aadhaar Card, Disability Certificate (if applicable)",
            "application_deadline": date(2026, 10, 25),
            "source_portal": "Buddy4Study",
            "source_url": "https://www.buddy4study.com/page/colgate-keep-india-smiling-scholarship",
            "is_external": False
        },
        {
            "name": "Vidyasaarathi Rural Youth Higher Education Scholarship",
            "provider": "Protean eGov Technologies / Vidyasaarathi Portal",
            "description": "Special corporate CSR education scholarship for young students from rural and farming families pursuing full-time technical diplomas and undergraduate programs.",
            "amount": "Up to Rs 40,000 per academic year",
            "education_level": "diploma",
            "eligibility": "Students with rural domicile who have completed Class 10/12 with minimum 60% marks and are currently enrolled in recognized full-time diploma or degree programs.",
            "income_limit": "Family income not exceeding Rs 4,00,000 per annum",
            "category": "Rural Youth Technical Scholarship",
            "course": "Diploma in Mechanical/Civil/Electrical/Automobile, B.Sc., B.Voc.",
            "required_documents": "Class 10/12 Passing Certificate, Rural Domicile Certificate, Admission Confirmation Letter, Fee Receipt, Aadhaar Card, Bank Passbook",
            "application_deadline": date(2026, 11, 20),
            "source_portal": "Vidyasaarathi Portal",
            "source_url": "https://www.vidyasaarathi.co.in/",
            "is_external": False
        }
    ]

    for item in scholarships_data:
        Scholarship.objects.create(**item)
    print(f"Successfully populated {len(scholarships_data)} Scholarships.")

if __name__ == '__main__':
    populate_schemes()
    populate_scholarships()
    print("ALL DONE SUCCESSFULLY!")
