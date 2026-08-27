# calbench
A working prototype covering data entry, calibration maths, BS EN ISO 6789 certificates, Code 128 barcode labels, and a searchable SQLite store — built to demonstrate software engineering ability alongside torque and force metrology experience.

🔗 Live demo: https://perfecthost-ship-it.github.io/calbench/

🌐 CALBENCH
Torque Calibration Certificates, Labels & Traceability

A working prototype covering data entry, calibration maths, BS EN ISO 6789 certificates, Code 128 barcode labels, and a searchable SQLite store — built to demonstrate software engineering ability alongside torque and force metrology experience.

Prototype · Demonstration data only
Built with deliberately ordinary tools, deliberately used well.

📌 Overview
Most calibration labs run torque calibration as three disconnected processes:

A spreadsheet for readings

A Word template for the certificate

A label printer’s own software

CALBENCH treats it as one flow.  
Enter readings once — the calculation, certificate, and labels all stay in sync.

✔ 01 — Capture
Ten‑point readings, both directions, with live pass/fail against a configurable tolerance.

✔ 02 — Certify
A BS EN ISO 6789 certificate that calculates linearity, repeatability, hysteresis, best‑fit slope, and R² from raw readings — never typed in.

✔ 03 — Trace
A Code 128 barcode that follows the instrument through production, and a database that answers:

“What did this standard underwrite?”

🔧 Instrument, Method & Conditions
Every field a UKAS‑style certificate needs:

Instrument under test

Procedure/method

Calibration conditions

Reference standards

Environmental window checks

Ambient temperature is validated live; outside the permitted window, the certificate fails automatically, because the method wasn’t followed — regardless of how the readings looked.

🧩 Reference Equipment & Traceability
A calibration is only as good as the standards behind it.

Real labs use several:

Transducer

Rig

Multimeter

Weight set

Each has its own serial and certificate, and each is checked against the calibration date.
Expired standards are flagged automatically — a standard out of calibration cannot underwrite the certificate it appears on.

📈 Ten Test Points, Both Directions
Right‑hand, left‑hand, or both.

With both selected, every point gets:

Individual readings

Mean

Verdict per direction

A wrench drifting in one direction doesn’t get averaged into a false pass.

📊 Linearity, Repeatability & Hysteresis
Every figure is calculated from raw readings:

Linearity

Repeatability

Hysteresis

Best‑fit slope

R²

The deviation chart plots applied torque vs deviation, with the tolerance band shaded behind it.
Any point drifting past 100% of range is highlighted in red instantly.

📝 Certificate Output
A certificate that reads as a real document:

Masthead

Instrument

Calibration conditions

Full reference‑equipment table

Results

Uncertainty statement referencing UKAS M3003

Environmental failure is stated separately from tolerance failure.
Prints straight to A4 with the interface stripped out.

🏷 Barcode & Labels
Code 128 generated in the page itself — no library, no CDN, no internet connection required.

The same payload prints on:

70×32mm instrument sticker

100×70mm box label

One scan follows the item through the whole process.

🔍 Scan & Search
Every certificate and every reference item lives in SQLite.

A scan returns:

The instrument

Its full calibration history

Search reaches into the reference‑equipment table too:

Enter a standard’s serial number → get every certificate it underwrote.

Exactly the query you need when a standard turns out to be faulty.

📱 Mobile Build
A separate build for the phone — not the desktop layout squeezed down, but a genuine mobile shell:

Bottom tab bar

Full‑height views

44px touch targets

16px inputs (Safari doesn’t zoom)

Every calculation and API call is identical between desktop and mobile; only the shell differs.
Certificates saved from either device are identical in the database.

🛠 Built With
Front End
Plain HTML, CSS, JavaScript — no build step, no framework

Code 128 barcode encoder written from scratch

SVG deviation chart with least‑squares linearity fit

Two builds sharing one application core: desktop + mobile shell

Back End
Python standard library only — zero pip installs

SQLite with a proper schema: instruments, certificates, readings, equipment

Server re‑derives every verdict from stored readings — client is never trusted

Small HTTP API: search, scan‑lookup, save, load

Engineering Judgement
Every pass/fail traced to a specific standard

Reverse traceability: find every certificate a given standard underwrote

Verified with synthetic data — a perfectly linear instrument returns R² = 1.0

Built iteratively against real feedback from working labs

README.md
  LICENSE
🚀 Status
Prototype · Demonstration data only
No releases published yet.


📜 License
This project is licensed under the MIT License.

👤 Author
Lee  
Leicester, UK
Embedded & Software Engineering
