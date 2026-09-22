from django.core.management.base import BaseCommand
from django.utils import timezone
from store_app.daily_report_service import collect_daily_data, build_daily_pdf, build_daily_excel, send_via_outlook


class Command(BaseCommand):
    help = 'Generate and send the daily Kensova Stores management report through Outlook Desktop.'

    def handle(self, *args, **options):
        data = collect_daily_data(timezone.localdate())
        pdf = build_daily_pdf(data)
        xlsx = build_daily_excel(data)
        send_via_outlook(pdf, xlsx, data['day'])
        self.stdout.write(self.style.SUCCESS(f'Daily report sent successfully for {data["day"]:%d-%b-%Y}.'))
