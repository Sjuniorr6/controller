import re

# Read the file
with open('core/equipament_cnfig.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace single quotes with double quotes for the GUIDs
# This regex matches single quotes around GUID patterns
pattern = r"'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})'"
replacement = r'"\1"'

# Apply the replacement
modified_content = re.sub(pattern, replacement, content)

# Write back to file
with open('core/equipament_cnfig.py', 'w', encoding='utf-8') as f:
    f.write(modified_content)

print('Successfully converted single quotes to double quotes in equipament_cnfig.py') 