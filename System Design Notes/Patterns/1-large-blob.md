https://www.hellointerview.com/learn/system-design/patterns/large-blobs

Presigned URLs — never proxy file bytes through your app server; generate a time-limited S3 presigned URL and redirect the client directly. This keeps your app stateless and offloads bandwidth.
Chunked / multipart upload — for large files, S3 multipart upload allows resumable uploads and parallel chunk transfers.
Content-addressable storage — storing files by hash (SHA-256 of content) gives you deduplication for free (Dropbox does this).
Separate read path — metadata queries hit your DB; file downloads hit S3 via CDN. Two completely independent scaling axes.
 https://www.hellointerview.com/learn/system-design/patterns/large-blobs