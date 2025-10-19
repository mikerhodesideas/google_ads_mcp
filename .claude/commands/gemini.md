---
description: Run task using Gemini 2.5 Flash Preview model
argument-hint: <task-description>
allowed-tools: "*"
---

Use the Gemini 2.5 Flash Preview (09-2025) model to complete this task: $ARGUMENTS

You will use Node.js to call the Gemini API directly.

**API Details:**
- Model ID: `gemini-2.5-flash-preview-09-2025`
- API Key: Load from `GEMINI_API_KEY` environment variable
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{modelId}:generateContent`

**Request Format:**
```javascript
{
  contents: [{
    role: "user",
    parts: [{ text: prompt }]
  }],
  generationConfig: {
    maxOutputTokens: 1000,
    temperature: 0.7
  }
}
```

**Headers:**
- `Content-Type: application/json`
- `x-goog-api-key: {API_KEY}`

**Steps:**
1. Create a simple Node.js script to call the Gemini API
2. Load API key from environment
3. Send the request with the user's task as the prompt
4. Parse response and extract text from `candidates[0].content.parts[0].text`
5. Return the result

Handle errors gracefully and report token usage if available in `usageMetadata`.
