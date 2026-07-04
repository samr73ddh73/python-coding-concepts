1. For the GET redirect endpoint, it is worth specifying the HTTP status code used for the redirect, either 301 (permanent) or 302 (temporary). This matters in practice because 301 redirects are cached by browsers, which can cause issues if you ever need to update where a short URL points, making 302 the safer default for most URL shorteners.

2. Base62 just means you build codes using 62 safe characters, usually a-z, A-Z, and 0-9. That matters here because full ASCII includes symbols that make URLs awkward, while base62 stays short and URL friendly. Also, 62^6 is already about 57 billion, so even 6 base62 characters gives you way more than 1 billion possible short codes.

3. URL shortener: Use global counter in redit and encode it or hashing with base 62 encoding. 

4. Remember, in non functional changes, always consider CAP theorem. (We should not say all 3, svcalable, available and consistent)

5.In a system like Dropbox, storing metadata separately from the raw file content is a common and useful pattern. It would capture things like file name, size, version history, and sync status without coupling that information to the raw bytes of the file itself.

6. Modern desktop and mobile operating systems usually provide some file change notification mechanism, and your app or background service can subscribe to it for folders it has permission to watch. The exact API differs by OS, but the interview point is just that the sync agent listens for file events from the OS instead of rescanning the whole folder on a timer.

7. Presigned URLs — never proxy file bytes through your app server; generate a time-limited S3 presigned URL and redirect the client directly. This keeps your app stateless and offloads bandwidth.
Chunked / multipart upload — for large files, S3 multipart upload allows resumable uploads and parallel chunk transfers.
Content-addressable storage — storing files by hash (SHA-256 of content) gives you deduplication for free (Dropbox does this).
Separate read path — metadata queries hit your DB; file downloads hit S3 via CDN. Two completely independent scaling axes.
 https://www.hellointerview.com/learn/system-design/patterns/large-blobs



8. In Non Functional requirements, for each feature if we are prioritising Availability and perf, say it will be eventually consistent as per the CAP theorem.


9. Whenever we need to analyse click streams, what we can do is, In real Google News, they would track analytics on article clicks to understand user behavior and improve recommendations. We consider this out of scope, but here's how it would work: article links would point to Google's tracking endpoint like GET /article/{article_id} which logs the click event and returns a 302 redirect to the publisher's site. This click data helps train recommendation algorithms and measure engagement.


10. Infinite Scrolling:
- obviously pagination, but talk how you can paginate faster without order and limit
- What are the problems with limit and offset:
    if new rows are added, we could miss some rows if order is not added since pg don't maintain order by default
- So, faster pagination could be on timestamp based uuids: design article IDs to be monotonically increasing from the start. Instead of using random UUIDs, we can use time-ordered UUIDs (like ULIDs) or database auto-increment IDs that naturally increase with each new article.



 Things to learn:
 1. Merkel Tree
 2. DB Isolation level and locking (Today)