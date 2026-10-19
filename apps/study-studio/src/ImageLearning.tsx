import {
  forwardRef,
  useEffect,
  useId,
  useImperativeHandle,
  useMemo,
  useRef,
  useState,
} from "react";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  FlaskConical,
  Lightbulb,
  RefreshCw,
} from "lucide-react";
import { api } from "./api";
import { useLocale } from "./Locale";
import Md from "./PilotMarkdown";
import { imageLearningContent, type BridgeId } from "./imageLearningContent";
import {
  addNoise,
  DEFAULT_CONTROLS,
  IMAGE_SIZE,
  imageRow,
  makeImage,
  response,
  smoothImage,
  type LabControls,
} from "./imageLab";
import "./imageLearning.css";

type Draft = { number: string; choice: string; working: string };
type Result = {
  passed: boolean;
  number_ok: boolean;
  choice_ok: boolean;
  status: string;
  feedback: string;
  suggested_bridge: BridgeId | null;
};
type Question = {
  id: string;
  kind: string;
  variant: number;
  prompt: string;
  number_label: string;
  choices: { id: string; label: string }[];
  result: Result | null;
  help: { hint?: string; solution?: string };
  retry_available?: boolean;
};
type Session = {
  unit_id: string;
  content_version: string;
  course_version: string;
  revision: number;
  language?: string;
  stage: number;
  controls: LabControls;
  prediction: string;
  reflection: string;
  opened_bridges: string[];
  questions: Question[];
  history: unknown[];
  drafts?: Record<string, Draft>;
};
type Patch = {
  stage?: number;
  controls?: LabControls;
  prediction?: string;
  reflection?: string;
  bridge?: BridgeId;
  drafts?: Record<string, Draft>;
};
export type ImageLearningHandle = { flush: () => Promise<void> };
type Props = { onCoursePractice: () => void; disabled?: boolean };
const BASE = "/pilot/learning/images";
const EMPTY: Draft = { number: "", choice: "", working: "" };

