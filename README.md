# Trapezoid PDF Generator

Choose language / زبان را انتخاب کنید:

- [English](#english)
- [فارسی](#فارسی)

---

## English

Generate clean, annotated trapezoid section drawings from an Excel sheet and export them as a multi-page PDF. The project is designed for practical engineering and drafting workflows where many sections must be plotted quickly, consistently, and with readable dimensions.

This tool reads section data from Excel, draws each section as a dynamically scaled trapezoid, adds key annotations such as top width, bottom width, height, width at 2 m, GL, and FL, then places the drawings into a paginated PDF layout. The repository can include both the Python source and a standalone Windows `.exe`, so users can run it either with Python installed or as a simple desktop application.

## What it does

- Reads section data from an Excel workbook.
- Draws each section as a geometrically scaled inverted trapezoid.
- Adds dimension-style labels for top width, bottom width, full height, width at 2 m from top, GL, and FL.
- Arranges up to 9 sections per page in an A4 landscape PDF.
- Adds page numbering automatically.
- Provides a desktop GUI for choosing the input Excel file and output PDF location.

## Why this tool is useful

When section drawings are prepared manually, repeated drafting and labeling can be slow and error-prone. This script automates the repetitive part of the workflow while still preserving the true visual proportion of each shape, making the generated sheets suitable for checking, reporting, and sharing with colleagues or clients.

Because the trapezoids are plotted with dynamic geometry rather than just relabeled placeholders, wider and taller sections actually look wider and taller in the output. This makes the PDF much more informative than a simple tabulated report.

## Input format

The script expects an Excel file with the following columns:

| Column | Meaning |
|---|---|
| `Title` | Section name or chainage label shown above each drawing |
| `B1` | One width value from the source sheet |
| `B2` | The other width value from the source sheet |
| `h` | Section height |
| `GL` | Ground level label |
| `FL` | Formation level label |

A sample workbook is included in this repository structure. In the sample input, the sheet contains 30 rows such as `Section 1`, `Section 2`, and so on, with corresponding `B1`, `B2`, `h`, `GL`, and `FL` values.

### Important note about `B1` and `B2`

In the current script logic, `B1` and `B2` are intentionally swapped when plotting, to match the original formatting used in the source spreadsheet. In other words, the code reads plotted top width from the Excel `B2` column and plotted bottom width from the Excel `B1` column.

If your workbook already stores top width and bottom width exactly as you want them plotted, you may want to remove that swap in the code before use.

## Output

The generated result is a multi-page PDF containing a 3×3 grid of section drawings on each page. In the sample output, 30 sections are distributed across 4 pages, with section titles, two-decimal labels, GL and FL values, and page numbers shown at the bottom-right corner.

Each section is drawn with dynamic margins and equal aspect ratio so the plotted geometry better represents the actual dimensions while still leaving room for labels and arrows.

## Running the tool

### Option 1: Run the standalone `.exe`

This is the easiest option for users who do not have Python installed.

1. Double-click the `.exe` file.
2. Click **Browse** and choose the input Excel file.
3. Choose where to save the output PDF.
4. Click **Generate PDF**.
5. Wait for the success message.

This is the recommended route for non-technical users or teammates who only need to generate section sheets from prepared Excel data.

### Option 2: Run the Python script

If you want to modify the code or run it directly from source:

```bash
pip install pandas matplotlib openpyxl
python sec2.py
```

The script opens a simple desktop interface where the user selects the Excel file and chooses the output PDF path.

## GUI workflow

The Python version uses a small Tkinter desktop application rather than command-line prompts. The interface includes:

- An input file picker for the Excel workbook.
- An output file picker for the PDF path.
- A **Generate PDF** button.
- Status pop-ups for success and error handling.

The app also auto-suggests an output file name based on the selected Excel file, which makes repeated use more convenient.

## Drawing logic

A few implementation details are useful for anyone planning to adapt the script:

- Sections are drawn as filled inverted trapezoids using Matplotlib polygon coordinates derived from `B1`, `B2`, and `h`.
- The plot uses equal aspect ratio so width and height stay visually proportional.
- Offsets for arrows and labels are computed dynamically from section size, which improves readability across small and large sections.
- Width at 2 m is only drawn when the section height is greater than 2 m.
- GL and FL are formatted to two decimal places and positioned on opposite sides of the section for clarity.
- Up to 9 sections are placed on each PDF page in a 3×3 layout.

## Example use cases

This project is useful anywhere repeated trapezoidal or section-style plots need to be generated from tabular data, for example:

- Earthworks or drainage section sheets.
- Canal, trench, or excavation section summaries.
- Roadway or embankment cross-section presentation.
- Internal checking drawings generated from survey or design spreadsheets.
- Quick reporting packages for design review.

## Limitations and notes

- The script expects the required Excel columns to exist: `Title`, `B1`, `B2`, `h`, `GL`, and `FL`.
- `GL` and `FL` are converted to numeric display with two decimal places, so non-numeric values may require code changes.
- The current plotting logic is tailored to the source workbook convention where plotted `B1` and `B2` are swapped from the spreadsheet columns.
- The sample script uses Windows-friendly GUI behavior and optional DPI awareness settings for sharper display on Windows systems.


## Credits

This project was created to automate section drawing generation from Excel input into paginated PDF sheets, with both Python-source and standalone-desktop usage in mind.

---

## فارسی

این ابزار برای تولید خودکار ترسیم مقاطع ذوزنقه‌ای از فایل اکسل و خروجی گرفتن به صورت PDF چندصفحه‌ای ساخته شده است. هدف پروژه این است که برای کارهای مهندسی و ترسیم، بتوان تعداد زیادی مقطع را سریع، منظم و با اندازه‌گذاری خوانا تولید کرد.

این برنامه داده‌های مقاطع را از اکسل می‌خواند، هر مقطع را به صورت یک ذوزنقه با مقیاس هندسی رسم می‌کند، و سپس برچسب‌هایی مانند عرض بالا، عرض پایین، ارتفاع، عرض در ۲ متر از بالا، GL و FL را اضافه می‌کند. در نهایت، همه ترسیم‌ها را در قالب یک PDF صفحه‌بندی‌شده ذخیره می‌کند. این مخزن می‌تواند هم شامل کد پایتون و هم یک فایل اجرایی مستقل ویندوزی `.exe` باشد تا کاربران بدون نصب پایتون هم بتوانند از آن استفاده کنند.

### چه کاری انجام می‌دهد

- داده‌های مقاطع را از فایل اکسل می‌خواند.
- هر مقطع را به صورت یک ذوزنقه معکوس با مقیاس واقعی رسم می‌کند.
- برچسب‌های اندازه‌گذاری برای عرض بالا، عرض پایین، ارتفاع کامل، عرض در ۲ متر از بالا، GL و FL اضافه می‌کند.
- حداکثر ۹ مقطع را در هر صفحه PDF و در چیدمان ۳×۳ قرار می‌دهد.
- شماره صفحه را به صورت خودکار اضافه می‌کند.
- یک رابط گرافیکی ساده برای انتخاب فایل ورودی و محل ذخیره خروجی ارائه می‌دهد.

### چرا این ابزار مفید است

وقتی ترسیم مقاطع به صورت دستی انجام شود، کار تکراریِ رسم و برچسب‌گذاری می‌تواند زمان‌بر و مستعد خطا باشد. این اسکریپت بخش تکراری کار را خودکار می‌کند و در عین حال تناسب واقعی شکل‌ها را حفظ می‌کند؛ بنابراین خروجی برای کنترل، گزارش‌دهی و اشتراک‌گذاری با همکاران یا کارفرما مناسب است.

چون ذوزنقه‌ها با هندسه پویا رسم می‌شوند و فقط برچسب‌ها عوض نشده‌اند، مقاطع عریض‌تر و بلندتر در خروجی هم واقعاً عریض‌تر و بلندتر دیده می‌شوند. به همین دلیل، PDF حاصل از یک جدول ساده بسیار مفیدتر است.

### فرمت ورودی

فایل اکسل باید ستون‌های زیر را داشته باشد:

| ستون | توضیح |
|---|---|
| `Title` | نام مقطع یا عنوانی که بالای هر شکل نمایش داده می‌شود |
| `B1` | یکی از مقادیر عرض |
| `B2` | مقدار عرض دیگر |
| `h` | ارتفاع مقطع |
| `GL` | برچسب تراز زمین |
| `FL` | برچسب تراز کف |

یک فایل نمونه در ساختار این مخزن قرار دارد. در فایل نمونه، شیت شامل ۳۰ ردیف مانند `Section 1`، `Section 2` و ... است و برای هر ردیف مقادیر `B1`، `B2`، `h`، `GL` و `FL` وجود دارد.

#### نکته مهم درباره `B1` و `B2`

در منطق فعلی اسکریپت، هنگام رسم، `B1` و `B2` به صورت عمدی جابه‌جا می‌شوند تا با قالب‌بندی اصلی فایل اکسل هماهنگ باشد. یعنی در کد، عرض بالای رسم‌شده از ستون `B2` و عرض پایین رسم‌شده از ستون `B1` خوانده می‌شود.

اگر فایل اکسل شما از قبل عرض بالا و پایین را دقیقاً همان‌طور که باید رسم شوند ذخیره کرده باشد، ممکن است لازم باشد این جابه‌جایی را از کد حذف کنید.

### خروجی

خروجی نهایی یک PDF چندصفحه‌ای است که در هر صفحه ۹ شکل در چیدمان ۳×۳ قرار می‌گیرد. در نمونه خروجی، ۳۰ مقطع در ۴ صفحه تقسیم شده‌اند و عنوان هر مقطع، برچسب‌های دو رقمی اعشار، مقادیر GL و FL، و شماره صفحه در گوشه پایین سمت راست دیده می‌شود.

برای اینکه شکل‌ها از نظر هندسی واقعی‌تر نمایش داده شوند، هر مقطع با نسبت ابعاد مساوی و حاشیه‌های پویا رسم می‌شود تا در عین حفظ تناسب واقعی، فضای کافی برای فلش‌ها و نوشته‌ها باقی بماند.

### اجرای برنامه

#### روش ۱: اجرای فایل اجرایی `.exe`

این ساده‌ترین روش برای کاربرانی است که پایتون نصب نکرده‌اند.

1. روی فایل `.exe` دوبار کلیک کنید.
2. روی **Browse** کلیک کنید و فایل اکسل ورودی را انتخاب کنید.
3. محل ذخیره PDF را انتخاب کنید.
4. روی **Generate PDF** کلیک کنید.
5. منتظر پیام موفقیت بمانید.

این روش برای کاربران غیر فنی یا همکارانی که فقط نیاز به تولید خروجی از فایل اکسل آماده دارند، پیشنهاد می‌شود.

#### روش ۲: اجرای اسکریپت پایتون

اگر بخواهید کد را تغییر دهید یا مستقیم از سورس اجرا کنید:

```bash
pip install pandas matplotlib openpyxl
python sec2.py
```

برنامه یک رابط ساده دسکتاپ باز می‌کند که در آن فایل اکسل انتخاب می‌شود و مسیر خروجی PDF تعیین می‌گردد.

### رابط کاربری

نسخه پایتون از یک برنامه کوچک Tkinter استفاده می‌کند و به جای خط فرمان، پنجره گرافیکی ارائه می‌دهد. این رابط شامل موارد زیر است:

- دکمه انتخاب فایل اکسل.
- دکمه انتخاب محل ذخیره PDF.
- دکمه **Generate PDF**.
- پیام‌های موفقیت و خطا.

همچنین برنامه به صورت خودکار نام فایل خروجی پیشنهادی را بر اساس نام فایل اکسل انتخاب‌شده می‌سازد تا استفاده‌های بعدی راحت‌تر شود.

### منطق ترسیم

چند نکته فنی مهم برای کسانی که می‌خواهند اسکریپت را تغییر دهند:

- هر مقطع به صورت یک ذوزنقه معکوسِ پرشده با استفاده از مختصات هندسی `B1`، `B2` و `h` رسم می‌شود.
- نسبت ابعاد برابر باعث می‌شود عرض و ارتفاع از نظر بصری متناسب باقی بمانند.
- اندازه فاصله فلش‌ها و نوشته‌ها به صورت پویا از ابعاد مقطع محاسبه می‌شود تا خوانایی برای شکل‌های کوچک و بزرگ حفظ شود.
- عرض در ۲ متر فقط زمانی رسم می‌شود که ارتفاع مقطع بیش از ۲ متر باشد.
- GL و FL با دو رقم اعشار نمایش داده می‌شوند و برای خوانایی در دو طرف شکل قرار می‌گیرند.
- حداکثر ۹ مقطع در هر صفحه PDF و در قالب ۳×۳ قرار می‌گیرد.

### موارد کاربرد

این پروژه در هر جایی که لازم باشد مقاطع ذوزنقه‌ای یا مقاطع مشابه از داده‌های جدولی تولید شوند مفید است، از جمله:

- مقاطع خاکبرداری و خاکریزی یا زهکشی.
- مقاطع کانال، ترانشه یا گودبرداری.
- نمایش مقاطع عرضی راه یا خاکریز.
- ترسیم‌های کنترلی داخلی از فایل‌های نقشه‌برداری یا طراحی.
- بسته‌های گزارش سریع برای بررسی طراحی.

### نکات و محدودیت‌ها

- فایل اکسل باید ستون‌های `Title`، `B1`، `B2`، `h`، `GL` و `FL` را داشته باشد.
- مقادیر `GL` و `FL` به صورت عددی و با دو رقم اعشار نمایش داده می‌شوند؛ بنابراین اگر مقدار متنی وارد شود، ممکن است نیاز به تغییر کد باشد.
- منطق فعلی ترسیم بر اساس همان ساختار فایل اکسل تنظیم شده است که در آن `B1` و `B2` در هنگام رسم جابه‌جا می‌شوند.
- اسکریپت نمونه برای ویندوز نوشته شده و برای نمایش بهتر روی ویندوز از تنظیمات اختیاری DPI نیز پشتیبانی می‌کند.


### درباره پروژه

این پروژه برای خودکارسازی تولید ترسیم مقاطع از فایل اکسل به PDF صفحه‌بندی‌شده ساخته شده است و هم برای استفاده از سورس پایتون و هم برای استفاده به صورت برنامه مستقل دسکتاپ مناسب است.
