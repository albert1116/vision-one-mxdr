import csv
import io
import json
from flask import Response


def export_json(data, filename='export.json'):
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(
        payload,
        mimetype='application/json; charset=utf-8',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'},
    )


def export_csv(rows, filename='export.csv'):
    output = io.StringIO()
    if rows:
        writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    else:
        output.write('no_data\n')

    return Response(
        output.getvalue(),
        mimetype='text/csv; charset=utf-8',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'},
    )
