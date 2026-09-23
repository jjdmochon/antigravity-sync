# Tone, Voice, and Person Guidelines (Google Developer Docs Style Guide)

## 1. Second Person ("You")
- **Use second person ("you", "your")** to address the developer directly.
- **Avoid first-person plural ("we", "our", "us")**.
  - *Incorrect:* Next, we will configure the database connection.
  - *Correct:* Next, configure the database connection.
- **Exceptions for "We":** Use "we" only when referring specifically to Google (or the project organization) as a corporate entity (e.g., "We recommend upgrading to API v2 before June 2026").

## 2. Active Voice & Present Tense
- **Prefer Active Voice:** The subject performs the action. Active voice is direct, shorter, and clearer.
  - *Incorrect:* The API request is processed by the server and a JSON response is returned.
  - *Correct:* The server processes the API request and returns a JSON response.
- **Use Present Tense:** Describe software behavior as happening now, not in the future.
  - *Incorrect:* Calling `connect()` will establish a socket connection.
  - *Correct:* Calling `connect()` establishes a socket connection.

## 3. Imperative Mood for Procedures & Instructions
- **Use direct commands** for instructional steps.
- **Avoid modal filler words** like "you should", "you can", "you may want to", "please".
  - *Incorrect:* You should click the **Save** button.
  - *Correct:* Click **Save**.
  - *Incorrect:* Please ensure that the environment variable is set.
  - *Correct:* Set the environment variable.

## 4. Clear, Direct, and Concise Phrasing
- Cut unnecessary fluff words ("in order to" → "to", "at this point in time" → "now", "utilize" → "use").
- State the condition before the action when giving conditional instructions:
  - *Incorrect:* Click **Deploy** if you want to deploy the container.
  - *Correct:* To deploy the container, click **Deploy**.

## 5. Polite and Helpful, Not Overly Casual
- Keep a professional, respectful tone. Avoid slang, emojis (in formal technical docs), internet acronyms (e.g., AFAIK, IMHO), or excessive exclamation marks.
