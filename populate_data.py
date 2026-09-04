"""
Script to populate the database with sample data for Rural Opportunity Connect
Run with: python manage.py shell < populate_data.py
"""

from datetime import datetime, timedelta
from django.utils import timezone
from opportunities.models import Job
from scholarships.models import Scholarship
from government_schemes.models import GovernmentScheme
from skills.models import SkillProgram
from business.models import BusinessOpportunity

# Clear existing data
Job.objects.all().delete()
Scholarship.objects.all().delete()
GovernmentScheme.objects.all().delete()
SkillProgram.objects.all().delete()
BusinessOpportunity.objects.all().delete()

# Create Jobs
jobs_data = [
    {
        'title': 'Data Entry Operator',
        'organization': 'ABC Tech Solutions',
        'description': 'Seeking a data entry operator to handle large databases and maintain data quality.',
        'location': 'Bangalore',
        'salary_min': 15000,
        'salary_max': 20000,
        'job_type': 'full_time',
        'required_skills': 'MS Office, Data Entry, Typing Speed',
        'experience_required': '1-2 years',
        'deadline': timezone.now().date() + timedelta(days=45),
    },
    {
        'title': 'Farm Assistant',
        'organization': 'Green Valley Farms',
        'description': 'Looking for enthusiastic farm assistants to help with crop management and harvesting.',
        'location': 'Tamil Nadu',
        'salary_min': 12000,
        'salary_max': 18000,
        'job_type': 'full_time',
        'required_skills': 'Agriculture Knowledge, Physical Fitness',
        'experience_required': 'Fresher or 1+ year',
        'deadline': timezone.now().date() + timedelta(days=30),
    },
    {
        'title': 'Computer Operator',
        'organization': 'Digital Services India',
        'description': 'Operate computers and peripherals for data management and file organization.',
        'location': 'Pune',
        'salary_min': 18000,
        'salary_max': 25000,
        'job_type': 'full_time',
        'required_skills': 'Computer Literacy, MS Office, Internet',
        'experience_required': '2+ years',
        'deadline': timezone.now().date() + timedelta(days=60),
    },
    {
        'title': 'Electrician',
        'organization': 'Power Solutions Co.',
        'description': 'Skilled electrician needed for residential and commercial installations.',
        'location': 'Delhi',
        'salary_min': 20000,
        'salary_max': 30000,
        'job_type': 'full_time',
        'required_skills': 'Electrical Work, Safety Knowledge, Problem Solving',
        'experience_required': '3+ years',
        'deadline': timezone.now().date() + timedelta(days=50),
    },
    {
        'title': 'Solar Technician',
        'organization': 'Renewable Energy Ltd',
        'description': 'Install and maintain solar panel systems for homes and businesses.',
        'location': 'Karnataka',
        'salary_min': 22000,
        'salary_max': 32000,
        'job_type': 'full_time',
        'required_skills': 'Solar Installation, Electrical Knowledge, Customer Service',
        'experience_required': '2+ years',
        'deadline': timezone.now().date() + timedelta(days=55),
    },
    {
        'title': 'Delivery Executive',
        'organization': 'FastDeliver Logistics',
        'description': 'Deliver packages to customers efficiently and collect payments.',
        'location': 'Chennai',
        'salary_min': 16000,
        'salary_max': 22000,
        'job_type': 'full_time',
        'required_skills': 'Communication, Time Management, Bike License',
        'experience_required': 'Fresher or 1+ year',
        'deadline': timezone.now().date() + timedelta(days=35),
    },
    {
        'title': 'Tailoring Assistant',
        'organization': 'Fashion Studio India',
        'description': 'Assist in tailoring and altering garments for customers.',
        'location': 'Hyderabad',
        'salary_min': 14000,
        'salary_max': 19000,
        'job_type': 'full_time',
        'required_skills': 'Sewing, Tailoring, Attention to Detail',
        'experience_required': '1-2 years',
        'deadline': timezone.now().date() + timedelta(days=40),
    },
    {
        'title': 'Agriculture Field Assistant',
        'organization': 'Modern Agriculture Foundation',
        'description': 'Support agricultural researchers in field trials and data collection.',
        'location': 'Gujarat',
        'salary_min': 13000,
        'salary_max': 19000,
        'job_type': 'part_time',
        'required_skills': 'Agriculture, Data Collection, Basic Computer Skills',
        'experience_required': 'Fresher',
        'deadline': timezone.now().date() + timedelta(days=25),
    },
    {
        'title': 'Call Center Executive',
        'organization': 'Customer Care Solutions',
        'description': 'Handle customer inquiries and provide support over the phone.',
        'location': 'Kolkata',
        'salary_min': 15000,
        'salary_max': 21000,
        'job_type': 'full_time',
        'required_skills': 'Communication, English Language, Customer Service',
        'experience_required': 'Fresher or 1+ year',
        'deadline': timezone.now().date() + timedelta(days=48),
    },
    {
        'title': 'Office Assistant',
        'organization': 'Corporate Solutions Ltd',
        'description': 'Assist with office administration and support various departments.',
        'location': 'Mumbai',
        'salary_min': 17000,
        'salary_max': 24000,
        'job_type': 'full_time',
        'required_skills': 'MS Office, Communication, Organization',
        'experience_required': '1+ year',
        'deadline': timezone.now().date() + timedelta(days=52),
    },
]

