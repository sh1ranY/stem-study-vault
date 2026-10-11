import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import rehypeKatex from "rehype-katex";
const slug = (s: string) =>
  s.replace(/[^\w\-\u4e00-\u9fff]+/g, "-").replace(/^-|-$/g, "");
export default function Md({ text }: { text: string }) {
  const markdown = text
    .split(/(```[\s\S]*?```)/g)
    .map((part, i) =>
      i % 2
        ? part
        : part.replace(
            /\$\$([\s\S]*?)\$\$/g,
            (_, formula: string) => "\n\n$$\n" + formula.trim() + "\n$$\n\n",
          ),
    )
    .join("");
  const headingId = (line?: number) =>
    slug((markdown.split("\n")[(line || 1) - 1] || "").replace(/^#+\s*/, ""));
  return (
    <div className="pilot-md">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[[rehypeKatex, { throwOnError: false }]]}
        skipHtml
        components={{
          img: ({ src, alt }) =>
            src?.startsWith("/api/pilot/assets/") ? (
              <img src={src} alt={alt} loading="lazy" />
            ) : null,
          a: ({ href, children }) => (
            <a
              href={href}
              target={href?.startsWith("/api/") ? "_blank" : undefined}
              rel="noreferrer"
            >
              {children}
            </a>
          ),
          p: ({ children }) =>
            typeof children === "string" &&
            /^\^[\w-]+$/.test(children.trim()) ? (
              <span id={children.trim().slice(1)} />
            ) : (
              <p>{children}</p>
            ),
          h2: ({ children, node }) => (
            <h2 id={headingId(node?.position?.start.line)}>{children}</h2>
          ),
          h3: ({ children, node }) => (
            <h3 id={headingId(node?.position?.start.line)}>{children}</h3>
          ),
        }}
      >
        {markdown}
      </ReactMarkdown>
    </div>
  );
}
