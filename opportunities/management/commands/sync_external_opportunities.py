from django.core.management.base import BaseCommand
from services.external_integrations import ExternalIntegrationsService

class Command(BaseCommand):
    help = 'Synchronize and fetch live verified opportunities from Buddy4Study, myScheme, NSP, NCS, Skill India, and Startup India'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='all',
            help='Source portal to sync (all, buddy4study, nsp, myscheme, ncs, skillindia, startupindia)'
        )

    def handle(self, *args, **options):
        source = options['source'].lower()
        self.stdout.write(self.style.NOTICE(f"Connecting to external opportunity networks [Source: {source}]..."))

        if source == 'all':
            results = ExternalIntegrationsService.sync_all()
            self.stdout.write(self.style.SUCCESS(f"[OK] Synchronized Buddy4Study Scholarships: {results['buddy4study']} items"))
            self.stdout.write(self.style.SUCCESS(f"[OK] Synchronized National Scholarship Portal: {results['nsp']} items"))
            self.stdout.write(self.style.SUCCESS(f"[OK] Synchronized myScheme.gov.in Schemes: {results['myscheme']} items"))
            self.stdout.write(self.style.SUCCESS(f"[OK] Synchronized National Career Service Jobs: {results['ncs']} items"))
            self.stdout.write(self.style.SUCCESS(f"[OK] Synchronized Skill India Digital Courses: {results['skill_india']} items"))
            self.stdout.write(self.style.SUCCESS(f"[OK] Synchronized Startup India / PMEGP Blueprints: {results['startup_india']} items"))
            self.stdout.write(self.style.SUCCESS(f"[DONE] Total External Opportunities Synchronized: {results['total_synced']} items"))

        elif source == 'buddy4study':
            count = ExternalIntegrationsService.sync_buddy4study_scholarships()
            self.stdout.write(self.style.SUCCESS(f"[OK] Buddy4Study Sync Complete: {count} scholarships updated."))

        elif source == 'myscheme':
            count = ExternalIntegrationsService.sync_myscheme_schemes()
            self.stdout.write(self.style.SUCCESS(f"[OK] myScheme.gov.in Sync Complete: {count} schemes updated."))

        elif source == 'ncs':
            count = ExternalIntegrationsService.sync_ncs_jobs()
            self.stdout.write(self.style.SUCCESS(f"[OK] National Career Service Sync Complete: {count} jobs updated."))

        elif source == 'skillindia':
            count = ExternalIntegrationsService.sync_skillindia_courses()
            self.stdout.write(self.style.SUCCESS(f"[OK] Skill India Digital Sync Complete: {count} courses updated."))

        elif source == 'startupindia':
            count = ExternalIntegrationsService.sync_startupindia_business()
            self.stdout.write(self.style.SUCCESS(f"[OK] Startup India / PMEGP Sync Complete: {count} business ideas updated."))

        else:
            self.stdout.write(self.style.ERROR(f"Unknown source '{source}'"))
