# Metadata Preview

A privacy-first, read-only command-line toolkit for inspecting metadata in local files. It reports universal filesystem metadata, image dimensions/EXIF, PDF document information, and optional SHA-256 hashes without modifying source files or sending data anywhere.

## English

### Why this exists
Files often carry useful—and sometimes sensitive—metadata. Metadata Preview provides a small, auditable way to inspect that information before archiving, sharing, or troubleshooting files, without requiring a cloud service.

### Key features
- General metadata: resolved path, filename, extension, MIME type, byte size, created/changed and modified timestamps in UTC.
- Images: format, dimensions, color mode, and available EXIF fields for JPEG/TIFF/PNG/WebP supported by Pillow.
- PDFs: page count, encryption flag, and document-info fields such as title, author, creator, and producer when present.
- Optional streaming SHA-256 for integrity checks without loading whole files into memory.
- Multiple files per command, Unicode/Arabic filenames, machine-readable JSON, and report-file output.
- Read-only design: no metadata removal, rewriting, uploads, telemetry, or network calls.
- Symbolic links are rejected deliberately to reduce surprising path traversal.

### Preview
```console
$ metadata-preview photo.jpg --hash
{
  "schema_version": 1,
  "files": [
    {
      "path": "/home/user/photo.jpg",
      "name": "photo.jpg",
      "extension": ".jpg",
      "mime_type": "image/jpeg",
      "size_bytes": 84231,
      "modified_utc": "2026-09-23T18:20:00+00:00",
      "created_utc": "2026-09-23T18:20:00+00:00",
      "sha256": "...",
      "image": {"format": "JPEG", "width": 1920, "height": 1080, "mode": "RGB"}
    }
  ]
}
```
Values above are illustrative; the tool always reports the inspected file's real values.

### Requirements and installation
- Python 3.10+
- Pillow and pypdf (installed automatically)

```bash
git clone https://github.com/rad03i2/metadata-preview.git
cd metadata-preview
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

### Usage
```bash
metadata-preview photo.jpg
metadata-preview report.pdf photo.jpg notes.txt
metadata-preview report.pdf --hash
metadata-preview report.pdf --output reports/metadata.json
python -m metadata_preview photo.jpg
metadata-preview --version
```
Exit codes: `0` all files inspected, `1` one or more requested files failed, `2` invalid invocation or report-write failure. A per-file parser problem (for example a malformed PDF) is recorded inside that file's `pdf`/`image` section so useful filesystem metadata remains available.

### Python API
```python
from metadata_preview import inspect_file, inspect_many

