from django.contrib import admin
from .models import Staff, Supplier, Project, Tool, ToolTransaction, Material, MaterialTransaction, PurchaseRequest, GatePass, GatePassItem

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_no', 'name', 'designation', 'is_store_custodian', 'is_deleted')
    search_fields = ('staff_no', 'name', 'designation')

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('tool_no', 'tool_name', 'store_location', 'status', 'calibration_due_date', 'is_deleted')
    list_filter = ('status', 'store_location', 'is_deleted')
    search_fields = ('tool_no', 'tool_name')

@admin.register(ToolTransaction)
class ToolTransactionAdmin(admin.ModelAdmin):
    list_display = ('tool', 'staff', 'project', 'issued_by', 'received_by', 'issue_date', 'status', 'return_condition')
    list_filter = ('status', 'return_condition')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('material_code', 'description', 'current_stock', 'unit', 'store_location', 'is_deleted')
    search_fields = ('material_code', 'description')

@admin.register(MaterialTransaction)
class MaterialTransactionAdmin(admin.ModelAdmin):
    list_display = ('material', 'transaction_type', 'quantity', 'project', 'supplier', 'date')
    list_filter = ('transaction_type',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_code', 'project_name', 'client_name', 'start_date', 'completion_date', 'status', 'is_deleted')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_code', 'company_name', 'contact_person', 'phone', 'email', 'is_deleted')

@admin.register(GatePass)
class GatePassAdmin(admin.ModelAdmin):
    list_display = ('movement_pass_no', 'pass_type', 'created_at', 'employee_name', 'destination', 'created_by')
    list_filter = ('pass_type', 'created_at')
    search_fields = ('movement_pass_no', 'employee_name', 'destination', 'created_by')

@admin.register(GatePassItem)
class GatePassItemAdmin(admin.ModelAdmin):
    list_display = ('gate_pass', 'description', 'quantity', 'serial_asset_no')
    search_fields = ('gate_pass__movement_pass_no', 'description', 'serial_asset_no')
