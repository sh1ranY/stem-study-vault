import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { english } from "./pilotMessages";
import type { TeachingLanguage } from "./guidedLocale";
import { setApiLanguage } from "./api";

type Locale = {
  language: TeachingLanguage;
  setLanguage: (value: TeachingLanguage) => void;
  t: (key: keyof typeof english) => string;
};
const Context = createContext<Locale | null>(null);
export function LocaleProvider({ children }: { children: ReactNode }) {
  const [language, update] = useState<TeachingLanguage>(() => {
    try {
      return localStorage.getItem("studio-language") === "en" ? "en" : "zh-CN";
    } catch {
      return "zh-CN";
    }
  });
  function setLanguage(value: TeachingLanguage) {
    setApiLanguage(value);
    update(value);
    try {
      localStorage.setItem("studio-language", value);
    } catch {
      /* Account setting still persists. */
    }
  }
  useEffect(() => {
    document.documentElement.lang = language;
    setApiLanguage(language);
  }, [language]);
  return (
    <Context.Provider
      value={{
        language,
        setLanguage,
        t: (key) => (language === "en" ? english[key] : key),
      }}
    >
      {children}
    </Context.Provider>
  );
}
export function useLocale() {
  const value = useContext(Context);
  if (!value) throw new Error("LocaleProvider missing");
  return value;
}
export function LanguagePicker({
  disabled = false,
  onChange,
}: {
  disabled?: boolean;
  onChange: (value: TeachingLanguage) => void;
}) {
  const { language } = useLocale();
  return (
    <label className="studio-language">
      Language / 语言{" "}
      <select
        value={language}
        disabled={disabled}
        onChange={(e) => onChange(e.target.value as TeachingLanguage)}
      >
        <option value="zh-CN">简体中文</option>
        <option value="en">English</option>
      </select>
    </label>
  );
}
