import { useEffect, useRef, useState } from "react";
import { api, post } from "./api";
import Md from "./PilotMarkdown";
import RampGraph from "./RampGraph";
import { guidedText, type TeachingLanguage } from "./guidedLocale";
import "./guided.css";

type Mode = "bridge" | "visual" | "algebra";
type CheckResult = {
  passed: boolean;
  number_ok: boolean;
  reason_ok: boolean;
  feedback: string;
  suggested_mode: Mode | null;
};
type Lesson = {
  check_id: string;
  step: number;
  mode: Mode;
  language: TeachingLanguage;
  title: string;
  goal: string;
  body: string;
  review?: { title: string; body: string }[];
  complete: boolean;
  retry_available: boolean;
  result: CheckResult | null;
  concepts: { id: string; title: string }[];
  checkpoint: {
    prompt: string;
    label: string;
    choices: { id: string; text: string }[];
  };
};
type Envelope = { language: TeachingLanguage; lesson: Lesson | null };
type Evidence = {
  id: string;
  at: string;
  language: TeachingLanguage;
  mode: Mode;
  number: string;
  choice: string;
  step: number;
  result: CheckResult;
  checkpoint: Lesson["checkpoint"];
};
const root = "/pilot/learning";

export default function GuidedLearning({
  disabled,
  language,
  onPractice,
}: {
  disabled: boolean;
  language: TeachingLanguage;
  onPractice: () => Promise<unknown>;
}) {
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [number, setNumber] = useState("");
  const [choice, setChoice] = useState("");
  const requestId = useRef(crypto.randomUUID());
  const tx = guidedText[language];
  const locked = disabled || busy;
  function envelope(e: Envelope) {
    setLesson(e.lesson);
    setLoaded(true);
  }
  async function action(fn: () => Promise<unknown>) {
    setBusy(true);
    setError("");
    try {
      await fn();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }
  async function reload() {
    envelope(await api<Envelope>(root + "/ramps"));
  }
  useEffect(() => {
    let active = true;
    api<Envelope>(root + "/ramps")
      .then((e) => {
        if (active) envelope(e);
      })
      .catch((e) => {
        if (active) setError(String(e));
      });
    return () => {
      active = false;
    };
  }, [language]);
  useEffect(() => {
    setNumber("");
    setChoice("");
    requestId.current = crypto.randomUUID();
  }, [lesson?.check_id]);
  async function next(useSuggestion = true) {
    if (!lesson) return;
    setLesson(
      await post<Lesson>(root + "/ramps/next", {
        check_id: lesson.check_id,
        use_suggestion: useSuggestion,
      }),
    );
  }
  return (
    <section className="guided-module" lang={language} aria-label={tx.title}>
      <div className="guided-heading">
        <span className="pilot-section-label">GUIDED LESSON · 01</span>
        <h3>{tx.title}</h3>
        <p>{tx.subtitle}</p>
      </div>
      <p className="pilot-muted">{tx.scope}</p>
      {error && (
        <div className="pilot-error" role="alert">
          {error}
          <button disabled={locked} onClick={() => void action(reload)}>
            {tx.reload}
          </button>
        </div>
      )}
      {!loaded ? (
        <p>{tx.loading}</p>
      ) : !lesson ? (
        <>
          <p>{tx.intro}</p>
          <button
            className="pilot-primary"
            disabled={locked}
            onClick={() =>
              void action(async () =>
                setLesson(await post<Lesson>(root + "/ramps/start")),
              )
            }
          >
            {tx.start}
          </button>
        </>
      ) : (
        <>
          <ol className="guided-progress" aria-label={tx.progress}>
            {lesson.concepts.map((c, i) => (
              <li
                key={c.id}
                aria-current={i === lesson.step ? "step" : undefined}
                className={
                  i < lesson.step ? "done" : i === lesson.step ? "current" : ""
                }
              >
                <span>{i + 1}</span>
                <div>
                  {c.title}
                  <small>
                    {i < lesson.step
                      ? tx.completed
                      : i === lesson.step
                        ? tx.current
                        : tx.pending}
                  </small>
                </div>
              </li>
            ))}
          </ol>
          {lesson.complete ? (
            <div className="guided-complete">
              <h4>{tx.done}</h4>
              <p>{tx.transfer}</p>
              <button
                className="pilot-primary"
                disabled={locked}
                onClick={() => void action(onPractice)}
              >
                {tx.practice}
              </button>
              <p className="pilot-muted">{tx.practiceScope}</p>
              <h4>{tx.review}</h4>
              <div className="pilot-routes">
                {(["bridge", "visual", "algebra"] as Mode[]).map((mode) => (
                  <button
                    key={mode}
                    aria-pressed={lesson.mode === mode}
                    disabled={locked}
                    onClick={() =>
                      void action(async () =>
                        setLesson(
                          await post<Lesson>(root + "/ramps/mode", { mode }),
                        ),
                      )
                    }
                  >
                    {tx[mode]}
                  </button>
                ))}
              </div>
              {lesson.review?.map((r, i) => (
                <details className="guided-review" key={i}>
                  <summary>{r.title}</summary>
                  <Md text={r.body} />
                  {lesson.mode === "visual" && (
                    <RampGraph step={i} language={language} />
                  )}
                </details>
              ))}
            </div>
          ) : (
            <>
              <h4>{lesson.title}</h4>
              <p>{lesson.goal}</p>
              <div
                className="pilot-routes"
                role="group"
                aria-label={tx.suggestion}
              >
                {(["bridge", "visual", "algebra"] as Mode[]).map((mode) => (
                  <button
                    key={mode}
                    aria-pressed={lesson.mode === mode}
                    className={lesson.mode === mode ? "active" : ""}
                    disabled={locked}
                    onClick={() =>
                      void action(async () =>
                        setLesson(
                          await post<Lesson>(root + "/ramps/mode", { mode }),
                        ),
                      )
                    }
                  >
                    {tx[mode]}
                  </button>
                ))}
              </div>
              <Md text={lesson.body} />
              {lesson.mode === "visual" && (
                <RampGraph
                  key={lesson.step}
                  step={lesson.step}
                  language={language}
                />
              )}
              <details className="guided-terms">
                <summary>{tx.terms}</summary>
                <p>
                  {tx.ramp} · {tx.slope} · {tx.plateau} · {tx.step}
                </p>
              </details>
              <div className="guided-check" key={lesson.check_id}>
                <h4>{tx.check}</h4>
                <Md text={lesson.checkpoint.prompt} />
                {!lesson.result ? (
                  <form
                    onSubmit={(e) => {
                      e.preventDefault();
                      void action(async () => {
                        const r = await post<{ lesson: Lesson }>(
                          root + "/ramps/check",
                          {
                            check_id: lesson.check_id,
                            request_id: requestId.current,
                            number,
                            choice,
                          },
                        );
                        setLesson(r.lesson);
                      });
                    }}
                  >
                    <label className="guided-number">
                      {lesson.checkpoint.label}
                      <input
                        required
                        value={number}
                        placeholder={tx.number}
                        maxLength={80}
                        disabled={locked}
                        onChange={(e) => {
                          setNumber(e.target.value);
                          requestId.current = crypto.randomUUID();
                        }}
                      />
                    </label>
                    <fieldset disabled={locked}>
                      <legend>{tx.reason}</legend>
                      {lesson.checkpoint.choices.map((c) => (
                        <label key={c.id}>
                          <input
                            type="radio"
                            name="guided-reason"
                            value={c.id}
                            checked={choice === c.id}
                            onChange={() => {
                              setChoice(c.id);
                              requestId.current = crypto.randomUUID();
                            }}
                            required
                          />
                          <span>{c.text}</span>
                        </label>
                      ))}
                    </fieldset>
                    <button
                      className="pilot-primary"
                      disabled={locked || !number.trim() || !choice}
                    >
                      {tx.submit}
                    </button>
                  </form>
                ) : (
                  <div aria-live="polite">
                    <strong>
                      {lesson.result.passed ? tx.passed : tx.failed}
                    </strong>
                    <p>{lesson.result.feedback}</p>
                    {lesson.result.suggested_mode && (
                      <p>
                        {tx.suggestion}:{" "}
                        <b>{tx[lesson.result.suggested_mode]}</b>
                      </p>
                    )}
                    <div className="guided-actions">
                      {lesson.result.passed ? (
                        <button
                          className="pilot-primary"
                          disabled={locked}
                          onClick={() => void action(() => next())}
                        >
                          {lesson.step === 2 ? tx.finish : tx.next}
                        </button>
                      ) : lesson.retry_available ? (
                        <>
                          <button
                            className="pilot-primary"
                            disabled={locked}
                            onClick={() => void action(() => next())}
                          >
                            {tx.retry}
                          </button>
                          <button
                            disabled={locked}
                            onClick={() => void action(() => next(false))}
                          >
                            {tx.keep}
                          </button>
                        </>
                      ) : (
                        <>
                          <p>{tx.exhausted}</p>
                          <button
                            disabled={locked}
                            onClick={() => void action(onPractice)}
                          >
                            {tx.practice}
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                )}
                <p className="pilot-muted">{tx.evidence}</p>
              </div>
            </>
          )}
          <p className="guided-saved">✓ {tx.saved}</p>
        </>
      )}
    </section>
  );
}

export function GuidedHistory() {
  const [records, setRecords] = useState<Evidence[]>([]);
  const [error, setError] = useState("");
  useEffect(() => {
    let active = true;
    api<Evidence[]>(root + "/history")
      .then((r) => {
        if (active) setRecords(r);
      })
      .catch((e) => {
        if (active) setError(String(e));
      });
    return () => {
      active = false;
    };
  }, []);
  return (
    <details className="guided-history">
      <summary>分步教学记录 / Guided learning ({records.length})</summary>
      <p>
        这些是讲解后的检查，不计为独立掌握。 / Guided checks do not establish
        independent mastery.
      </p>
      {error && <p role="alert">{error}</p>}
      {!records.length && !error && <p>尚无记录 / No guided checks yet.</p>}
      {[...records].reverse().map((r) => (
        <article key={r.id} lang={r.language}>
          <small>
            {new Date(r.at).toLocaleString(r.language)} · {r.language} ·{" "}
            {guidedText[r.language][r.mode]}
          </small>
          <b>
            {r.result.passed
              ? guidedText[r.language].passed
              : guidedText[r.language].failed}
          </b>
          <Md text={r.checkpoint.prompt} />
          <p>
            {r.checkpoint.label} = {r.number}
          </p>
          <p>{r.checkpoint.choices.find((c) => c.id === r.choice)?.text}</p>
        </article>
      ))}
    </details>
  );
}
