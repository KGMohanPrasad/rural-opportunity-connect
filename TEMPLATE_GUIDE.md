# Template Development Guide

This document provides instructions for creating the remaining templates for Rural Opportunity Connect. Templates follow a consistent design pattern using Tailwind CSS and Django template syntax.

## Completed Templates ✅

- ✅ base.html - Master template with navbar, footer, styling
- ✅ landing.html - Homepage with hero section
- ✅ login.html - User login form
- ✅ register.html - User registration form
- ✅ profile_setup.html - Initial profile completion
- ✅ dashboard.html - User dashboard with recommendations
- ✅ jobs_list.html - Job listings with filters
- ✅ scholarships_list.html - Scholarship listings
- ✅ schemes_list.html - Government schemes
- ✅ skills_list.html - Skill programs
- ✅ business_list.html - Business opportunities
- ✅ about.html - About page with Design Thinking process

## Templates to Create

### Detail Pages (Pattern-Based)

Each detail page should follow this structure:

```html
{% extends 'base.html' %}

{% block title %}[Title] - Rural Opportunity Connect{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto px-4 py-12">
    <button class="text-green-700 hover:text-green-900 mb-4">← Back</button>
    
    <div class="card p-8">
        <!-- Header -->
        <div class="flex justify-between items-start mb-6">
            <div>
                <h1 class="text-4xl font-bold text-gray-900 mb-2">[Title]</h1>
                <p class="text-gray-600">[Organization/Provider]</p>
            </div>
            <button class="save-btn" data-type="[type]" data-id="[id]">
                <i class="fas fa-heart text-gray-400"></i>
            </button>
        </div>

        <!-- Details Section -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <!-- Main Content -->
            <div class="md:col-span-2">
                <!-- Key Information -->
                <!-- Description -->
                <!-- Requirements/Eligibility -->
            </div>

            <!-- Sidebar (Key Details) -->
            <div class="space-y-4">
                <!-- Key stat boxes -->
            </div>
        </div>

        <!-- CTA Button -->
        <div class="flex gap-4">
            <button class="btn-primary">Apply/Enroll</button>
            <button class="btn-secondary">Share</button>
        </div>
    </div>
</div>
{% endblock %}
```

### Specific Detail Pages to Create

#### 1. job_detail.html
**Context variables from views.py:**
- `job` (Job object)
- `skills_list` (formatted skills)

**Sections:**
- Job title, organization, location
- Salary range, job type
- About the role (description)
- Key responsibilities (required_skills)
- Required qualifications
- Application deadline
- Apply button

**Template code location:** `templates/job_detail.html`

---

#### 2. scholarship_detail.html
**Context variables:**
- `scholarship` (Scholarship object)

**Sections:**
- Scholarship name, provider
- Amount and educational level
- Eligibility criteria
- Income limit information
- Required documents
- Application deadline
- How to apply (link to official website)

**Key styling:** Use purple accent colors for consistency with scholarships_list.html

---

#### 3. scheme_detail.html
**Context variables:**
- `scheme` (GovernmentScheme object)

**Sections:**
- Scheme name and department
- Category badge
- Full description
- Target beneficiaries
- Eligibility criteria
- How to benefit (benefits)
- Application process (steps)
- Official website link
- Contact information

**Note:** Government schemes are official; ensure all links point to authentic government sources.

---

#### 4. skill_detail.html
**Context variables:**
- `skill` (SkillProgram object)

**Sections:**
- Course name and provider
- Duration and level
- Price (if applicable)
- Course description
- What you'll learn (skills field)
- Prerequisites
- Certification information
- Enroll button
- Provider contact/website

---

#### 5. business_detail.html
**Context variables:**
- `business` (BusinessOpportunity object)

**Sections:**
- Business idea name
- Investment required
- Difficulty level
- Market demand
- Expected income potential
- Full description
- How to get started (steps)
- Required resources
- Profit margins / Returns
- Risk factors
- Related business ideas (links to similar opportunities)

---

### Dashboard Support Pages

#### 6. profile.html (User Profile Edit)
**Purpose:** Allow users to view and edit their profile

**Sections:**
- Profile picture upload (optional)
- All 9 profile fields (same as profile_setup.html)
- Edit mode toggle
- Save changes button
- Profile completion percentage

**Key feature:** Reusable form (can be partial template)

---

#### 7. saved_opportunities.html
**Context variables:**
- `saved_jobs` (list of saved Job objects)
- `saved_scholarships` (list of saved Scholarship objects)
- `saved_schemes` (list of saved GovernmentScheme objects)
- `saved_skills` (list of saved SkillProgram objects)
- `saved_business` (list of saved BusinessOpportunity objects)

**Sections:**
- Tabs for each opportunity type
- Grid of saved items
- Unsave button on each card
- Link to view details
- Empty state if no saved items

**Implementation note:** Use same card component as list pages

---

#### 8. application_tracker.html
**Context variables:**
- `applications` (list of Application objects)

**Sections:**
- Application status timeline visualization:
  - Applied → Under Review → Shortlisted → Interview → Selected/Rejected
- List of user's applications with:
  - Opportunity name and type
  - Current status (with visual indicator)
  - Application date
  - Last updated date
  - Action links (view opportunity, cancel application)

**Styling:** Use progress indicators and color-coded status badges

**Example statuses:**
- Applied: Gray
- Under Review: Yellow
- Shortlisted: Blue
- Interview: Orange
- Selected: Green
- Rejected: Red

---