for job_data in jobs_data:
    Job.objects.create(**job_data)

print("✓ Created 10 Jobs")

# Create Scholarships
scholarships_data = [
    {
        'name': 'HDFC Bank Scholarship for Rural Students',
        'provider': 'HDFC Bank',
        'description': 'Merit-based scholarship for rural students pursuing higher education.',
        'amount': '₹50,000 - ₹1,00,000',
        'education_level': 'bachelor',
        'eligibility': 'Merit above 75%, Rural background, Annual income < ₹3 lakhs',
        'income_limit': '< ₹3,00,000',
        'category': 'Merit',
        'course': 'Engineering, Commerce, Science',
        'required_documents': 'Aadhaar, Mark Sheet, Income Certificate, Community Certificate',
        'application_deadline': timezone.now().date() + timedelta(days=60),
    },
    {
        'name': 'Central Sector Scholarship for Girls',
        'provider': 'Ministry of Education',
        'description': 'Scholarship for girls from economically weaker sections.',
        'amount': '₹25,000 - ₹40,000',
        'education_level': 'bachelor',
        'eligibility': 'Girls only, Merit above 60%, Annual income < ₹4.5 lakhs',
        'income_limit': '< ₹4,50,000',
        'category': 'Special Category',
        'course': 'All courses',
        'required_documents': 'Aadhaar, Mark Sheet, Income Certificate, Caste Certificate',
        'application_deadline': timezone.now().date() + timedelta(days=75),
    },
    {
        'name': 'Vidyasaarathi Scholarship',
        'provider': 'VidyaSaarathi NGO',
        'description': 'Comprehensive support for meritorious rural students.',
        'amount': '₹30,000 - ₹70,000',
        'education_level': '12th',
        'eligibility': 'Merit above 70%, Rural school background, Annual income < ₹2.5 lakhs',
        'income_limit': '< ₹2,50,000',
        'category': 'Need-Based',
        'course': 'Any stream',
        'required_documents': 'Aadhaar, Certificate, Income Proof',
        'application_deadline': timezone.now().date() + timedelta(days=50),
    },
    {
        'name': 'Post Matric Scholarship for OBC Students',
        'provider': 'Department of Social Justice',
        'description': 'Scholarship for OBC category students pursuing higher education.',
        'amount': '₹15,000 - ₹35,000',
        'education_level': 'bachelor',
        'eligibility': 'OBC category, Annual income < ₹2.5 lakhs',
        'income_limit': '< ₹2,50,000',
        'category': 'Reserved Category',
        'course': 'All courses',
        'required_documents': 'OBC Certificate, Aadhaar, Mark Sheet, Income Certificate',
        'application_deadline': timezone.now().date() + timedelta(days=90),
    },
    {
        'name': 'NSP Agricultural Scholarships',
        'provider': 'National Scholarship Portal',
        'description': 'Scholarships for students pursuing agriculture and related courses.',
        'amount': '₹20,000 - ₹50,000',
        'education_level': 'diploma',
        'eligibility': 'Agriculture students, Merit above 65%',
        'income_limit': '< ₹3,00,000',
        'category': 'Course-Specific',
        'course': 'Agriculture, Horticulture',
        'required_documents': 'Aadhaar, Mark Sheet, Admission Letter',
        'application_deadline': timezone.now().date() + timedelta(days=65),
    },
]

