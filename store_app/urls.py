from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('tools/issue/', views.tool_issue, name='tool_issue'),
    path('tools/return/', views.tool_return, name='tool_return'),
    path('tools/pending/', views.tool_pending, name='tool_pending'),
    path('tools/gatepass/<int:gp_id>/', views.print_gate_pass, name='print_gate_pass'),
    path('reports/daily/', views.daily_report, name='daily_report'),
    path('reports/daily/send/', views.send_daily_report_now, name='send_daily_report_now'),
    path('materials/inventory/', views.material_inventory, name='material_inventory'),
    path('materials/issue/', views.material_issue, name='material_issue'),
    path('materials/receive/', views.material_receive, name='material_receive'),
    path('materials/return/', views.material_return, name='material_return'),
    path('projects/', views.projects_list, name='projects_list'),
    path('suppliers/', views.suppliers_list, name='suppliers_list'),
    path('reports/', views.reports_hub, name='reports_hub'),
    path('reports/export/', views.export_reports_excel, name='export_reports_excel'),
    path('ai/chat/', views.ai_chat, name='ai_chat'),
    path('ai/history/', views.ai_history, name='ai_history'),
]