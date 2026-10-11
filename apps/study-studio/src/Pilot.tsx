import { useEffect, useState } from "react";
import Md from "./PilotMarkdown";
import GuidedLearning, { GuidedHistory } from "./GuidedLearning";
import {
  BookOpen,
  Camera,
  Check,
  ChevronRight,
  FileText,
  Leaf,
  LoaderCircle,
  LogOut,
  Search,
  Settings,
  ShieldCheck,
} from "lucide-react";
import { api, post } from "./api";
import "./pilot.css";

type User = { id: string; name: string; role: string };
type Status = {
  setup_required: boolean;
  course_ready: boolean;
  model_available: boolean;
  user: User | null;
  database: string;
};
type Block = { id: string; role: string; title?: string; body: string | null };
type Lesson = {
  id: string;
  title: string;
  week: number;
  blocks: Block[];
  version: string;
};
type Topic = {
  title: string;
  week: number;
  objective: string;
  routes: string[];
};
type Course = {
  id: string;
  title: string;
  lessons: Lesson[];
  topics: Record<string, Topic>;
  asset_count: number;
  warnings: string[];
  legacy_records: { id: string; title: string; body: string; note: string }[];
};
type Task = {
  id: string;
  topic: string;
  phase: string;
  title: string;
  prompt: string;
  fields: { id: string; label: string }[];
  source_note: string;
};
type Result = {
  status: string;
  checks: Record<string, boolean>;
  route: string;
  feedback: string;
  teaching: string;
  scope: string;
  passed: boolean;
};
type Attempt = {
  id: string;
  task_id: string;
  topic: string;
  at: string;
  working: string;
  answers: Record<string, string>;
  photo_id?: string;
  result: Result;
  active: boolean;
  review_due: string;
  withdrawal_reason?: string;
};
type Transcript = {
  working: string;
  fields: { id: string; value: string }[];
  uncertainties: string[];
};
type Photo = {
  at: string;
  id: string;
  task_id: string;
  transcription: Transcript | null;
};
type State = {
  tasks: Task[];
  attempts: Attempt[];
  summaries: Record<
    string,
    {
      attempts: number;
      independent: number;
      status: string;
      due_at?: string;
      route: string;
    }
  >;
  progress: { id: string; notes: string; at: string }[];
  photos: Photo[];
  runs: { id: string; operation: string; status: string; at: string }[];
  feedback: {
    id: string;
    attempt_id: string;
    value: { feedback: string; uncertainties: string[] };
  }[];
};
type Source = {
  id: string;
  name: string;
  suffix: string;
  role: string;
  locations: string[];
  bytes: number;
};
const p = "/pilot";
const newId = () => crypto.randomUUID();
const routeNames: Record<string, string> = {
  bridge: "补一点基础",
  visual: "图形与直觉",
  algebra: "代数与推导",
};
const statusNames: Record<string, string> = {
  unknown: "尚未检查",
  needs_review: "需要再核对",
  independent: "新题独立数值检查通过",
  supported: "在帮助后检查通过",
  diagnostic_match: "诊断数值符合判据",
};
const fmt = (s: string) =>
  new Date(s).toLocaleString("zh-CN", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

export default function Pilot() {
  const [status, setStatus] = useState<Status | null>(null),
    [course, setCourse] = useState<Course | null>(null),
    [state, setState] = useState<State | null>(null);
  const [view, setView] = useState("learn"),
    [topic, setTopic] = useState("ramps"),
    [lesson, setLesson] = useState<Lesson | null>(null),
    [route, setRoute] = useState("visual"),
    [help, setHelp] = useState<{ body: string; example: string } | null>(null);
  const [task, setTask] = useState<Task | null>(null),
    [answers, setAnswers] = useState<Record<string, string>>({}),
    [working, setWorking] = useState(""),
    [photo, setPhoto] = useState<Photo | null>(null),
    [confirmed, setConfirmed] = useState(false),
    [priorSeen, setPriorSeen] = useState(false),
    [attempt, setAttempt] = useState<Attempt | null>(null),
    [support, setSupport] = useState("");
  const [busy, setBusy] = useState(""),
    [error, setError] = useState(""),
    [notice, setNotice] = useState(""),
    [query, setQuery] = useState(""),
    [matches, setMatches] = useState<
      { lesson_id: string; title: string; excerpt: string }[]
    >([]),
    [sources, setSources] = useState<Source[]>([]),
    [notes, setNotes] = useState(""),
    [invite, setInvite] = useState("");
  const [name, setName] = useState(""),
    [password, setPassword] = useState(""),
    [register, setRegister] = useState(false),
    [inviteCode, setInviteCode] = useState("");
  const [confirmDelete, setConfirmDelete] = useState(false),
    [withdrawId, setWithdrawId] = useState(""),
    [withdrawReason, setWithdrawReason] = useState("");
  async function run(label: string, fn: () => Promise<unknown>) {
    setBusy(label);
    setError("");
    setNotice("");
    try {
      await fn();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy("");
    }
  }
  async function refresh() {
    const s = await api<State>(p + "/state");
    setState(s);
    return s;
  }
  async function loadLesson(id: string, s?: State) {
    const l = await api<Lesson>(p + "/lessons/" + id);
    setLesson(l);
    if (lesson?.id !== id) {
      const saved = s || state;
      setNotes(saved?.progress.find((x) => x.id === id)?.notes || "");
      if (l.week <= 3) {
        const key = ["ramps", "convolution", "fourier"][l.week - 1];
        setTopic(key);
        setRoute(saved?.summaries[key]?.route || "visual");
        const currentTask = [...(saved?.tasks || [])]
          .reverse()
          .find((t) => t.topic === key);
        if (currentTask && saved) useTask(currentTask, saved);
        else {
          setTask(null);
          setAttempt(null);
          setAnswers({});
          setWorking("");
          setPhoto(null);
        }
      }
    }
  }
  function useTask(t: Task, s: State) {
    setTask(t);
    const a = [...s.attempts]
      .reverse()
      .find((a) => a.task_id === t.id && a.active);
    setAttempt(a || null);
    const restoredPhoto =
      s.photos.find((p) => p.id === a?.photo_id) ||
      [...s.photos]
        .filter((p) => p.task_id === t.id)
        .sort((a, b) => b.at.localeCompare(a.at))[0] ||
      null;
    setAnswers(
      a?.answers ||
        Object.fromEntries(
          (restoredPhoto?.transcription?.fields || []).map((f) => [
            f.id,
            f.value,
          ]),
        ),
    );
    setWorking(a?.working || restoredPhoto?.transcription?.working || "");
    setPhoto(restoredPhoto);
    setSupport("");
    setConfirmed(false);
    setPriorSeen(false);
  }
  async function boot() {
    const st = await api<Status>(p + "/status");
    setStatus(st);
    if (st.user && st.course_ready) {
      const [c, s] = await Promise.all([
        api<Course>(p + "/course"),
        api<State>(p + "/state"),
      ]);
      setCourse(c);
      setState(s);
      const requested = new URLSearchParams(location.search).get("lesson");
      const latest = [...s.progress].sort((a, b) =>
        b.at.localeCompare(a.at),
      )[0];
      const lastTask = s.tasks[s.tasks.length - 1];
      const taskLesson = lastTask
        ? c.lessons.find((l) => l.week === c.topics[lastTask.topic].week)
        : undefined;
      await loadLesson(
        requested || latest?.id || taskLesson?.id || c.lessons[0].id,
        s,
      );
    }
  }
  useEffect(() => {
    void run("正在载入课程", boot);
  }, []);
  useEffect(() => {
    if (lesson && location.hash) {
      const el = document.getElementById(
        decodeURIComponent(location.hash.slice(1)),
      );
      el?.scrollIntoView({ block: "start" });
    }
  }, [lesson?.id]);
  useEffect(() => {
    if (status?.user)
      api<{ body: string; example: string }>(
        p + "/teaching/" + topic + "?route=" + route,
      )
        .then(setHelp)
        .catch((e) => setError(e.message));
  }, [topic, route, status?.user?.id]);
  async function selectTopic(key: string) {
    setTopic(key);
    setRoute(state?.summaries[key].route || "visual");
    const l = course?.lessons.find((l) => l.week === course.topics[key].week);
    if (l) await loadLesson(l.id);
    const t = [...(state?.tasks || [])].reverse().find((t) => t.topic === key);
    if (t && state) useTask(t, state);
    else {
      setTask(null);
      setAttempt(null);
      setWorking("");
      setAnswers({});
      setPhoto(null);
      setSupport("");
    }
  }
  async function begin(phase: string) {
    const t = await post<Task>(p + "/tasks", {
      topic,
      phase,
      request_id: newId(),
    });
    const s = await refresh();
    useTask(t, s);
  }
  async function login() {
    const st = await post<User>(
      p +
        "/auth/" +
        (status?.setup_required || register ? "register" : "login"),
      { name, password, invite: inviteCode },
    );
    setPassword("");
    setStatus((s) => (s ? { ...s, user: st } : s));
    await boot();
  }
  async function submit() {
    if (!task) return;
    const a = await post<Attempt>(p + "/attempts", {
      task_id: task.id,
      request_id: newId(),
      answers,
      working,
      photo_id: photo?.id || null,
      confirmed,
      prior_seen: priorSeen,
    });
    setAttempt(a);
    setRoute(a.result.route);
    await refresh();
  }
  async function upload(file: File) {
    if (!task) return;
    const form = new FormData();
    form.append("file", file);
    const pht = await api<Photo>(p + "/photos/" + task.id, {
      method: "POST",
      body: form,
    });
    setPhoto(pht);
    setConfirmed(false);
    setNotice("照片已保存。识别或手动录入后，请确认关键公式与数值。");
    await refresh();
  }
  async function transcribe() {
    if (!photo) return;
    const t = await post<Transcript>(
      p + "/photos/" + photo.id + "/transcribe",
      { request_id: newId() },
    );
    setPhoto({ ...photo, transcription: t });
    setWorking(t.working);
    setAnswers(Object.fromEntries(t.fields.map((f) => [f.id, f.value])));
    setConfirmed(false);
    await refresh();
  }
  if (!status)
    return (
      <div className="pilot-loading">
        <LoaderCircle className="spin" /> 正在连接学习空间…
        {error && <p role="alert">{error}</p>}
      </div>
    );
  if (!status.user)
    return (
      <div className="pilot-auth">
        <div className="pilot-auth-card">
          <div className="pilot-wordmark">
            <Leaf /> STUDY VAULT
          </div>
          <span className="pilot-eyebrow">ELEC270 · 信号与系统</span>
          <h1>
            让每一步学习，
            <br />
            都有据可循。
          </h1>
          <p>
            课程讲义、纸笔作答与个人学习记录，连接成一个可以继续的学习过程。
          </p>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              void run("正在进入", login);
            }}
          >
            <h2>
              {status.setup_required
                ? "创建本机学习账号"
                : register
                  ? "使用邀请加入"
                  : "继续学习"}
            </h2>
            <label>
              用户名
              <input
                autoComplete="username"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </label>
            <label>
              密码（至少 10 位）
              <input
                type="password"
                autoComplete={
                  register || status.setup_required
                    ? "new-password"
                    : "current-password"
                }
                minLength={10}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            {register && !status.setup_required && (
              <label>
                邀请码
                <input
                  value={inviteCode}
                  onChange={(e) => setInviteCode(e.target.value)}
                />
              </label>
            )}
            <button className="pilot-primary" disabled={!!busy}>
              {busy || "进入 ELEC270"} <ChevronRight size={16} />
            </button>
            {!status.setup_required && (
              <button
                type="button"
                className="pilot-link"
                onClick={() => setRegister(!register)}
              >
                {register ? "已有账号，登录" : "使用邀请码创建账号"}
              </button>
            )}
            {error && (
              <p className="pilot-error" role="alert">
                {error}
              </p>
            )}
          </form>
          <small>
            目前运行在这台电脑上。资料原件不会被修改；只有主动识别或请求 AI
            反馈时，相关图片或片段才会发往模型服务。
          </small>
        </div>
      </div>
    );
  const currentTopic = course?.topics[topic];
  const disabled = !!busy;
  const supportedLesson = !!lesson && lesson.week <= 3;
  return (
    <div className="pilot-shell">
      <aside className="pilot-sidebar">
        <div className="pilot-wordmark">
          <Leaf /> STUDY VAULT
        </div>
        <div className="pilot-course-name">
          ELEC270<small>信号与系统 · 2026–27</small>
        </div>
        <nav>
          {[
            ["learn", "学习与练习", BookOpen],
            ["records", "我的学习记录", ShieldCheck],
            ["sources", "课程资料", FileText],
            ["settings", "设置与导出", Settings],
          ].map(([id, label, Icon]) => (
            <button
              key={String(id)}
              className={view === id ? "active" : ""}
              onClick={() => {
                setView(String(id));
                if (id === "sources")
                  void run("读取来源", async () =>
                    setSources(await api<Source[]>(p + "/sources")),
                  );
              }}
            >
              {typeof Icon !== "string" && <Icon size={17} />} {String(label)}
            </button>
          ))}
        </nav>
        <div className="pilot-nav-label">
          课程目录 · {course?.lessons.length || 0} 单元
        </div>
        <div className="pilot-lessons">
          {course?.lessons.map((l) => (
            <button
              key={l.id}
              className={lesson?.id === l.id ? "active" : ""}
              onClick={() =>
                void run("读取讲义", async () => {
                  setView("learn");
                  await loadLesson(l.id);
                  if (l.week <= 3)
                    await selectTopic(
                      ["ramps", "convolution", "fourier"][l.week - 1],
                    );
                })
              }
            >
              <span>{String(l.week).padStart(2, "0")}</span>
              {l.title.replace(/^Week\s*\d+\s*[-｜]?\s*/, "")}
            </button>
          ))}
        </div>
        <div className="pilot-user">
          <span>{status.user.name}</span>
          <button
            aria-label="退出登录"
            onClick={() =>
              void run("退出", async () => {
                await post(p + "/auth/logout");
                setState(null);
                setCourse(null);
                setTask(null);
                setPhoto(null);
                setWorking("");
                await boot();
              })
            }
          >
            <LogOut size={16} />
          </button>
        </div>
      </aside>
      <main className="pilot-main">
        <header className="pilot-top">
          <span>
            我的课程 <ChevronRight size={14} /> ELEC270
          </span>
          <span className="pilot-badge">
            {status.model_available ? "AI 已配置" : "离线教学可用 · AI 待配置"}
          </span>
        </header>
        {error && (
          <div role="alert" className="pilot-error pilot-alert">
            {error}
            <button aria-label="关闭错误" onClick={() => setError("")}>
              ×
            </button>
          </div>
        )}
        {notice && (
          <div role="status" className="pilot-notice">
            {notice}
          </div>
        )}
        {busy && (
          <div className="pilot-running" role="status">
            <LoaderCircle size={14} className="spin" /> {busy}…
          </div>
        )}
        {!course ? (
          <section className="pilot-page">
            <h1>等待导入 ELEC270</h1>
            <p>课程导入完成后刷新即可开始。</p>
          </section>
        ) : view === "learn" ? (
          <>
            <section className="pilot-heading">
              <div>
                <span className="pilot-eyebrow">从理解，到独立完成</span>
                <h1>今天，把一个难点弄清楚。</h1>
                <p>先检查起点，选择讲法，再用自己的解题过程验证。</p>
              </div>
              <div className="pilot-topic-tabs">
                {Object.entries(course.topics).map(([key, t]) => (
                  <button
                    disabled={disabled}
                    className={topic === key ? "active" : ""}
                    key={key}
                    onClick={() => void run("切换主题", () => selectTopic(key))}
                  >
                    {t.title}
                    <small>
                      {statusNames[state?.summaries[key]?.status || "unknown"]}
                    </small>
                  </button>
                ))}
              </div>
            </section>
            <div className="pilot-learning">
              <article className="pilot-reading">
                <div className="pilot-section-label">01 / 理解与教学</div>
                <h2>{supportedLesson ? currentTopic?.title : lesson?.title}</h2>
                <p>
                  {supportedLesson
                    ? currentTopic?.objective
                    : "当前单元提供原知识库正文与来源查阅。自动诊断与反馈先覆盖上方三个试点主题。"}
                </p>
                {topic === "ramps" && supportedLesson && (
                  <GuidedLearning
                    disabled={disabled}
                    onPractice={() =>
                      run("准备新题", async () => {
                        await begin("practice");
                        document
                          .getElementById("pilot-practice")
                          ?.scrollIntoView({ block: "start" });
                      })
                    }
                  />
                )}
                <div
                  className="pilot-routes"
                  hidden={!supportedLesson || topic === "ramps"}
                  aria-label="选择教学路径"
                >
                  {Object.entries(routeNames).map(([k, n]) => (
                    <button
                      key={k}
                      disabled={disabled}
                      className={route === k ? "active" : ""}
                      onClick={() =>
                        void run("保存教学选择", async () => {
                          setRoute(k);
                          setHelp(
                            await post(p + "/route", { topic, route: k }),
                          );
                          await refresh();
                        })
                      }
                    >
                      {n}
                    </button>
                  ))}
                </div>
                {help && supportedLesson && topic !== "ramps" && (
                  <div className="pilot-teaching">
                    <Md text={help.body} />
                    <details>
                      <summary>看一个不同参数的示范</summary>
                      <Md text={help.example} />
                    </details>
                  </div>
                )}
                <details className="pilot-full-lesson" open>
                  <summary>
                    <BookOpen size={18} /> 原知识库讲义 · {lesson?.title}
                  </summary>
                  <p className="pilot-muted">
                    正文保留原课程结构。提示和解答需单独展开；展开会记入学习记录。
                  </p>
                  {lesson?.blocks.map((b) => (
                    <div id={b.id} key={b.id}>
                      {b.body !== null ? (
                        <>
                          <b>{b.role !== "lesson" ? b.title : ""}</b>
                          <Md text={b.body} />
                        </>
                      ) : (
                        <button
                          className="pilot-reveal"
                          disabled={disabled}
                          onClick={() =>
                            void run("打开内容", async () => {
                              await post(p + "/reveal", {
                                lesson_id: lesson.id,
                                block_id: b.id,
                              });
                              await loadLesson(lesson.id);
                              await refresh();
                            })
                          }
                        >
                          {b.role === "hint" ? "查看提示" : "查看完整解答"} ·{" "}
                          {b.title}
                        </button>
                      )}
                    </div>
                  ))}
                </details>
                <div className="pilot-notes">
                  <label htmlFor="personal-notes">这一节，我自己的理解</label>
                  <textarea
                    id="personal-notes"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="用自己的话记录；阅读与笔记不会自动计为掌握。"
                  />
                  <button
                    disabled={disabled || !lesson}
                    onClick={() =>
                      void run("保存笔记", async () => {
                        await api(p + "/progress", {
                          method: "PATCH",
                          body: JSON.stringify({
                            lesson_id: lesson!.id,
                            notes,
                          }),
                        });
                        await refresh();
                        setNotice("笔记和当前单元已保存。");
                      })
                    }
                  >
                    保存并记住当前位置
                  </button>
                </div>
              </article>
              <aside id="pilot-practice" className="pilot-practice">
                <div className="pilot-section-label">02 / 留下自己的证据</div>
                <h2>
                  {!supportedLesson
                    ? "这个单元可以阅读全文"
                    : task
                      ? "当前练习"
                      : "先检查起点"}
                </h2>
                {!supportedLesson && (
                  <p className="pilot-caution">
                    本单元的自动练习尚未接入。选择上方三个试点主题可进入诊断与反馈流程。
                  </p>
                )}
                <p className="pilot-muted">
                  可以跳过前测直接学习。诊断只用于当前目标，不给你贴固定的学习类型标签。
                </p>
                <div className="pilot-actions">
                  <button
                    disabled={disabled || !supportedLesson}
                    onClick={() =>
                      void run("准备诊断", () => begin("diagnosis"))
                    }
                  >
                    做前置诊断
                  </button>
                  <button
                    disabled={disabled || !supportedLesson}
                    onClick={() =>
                      void run("准备新题", () => begin("practice"))
                    }
                  >
                    尝试新题
                  </button>
                  <button
                    disabled={disabled || !supportedLesson}
                    onClick={() => void run("准备复查", () => begin("review"))}
                  >
                    复查一题
                  </button>
                </div>
                {task && supportedLesson && (
                  <div className="pilot-task" key={task.id}>
                    <h3>{task.title}</h3>
                    <Md text={task.prompt} />
                    <small>{task.source_note}</small>
                    <div className="pilot-input-tabs">
                      <label className="pilot-photo-button">
                        <Camera size={17} /> 拍照 / 上传
                        <input
                          disabled={disabled}
                          type="file"
                          accept="image/jpeg,image/png,image/webp"
                          capture="environment"
                          onChange={(e) => {
                            const f = e.target.files?.[0];
                            if (f) void run("保存照片", () => upload(f));
                            e.target.value = "";
                          }}
                        />
                      </label>
                      <span>也可以直接输入</span>
                    </div>
                    {photo && (
                      <div className="pilot-photo">
                        <img
                          src={"/api/pilot/photos/" + photo.id}
                          alt="本题的纸笔解答"
                        />
                        <button
                          disabled={disabled || !status.model_available}
                          onClick={() =>
                            void run("识别照片（最多一次模型调用）", transcribe)
                          }
                        >
                          识别照片中的过程
                        </button>
                        {!status.model_available && (
                          <p>AI 尚未配置。可对照照片手动填写下方内容。</p>
                        )}
                        {photo.transcription?.uncertainties.map((s, i) => (
                          <p className="pilot-caution" key={i}>
                            需要核对：{s}
                          </p>
                        ))}
                      </div>
                    )}
                    <label className="pilot-field">
                      我的解题过程
                      <textarea
                        value={working}
                        onChange={(e) => {
                          setWorking(e.target.value);
                          setConfirmed(false);
                        }}
                        placeholder="写下关键等式、区间或推理。照片转写后可在这里更正。"
                        rows={5}
                      />
                    </label>
                    <div className="pilot-numbers">
                      {task.fields.map((f) => (
                        <label key={f.id}>
                          {f.label}
                          <input
                            value={answers[f.id] || ""}
                            onChange={(e) => {
                              setAnswers({
                                ...answers,
                                [f.id]: e.target.value,
                              });
                              setConfirmed(false);
                            }}
                            placeholder="数值或简单算式"
                          />
                          {attempt && (
                            <small
                              className={
                                attempt.result.checks[f.id] ? "ok" : "check"
                              }
                            >
                              {attempt.result.checks[f.id]
                                ? "上次：符合判据"
                                : "上次：需要核对"}
                            </small>
                          )}
                        </label>
                      ))}
                    </div>
                    <label className="pilot-checkbox">
                      <input
                        type="checkbox"
                        checked={confirmed}
                        onChange={(e) => setConfirmed(e.target.checked)}
                      />
                      我已核对文字、负号、上下限和关键数值
                    </label>
                    <label className="pilot-checkbox">
                      <input
                        type="checkbox"
                        checked={priorSeen}
                        onChange={(e) => setPriorSeen(e.target.checked)}
                      />
                      我以前见过这道题的解答 / 使用了外部帮助
                    </label>
                    <button
                      className="pilot-primary"
                      disabled={disabled || !confirmed || !working.trim()}
                      onClick={() => void run("检查并保存作答", submit)}
                    >
                      确认并获取反馈 <Check size={17} />
                    </button>
                    <div className="pilot-actions">
                      <button
                        disabled={disabled}
                        onClick={() =>
                          void run("显示提示", async () => {
                            setSupport(
                              (
                                await post<{ body: string }>(p + "/reveal", {
                                  task_id: task.id,
                                  kind: "hint",
                                })
                              ).body,
                            );
                            await refresh();
                          })
                        }
                      >
                        需要一点提示
                      </button>
                      <button
                        disabled={disabled}
                        onClick={() =>
                          void run("显示解答", async () => {
                            setSupport(
                              (
                                await post<{ body: string }>(p + "/reveal", {
                                  task_id: task.id,
                                  kind: "solution",
                                })
                              ).body,
                            );
                            await refresh();
                          })
                        }
                      >
                        查看解答
                      </button>
                    </div>
                    {support && (
                      <div className="pilot-support">
                        <Md text={support} />
                      </div>
                    )}
                    {attempt && (
                      <section className="pilot-feedback">
                        <div className="pilot-section-label">
                          03 / 反馈与下一步
                        </div>
                        <h3>{statusNames[attempt.result.status]}</h3>
                        <p>{attempt.result.feedback}</p>
                        <Md text={attempt.result.teaching} />
                        <small>{attempt.result.scope}</small>
                        <button
                          disabled={disabled || !status.model_available}
                          onClick={() =>
                            void run("分析解题过程", async () => {
                              await post(
                                p + "/attempts/" + attempt.id + "/feedback",
                                { request_id: newId() },
                              );
                              await refresh();
                            })
                          }
                        >
                          让 AI 检查我的解题过程
                        </button>
                        {!status.model_available && (
                          <small>
                            AI 过程反馈待配置；上面的数值检查已实际完成。
                          </small>
                        )}
                        {state?.feedback
                          .filter((f) => f.attempt_id === attempt.id)
                          .map((f) => (
                            <div key={f.id} className="pilot-ai-feedback">
                              <b>AI 建议 · 可核对</b>
                              <Md text={f.value.feedback} />
                              {f.value.uncertainties.map((x, i) => (
                                <p key={i}>{x}</p>
                              ))}
                            </div>
                          ))}
                        <p className="pilot-muted">
                          建议 {fmt(attempt.review_due)}{" "}
                          后用新参数复查；完成复查前，延迟保持情况仍未知。
                        </p>
                        <button
                          disabled={disabled}
                          className="pilot-primary"
                          onClick={() =>
                            void run("准备新题", () => begin("practice"))
                          }
                        >
                          用另一道题检查理解 <ChevronRight size={16} />
                        </button>
                      </section>
                    )}
                  </div>
                )}
              </aside>
            </div>
          </>
        ) : view === "records" ? (
          <section className="pilot-page">
            <span className="pilot-eyebrow">每个判断，都能回到一次作答</span>
            <h1>我的学习记录</h1>
            <GuidedHistory />
            <div className="pilot-stat-grid">
              {Object.entries(course.topics).map(([k, t]) => (
                <div key={k}>
                  <h3>{t.title}</h3>
                  <p>{statusNames[state?.summaries[k].status || "unknown"]}</p>
                  <small>
                    {state?.summaries[k].attempts || 0} 次有效作答 ·{" "}
                    {state?.summaries[k].independent || 0} 次新题独立数值检查
                  </small>
                </div>
              ))}
            </div>
            {!state?.attempts.length && (
              <p>
                尚无诊断或练习作答。分步教学小检查单独显示在上方；原库笔记不会替代作答证据。
              </p>
            )}
            {[...(state?.attempts || [])].reverse().map((a) => (
              <div
                key={a.id}
                className={"pilot-record " + (!a.active ? "withdrawn" : "")}
              >
                <small>
                  {fmt(a.at)} · {course.topics[a.topic].title}
                </small>
                <h3>
                  {statusNames[a.result.status]}
                  {!a.active ? "（已撤回）" : ""}
                </h3>
                <Md text={a.working} />
                <p>{a.result.feedback}</p>
                {a.photo_id && (
                  <a
                    href={"/api/pilot/photos/" + a.photo_id}
                    target="_blank"
                    rel="noreferrer"
                  >
                    查看原作答照片
                  </a>
                )}
                <div className="pilot-actions">
                  <button
                    onClick={() =>
                      void run("打开这次作答", async () => {
                        const t = state?.tasks.find((t) => t.id === a.task_id);
                        if (t && state) {
                          await selectTopic(a.topic);
                          useTask(t, state);
                          setView("learn");
                        }
                      })
                    }
                  >
                    回到这道题
                  </button>
                  {a.active && (
                    <button
                      onClick={() => {
                        setWithdrawId(a.id);
                        setWithdrawReason("");
                      }}
                    >
                      更正 / 撤回记录
                    </button>
                  )}
                </div>
                {withdrawId === a.id && (
                  <div>
                    <label>
                      更正原因
                      <input
                        value={withdrawReason}
                        onChange={(e) => setWithdrawReason(e.target.value)}
                      />
                    </label>
                    <button
                      disabled={disabled || !withdrawReason.trim()}
                      onClick={() =>
                        void run("撤回作答", async () => {
                          await post(p + "/attempts/" + a.id + "/withdraw", {
                            reason: withdrawReason,
                          });
                          setWithdrawId("");
                          await refresh();
                        })
                      }
                    >
                      撤回这条判断，保留历史
                    </button>
                  </div>
                )}
                {a.withdrawal_reason && <p>原因：{a.withdrawal_reason}</p>}
              </div>
            ))}
            {course.legacy_records.map((r) => (
              <details key={r.id}>
                <summary>原 Obsidian 记录 · {r.title}</summary>
                <p>{r.note}</p>
                <Md text={r.body} />
              </details>
            ))}
          </section>
        ) : view === "sources" ? (
          <section className="pilot-page">
            <h1>课程资料与检索</h1>
            <p>
              {course.lessons.length} 个单元 · {course.asset_count}{" "}
              份去重附件。原件保留，课程使用版本快照。
            </p>
            <form
              className="pilot-search"
              onSubmit={(e) => {
                e.preventDefault();
                void run("检索正文", async () =>
                  setMatches(await post(p + "/search", { query })),
                );
              }}
            >
              <input
                aria-label="检索课程"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="搜索概念、英文术语或题号…"
              />
              <button disabled={disabled || !query.trim()}>
                <Search size={18} /> 检索
              </button>
            </form>
            <small>
              当前按关键词检索正文，不搜索隐藏解答；支持中英文原词，语义检索尚未启用。
            </small>
            {matches.map((m, i) => (
              <button
                className="pilot-search-result"
                key={i}
                onClick={() =>
                  void run("打开讲义", async () => {
                    await loadLesson(m.lesson_id);
                    setView("learn");
                  })
                }
              >
                <b>{m.title}</b>
                <span>{m.excerpt}</span>
              </button>
            ))}
            <h2>原始课件与习题</h2>
            <p className="pilot-muted">
              打开原始习题 /
              试卷可能看到答案，会记录资料访问。历史卷保持原有身份。
            </p>
            {sources.map((s) => (
              <div className="pilot-source" key={s.id}>
                <a
                  href={"/api/pilot/assets/" + s.id}
                  target="_blank"
                  rel="noreferrer"
                >
                  {s.name}
                </a>
                <small>
                  {s.role === "historical" ? "历史资料" : "课程资料"} ·{" "}
                  {s.locations.length} 个来源位置 · {Math.round(s.bytes / 1024)}{" "}
                  KB
                </small>
              </div>
            ))}
            {!!course.warnings.length && (
              <details>
                <summary>{course.warnings.length} 项导入待核对</summary>
                {course.warnings.map((w, i) => (
                  <p key={i}>{w}</p>
                ))}
              </details>
            )}
          </section>
        ) : (
          <section className="pilot-page">
            <h1>设置与个人资料</h1>
            <button
              onClick={() =>
                void run("退出", async () => {
                  await post(p + "/auth/logout");
                  setState(null);
                  setCourse(null);
                  setTask(null);
                  setPhoto(null);
                  setWorking("");
                  await boot();
                })
              }
            >
              退出当前账号
            </button>
            <div className="pilot-settings-card">
              <h2>学习数据</h2>
              {status.user.role === "owner" && (
                <p>
                  <a href="/?prototype=1">查看旧版 Study Studio 与原会话记录</a>
                  （独立保存，不自动计入本版能力判断）
                </p>
              )}{" "}
              {status.user.role === "owner" && (
                <p>
                  <button
                    disabled={disabled}
                    onClick={() =>
                      void run("归档旧记录", async () => {
                        const r = await post<{ count: number }>(
                          p + "/legacy/import",
                        );
                        setNotice(
                          "已归档 " +
                            r.count +
                            " 个旧会话，可随个人记录导出；未据此推断掌握情况。",
                        );
                      })
                    }
                  >
                    把旧会话接入个人导出
                  </button>
                </p>
              )}
              <p>
                课程版本：{course.id}。学习证据按账号保存；关闭浏览器后可继续。
              </p>
              <a className="pilot-primary" href="/api/pilot/export">
                导出到 Obsidian（ZIP）
              </a>
              <p className="pilot-muted">
                包含个人笔记、作答、照片与结构化证据；不会覆盖原知识库。
              </p>
            </div>
            <div className="pilot-settings-card">
              <h2>模型与用量</h2>
              <p>
                {status.model_available
                  ? "模型已配置。每个操作最多调用一次，不自动重试。"
                  : "尚未配置模型。在本机 .env 设置 OPENAI_API_KEY 与 STUDIO_VISION_MODEL，重启后可识别照片和获取过程反馈。"}
              </p>
              <p>
                模型只接收当前题、相关片段和你主动提交的作答。每次调用最多输出
                2500 tokens，每账号每天默认最多 30 次。
              </p>
              <p className="pilot-muted">
                这里记录调用结果；未接入价格表，不显示未经核实的金额。
              </p>
              {state?.runs.map((r) => (
                <div key={r.id}>
                  {fmt(r.at)} ·{" "}
                  {r.operation === "transcribe" ? "照片识别" : "过程反馈"} ·{" "}
                  {r.status}
                </div>
              ))}
            </div>
            {status.user.role === "owner" && (
              <div className="pilot-settings-card">
                <h2>本机试点邀请</h2>
                <p>
                  为使用同一台电脑的试点学生创建独立账号。跨设备部署尚未启用。
                </p>
                <button
                  disabled={disabled}
                  onClick={() =>
                    void run("创建邀请", async () =>
                      setInvite(
                        (await post<{ invite: string }>(p + "/auth/invite"))
                          .invite,
                      ),
                    )
                  }
                >
                  生成一次性邀请码
                </button>
                {invite && (
                  <p>
                    <code>{invite}</code>
                  </p>
                )}
              </div>
            )}
            <div className="pilot-settings-card">
              <h2>清空我的学习数据</h2>
              <p>
                删除当前账号的作答、照片、笔记与模型记录，保留账号和共享课程。
              </p>
              <label className="pilot-checkbox">
                <input
                  type="checkbox"
                  checked={confirmDelete}
                  onChange={(e) => setConfirmDelete(e.target.checked)}
                />
                我确认要删除这些个人数据
              </label>
              <button
                disabled={disabled || !confirmDelete}
                onClick={() =>
                  void run("删除个人数据", async () => {
                    await api(p + "/my-data", { method: "DELETE" });
                    setTask(null);
                    setAttempt(null);
                    setPhoto(null);
                    setWorking("");
                    setAnswers({});
                    setNotes("");
                    setConfirmDelete(false);
                    await refresh();
                    setNotice("个人学习数据已清空。");
                  })
                }
              >
                删除我的数据
              </button>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