for sch_data in scholarships_data:
    Scholarship.objects.create(**sch_data)

print("✓ Created 5 Scholarships")

# Create Government Schemes
schemes_data = [
    {
        'name': 'PM-KISAN Samman Nidhi',
        'department': 'Ministry of Agriculture & Farmers Welfare',
        'category': 'agriculture',
        'description': 'Direct income support to all farming families.',
        'target_beneficiaries': 'All agricultural land holding farmers',
        'benefits': '₹6,000 per annum in 3 installments',
        'eligibility': 'Should have agricultural land',
        'required_documents': 'Land records, Aadhaar, Bank account details',
        'application_process': 'Apply online at pmkisan.gov.in or through village patwari',
        'official_website': 'https://pmkisan.gov.in/',
    },
    {
        'name': 'MGNREGA - Mahatma Gandhi National Rural Employment Guarantee Act',
        'department': 'Ministry of Rural Development',
        'category': 'employment',
        'description': 'Guarantee of 100 days of wage employment per financial year.',
        'target_beneficiaries': 'Rural laborers and landless workers',
        'benefits': 'Minimum wage employment guaranteed',
        'eligibility': 'Adult member of rural household',
        'required_documents': 'Aadhaar, Job card application',
        'application_process': 'Apply at nearest Gram Panchayat office',
        'official_website': 'https://nrega.nic.in/',
    },
    {
        'name': 'Pradhan Mantri Awas Yojana - Gramin',
        'department': 'Ministry of Rural Development',
        'category': 'housing',
        'description': 'Housing assistance for BPL and AAY families.',
        'target_beneficiaries': 'BPL and AAY families below poverty line',
        'benefits': '₹1,20,000 to ₹1,30,000 for house construction',
        'eligibility': 'BPL/AAY family, Annual income < ₹1.80 lakhs',
        'required_documents': 'Aadhaar, BPL certificate, Income proof',
        'application_process': 'Apply through Gram Panchayat or online',
        'official_website': 'https://pmayg.nic.in/',
    },
    {
        'name': 'Pradhan Mantri Mudra Yojana',
        'department': 'Ministry of Finance',
        'category': 'entrepreneurship',
        'description': 'Collateral-free loans for small businesses and entrepreneurs.',
        'target_beneficiaries': 'Small business owners and entrepreneurs',
        'benefits': 'Loans up to ₹10 lakhs at reasonable interest',
        'eligibility': 'Indian citizen, business plan required',
        'required_documents': 'Business plan, ID proof, Address proof',
        'application_process': 'Apply at participating banks or online',
        'official_website': 'https://www.mudra.org.in/',
    },
    {
        'name': 'National Scholarship Portal',
        'department': 'Ministry of Education',
        'category': 'education',
        'description': 'Multiple scholarships for students from classes 1 to postgraduate.',
        'target_beneficiaries': 'Students from economically weaker sections',
        'benefits': 'Various scholarships ranging from ₹12,000 to ₹1,00,000',
        'eligibility': 'Student pursuing education, income limits apply',
        'required_documents': 'Aadhaar, Academic records, Income certificate',
        'application_process': 'Apply online at scholarships.gov.in',
        'official_website': 'https://scholarships.gov.in/',
    },
]

