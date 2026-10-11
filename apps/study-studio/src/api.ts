let apiCourse = new URLSearchParams(location.search).get("course") || "";
export function setApiCourse(value: string) { apiCourse = value; }
let apiLanguage = "zh-CN";
export function setApiLanguage(value: string) {
  apiLanguage = value;
}
export async function api<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  let response: Response;
  try {
    response = await fetch("/api" + path, {
      ...options,
      headers: {
        "Accept-Language": apiLanguage,
        ...(apiCourse ? { "X-Study-Course": apiCourse } : {}),
        ...(options.body instanceof FormData
          ? {}
          : { "Content-Type": "application/json" }),
        ...options.headers,
      },
    });
  } catch {
    throw new Error(
      apiLanguage === "en"
        ? "Cannot reach the learning space. Try again shortly; saved work is retained."
        : "暂时无法连接学习空间，请稍后重试；已保存内容仍然保留。",
    );
  }
  if (!response.ok) {
    let message = "The request could not be completed.";
    try {
      const data = await response.json();
      message =
        typeof data.detail === "string"
          ? data.detail
          : apiLanguage === "en"
            ? "Check the required fields and input lengths."
            : "请检查必填项与输入长度。";
    } catch {
      /* Use safe fallback. */
    }
    throw new Error(message);
  }
  return response.json();
}
export const post = <T>(path: string, body: unknown = {}) =>
  api<T>(path, { method: "POST", body: JSON.stringify(body) });
