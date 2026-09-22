from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def staff_display(value):
    """Render 'ID, Name' as blue ID on line 1 and black name on line 2."""
    if value is None:
        return mark_safe('<span class="text-slate-400">—</span>')
    text = str(value).strip()
    if not text or text == '—':
        return mark_safe('<span class="text-slate-400">—</span>')
    if ',' in text:
        staff_id, name = text.split(',', 1)
        staff_id = conditional_escape(staff_id.strip())
        name = conditional_escape(name.strip())
        return mark_safe(f'<span class="staff-id-line">{staff_id}</span><span class="staff-name-line">{name}</span>')
    return mark_safe(f'<span class="staff-name-line">{conditional_escape(text)}</span>')
