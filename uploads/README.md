# Uploads Directory

This directory contains uploaded files organized by type:

- `avatars/` - User profile pictures and avatars
- `documents/` - Document uploads (future use)
- `images/` - General image uploads (future use)

## File Naming Convention

Files are stored with the following naming pattern:
- Avatars: `{user_id}_{uuid}.{extension}`

## File Size Limits

- Avatars: Maximum 5MB
- Supported formats: JPEG, PNG, GIF, WebP

## Security Notes

- All uploads are validated for file type and size
- File names are sanitized to prevent directory traversal attacks
- Old files are cleaned up when new ones are uploaded
