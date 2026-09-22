from pathlib import Path
from io import BytesIO
import pymupdf as fitz
from django.conf import settings

TEMPLATE_NAME = 'Material Movement Pass Form.pdf'


def _template_path():
    return Path(settings.BASE_DIR) / 'store_app' / 'static' / 'store_app' / TEMPLATE_NAME


def _safe_text(value, max_len=48):
    value = str(value or '').strip()
    return value[:max_len]


def _put(page, text, x, y, size=8.5, bold=False):
    if not text:
        return
    page.insert_text((x, y), _safe_text(text), fontsize=size,
                     fontname='hebo' if bold else 'helv', color=(0, 0, 0), overlay=True)


def _white_box(page, rect):
    page.draw_rect(fitz.Rect(*rect), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)


def _draw_page(doc, gate_pass, items, page_items_start=0):
    page = doc.new_page(width=595, height=842)
    template = fitz.open(str(_template_path()))
    page.show_pdf_page(page.rect, template, 0)
    template.close()

    # Header / movement details. Coordinates follow the supplied UUDS form.
    _put(page, gate_pass.movement_pass_no.rsplit('/', 1)[-1], 204, 151, 9.5, True)
    _put(page, gate_pass.created_at.strftime('%d-%b-%Y'), 465, 151, 9.5, True)
    _put(page, gate_pass.employee_name, 190, 199, 9, True)
    _put(page, gate_pass.employee_id_designation, 190, 215, 8.5, True)
    _put(page, gate_pass.department, 190, 231, 8.5)
    _put(page, gate_pass.reason, 190, 247, 8.5)
    _put(page, gate_pass.destination, 190, 263, 8.5, True)

    # Requested By (Employee) is the only authorization field with source data.
    _put(page, gate_pass.employee_name, 416, 565, 7.8, True)
    if gate_pass.employee_id_designation:
        employee_id = gate_pass.employee_id_designation.split('/', 1)[0].strip()
        _put(page, employee_id, 438, 586, 7.8, True)
    _put(page, gate_pass.created_at.strftime('%d-%b-%Y'), 414, 606, 7.8)

    # Replace the seven source row numbers with sequential numbers for continuation pages.
    row_y = [353, 371, 389, 407, 425, 443, 461]
    for idx, item in enumerate(items[:7]):
        number = page_items_start + idx + 1
        if number != idx + 1:
            _white_box(page, (66, row_y[idx] - 11, 93, row_y[idx] + 5))
        _put(page, str(number), 72, row_y[idx], 8.5, True)
        desc = _safe_text(item['description'], 85)
        page.insert_textbox(fitz.Rect(98, row_y[idx]-11, 345, row_y[idx]+3), desc,
                            fontsize=7.4, fontname='helv', color=(0,0,0),
                            align=fitz.TEXT_ALIGN_LEFT, overlay=True)
        # Quantity column is centered in the supplied form (x 329-433 approx.).
        q = str(item['quantity'] or '')
        q_width = fitz.get_text_length(q, fontname='helv', fontsize=8.0)
        _put(page, q, 381 - (q_width / 2), row_y[idx], 8.0)
        _put(page, item['serial_asset_no'], 440, row_y[idx], 8.0)

    return page


def render_gate_pass_pdf(gate_pass):
    template = _template_path()
    if not template.exists():
        raise FileNotFoundError(f'Gate pass template not found: {template}')

    items = list(gate_pass.items.all())
    item_data = []
    for item in items:
        if item.tool_transaction_id and getattr(item.tool_transaction, 'tool', None):
            tool = item.tool_transaction.tool
            ref_label = f"Tool No: {tool.tool_no}"
            description = f"{ref_label} - {item.description}"
        elif item.material_transaction_id and getattr(item.material_transaction, 'material', None):
            material = item.material_transaction.material
            ref_label = f"Part No: {material.material_code}"
            description = f"{ref_label} - {item.description}"
        else:
            description = item.description
        item_data.append({
            'description': description,
            'quantity': item.quantity,
            'serial_asset_no': item.serial_asset_no or '',
        })

    # Build from the supplied one-page form, preserving its exact layout on every page.
    doc = fitz.open()
    for start in range(0, len(item_data) or 1, 7):
        _draw_page(doc, gate_pass, item_data[start:start + 7], page_items_start=start)

    out = BytesIO(doc.tobytes(garbage=4, deflate=True))
    doc.close()
    out.seek(0)
    return out
