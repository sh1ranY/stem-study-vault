export type User = { id: string; name: string; role: string };
export type Status = {
  language?: "zh-CN" | "en";
  deployment: "local-invitation" | "hosted-invitation";
  setup_required: boolean;
  course_ready: boolean;
  model_available: boolean;
  daily_model_calls: number;
  user: User | null;
  database: string;
};
export type Block = {
  id: string;
  role: string;
  title?: string;
  body: string | null;
};
export type Lesson = {
  id: string;
  title: string;
  week: number;
  blocks: Block[];
  version: string;
};
export type Topic = {
  title: string;
  week: number;
  objective: string;
  routes: string[];
};
export type Course = {
  id: string;
  title: string;
  lessons: Lesson[];
  topics: Record<string, Topic>;
  asset_count: number;
  warnings: string[];
  legacy_records: { id: string; title: string; body: string; note: string }[];
};
export type Task = {
  id: string;
  topic: string;
  phase: string;
  title: string;
  prompt: string;
  fields: { id: string; label: string }[];
  source_note: string;
};
export type Result = {
  status: string;
  checks: Record<string, boolean>;
  route: string;
  feedback: string;
  teaching: string;
  scope: string;
  passed: boolean;
};
export type Attempt = {
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
export type Transcript = {
  working: string;
  fields: { id: string; value: string }[];
  uncertainties: string[];
};
export type Photo = {
  at: string;
  id: string;
  task_id: string;
  transcription: Transcript | null;
};
export type Draft = {
  id: string;
  revision: number;
  at: string;
  working: string;
  answers: Record<string, string>;
  photo_id: string | null;
  prior_seen: boolean;
};
export type State = {
  drafts: Draft[];
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
export type Source = {
  id: string;
  name: string;
  suffix: string;
  role: string;
  locations: string[];
  bytes: number;
};
