import os, random, pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from store_app.models import Tool, Material, Staff, Project, Supplier, ToolTransaction, MaterialTransaction

class Command(BaseCommand):
    help = 'Seeds database with master data and generates 30 days of real operational telemetry'

    def handle(self, *args, **kwargs):
        self.stdout.write("Configuring Kensova ERP Master System & Operational Datasets...")

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@kensova.ae', 'abc@123')
            self.stdout.write(self.style.SUCCESS("Created Master Admin: admin (Password: abc@123)"))
        else:
            u = User.objects.get(username='admin')
            u.set_password('abc@123')
            u.save()

        excel_path = os.path.join(settings.BASE_DIR, 'data', 'Kensova_ERP_Updated_Master_Data.xlsx')
        if os.path.exists(excel_path):
            try:
                df_staff = pd.read_excel(excel_path, sheet_name='Staff', skiprows=2)
                for _, r in df_staff.iterrows():
                    staff_no = str(r['Staff No']).strip()
                    if staff_no and staff_no != 'nan':
                        Staff.objects.update_or_create(
                            staff_no=staff_no,
                            defaults={
                                'name': str(r['Name']).strip(),
                                'designation': str(r.get('Designation', 'Staff Member')).strip(),
                                'is_store_custodian': True if str(r.get('Store Custodian', '')).lower() == 'yes' else False
                            }
                        )

                df_tools = pd.read_excel(excel_path, sheet_name='Tools', skiprows=2)
                for _, r in df_tools.iterrows():
                    tool_no = str(r['Tool No']).strip()
                    if tool_no and tool_no != 'nan':
                        Tool.objects.update_or_create(
                            tool_no=tool_no,
                            defaults={
                                'tool_name': str(r['Tool Name']).strip(),
                                'store_location': str(r.get('Store Location', 'F20')).strip(),
                                'status': 'Available',
                                'calibration_due_date': timezone.now().date() + timedelta(days=random.randint(30, 180)),
                                'is_deleted': False
                            }
                        )

                df_mat = pd.read_excel(excel_path, sheet_name='Materials', skiprows=2)
                for _, r in df_mat.iterrows():
                    code = str(r['Material Code']).strip()
                    if code and code != 'nan':
                        Material.objects.update_or_create(
                            material_code=code,
                            defaults={
                                'description': str(r['Description']).strip(),
                                'specification': str(r.get('Specification', '')).strip() if pd.notna(r.get('Specification')) else 'Standard Spec',
                                'current_stock': int(r['Opening Qty']) if pd.notna(r.get('Opening Qty')) else 100,
                                'unit': str(r.get('Unit', 'pcs')).strip(),
                                'store_location': str(r.get('Store Location', 'F20')).strip(),
                                'min_stock_alert': 20,
                                'is_deleted': False
                            }
                        )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Excel read note: {e}"))

        custodians = [
            ('UUDS-804', 'Manuja', 'Shehan', 'manuja@kensova.ae'),
            ('UUDS-981', 'Chaturanga', 'Ruwan', 'chaturanga@kensova.ae'),
            ('UUDS-1435', 'Samal', 'Udawaththa', 'samal@kensova.ae'),
        ]
        for staff_id, first_name, last_name, email in custodians:
            user, _ = User.objects.get_or_create(
                username=staff_id,
                defaults={'first_name': first_name, 'last_name': last_name, 'email': email, 'is_staff': True}
            )
            user.set_password('abc@123')
            user.save()

        projects = [
            ('CNC-WORK', 'CNC Work', 'Kensova Workshop', 'Location F20', 250000, '2026-01-10', '2026-12-31'),
            ('DMCC-PRJ', 'DMCC Project', 'DMCC Corporate Tower', 'JLT, Dubai', 850000, '2026-03-01', '2026-11-15'),
            ('HANGER-PRJ', 'Hanger Project', 'Aviation Logistics Hanger', 'Dubai South', 1250000, '2026-02-15', '2026-10-30'),
            ('PRJ-DXB-001', 'Palm Jumeirah Villa', 'Private Residence', 'Palm Jumeirah', 1500000, '2026-04-01', '2026-12-20'),
        ]
        for c, n, cl, loc, b, s_dt, c_dt in projects:
            Project.objects.get_or_create(project_code=c, defaults={'project_name': n, 'client_name': cl, 'location': loc, 'budget_aed': b, 'start_date': s_dt, 'completion_date': c_dt, 'status': 'Active', 'is_deleted': False})

        suppliers = [
            ('SUP-001', 'Al Quoz Architectural Hardware LLC', 'Faisal Mehmood', '+971 4 347 1122', 'orders@alquozhardware.ae', 'Al Quoz Industrial 3, Dubai'),
            ('SUP-002', 'Emirates Precision Timber & Joinery', 'Rajesh Patel', '+971 4 288 9900', 'sales@emiratestimber.ae', 'Ras Al Khor Industrial Area 2, Dubai'),
            ('SUP-003', 'Gulf Architectural Coatings & Acrylics', 'Sarah Al Nuaimi', '+971 4 330 4488', 'procurement@gulfcoatings.ae', 'Dubai Investment Park 1, Dubai'),
        ]
        for c, n, cp, ph, em, addr in suppliers:
            Supplier.objects.get_or_create(supplier_code=c, defaults={'company_name': n, 'contact_person': cp, 'phone': ph, 'email': em, 'address': addr, 'is_deleted': False})

        now = timezone.now()
        all_tools = list(Tool.objects.filter(is_deleted=False))
        all_staff = list(Staff.objects.all())
        all_projects = list(Project.objects.filter(is_deleted=False))
        all_mats = list(Material.objects.filter(is_deleted=False))
        all_sups = list(Supplier.objects.filter(is_deleted=False))

        if all_tools and all_staff and all_projects and all_mats:
            # Seed 30 days of historical transactions
            for day_offset in range(30, 2, -1):
                tx_date = now - timedelta(days=day_offset, hours=random.randint(1, 8))
                
                # Daily tool movements
                for _ in range(random.randint(1, 3)):
                    t = random.choice(all_tools)
                    s = random.choice(all_staff)
                    p = random.choice(all_projects)
                    ret_date = tx_date + timedelta(hours=random.randint(6, 48))
                    ToolTransaction.objects.create(
                        tool=t,
                        staff=s,
                        project=p,
                        issued_by="UUDS-804, Manuja Shehan",
                        received_by=s.formatted_name(),
                        received_by_store="UUDS-804, Manuja Shehan",
                        issue_date=tx_date,
                        return_date=ret_date,
                        status='Returned',
                        return_condition='Good',
                        gate_pass_no=f"GP-DXB-{random.randint(1000, 9999)}"
                    )

                # Daily Material movements
                mat = random.choice(all_mats)
                MaterialTransaction.objects.create(
                    material=mat,
                    transaction_type='Issue',
                    quantity=random.randint(2, 20),
                    project=random.choice(all_projects),
                    staff=random.choice(all_staff),
                    issued_by="UUDS-804, Manuja Shehan",
                    received_by="UUDS-146, Technician Lead",
                    date=tx_date,
                    reference_no=f"MAT-ISS-{random.randint(100, 999)}"
                )
                if random.random() > 0.4:
                    MaterialTransaction.objects.create(
                        material=random.choice(all_mats),
                        transaction_type='Receive',
                        quantity=random.randint(20, 80),
                        supplier=random.choice(all_sups),
                        issued_by="UUDS-804, Manuja Shehan",
                        date=tx_date,
                        reference_no=f"DO-DXB-{random.randint(1000, 9999)}"
                    )

            # Set a small, controlled number of active checkout tools for live testing
            active_checkout_sample = all_tools[:5]
            for i, t in enumerate(active_checkout_sample):
                s = all_staff[i % len(all_staff)]
                p = all_projects[i % len(all_projects)]
                ToolTransaction.objects.create(
                    tool=t,
                    staff=s,
                    project=p,
                    issued_by="UUDS-804, Manuja Shehan",
                    received_by=s.formatted_name(),
                    issue_date=now - timedelta(hours=random.randint(2, 12)),
                    status='Issued',
                    gate_pass_no=f"GP-DXB-{random.randint(1000, 9999)}"
                )
                t.status = 'Issued'
                t.save()

        self.stdout.write(self.style.SUCCESS("Master Datasets Seeded Successfully!"))