function ImageCanvas({
  pixels,
  row,
  label,
  description,
  colour,
}: {
  pixels: Float64Array;
  row: number;
  label: string;
  description: string;
  colour: string;
}) {
  const ref = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const ctx = ref.current?.getContext("2d");
    if (!ctx) return;
    const image = ctx.createImageData(IMAGE_SIZE, IMAGE_SIZE);
    for (let i = 0; i < pixels.length; i++) {
      const value = Math.round(pixels[i] * 255);
      image.data.set([value, value, value, 255], i * 4);
    }
    ctx.putImageData(image, 0, 0);
  }, [pixels]);
  return (
    <figure className="image-unit-image">
      <figcaption>
        <span className="image-unit-dot" style={{ background: colour }} />
        {label}
      </figcaption>
      <div className="image-unit-canvas-wrap">
        <canvas
          ref={ref}
          width={IMAGE_SIZE}
          height={IMAGE_SIZE}
          role="img"
          aria-label={`${label}. ${description}`}
        />
        <span
          className="image-unit-row-line"
          aria-hidden="true"
          style={{
            top: `${((row + 0.5) / IMAGE_SIZE) * 100}%`,
            background: colour,
          }}
        />
      </div>
    </figure>
  );
}
const colours = ["#5c6e62", "#ab731e", "#2478b7"];
function ImageLab({
  controls,
  change,
  language,
}: {
  controls: LabControls;
  change: (v: LabControls) => void;
  language: "en" | "zh-CN";
}) {
  const c = imageLearningContent[language],
    id = useId();
  const data = useMemo(() => {
    const clean = makeImage(controls.pattern);
    const noisy = addNoise(clean, controls.noise);
    return [clean, noisy, smoothImage(noisy, controls.passes)];
  }, [controls.pattern, controls.noise, controls.passes]);
  const rows = useMemo(
    () => data.map((x) => imageRow(x, controls.row)),
    [data, controls.row],
  );
  const labels = [c.clean, c.noisy, c.filtered];
  const path = (values: number[]) =>
    values
      .map(
        (v, i) =>
          `${i === 0 ? "M" : "L"}${54 + (i / 95) * 574},${174 - v * 140}`,
      )
      .join(" ");
  return (
    <div className="image-unit-lab">
      <div className="image-unit-controls">
        <label htmlFor={`${id}-pattern`}>
          {c.pattern}
          <select
            id={`${id}-pattern`}
            value={controls.pattern}
            onChange={(e) =>
              change({
                ...controls,
                pattern: e.target.value as LabControls["pattern"],
              })
            }
          >
            <option value="scene">{c.scene}</option>
            <option value="stripes">{c.stripes}</option>
          </select>
        </label>
        <label htmlFor={`${id}-passes`}>
          {c.passes}
          <output>{controls.passes}</output>
          <input
            id={`${id}-passes`}
            type="range"
            min="0"
            max="8"
            step="1"
            value={controls.passes}
            onChange={(e) =>
              change({ ...controls, passes: Number(e.target.value) })
            }
          />
        </label>
        <label htmlFor={`${id}-noise`}>
          {c.noise}
          <output>{controls.noise.toFixed(2)}</output>
          <input
            id={`${id}-noise`}
            type="range"
            min="0"
            max="0.35"
            step="0.01"
            value={controls.noise}
            onChange={(e) =>
              change({ ...controls, noise: Number(e.target.value) })
            }
          />
        </label>
        <label htmlFor={`${id}-row`}>
          {c.row}
          <output>{controls.row}</output>
          <input
            id={`${id}-row`}
            type="range"
            min="0"
            max="95"
            step="1"
            value={controls.row}
            onChange={(e) =>
              change({ ...controls, row: Number(e.target.value) })
            }
          />
        </label>
      </div>
      <p className="image-unit-small">{c.zero}</p>
      <div className="image-unit-images">
        {data.map((pixels, i) => (
          <ImageCanvas
            key={i}
            pixels={pixels}
            row={controls.row}
            label={labels[i]}
            description={c.imageAlt}
            colour={colours[i]}
          />
        ))}
      </div>
      <figure className="image-unit-profile">
        <figcaption>
          {c.profile} · {c.row} {controls.row}
        </figcaption>
        <svg
          viewBox="0 0 664 223"
          role="img"
          aria-label={`${c.profile}. ${c.position}; ${c.brightness}: 0–1.`}
        >
          {[0, 0.5, 1].map((v) => (
            <g key={v}>
              <line
                x1="54"
                x2="628"
                y1={174 - v * 140}
                y2={174 - v * 140}
                stroke="#dce3dc"
              />
              <text x="44" y={178 - v * 140} textAnchor="end">
                {v}
              </text>
            </g>
          ))}
          {[0, 24, 48, 72, 95].map((v) => (
            <text key={v} x={54 + (v / 95) * 574} y="191" textAnchor="middle">
              {v}
            </text>
          ))}
          <text x="54" y="18">
            {c.brightness}
          </text>
          <text x="342" y="216" textAnchor="middle">
            {c.position}
          </text>
          {rows.map((values, i) => (
            <path
              key={i}
              d={path(values)}
              stroke={colours[i]}
              strokeWidth={i === 2 ? 2.7 : 1.4}
              strokeDasharray={i === 0 ? "5 3" : undefined}
              fill="none"
            />
          ))}
        </svg>
        <div className="image-unit-legend">
          {labels.map((label, i) => (
            <span key={label}>
              <span style={{ background: colours[i] }} />
              {label}
            </span>
          ))}
        </div>
      </figure>
      <details className="image-unit-data">
        <summary>{c.table}</summary>
        <div className="image-unit-table-scroll">
          <table>
            <thead>
              <tr>
                <th>{c.sample}</th>
                {labels.map((x) => (
                  <th key={x}>{x}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: 12 }, (_, i) => i * 8).map((n) => (
                <tr key={n}>
                  <th>{n}</th>
                  {rows.map((r, i) => (
                    <td key={i}>{r[n].toFixed(3)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
      <p className="image-unit-small">{c.method}</p>
    </div>
  );
}
function FrequencyPlot({ language }: { language: "en" | "zh-CN" }) {
  const c = imageLearningContent[language];
  return (
    <figure className="image-unit-frequency">
      <figcaption>{c.frequencyPlot}</figcaption>
      <svg
        viewBox="0 0 600 200"
        role="img"
        aria-label={`${c.frequencyCaption} ${c.frequencyAxis}; ${c.gain}.`}
      >
        <line x1="48" x2="565" y1="150" y2="150" stroke="#b8c8b9" />
        <line x1="48" x2="48" y1="25" y2="150" stroke="#b8c8b9" />
        {[0, 0.25, 0.5].map((f) => (
          <g key={f}>
            <line
              x1={48 + f * 1034}
              x2={48 + f * 1034}
              y1="25"
              y2="150"
              stroke="#e0e7dc"
            />
            <text x={48 + f * 1034} y="169" textAnchor="middle">
              {f}
            </text>
          </g>
        ))}
        {[0, 0.5, 1].map((v) => (
          <text key={v} x="36" y={154 - v * 125} textAnchor="end">
            {v}
          </text>
        ))}
        <path
          d={Array.from(
            { length: 101 },
            (_, i) =>
              `${i === 0 ? "M" : "L"}${48 + i * 5.17},${150 - response(i / 200) * 125}`,
          ).join(" ")}
          stroke="#2478b7"
          strokeWidth="3"
          fill="none"
        />
        <text x="48" y="16">
          {c.gain}
        </text>
        <text x="306" y="193" textAnchor="middle">
          {c.frequencyAxis}
        </text>
      </svg>
      <p>{c.frequencyCaption}</p>
    </figure>
  );
}

const ImageLearning = forwardRef<ImageLearningHandle, Props>(
  function ImageLearning({ onCoursePractice, disabled = false }, ref) {
    const { language } = useLocale(),
      c = imageLearningContent[language];
    const [session, setSession] = useState<Session | null>(null),
      [loading, setLoading] = useState(true),
      [busy, setBusy] = useState(0),
      [dirty, setDirty] = useState(false),
      [error, setError] = useState("");
    const [stage, setStage] = useState(0),
      [controls, setControls] = useState<LabControls>(DEFAULT_CONTROLS),
      [prediction, setPrediction] = useState(""),
      [reflection, setReflection] = useState(""),
      [drafts, setDrafts] = useState<Record<string, Draft>>({});
    const [validation, setValidation] = useState<Record<string, string>>({}),
      [focusBridge, setFocusBridge] = useState<BridgeId | null>(null),
      [returnQuestion, setReturnQuestion] = useState<string | null>(null);
    const alive = useRef(true),
      server = useRef<Session | null>(null),
      pending = useRef<Patch>({}),
      timer = useRef<ReturnType<typeof setTimeout> | null>(null),
      queue = useRef<Promise<unknown>>(Promise.resolve()),
      outstandingWrites = useRef(0),
      failure = useRef<Error | null>(null),
      lang = useRef(language),
      readEpoch = useRef(0),
      hydrated = useRef(false),
      latestDraft = useRef<Patch>({}),
      requestedBridges = useRef(new Set<BridgeId>());
    lang.current = language;
    function showSession(s: Session) {
      server.current = s;
      if (alive.current) {
        setSession(s);
        const ids = new Set(s.questions.map((q) => q.id));
        setDrafts((previous) =>
          Object.fromEntries(
            [...ids].map((id) => [id, previous[id] || s.drafts?.[id] || EMPTY]),
          ),
        );
      }
    }
    function hydrate(s: Session | null) {
      server.current = s;
      setSession(s);
      if (s) {
        latestDraft.current = {
          stage: s.stage,
          controls: s.controls,
          prediction: s.prediction,
          reflection: s.reflection,
          drafts: s.drafts || {},
        };
        requestedBridges.current = new Set(s.opened_bridges as BridgeId[]);
        setStage(s.stage);
        setControls(s.controls);
        setPrediction(s.prediction);
        setReflection(s.reflection);
        setDrafts(s.drafts || {});
      }
      hydrated.current = true;
    }
    function enqueue(
      path: string,
      body: Record<string, unknown>,
      method = "POST",
    ): Promise<Session> {
      outstandingWrites.current++;
      if (alive.current) setBusy((n) => n + 1);
      const task = queue.current
        .catch(() => {})
        .then(async () => {
          if (failure.current) throw failure.current;
          const s = await api<Session>(BASE + path, {
            method,
            body: JSON.stringify({
              ...body,
              ...(server.current ? { revision: server.current.revision } : {}),
            }),
            headers: { "Accept-Language": lang.current },
          });
          showSession(s);
          return s;
        })
        .catch((e) => {
          const problem = e instanceof Error ? e : new Error(String(e));
          failure.current = problem;
          if (alive.current) setError(problem.message);
          throw problem;
        })
        .finally(() => {
          outstandingWrites.current--;
          if (alive.current) setBusy((n) => n - 1);
        });
      queue.current = task.catch(() => {});
      return task;
    }
    function savePending(): Promise<void> {
      if (timer.current) {
        clearTimeout(timer.current);
        timer.current = null;
      }
      if (!Object.keys(pending.current).length) return Promise.resolve();
      const patch = pending.current;
      pending.current = {};
      return enqueue("/session", patch, "PATCH")
        .then(() => {
          if (alive.current) setDirty(Object.keys(pending.current).length > 0);
        })
        .catch((e) => {
          const latest = Object.fromEntries(
            Object.keys(patch).map((key) => [
              key,
              latestDraft.current[key as keyof Patch] ??
                patch[key as keyof Patch],
            ]),
          );
          pending.current = { ...patch, ...pending.current, ...latest };
          if (alive.current) setDirty(true);
          throw e;
        });
    }
    async function flush() {
      await savePending();
      await queue.current;
      if (failure.current) throw failure.current;
    }
    useImperativeHandle(ref, () => ({ flush }));
    function edit(patch: Patch) {
      latestDraft.current = { ...latestDraft.current, ...patch };
      pending.current = { ...pending.current, ...patch };
      setDirty(true);
      if (timer.current) clearTimeout(timer.current);
      timer.current = setTimeout(() => {
        void savePending().catch(() => {});
      }, 450);
    }
    useEffect(() => {
      alive.current = true;
      const protectUnsavedWork = (event: BeforeUnloadEvent) => {
        // Refs cover the debounce window and queued writes before React rerenders.
        // A browser warning does not imply the outstanding write was completed.
        if (
          Object.keys(pending.current).length ||
          outstandingWrites.current > 0 ||
          failure.current
        ) {
          event.preventDefault();
          event.returnValue = "";
        }
      };
      window.addEventListener("beforeunload", protectUnsavedWork);
      return () => {
        window.removeEventListener("beforeunload", protectUnsavedWork);
        alive.current = false;
        readEpoch.current++;
        if (timer.current) clearTimeout(timer.current);
      };
    }, []);
    useEffect(() => {
      const epoch = ++readEpoch.current,
        controller = new AbortController();
      setLoading(true);
      void (async () => {
        await queue.current.catch(() => {});
        const data = await api<{ session: Session | null }>(BASE, {
          signal: controller.signal,
          headers: { "Accept-Language": language },
        });
        if (!alive.current || epoch !== readEpoch.current) return;
        if (!hydrated.current) hydrate(data.session);
        else if (data.session) showSession(data.session);
      })()
        .catch((e) => {
          if (
            alive.current &&
            epoch === readEpoch.current &&
            !controller.signal.aborted
          )
            setError(e.message);
        })
        .finally(() => {
          if (alive.current && epoch === readEpoch.current) setLoading(false);
        });
      return () => controller.abort();
    }, [language]);
    async function run(action: () => Promise<unknown>) {
      try {
        await flush();
        await action();
      } catch {
        /* Error is retained next to the controls. */
      }
    }
    async function start() {
      failure.current = null;
      setError("");
      try {
        hydrate(await enqueue("/start", {}));
      } catch {
        /* visible error */
      }
    }
    async function retrySave() {
      try {
        const latest = await api<{ session: Session | null }>(BASE, {
          headers: { "Accept-Language": language },
        });
        if (latest.session?.revision !== server.current?.revision) {
          setError(
            language === "en"
              ? "The saved version changed in another window. Your unsaved inputs are still here. Choose ‘Use saved version’ to replace them, or copy them before leaving."
              : "另一窗口修改了已保存版本。你的未保存输入仍在这里；可先复制，或选择“使用已保存版本”替换它们。",
          );
          return;
        }
        failure.current = null;
        setError("");
        await flush();
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e));
      }
    }
    async function reloadSaved() {
      try {
        await queue.current.catch(() => {});
        const data = await api<{ session: Session | null }>(BASE);
        pending.current = {};
        failure.current = null;
        setError("");
        setDirty(false);
        hydrate(data.session);
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e));
      }
    }
    function navigate(next: number) {
      setStage(next);
      edit({ stage: next });
      document.getElementById("image-unit-stage-heading")?.focus();
    }
    function recordBridge(id: BridgeId) {
      if (
        server.current?.opened_bridges.includes(id) ||
        requestedBridges.current.has(id)
      )
        return;
      requestedBridges.current.add(id);
      void (async () => {
        try {
          await flush();
          await enqueue("/session", { bridge: id }, "PATCH");
        } catch {
          requestedBridges.current.delete(id);
        }
      })();
    }
    function openBridge(id: BridgeId, questionId?: string) {
      setReturnQuestion(questionId || null);
      setFocusBridge(id);
      if (stage !== 2) {
        setStage(2);
        edit({ stage: 2 });
      }
      recordBridge(id);
      setTimeout(
        () =>
          document
            .getElementById(`image-bridge-${id}`)
            ?.scrollIntoView({ behavior: "instant", block: "center" }),
        0,
      );
    }
    function returnToCheck() {
      navigate(3);
      setTimeout(() => {
        const target = document.getElementById(
          `image-question-${returnQuestion}`,
        );
        target?.scrollIntoView({ block: "center" });
        target?.focus();
      }, 0);
    }
    function updateDraft(id: string, value: Draft) {
      const next = { ...drafts, [id]: value };
      setDrafts(next);
      edit({ drafts: next });
    }
    function check(q: Question) {
      const draft = drafts[q.id] || EMPTY;
      if (!draft.number.trim() || !draft.choice) {
        setValidation((v) => ({ ...v, [q.id]: c.numberError }));
        return;
      }
      setValidation((v) => ({ ...v, [q.id]: "" }));
      void run(() =>
        enqueue("/check", {
          question_id: q.id,
          request_id: crypto.randomUUID(),
          number: draft.number.trim(),
          choice: draft.choice,
          working: draft.working,
        }),
      );
    }
    const locked = disabled || loading || busy > 0;
    return (
      <section className="image-unit" aria-busy={loading}>
        <header className="image-unit-hero">
          <div className="image-unit-eyebrow">
            <FlaskConical size={15} />
            {c.eyebrow}
          </div>
          <h1>{c.title}</h1>
          <p>{c.subtitle}</p>
          <div className="image-unit-status" role="status" aria-live="polite">
            {loading
              ? c.loading
              : error
                ? c.saveError
                : session
                  ? busy || dirty
                    ? c.saving
                    : c.save
                  : ""}
          </div>
        </header>
        {error && (
          <div className="image-unit-error" role="alert">
            <p>{error}</p>
            <button
              type="button"
              onClick={() => void retrySave()}
              disabled={busy > 0}
            >
              <RefreshCw size={14} />
              {c.retry}
            </button>
            <button
              type="button"
              onClick={() => void reloadSaved()}
              disabled={busy > 0}
            >
              {c.reload}
            </button>
          </div>
        )}
        {!loading && !session && (
          <div className="image-unit-card image-unit-entry">
            <div>
              <span className="image-unit-kicker">01 / 05</span>
              <h2>{c.predictionQuestion}</h2>
              <p>{c.intro}</p>
              <ul>
                {c.goals.map((goal) => (
                  <li key={goal}>{goal}</li>
                ))}
              </ul>
              <button
                className="image-unit-primary"
                type="button"
                onClick={() => void start()}
                disabled={locked}
              >
                {c.start}
                <ArrowRight size={17} />
              </button>
              <p className="image-unit-small">{c.limits}</p>
            </div>
            <div className="image-unit-entry-image">
              <ImageCanvas
                pixels={makeImage("scene")}
                row={48}
                label={c.clean}
                description={c.imageAlt}
                colour={colours[0]}
              />
            </div>
          </div>
        )}
        {session && (
          <>
            <nav className="image-unit-steps" aria-label={c.stage}>
              {c.stages.map((label, i) => (
                <button
                  type="button"
                  key={label}
                  className={stage === i ? "active" : ""}
                  aria-current={stage === i ? "step" : undefined}
                  onClick={() => navigate(i)}
                  disabled={disabled || loading}
                >
                  <span>{String(i + 1).padStart(2, "0")}</span>
                  {label}
                </button>
              ))}
            </nav>
            <div className="image-unit-card">
              <h2 id="image-unit-stage-heading" tabIndex={-1}>
                {
                  [
                    c.predictionQuestion,
                    c.labTitle,
                    c.theoryTitle,
                    c.checkTitle,
                    c.finishTitle,
                  ][stage]
                }
              </h2>
              {stage === 0 && (
                <>
                  <p>{c.intro}</p>
                  <ul className="image-unit-goals">
                    {c.goals.map((goal) => (
                      <li key={goal}>
                        <CheckCircle2 size={17} />
                        {goal}
                      </li>
                    ))}
                  </ul>
                  <label className="image-unit-field">
                    {c.predictionLabel}
                    <textarea
                      value={prediction}
                      maxLength={4000}
                      placeholder={c.predictionPlaceholder}
                      onChange={(e) => {
                        setPrediction(e.target.value);
                        edit({ prediction: e.target.value });
                      }}
                      disabled={disabled}
                    />
                  </label>
                  <p className="image-unit-small">{c.predictionNote}</p>
                  <aside className="image-unit-note">
                    <Lightbulb size={20} />
                    <p>{c.limits}</p>
                  </aside>
                </>
              )}
              {stage === 1 && (
                <>
                  <p>{c.labIntro}</p>
                  <fieldset
                    className="image-unit-lab-fieldset"
                    disabled={disabled}
                  >
                    <ImageLab
                      controls={controls}
                      language={language}
                      change={(value) => {
                        setControls(value);
                        edit({ controls: value });
                      }}
                    />
                  </fieldset>
                  <aside className="image-unit-note">
                    <Lightbulb size={20} />
                    <p>{c.labMeaning}</p>
                  </aside>
                  <h3>{c.observeTitle}</h3>
                  <ol className="image-unit-experiments">
                    {c.experiments.map((x) => (
                      <li key={x}>{x}</li>
                    ))}
                  </ol>
                  <button
                    type="button"
                    onClick={() => openBridge("pixels")}
                    disabled={locked}
                  >
                    {c.bridges[0].title}
                    <ArrowRight size={15} />
                  </button>
                </>
              )}
              {stage === 2 && (
                <>
                  {returnQuestion && (
                    <button type="button" onClick={returnToCheck}>
                      <ArrowLeft size={15} />
                      {language === "en"
                        ? "Return to the check you were working on"
                        : "回到刚才的练习"}
                    </button>
                  )}
                  <Md text={c.core} />
                  <FrequencyPlot language={language} />
                  <details className="image-unit-detail">
                    <summary>
                      {language === "en"
                        ? "From a row to the two-dimensional image"
                        : "从一行信号到二维图像"}
                    </summary>
                    <Md text={c.twoD} />
                  </details>
                  <h3>{c.bridgesTitle}</h3>
                  <p>{c.bridgesIntro}</p>
                  <div className="image-unit-bridges">
                    {c.bridges.map((bridge) => (
                      <details
                        key={bridge.id}
                        id={`image-bridge-${bridge.id}`}
                        open={focusBridge === bridge.id || undefined}
                        onToggle={(e) => {
                          if (
                            !e.currentTarget.open &&
                            focusBridge === bridge.id
                          )
                            setFocusBridge(null);
                          if (e.currentTarget.open) recordBridge(bridge.id);
                        }}
                      >
                        <summary>
                          <span>
                            <small>{bridge.relation}</small>
                            {bridge.title}
                          </span>
                          <ChevronDown size={18} />
                        </summary>
                        <div>
                          <p className="image-unit-small">{bridge.reason}</p>
                          <Md text={bridge.body} />
                          <aside className="image-unit-mini">
                            <strong>{c.miniCheck}</strong>
                            <p>{bridge.check}</p>
                            <details>
                              <summary>{c.showAnswer}</summary>
                              <p>{bridge.answer}</p>
                            </details>
                          </aside>
                        </div>
                      </details>
                    ))}
                  </div>
                </>
              )}
              {stage === 3 && (
                <>
                  <p>{c.checkIntro}</p>
                  <div className="image-unit-question-list">
                    {session.questions.map((q, index) => {
                      const draft = drafts[q.id] || EMPTY;
                      return (
                        <article
                          className="image-unit-question"
                          key={q.id}
                          id={`image-question-${q.id}`}
                          tabIndex={-1}
                        >
                          <div className="image-unit-question-label">
                            <span>{String(index + 1).padStart(2, "0")}</span>
                            <span>
                              {q.kind === "recovery"
                                ? language === "en"
                                  ? "Optional extension · recovery"
                                  : "可选拓展 · 恢复信息"
                                : q.result
                                  ? q.result.passed
                                    ? q.result.status === "independent"
                                      ? c.checked
                                      : c.supported
                                    : c.needsReview
                                  : c.notChecked}
                            </span>
                          </div>
                          <Md text={q.prompt} />
                          <form
                            onSubmit={(e) => {
                              e.preventDefault();
                              check(q);
                            }}
                          >
                            <label className="image-unit-field">
                              {q.number_label || c.number}
                              <input
                                type="text"
                                inputMode="text"
                                maxLength={80}
                                value={draft.number}
                                onChange={(e) =>
                                  updateDraft(q.id, {
                                    ...draft,
                                    number: e.target.value,
                                  })
                                }
                                disabled={
                                  disabled || loading || Boolean(q.result)
                                }
                                autoComplete="off"
                              />
                            </label>
                            <fieldset
                              className="image-unit-options"
                              disabled={
                                disabled || loading || Boolean(q.result)
                              }
                            >
                              <legend>{c.choose}</legend>
                              {q.choices.map((choice) => (
                                <label key={choice.id}>
                                  <input
                                    type="radio"
                                    name={`choice-${q.id}`}
                                    checked={draft.choice === choice.id}
                                    onChange={() =>
                                      updateDraft(q.id, {
                                        ...draft,
                                        choice: choice.id,
                                      })
                                    }
                                  />
                                  <span>{choice.label}</span>
                                </label>
                              ))}
                            </fieldset>
                            <details className="image-unit-working">
                              <summary>{c.working}</summary>
                              <textarea
                                value={draft.working}
                                maxLength={8000}
                                onChange={(e) =>
                                  updateDraft(q.id, {
                                    ...draft,
                                    working: e.target.value,
                                  })
                                }
                                disabled={
                                  disabled || loading || Boolean(q.result)
                                }
                                aria-label={c.working}
                              />
                            </details>
                            {validation[q.id] && (
                              <p role="alert" className="image-unit-error-text">
                                {validation[q.id]}
                              </p>
                            )}
                            <div className="image-unit-actions">
                              <button
                                className="image-unit-primary"
                                type="submit"
                                disabled={locked || Boolean(q.result)}
                              >
                                {c.submit}
                                <ArrowRight size={15} />
                              </button>
                              <button
                                type="button"
                                disabled={locked || Boolean(q.help.hint)}
                                onClick={() =>
                                  void run(() =>
                                    enqueue("/reveal", {
                                      question_id: q.id,
                                      kind: "hint",
                                    }),
                                  )
                                }
                              >
                                {c.hint}
                              </button>
                              <button
                                type="button"
                                disabled={locked || Boolean(q.help.solution)}
                                onClick={() =>
                                  void run(() =>
                                    enqueue("/reveal", {
                                      question_id: q.id,
                                      kind: "solution",
                                    }),
                                  )
                                }
                              >
                                {c.solution}
                              </button>
                            </div>
                          </form>
                          {q.result && (
                            <div
                              className={`image-unit-feedback ${q.result.passed ? "passed" : "review"}`}
                              role="status"
                            >
                              <strong>
                                {q.result.passed
                                  ? q.result.status === "independent"
                                    ? c.checked
                                    : c.supported
                                  : c.needsReview}
                              </strong>
                              <Md text={q.result.feedback} />
                              {q.result.suggested_bridge && (
                                <button
                                  type="button"
                                  disabled={locked}
                                  onClick={() =>
                                    openBridge(
                                      q.result!.suggested_bridge!,
                                      q.id,
                                    )
                                  }
                                >
                                  {c.recommend}{" "}
                                  {
                                    c.bridges.find(
                                      (b) =>
                                        b.id === q.result?.suggested_bridge,
                                    )?.title
                                  }
                                </button>
                              )}
                              <button
                                type="button"
                                disabled={locked || q.retry_available === false}
                                onClick={() =>
                                  void run(() =>
                                    enqueue("/retry", { question_id: q.id }),
                                  )
                                }
                              >
                                {c.fresh}
                              </button>
                              {q.retry_available === false && (
                                <p className="image-unit-small">{c.noFresh}</p>
                              )}
                            </div>
                          )}
                          {q.help.hint && (
                            <aside className="image-unit-help">
                              <strong>{c.hintTitle}</strong>
                              <Md text={q.help.hint} />
                            </aside>
                          )}
                          {q.help.solution && (
                            <aside className="image-unit-help">
                              <strong>{c.solutionTitle}</strong>
                              <Md text={q.help.solution} />
                            </aside>
                          )}
                        </article>
                      );
                    })}
                  </div>
                  <p className="image-unit-small">{c.assessmentLimit}</p>
                </>
              )}
              {stage === 4 && (
                <>
                  <p>{c.finishIntro}</p>
                  <div className="image-unit-lenses">
                    {c.lenses.map((lens) => (
                      <article key={lens.title}>
                        <h3>{lens.title}</h3>
                        <p>{lens.body}</p>
                      </article>
                    ))}
                  </div>
                  <p className="image-unit-small">{c.crossCourse}</p>
                  <div className="image-unit-recap">
                    <h3>{c.recap}</h3>
                    <span>
                      {c.independent}:{" "}
                      <strong>
                        {
                          session.questions.filter(
                            (q) =>
                              q.result?.passed &&
                              q.result.status === "independent",
                          ).length
                        }
                      </strong>
                    </span>
                    <span>
                      {c.supported}:{" "}
                      <strong>
                        {
                          session.questions.filter(
                            (q) =>
                              q.result?.passed &&
                              q.result.status !== "independent",
                          ).length
                        }
                      </strong>
                    </span>
                    <span>
                      {c.open}:{" "}
                      <strong>
                        {
                          session.questions.filter((q) => !q.result?.passed)
                            .length
                        }
                      </strong>
                    </span>
                    <p>{c.assessmentLimit}</p>
                  </div>
                  {prediction && (
                    <blockquote>
                      <strong>{c.predictionLabel}</strong>
                      <p>{prediction}</p>
                    </blockquote>
                  )}
                  <label className="image-unit-field">
                    {c.reflection}
                    <textarea
                      value={reflection}
                      maxLength={4000}
                      placeholder={c.reflectionPlaceholder}
                      onChange={(e) => {
                        setReflection(e.target.value);
                        edit({ reflection: e.target.value });
                      }}
                      disabled={disabled}
                    />
                  </label>
                  <p className="image-unit-small">{c.reflectionNote}</p>
                  <button
                    type="button"
                    className="image-unit-primary"
                    disabled={locked}
                    onClick={() => void run(async () => onCoursePractice())}
                  >
                    {c.coursePractice}
                    <ArrowRight size={16} />
                  </button>
                  <p className="image-unit-small">{c.courseNote}</p>
                </>
              )}
            </div>
            <footer className="image-unit-footer">
              <button
                type="button"
                onClick={() => navigate(stage - 1)}
                disabled={stage === 0 || disabled || loading}
              >
                <ArrowLeft size={15} />
                {c.back}
              </button>
              <span>{stage + 1} / 5</span>
              <button
                type="button"
                onClick={() => navigate(stage + 1)}
                disabled={stage === 4 || disabled || loading}
              >
                {c.next}
                <ArrowRight size={15} />
              </button>
            </footer>
            <p className="image-unit-provenance">
              {c.source} {session.content_version}
            </p>
          </>
        )}
      </section>
    );
  },
);
export default ImageLearning;
