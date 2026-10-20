import { useEffect, useState } from "react";
import { ArrowUpRight, ScanLine } from "lucide-react";
import { api } from "./api";
import { useLocale } from "./Locale";
import "./imageEntry.css";

type Snapshot = { stage: number; history: { result: { passed: boolean } }[] };

export default function ImageLearningEntry({ onOpen, disabled, records = false }: {
  onOpen: () => void; disabled: boolean; records?: boolean;
}) {
  const { language } = useLocale();
  const en = language === "en";
  const [saved, setSaved] = useState<Snapshot | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    let active = true;
    api<{ session: Snapshot | null }>("/pilot/learning/images").then(r => {
      if (active) { setSaved(r.session); setFailed(false); }
    }).catch(() => { if (active) setFailed(true); });
    return () => { active = false; };
  }, [language]);
  return <section className={"image-entry" + (records ? " image-entry-records" : "")} aria-label={en ? "Image-processing exploration" : "图像处理探索单元"}>
    <div>
      <span className="pilot-eyebrow"><ScanLine size={16} /> {en ? "ELEC270 · FROM SIGNALS TO IMAGES" : "ELEC270 · 从信号走进图像"}</span>
      <h2>{records ? (en ? "Your image-processing exploration" : "你的图像处理探索") : (en ? "A smoother photo. Where did the detail go?" : "噪声少了，为什么细节也消失了？")}</h2>
      <p>{en ? "Make a prediction, experiment with an image, and connect what you see to convolution and frequency. Open the maths whenever you need it." : "先作预测，亲手改变图像，再把看到的变化连接到卷积与频率。需要时，随时展开背后的数学。"}</p>
      {saved && <p className="image-entry-progress">{en ? `Saved at stage ${saved.stage + 1} of 5 · ${saved.history.length} recorded checks` : `已保存至第 ${saved.stage + 1} / 5 步 · ${saved.history.length} 次检查记录`}{records && (en ? ". These records describe individual checks, not whole-course mastery." : "。这些记录只说明具体检查的表现，不代表整门课已掌握。")}</p>}
      {failed && <p className="image-entry-progress">{en ? "Progress could not be loaded. Open the unit to reconnect." : "暂未读到进度，进入单元后可重新连接。"}</p>}
      <button className="pilot-primary" disabled={disabled} onClick={onOpen}>
        {saved ? (en ? "Continue exploring" : "继续探索") : (en ? "Explore image processing" : "开始图像探索")} <ArrowUpRight size={17} />
      </button>
      <small>{en ? "Original interactive lesson · Chinese & English · No AI calls needed" : "原创交互单元 · 中英双语 · 无需调用 AI"}</small>
    </div>
    {!records && <div className="image-entry-art" aria-hidden="true"><div /><div /><span>01 → 02</span></div>}
  </section>;
}
