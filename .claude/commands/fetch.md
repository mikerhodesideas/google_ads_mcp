---
description: Fetch YouTube transcript and save to research folder
argument-hint: <youtube-url>
allowed-tools: Bash(node:*), Bash(yt-dlp:*)
---

Fetch the YouTube transcript for the video at: $ARGUMENTS

Follow these steps:

1. **Extract video ID** from the URL
2. **Fetch video info** using yt-dlp to get:
   - Title
   - Upload date
   - Channel name and URL

3. **Check if known channel**:
   - Load known channels from `code/youtube/config.js` CHANNELS object
   - If unknown, ask user: "Unknown channel detected. Create new folder or use 'other'?"
   - If new folder: ask for folder name (lowercase, no spaces)

4. **Fetch transcript**:
   - Try manual subtitles first: `yt-dlp --skip-download --write-sub --sub-lang en --sub-format vtt`
   - Fallback to auto-generated: `yt-dlp --skip-download --write-auto-sub --sub-lang en --sub-format vtt`

5. **Clean transcript**:
   - Remove VTT formatting (WEBVTT, timestamps, `<c>` tags)
   - Remove duplicate consecutive lines
   - Join as single paragraph with spaces

6. **Create markdown file**:
   - Filename: `YYYYMMDD-title-slug.md`
   - Location: `research/youtube/{channel}/`
   - Format:
     ```markdown
     # {title}

     - **Channel:** {channel_url}
     - **Video ID:** {video_id}
     - **Upload Date:** {date}
     - **URL:** https://www.youtube.com/watch?v={video_id}

     ## Transcript

     {cleaned_transcript}
     ```

7. **Update INDEX.md**:
   - Scan all channel folders
   - List videos newest first per channel
   - Format: `- [{title}]({channel}/{filename}) - {date}`

Use Node.js script at `code/fetch-youtube-transcripts.js` as reference for implementation details.