for scheme_data in schemes_data:
    GovernmentScheme.objects.create(**scheme_data)

print("✓ Created 5 Government Schemes")

# Create Skill Programs
skills_data = [
    {
        'name': 'Basic Computer Skills',
        'category': 'Digital Skills',
        'provider': 'NASSCOM Foundation',
        'description': 'Learn fundamentals of computer usage, MS Office, and internet.',
        'duration': '3 Months',
        'level': 'beginner',
        'price_type': 'free',
        'price': '',
        'prerequisites': 'None',
        'certificate': True,
    },
    {
        'name': 'Digital Marketing Fundamentals',
        'category': 'Digital Skills',
        'provider': 'Google Digital Garage',
        'description': 'Learn social media, email marketing, and online advertising.',
        'duration': '2 Months',
        'level': 'intermediate',
        'price_type': 'free',
        'price': '',
        'prerequisites': 'Basic computer knowledge',
        'certificate': True,
    },
    {
        'name': 'Organic Farming Techniques',
        'category': 'Agriculture',
        'provider': 'National Institute of Organic Farming',
        'description': 'Learn sustainable organic farming methods for higher yield.',
        'duration': '6 Weeks',
        'level': 'intermediate',
        'price_type': 'free',
        'price': '',
        'prerequisites': 'Agricultural background preferred',
        'certificate': True,
    },
    {
        'name': 'Solar Panel Installation',
        'category': 'Technical Skills',
        'provider': 'Ministry of New and Renewable Energy',
        'description': 'Hands-on training in solar panel installation and maintenance.',
        'duration': '4 Months',
        'level': 'intermediate',
        'price_type': 'paid',
        'price': '₹10,000',
        'prerequisites': 'Basic electrical knowledge',
        'certificate': True,
    },
    {
        'name': 'Spoken English for Rural Areas',
        'category': 'Communication',
        'provider': 'British Council',
        'description': 'Improve English communication skills for better job opportunities.',
        'duration': '3 Months',
        'level': 'beginner',
        'price_type': 'free',
        'price': '',
        'prerequisites': 'None',
        'certificate': True,
    },
    {
        'name': 'Financial Literacy and Entrepreneurship',
        'category': 'Financial Skills',
        'provider': 'NABARD',
        'description': 'Learn financial management, budgeting, and business planning.',
        'duration': '8 Weeks',
        'level': 'beginner',
        'price_type': 'free',
        'price': '',
        'prerequisites': 'None',
        'certificate': True,
    },
    {
        'name': 'Smartphone and Internet Basics',
        'category': 'Digital Skills',
        'provider': 'NASSCOM',
        'description': 'Master smartphone usage and internet navigation.',
        'duration': '2 Months',
        'level': 'beginner',
        'price_type': 'free',
        'price': '',
        'prerequisites': 'None',
        'certificate': True,
    },
    {
        'name': 'Food Processing and Preservation',
        'category': 'Entrepreneurship',
        'provider': 'Ministry of Food Processing',
        'description': 'Learn to process and preserve agricultural produce.',
        'duration': '3 Months',
        'level': 'intermediate',
        'price_type': 'paid',
        'price': '₹8,000',
        'prerequisites': 'None',
        'certificate': True,
    },
]

for skill_data in skills_data:
    SkillProgram.objects.create(**skill_data)

print("✓ Created 8 Skill Programs")

