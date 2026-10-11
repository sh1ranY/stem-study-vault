import { useEffect, useState } from "react";
import { api } from "./api";
import { useLocale } from "./Locale";
import type { Course } from "./pilotTypes";
export type NextStep = {
  topic: string;
  action: "resume" | "revisit" | "review" | "guided" | "practice" | "diagnosis";
  task_id: string | null;
  due_at: string | null;
  attempts: number;
  independent: number;
  guided_steps: number;
  guided_available: boolean;
  draft_saved: boolean;
};
const copy = {
  en: {
    title: "Your next step",
    scope:
      "Suggestions from your saved work. You can choose any unit; reading and guided checks are separate from independent evidence.",
    resume: "Continue unfinished problem",
    revisit: "Revisit the difficult step",
    review: "Try a scheduled review",
    guided: "Continue guided lesson",
    practice: "Try a fresh problem",
    diagnosis: "Check your starting point",
    attempts: "active attempts",
    independent: "independent answer checks",
    guidedSteps: "guided steps checked",
    due: "Suggested review",
    draft: "Draft saved",
    read: "Read course notes",
    coverage:
      "Coverage: 3 authored practice topics; step-by-step teaching currently covers ramps. Other units retain the original notes.",
    reload: "Reload learning overview",
  },
  "zh-CN": {
    title: "接下来，学什么",
    scope:
      "根据已保存的作答提出建议。你仍可自由选择单元；阅读、引导检查与独立证据分开记录。",
    resume: "继续未完成的题",
    revisit: "回到刚才的卡点",
    review: "做一次到期复查",
    guided: "继续分步教学",
    practice: "用新题检查理解",
    diagnosis: "检查当前起点",
    attempts: "次有效作答",
    independent: "次独立检查",
    guidedSteps: "步引导检查",
    due: "建议复查",
    draft: "草稿已保存",
    read: "阅读课程讲义",
    coverage:
      "当前覆盖：3 个自编练习主题；分步教学先覆盖斜坡。其他单元提供原知识库讲义。",
    reload: "重新载入学习建议",
  },
};
export default function LearningOverview({
  course,
  version,
  disabled,
  onContinue,
  onRead,
}: {
  course: Course;
  version: number;
  disabled: boolean;
  onContinue: (step: NextStep) => void;
  onRead: () => void;
}) {
  const { language } = useLocale();
  const tx = copy[language];
  const [rows, setRows] = useState<NextStep[]>([]);
  const [error, setError] = useState("");
  const [retry, setRetry] = useState(0);
  useEffect(() => {
    let active = true;
    api<{ topics: NextStep[] }>("/pilot/learning/overview")
      .then((r) => {
        if (active) {
          setRows(r.topics);
          setError("");
        }
      })
      .catch((e) => {
        if (active) setError(String(e));
      });
    return () => {
      active = false;
    };
  }, [version, retry, course.id]);
  return (
    <section className="learning-overview" aria-labelledby="overview-title">
      <div>
        <span className="pilot-eyebrow">{course.code} · STUDY PLAN</span>
        <h2 id="overview-title">{tx.title}</h2>
        <p>{tx.scope}</p>
      </div>
      {error && (
        <p role="alert">
          {error}{" "}
          <button onClick={() => setRetry((x) => x + 1)}>{tx.reload}</button>
        </p>
      )}
      <div className="overview-grid">
        {rows.filter(r => course.topics[r.topic]).map((r) => (
          <article key={r.topic}>
            <span className="overview-number">
              {String(course.topics[r.topic].week).padStart(2, "0")}
            </span>
            <h3>{course.topics[r.topic].title}</h3>
            <p>{course.topics[r.topic].objective}</p>
            <small>
              {r.attempts} {tx.attempts} · {r.independent} {tx.independent}
              {r.guided_available && (
                <>
                  {" "}
                  · {r.guided_steps}/3 {tx.guidedSteps}
                </>
              )}
            </small>
            {r.due_at && (
              <small>
                {tx.due}: {new Date(r.due_at).toLocaleDateString(language)}
              </small>
            )}
            {r.draft_saved && <small>{tx.draft}</small>}
            <button
              className="pilot-primary"
              disabled={disabled}
              onClick={() => onContinue(r)}
            >
              {tx[r.action]}
            </button>
          </article>
        ))}
      </div>
      <p className="pilot-muted">{language === "en" ? `Coverage: ${Object.keys(course.topics).length} original starter topics with bounded answer checks. ${course.code === "ELEC270" ? "Step-by-step guided teaching is available for ramps. " : ""}${course.mode === "demo" ? "Demo notes are original examples, not a full course." : "Other units provide imported reading materials."}` : `当前覆盖：${Object.keys(course.topics).length}个原创入门练习主题，检查范围限于题目判据。${course.code === "ELEC270" ? "斜坡另有分步教学。" : ""}${course.mode === "demo" ? "演示讲义是原创示例，不代表完整课程。" : "其他单元提供导入的阅读资料。"}`}</p>
      <button disabled={disabled} onClick={onRead}>
        {tx.read}
      </button>
    </section>
  );
}