report = inspect_file("photo.jpg", include_hash=True)
reports = inspect_many(["photo.jpg", "report.pdf"])
```

### Configuration
No environment variables, credentials, API keys, accounts, or configuration files are required. Use `--hash` only when a digest is needed because it reads the entire file. Use `--output PATH` to persist JSON; parent directories are created automatically.

### Project structure
```text
src/metadata_preview/   package, extraction engine, CLI
tests/                  functional and CLI tests
.github/workflows/      cross-platform CI
pyproject.toml           package/dependency metadata
SECURITY.md              security and privacy model
CONTRIBUTING.md          contribution guide
LICENSE                  MIT license
```

### Testing
```bash
python -m pip install -e . pytest
python -m compileall -q src tests
python -m pytest
```
CI runs these checks on Windows, macOS, and Linux with supported Python versions.

### Security and privacy
Inspection is local and read-only. File contents are not uploaded or executed. Metadata itself can be sensitive: EXIF may expose camera/device/location information and PDF fields may contain author or software names. Review generated JSON before sharing it. Dependencies parse untrusted formats, so keep them updated and avoid inspecting hostile files in a privileged environment. See [SECURITY.md](SECURITY.md).

### Limitations
- This is an inspector, not a metadata scrubber/editor.
- Supported rich metadata is currently focused on images and PDFs; other files still receive general filesystem metadata and optional hashes.
- EXIF availability depends on the image and Pillow support.
- PDF encryption or malformed files can limit document metadata extraction.
- `created_utc` is based on the platform's `st_ctime`; its exact meaning differs across operating systems.
- The tool does not validate whether metadata claims are truthful.

### Optional roadmap
Potential future additions include audio/video container metadata, CSV report export, and explicit metadata-risk highlighting. These are not current features.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Keep additions local-first, read-only by default, tested, and documented in both languages.

### License
MIT — see [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**Metadata Preview** أداة سطر أوامر محلية للمعاينة الآمنة للبيانات الوصفية للملفات دون تعديل الملفات الأصلية أو إرسالها إلى أي خدمة. تعرض معلومات نظام الملفات، وأبعاد الصور وEXIF، وبيانات مستندات PDF، مع إمكانية حساب SHA-256.

### لماذا هذا المشروع؟
قد تحتوي الملفات على معلومات وصفية مفيدة أو حساسة لا تظهر عند فتح الملف بصورة عادية. يوفر المشروع طريقة صغيرة وقابلة للمراجعة لفحص هذه البيانات قبل المشاركة أو الأرشفة أو استكشاف المشكلات، من دون الاعتماد على خدمة سحابية.

### الميزات
- معلومات عامة: المسار، الاسم، الامتداد، MIME، الحجم، ووقت التعديل والإنشاء/التغيير بصيغة UTC.
- الصور: النوع، الأبعاد، نمط الألوان وحقول EXIF المتاحة للأنواع التي تدعمها Pillow.
- PDF: عدد الصفحات، حالة التشفير، وحقول مثل العنوان والمؤلف والمنشئ والمنتج عند وجودها.
- SHA-256 اختياري بطريقة streaming لتجنب تحميل الملف كاملًا في الذاكرة.
- فحص عدة ملفات، دعم أسماء عربية وUnicode، JSON وحفظ التقرير إلى ملف.
- تصميم للقراءة فقط: لا حذف للبيانات الوصفية ولا تعديل ولا رفع ملفات ولا telemetry ولا اتصالات شبكة.
- رفض الروابط الرمزية عمدًا لتقليل الوصول غير المتوقع إلى مسارات أخرى.

### المعاينة
مثال JSON الموجود في القسم الإنجليزي توضيحي فقط؛ القيم الفعلية تُقرأ دائمًا من الملف الذي تختاره.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث. تثبت Pillow وpypdf تلقائيًا:
```bash
git clone https://github.com/rad03i2/metadata-preview.git
cd metadata-preview
python -m venv .venv
python -m pip install -e .
```
فعّل البيئة الافتراضية بالطريقة المناسبة لنظامك قبل التثبيت.

### الاستخدام
```bash
metadata-preview photo.jpg
metadata-preview report.pdf photo.jpg notes.txt
metadata-preview report.pdf --hash
metadata-preview report.pdf --output reports/metadata.json
python -m metadata_preview photo.jpg
```
رموز الخروج: `0` نجاح جميع الملفات، `1` فشل ملف مطلوب واحد أو أكثر، و`2` استدعاء غير صحيح أو تعذر كتابة التقرير.

### Python API
```python
from metadata_preview import inspect_file, inspect_many
report = inspect_file("photo.jpg", include_hash=True)
```

### الإعداد
لا تحتاج متغيرات بيئة أو مفاتيح API أو حسابات أو ملف إعداد. استخدم `--hash` عند الحاجة فقط لأنه يقرأ الملف كاملًا، و`--output` لحفظ JSON.

### بنية المشروع
المحرك والـCLI داخل `src/metadata_preview/`، والاختبارات داخل `tests/`، وCI داخل `.github/workflows/`، بينما يحدد `pyproject.toml` الحزمة واعتمادياتها.

### الاختبارات
```bash
python -m pip install -e . pytest
python -m compileall -q src tests
python -m pytest
```
يختبر CI المشروع على Windows وmacOS وLinux.

### الأمان والخصوصية
المعالجة محلية وللقراءة فقط، ولا يتم رفع المحتوى أو تنفيذه. مع ذلك قد تكون البيانات الوصفية نفسها حساسة؛ قد تتضمن EXIF معلومات جهاز أو موقع، وقد تتضمن ملفات PDF أسماء المؤلف أو البرامج المستخدمة. راجع JSON قبل مشاركته، وحدّث مكتبات التحليل باستمرار. راجع [SECURITY.md](SECURITY.md).

### القيود
- الأداة للمعاينة وليست لحذف أو تحرير metadata.
- التحليل الغني يركز حاليًا على الصور وPDF؛ بقية الملفات تحصل على معلومات عامة وبصمة اختيارية.
- توفر EXIF يعتمد على الملف ودعم Pillow.
- التشفير أو تلف PDF قد يمنع استخراج بعض المعلومات.
- معنى `created_utc` يعتمد على معنى `st_ctime` في نظام التشغيل.
- الأداة لا تتحقق من صحة الادعاءات المكتوبة داخل metadata.

### تطوير اختياري مستقبلي
يمكن لاحقًا إضافة بيانات حاويات الصوت والفيديو، وتصدير CSV، وإبراز حقول metadata الحساسة. هذه ليست ميزات حالية.

### المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md). يجب أن تبقى الإضافات محلية وآمنة للقراءة افتراضيًا ومغطاة بالاختبارات وموثقة باللغتين.

### الترخيص
MIT — راجع [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
