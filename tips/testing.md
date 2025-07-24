# Testing

<details>
<summary>How to save a base64 encoded image temporarily in file system?</summary>

```py
import base64
import tempfile
import os

# Your base64-encoded image data
image_data = b"iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8z8BQz0AEYBxVSF+FABJADveWkH6oAAAAAElFTkSuQmCC"

# Create a temporary file
with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
    # Decode and write the image data
    decoded_data = base64.b64decode(image_data)
    temp_file.write(decoded_data)
    temp_file_path = temp_file.name
```

</details>