#### 9. document_checklist.html
**Context variables:**
- `checklist` (DocumentChecklist object)
- `completion_percentage` (calculated value)

**Documents to track:**
1. Aadhaar Card
2. Educational Marksheet
3. Income Certificate
4. Caste Certificate
5. Bank Account Details
6. Resume
7. Passport (if applicable)
8. Work Experience Letter

**Sections:**
- Document progress bar (X/8 complete)
- Checklist of 8 documents with:
  - Checkbox (editable via AJAX)
  - Document name
  - Status (Optional/Required)
  - Upload button (optional)
- Tips section for obtaining documents
- Download combined checklist as PDF (nice-to-have)

---

## Template Development Patterns

### Form Handling Pattern
```django
<form method="POST" class="space-y-6">
    {% csrf_token %}
    
    {% if form.non_field_errors %}
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {{ form.non_field_errors }}
        </div>
    {% endif %}
    
    {% for field in form %}
        <div>
            <label class="block text-gray-700 font-semibold mb-2">{{ field.label }}</label>
            {{ field|add_class:"px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-700" }}
            {% if field.errors %}
                <p class="text-red-500 text-sm mt-2">{{ field.errors|first }}</p>
            {% endif %}
        </div>
    {% endfor %}
    
    <button type="submit" class="btn-primary">Submit</button>
</form>
```

### Filter Form Pattern
```django
<form method="GET" class="space-y-4">
    <div>
        <label class="block text-gray-700 font-semibold mb-2">Filter Name</label>
        <select name="field" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-700">
            <option value="">All Options</option>
            {% for value, label in options %}
                <option value="{{ value }}" {% if value == filters.field %}selected{% endif %}>{{ label }}</option>
            {% endfor %}
        </select>
    </div>
    <button type="submit" class="btn-primary w-full text-sm">Apply Filters</button>
</form>
```

### Grid Card Pattern
```django
<div class="card p-6 hover:shadow-lg transition">
    <h3 class="text-xl font-bold text-gray-900 mb-2">{{ item.title }}</h3>
    <p class="text-gray-600 mb-4">{{ item.description|truncatewords:20 }}</p>
    
    <div class="flex justify-between items-center">
        <p class="text-sm text-gray-500">Extra info</p>
        <a href="{% url 'detail_view' item.id %}" class="btn-primary text-sm">View Details</a>
    </div>
</div>
```

### Status Badge Pattern
```django
<span class="inline-block px-3 py-1 rounded-full text-sm font-semibold
    {% if status == 'applied' %}bg-gray-100 text-gray-700
    {% elif status == 'shortlisted' %}bg-blue-100 text-blue-700
    {% elif status == 'selected' %}bg-green-100 text-green-700
    {% else %}bg-red-100 text-red-700
    {% endif %}">
    {{ status|title }}
</span>
```

## Color Scheme Reference

Use these color accents consistently:

- **Primary Actions:** Green (#2E7D32) - Use for main buttons
- **Secondary Actions:** White with border - Use for alternative buttons
- **Scholarships:** Purple (#7C3AED) - Use in headers and accents
- **Skills:** Blue (#2563EB) - Use for skill-related content
- **Business:** Orange (#EA580C) - Use for business opportunities
- **Government:** Teal (#0891B2) - Use for government schemes
- **Status Success:** Green (#10B981)
- **Status Warning:** Yellow (#F59E0B)
- **Status Error:** Red (#EF4444)
- **Text Primary:** Dark Gray (#263238)
- **Text Secondary:** Gray (#6B7280)
- **Background:** Light (#F8FAF7)

## JavaScript Features Needed

### 1. Save Opportunity AJAX
```javascript
document.querySelectorAll('.save-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
        const form = new FormData();
        form.append('type', this.dataset.type);
        form.append('id', this.dataset.id);
        
        const response = await fetch('{% url "save_opportunity" %}', {
            method: 'POST',
            body: form,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
        
        const data = await response.json();
        if (data.status === 'saved') {
            this.querySelector('i').classList.add('text-red-500');
        } else {
            this.querySelector('i').classList.remove('text-red-500');
        }
    });
});
```

### 2. Apply Opportunity AJAX
```javascript
document.getElementById('apply-btn')?.addEventListener('click', async function() {
    const response = await fetch('{% url "apply_opportunity" %}', {
        method: 'POST',
        body: JSON.stringify({
            type: '{{ opportunity_type }}',
            id: '{{ opportunity_id }}'
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    });
    
    const data = await response.json();
    if (data.status === 'success') {
        alert('Application submitted successfully!');
        window.location.href = '{% url "applications" %}';
    }
});
```

## Implementation Priority

1. **High Priority (Immediate):**
   - job_detail.html
   - scholarship_detail.html
   - profile.html
   - saved_opportunities.html

2. **Medium Priority:**
   - application_tracker.html
   - document_checklist.html
   - skill_detail.html
   - scheme_detail.html

3. **Lower Priority:**
   - business_detail.html
   - Additional refinements

## Testing Checklist

For each new template:
- ✓ Responsive design (test on mobile, tablet, desktop)
- ✓ All Django template variables render correctly
- ✓ Links are properly formatted with {% url %} tags
- ✓ Forms include {% csrf_token %}
- ✓ Error messages display correctly
- ✓ Styling matches existing templates (colors, spacing, fonts)
- ✓ AJAX features work (save, apply buttons)
- ✓ No broken images or missing icons

---

**All templates use Tailwind CSS for styling. No Bootstrap or external UI frameworks are used.**
