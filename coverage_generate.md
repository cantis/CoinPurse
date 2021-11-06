# Coverage Report Generation
To generate a code coverage report, run the following command:
```powershell
# Generage the coverage data
PS coverage run --source=. -m pytest

# Show the report (command line)
PS coverage report

# Generate the HTML Coverage report into
PS coverage html
```