# Create Business Opportunities
business_data = [
    {
        'name': 'Dairy Farming',
        'category': 'Agriculture',
        'description': 'Start a dairy farm with high-quality cattle for milk production.',
        'investment_level': 'high',
        'opportunity_level': 'moderate',
        'required_skills': 'Animal husbandry, Business management, Veterinary knowledge',
        'expected_income': '₹30,000 - ₹80,000 per month',
        'market_demand': 'Very High',
        'resources': 'Land, cattle, feed, equipment, veterinary services',
    },
    {
        'name': 'Organic Vegetable Farming',
        'category': 'Agriculture',
        'description': 'Grow certified organic vegetables for local and urban markets.',
        'investment_level': 'medium',
        'opportunity_level': 'moderate',
        'required_skills': 'Agriculture, Organic farming, Marketing',
        'expected_income': '₹20,000 - ₹60,000 per month',
        'market_demand': 'High',
        'resources': 'Land, seeds, fertilizer, irrigation, storage facilities',
    },
    {
        'name': 'Poultry Farming',
        'category': 'Agriculture',
        'description': 'Raise poultry for eggs and meat production.',
        'investment_level': 'medium',
        'opportunity_level': 'easy',
        'required_skills': 'Animal care, Basic business knowledge',
        'expected_income': '₹15,000 - ₹40,000 per month',
        'market_demand': 'High',
        'resources': 'Shed, poultry birds, feed, equipment',
    },
    {
        'name': 'Food Processing and Preservation',
        'category': 'Food Processing',
        'description': 'Process and preserve agricultural products for sale.',
        'investment_level': 'medium',
        'opportunity_level': 'moderate',
        'required_skills': 'Food preservation, Packaging, Marketing',
        'expected_income': '₹25,000 - ₹70,000 per month',
        'market_demand': 'High',
        'resources': 'Processing equipment, storage, packaging materials, certifications',
    },
    {
        'name': 'Handicrafts Business',
        'category': 'Handicrafts',
        'description': 'Create and sell traditional handicrafts online and offline.',
        'investment_level': 'low',
        'opportunity_level': 'easy',
        'required_skills': 'Craftsmanship, Digital marketing, Customer service',
        'expected_income': '₹10,000 - ₹50,000 per month',
        'market_demand': 'Medium',
        'resources': 'Raw materials, workspace, marketing channels',
    },
    {
        'name': 'Tailoring and Garment Production',
        'category': 'Tailoring',
        'description': 'Provide tailoring services or produce garments for retail.',
        'investment_level': 'low',
        'opportunity_level': 'easy',
        'required_skills': 'Sewing, Garment design, Customer service',
        'expected_income': '₹12,000 - ₹45,000 per month',
        'market_demand': 'High',
        'resources': 'Sewing machines, fabric, workspace',
    },
    {
        'name': 'Agro-Forestry',
        'category': 'Agriculture',
        'description': 'Combine agriculture with tree cultivation for multiple income streams.',
        'investment_level': 'medium',
        'opportunity_level': 'moderate',
        'required_skills': 'Agriculture, Forestry, Land management',
        'expected_income': '₹20,000 - ₹60,000 per month',
        'market_demand': 'Medium',
        'resources': 'Land, seedlings, maintenance equipment',
    },
    {
        'name': 'Online Tutoring and Education Services',
        'category': 'Education',
        'description': 'Provide online tutoring and skill-sharing services to rural students.',
        'investment_level': 'low',
        'opportunity_level': 'easy',
        'required_skills': 'Subject expertise, Teaching, Digital literacy',
        'expected_income': '₹5,000 - ₹30,000 per month',
        'market_demand': 'High',
        'resources': 'Internet, laptop, online platform access',
    },
]

for bus_data in business_data:
    BusinessOpportunity.objects.create(**bus_data)

print("✓ Created 8 Business Opportunities")

print("\n✅ Database successfully populated with demo data!")
print("\nSummary:")
print("  - 10 Jobs")
print("  - 5 Scholarships")
print("  - 5 Government Schemes")
print("  - 8 Skill Programs")
print("  - 8 Business Opportunities")
print("\nTotal: 36 opportunity records created")
