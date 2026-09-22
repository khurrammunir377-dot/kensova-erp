from django.db import models
from django.utils import timezone

class Staff(models.Model):
    staff_no = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, blank=True, null=True)
    is_store_custodian = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['staff_no', 'name']

    def formatted_name(self):
        return f"{self.staff_no}, {self.name}"

    def __str__(self):
        return f"{self.staff_no} — {self.name} ({self.designation})"

class Supplier(models.Model):
    supplier_code = models.CharField(max_length=50, primary_key=True)
    company_name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return f"{self.company_name} ({self.supplier_code})"

class Project(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active Execution'),
        ('Completed', 'Handed Over'),
        ('On Hold', 'On Hold'),
    ]
    project_code = models.CharField(max_length=50, primary_key=True)
    project_name = models.CharField(max_length=200)
    client_name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, default="Dubai, UAE")
    budget_aed = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    start_date = models.DateField(default=timezone.now)
    completion_date = models.DateField(blank=True, null=True, verbose_name="Target Completion Date")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.project_code} — {self.project_name}"

class Tool(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available (Store F20)'),
        ('Issued', 'Issued to Site'),
        ('Maintenance', 'Under Maintenance'),
        ('Scrapped', 'Decommissioned'),
    ]
    tool_no = models.CharField(max_length=50, primary_key=True)
    tool_name = models.CharField(max_length=200)
    store_location = models.CharField(max_length=50, default="F20")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    serial_no = models.CharField(max_length=100, blank=True, null=True)
    calibration_due_date = models.DateField(blank=True, null=True, verbose_name="Calibration Due Date")
    status_changed_at = models.DateTimeField(default=timezone.now, verbose_name="Status Date")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['tool_no']

    def __str__(self):
        return f"{self.tool_no} - {self.tool_name}"

class ToolTransaction(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='transactions')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='tool_logs')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    issued_by = models.CharField(max_length=150, default="UUDS-804, Manuja Shehan")
    received_by = models.CharField(max_length=150, blank=True, null=True)
    received_by_store = models.CharField(max_length=150, blank=True, null=True)
    issue_date = models.DateTimeField(default=timezone.now)
    expected_return_date = models.DateField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Issued', 'Issued'), ('Returned', 'Returned')], default='Issued')
    return_condition = models.CharField(max_length=30, choices=[('Good', 'Good'), ('Needs Repair', 'Needs Repair'), ('Damaged', 'Damaged')], blank=True, null=True)
    gate_pass_no = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-issue_date']

class Material(models.Model):
    material_code = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=255)
    specification = models.CharField(max_length=255, blank=True, null=True)
    current_stock = models.IntegerField(default=0)
    unit = models.CharField(max_length=20, default="pcs")
    min_stock_alert = models.IntegerField(default=20)
    store_location = models.CharField(max_length=50, default="F20")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['material_code']

    def is_low_stock(self):
        return self.current_stock <= self.min_stock_alert

    def __str__(self):
        return f"{self.material_code} - {self.description} ({self.current_stock} {self.unit})"

    def save(self, *args, **kwargs):
        self.unit = (self.unit or 'PCS').upper()
        super().save(*args, **kwargs)

class MaterialTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('Receive', 'Receive GRN (Inward)'),
        ('Issue', 'Issue to Site (Outward)'),
        ('Return', 'Return to Store (Restock)'),
    ]
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='movements')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField(default=1)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    issued_by = models.CharField(max_length=150, default="UUDS-804, Manuja Shehan")
    received_by = models.CharField(max_length=150, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    reference_no = models.CharField(max_length=100, blank=True, null=True)
    gate_pass_no = models.CharField(max_length=50, blank=True, null=True)
    delivery_note_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Delivery Note / PO No")
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

class PurchaseRequest(models.Model):
    pr_number = models.CharField(max_length=50, primary_key=True)
    generated_by = models.CharField(max_length=150, default="UUDS-804, Manuja Shehan")
    created_date = models.DateTimeField(default=timezone.now)
    total_items = models.IntegerField(default=0)
    status = models.CharField(max_length=30, default='Pending Approval')
    notes = models.TextField(blank=True, null=True)
    items_json = models.TextField(blank=True, null=True, default='[]')

    class Meta:
        ordering = ['-created_date']

class GatePass(models.Model):
    PASS_TYPES = [
        ('Tool', 'Tools Gate Pass'),
        ('Material', 'Material Gate Pass'),
    ]
    movement_pass_no = models.CharField(max_length=50, unique=True)
    pass_type = models.CharField(max_length=20, choices=PASS_TYPES)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=150, blank=True, null=True)
    employee_name = models.CharField(max_length=150, blank=True, null=True)
    employee_id_designation = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=150, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    destination = models.CharField(max_length=255, blank=True, null=True)
    returnable = models.BooleanField(blank=True, null=True)
    expected_return_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.movement_pass_no} — {self.get_pass_type_display()}"


class GatePassItem(models.Model):
    gate_pass = models.ForeignKey(GatePass, on_delete=models.CASCADE, related_name='items')
    tool_transaction = models.ForeignKey(ToolTransaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='gate_pass_items')
    material_transaction = models.ForeignKey(MaterialTransaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='gate_pass_items')
    description = models.CharField(max_length=255)
    quantity = models.CharField(max_length=50, default='1')
    serial_asset_no = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['id']
