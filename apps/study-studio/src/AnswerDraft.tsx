import {
  forwardRef,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from "react";
import { api } from "./api";
import { useLocale } from "./Locale";
import type { Draft } from "./pilotTypes";

export type DraftHandle = { flush: () => Promise<void> };
type Value = Pick<Draft, "answers" | "working" | "photo_id" | "prior_seen">;
export default forwardRef<
  DraftHandle,
  {
    taskId: string;
    initial?: Draft;
    value: Value;
    onSaved: (draft: Draft) => void;
    onRestore: (draft: Draft) => void;
  }
>(function AnswerDraft({ taskId, initial, value, onSaved, onRestore }, ref) {
  const { language } = useLocale();
  const en = language === "en";
  const [status, setStatus] = useState("saved");
  const [error, setError] = useState("");
  const current = useRef(value);
  current.current = value;
  const revision = useRef(initial?.revision || 0);
  const saved = useRef(JSON.stringify(value));
  const inFlight = useRef<Promise<void> | null>(null);
  const mounted = useRef(true);
  const callbacks = useRef({ onSaved, onRestore });
  callbacks.current = { onSaved, onRestore };
  async function flush() {
    if (inFlight.current) await inFlight.current;
    if (JSON.stringify(current.current) === saved.current) return;
    const snapshot = current.current;
    const serialized = JSON.stringify(snapshot);
    if (mounted.current) {
      setStatus("saving");
      setError("");
    }
    const work = (async () => {
      try {
        const draft = await api<Draft>("/pilot/drafts/" + taskId, {
          method: "PUT",
          body: JSON.stringify({ ...snapshot, revision: revision.current }),
        });
        revision.current = draft.revision;
        saved.current = serialized;
        callbacks.current.onSaved(draft);
        if (mounted.current)
          setStatus(
            JSON.stringify(current.current) === serialized ? "saved" : "saving",
          );
      } catch (e) {
        if (mounted.current) {
          setStatus("error");
          setError(e instanceof Error ? e.message : String(e));
        }
        throw e;
      } finally {
        inFlight.current = null;
      }
    })();
    inFlight.current = work;
    await work;
    if (JSON.stringify(current.current) !== saved.current) await flush();
  }
  useImperativeHandle(ref, () => ({ flush }));
  const serialized = JSON.stringify(value);
  useEffect(() => {
    if (serialized === saved.current) return;
    setStatus("saving");
    const timer = setTimeout(() => void flush().catch(() => {}), 650);
    return () => clearTimeout(timer);
  }, [serialized]);
  useEffect(() => {
    mounted.current = true;
    function preventLoss(e: BeforeUnloadEvent) {
      if (JSON.stringify(current.current) !== saved.current) {
        e.preventDefault();
        e.returnValue = "";
      }
    }
    window.addEventListener("beforeunload", preventLoss);
    return () => {
      mounted.current = false;
      window.removeEventListener("beforeunload", preventLoss);
    };
  }, []);
  return (
    <div className="answer-draft" role="status">
      <small>
        {status === "saved"
          ? en
            ? "Draft ready · saved changes resume after refresh; confirm again before assessment."
            : "草稿就绪 · 修改保存后可刷新恢复；正式提交前仍需确认。"
          : status === "saving"
            ? en
              ? "Saving draft…"
              : "正在保存草稿…"
            : en
              ? "Draft not saved. Keep this page open."
              : "草稿尚未保存，请保留此页面。"}
      </small>
      {error && <p className="pilot-error">{error}</p>}
      {status === "error" && (
        <div className="pilot-actions">
          <button onClick={() => void flush().catch(() => {})}>
            {en ? "Retry save" : "重试保存"}
          </button>
          <button
            onClick={() =>
              void (async () => {
                const draft = await api<Draft | null>(
                  "/pilot/drafts/" + taskId,
                );
                if (draft) {
                  revision.current = draft.revision;
                  saved.current = JSON.stringify({
                    answers: draft.answers,
                    working: draft.working,
                    photo_id: draft.photo_id,
                    prior_seen: draft.prior_seen,
                  });
                  callbacks.current.onRestore(draft);
                  setStatus("saved");
                  setError("");
                }
              })().catch((e) => setError(String(e)))
            }
          >
            {en ? "Replace with saved draft" : "使用已保存草稿替换当前输入"}
          </button>
        </div>
      )}
    </div>
  );
});
