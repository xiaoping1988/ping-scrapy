from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exporters import JsonLinesItemExporter


class MyCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter
        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export:
            kwargs['fields_to_export'] = fields_to_export
        super(MyCsvItemExporter, self).__init__(*args, **kwargs)


# 定义ensure_ascii=False,避免直接输出unicode
class CustomJsonLinesItemExporter(JsonLinesItemExporter):
    def __init__(self, file, **kwargs):
        super(CustomJsonLinesItemExporter, self).__init__(file, ensure_ascii=False, **kwargs)
