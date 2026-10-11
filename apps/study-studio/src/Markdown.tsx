import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';
export default function Markdown({children}:{children:string}){
  return <div className="markdown"><ReactMarkdown remarkPlugins={[remarkMath,remarkGfm]} rehypePlugins={[[rehypeKatex,{throwOnError:false}]]} skipHtml components={{img:()=>null,a:({children,href})=><a href={href} target="_blank" rel="noreferrer">{children}</a>}}>{children}</ReactMarkdown></div>;
}
