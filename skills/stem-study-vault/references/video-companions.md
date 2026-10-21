# Concept-level companion videos

Read when adding, maintaining or recommending videos alongside a course explanation or practice task. The intended experience is **reach the concept → open the relevant moment → notice a specific idea → return to the lesson or exercise**. These rules guide authored notes; they do not add video extraction, playback tracking or automatic synchronization to the helper or Study Studio.

## Match the current learning need

Start with the existing course video map and the actual passage being taught. Within the requested batch, look for a useful companion for each substantive concept or difficult step, rather than attaching the same full-course playlist to every heading. Prefer a focused segment that explains the missing distinction, derivation, visual relationship or practical application. A short self-contained video may be recommended in full when its relevance and duration are known. Do not cut off a premise simply to make the clip shorter.

Choose for clarity, correctness, course fit, language and accessibility. Prefer identifiable authors and original university/course/creator pages over anonymous reposts; reputation and a matching title alone do not verify the explanation. Offer a primary clip and an alternative only when the alternative serves a different need, such as language or depth. A useful clip remains optional support, not an extra compulsory lecture.

Keep a concise coverage note in the existing source/video map or progress record: matched, candidate needing verification, no suitable source found, or no additional video needed with a reason. Do not fabricate precision to claim every concept has a video, and do not label a directory link as a verified segment. Preserve the complete written teaching even when no video is available.

## Put the link at the learning point

Use a normal Markdown link in an Obsidian callout beside the relevant explanation. No community plugin or embedded player is required. Include:

- The concept and its role here: foundation, explanation, derivation or application; identify the local Lecture/Week only when supported by course materials.
- Author and recognizable video title, with the clickable link opening the recommended starting point when the platform supports it.
- Start–end time on the original video's timeline and the suggested duration. For a verified short whole video, label it “full video.” State explicitly when timing is unknown.
- What to notice or resolve, the relevant course-specific difference, and a link back to the exact explanation, example or next task.
- Spoken language and known subtitle availability. Put access limits or a verification caveat on the card when they affect its use; detailed evidence belongs in the source map.

Adapt this layout; the parenthesized destinations below are template fields to replace, not usable links:

```markdown
> [!info] 配套视频 · 知识点 / 已核实的课程位置
> [作者 · 视频标题](已核实的起点链接) · 起点–终点 · 建议观看时长
> 看什么：这段要帮助你理解的具体关系或步骤。
> 课程边界：本课采用的定义、符号或条件与视频的差别。
> 语言与核验：实际语言／已知字幕；已核实的部分与尚未核实的部分。
> 看完后：[回到当前例题或小节](实际存在的笔记与锚点)。
```

Use “Companion video / What to notice / Course alignment / Return to the example” for the English version. Keep the same concept and segment identity across languages; translate the guidance and boundary note, retaining a recognizable original title. Label an English-only video honestly and provide a Chinese written equivalent when needed. Do not claim that changing the page language translates audio or creates subtitles. Automatic captions are not verified mathematical notation or terminology.

For many clips, maintain a course-level lookup table as well as the inline cards, with links to exact teaching sections. Reuse an existing index and layout rather than creating competing maps. Keep a stable concept/segment identity where practical so corrections reach every occurrence. Preserve existing generated-block markers; update the matching card rather than appending duplicates, and leave personal text around it unchanged.

## Verify timestamps and content separately

Record the evidence actually available, rather than assigning a single blanket “verified” label:

| Check | What it establishes and what it does not |
| --- | --- |
| Original page / course directory | Identity, provenance and advertised topic; not segment contents or successful playback |
| Author's chapters | A published starting point and chapter label; not minute-by-minute instructional accuracy |
| Timestamped transcript / captions | Wording near the topic and approximate timing; may omit diagrams, equations or contain recognition errors |
| Segment inspected | The actual spoken/visual explanation and its scope, to the extent inspected |
| Link opened and seek tested | Whether the target platform/browser opens the intended video and start time in that environment; not universal availability |

Use the original source or a timestamped transcript to establish the interval. Inspect the recommended segment, including relevant visual material, where the available tools permit. If access, captions or playback are blocked, retain the supported facts and label the missing checks. Do not imply listening/watching occurred because a search snippet or chapter list was read. A search result alone is a candidate, not proof of an exact segment.

Build the timestamp link using that platform's supported share/start format, preserving the correct video and any necessary part identifier. Keep times tied to the exact upload/version; a recut or reupload may have a different timeline. Do not transplant one site's parameters to another. For a YouTube watch link, the familiar `t=2430s` represents 40:30; verify the actual link's behavior before claiming it was playback-tested. Convert hours/minutes/seconds carefully: 40:30–42:43 spans **2 minutes 13 seconds**, not 2 minutes 43 seconds. Check that the start precedes the end and the end does not exceed known video duration; leave an unknown end explicit instead of guessing it.

Display the recommended stopping time. A start-time link does **not** by itself stop playback at the endpoint. Only claim automatic stopping if the actual player supports it and that behavior was tested. When timed links are unsupported or unverified, provide the original link and manual seek instruction with an honest status; do not promise one-click precision.

Keep the source URL, author/title, interval, lesson destination, language/access notes, evidence basis, known limits and actual check date in the existing map or source record. Recheck changed or reported broken links and affected cards during updates; do not imply a past check guarantees future access. Preserve personal annotations when adjusting generated cards.

## Keep the course boundary explicit

Compare the clip with the local explanation: definitions, notation, assumptions, implementation/version and depth. Name the actual difference where it matters. For example, ACID consistency, read consistency and eventual consistency must not be treated as interchangeable merely because a video uses the word “consistency.” An external course's Lecture number is not the learner's Lecture number; a vault's Week arrangement does not prove the order of future live lectures.

For assessment requirements, use the supplied course's stated scope and conventions. If the course and external source appear to conflict, explain the distinction or flag the unresolved discrepancy; do not endorse a technical error solely because it appears in either source. External application material is not evidence of added exam content.

Link to the source by default. Adding a link does not authorize downloading, redistributing clips, copying substantial transcripts or publishing private university files. Preserve private authenticated lecture links in their intended private context; never copy signed access tokens or personal session URLs into a public skill. Essential explanations and required exercise inputs remain readable locally.

## Return to learning without inventing evidence

After the clip, direct the student to the current explanation, a worked example or a short relevant check. Keep any question that must precede a reveal before the video link, and mark clips that expose the current solution. Follow the existing support/exposure rules when actual viewing or help is known; do not infer that a student watched or mastered a concept from the presence of a link or a click. Reading progress, video activity and independent performance remain distinct.
